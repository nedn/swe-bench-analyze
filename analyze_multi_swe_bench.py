import os
import subprocess
import json
import shutil
import tempfile
from collections import defaultdict
import argparse


from common import check_scc_installed, get_loc_counts, write_loc_stats_csv, EvalSet, clone_repo_with_retry, checkout_with_retry



import concurrent.futures

def process_repository(repo_name, tasks):
    """
    Clones a repo once, then iterates through all associated tasks/commits.
    Returns a list of dicts: {'instance_id': ..., 'repo': ..., 'commit': ..., 'stats': ...}
    """
    repo_url = f"https://github.com/{repo_name}.git"
    results = []

    print(f"Processing Repo: {repo_name} ({len(tasks)} items)")

    # Create a temporary directory for the repo
    # Use a unique prefix to avoid collisions in parallel execution
    prefix = repo_name.replace("/", "_") + "_"
    with tempfile.TemporaryDirectory(dir=os.getcwd(), prefix=prefix) as temp_dir:
        try:
            # 1. Clone the repository
            # We use --filter=blob:none (Blobless Clone).
            # This downloads the commit history (so we can checkout any SHA)
            # but doesn't download file contents until we actually checkout.
            # Much faster than a full clone.
            clone_repo_with_retry(repo_url, temp_dir)

            # 2. Iterate through commits for this repo
            for task in tasks:
                commit_sha = task['base']['sha']
                instance_id = task['instance_id']

                # print(f"  Checking out {commit_sha[:7]} for {instance_id}...")

                # Force checkout the specific commit
                checkout_with_retry(temp_dir, commit_sha)

                # 3. Run Analysis
                stats = get_loc_counts(temp_dir)

                results.append({
                    "instance_id": instance_id,
                    "repo": repo_name,
                    "commit": commit_sha,
                    "stats": stats
                })
        except subprocess.CalledProcessError as e:
            print(f"Error processing {repo_name}: {e}")
            # Optionally return partial results or raise

    print(f"Finished {repo_name}")
    return results

def main():
    parser = argparse.ArgumentParser(description="Analyze LOC statistics for Multi-SWE-bench datasets.")
    parser.add_argument("--max-workers", type=int, default=8, help="Number of parallel workers.")
    args = parser.parse_args()

    output_file = "multi_swe_bench_loc_stats.csv"

    check_scc_installed()

    print(f"Loading Multi-SWE-bench dataset...")
    
    tasks = []
    base_dir = "Multi-SWE-bench"
    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} directory not found.")
        print("Please download Multi-SWE-bench first following the instructions "
              "in https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench.")
        return

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".jsonl"):
                file_path = os.path.join(root, file)
                print(f"Reading {file_path}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                tasks.append(json.loads(line))
                            except json.JSONDecodeError as e:
                                print(f"Error decoding json in {file_path}: {e}")

    # 1. Group data by Repository
    print("Grouping tasks by repository...")
    repo_groups = defaultdict(list)
    for row in tasks:
        # Construct full repo name "org/repo"
        repo_full_name = f"{row['org']}/{row['repo']}"
        repo_groups[repo_full_name].append(row)

    print(f"Found {len(repo_groups)} unique repositories across {len(tasks)} tasks.")

    # Prepare results map
    results_map = {} # instance_id -> result_dict

    # 2. Parallel Processing
    print(f"Starting parallel analysis with {args.max_workers} workers...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        future_to_repo = {
            executor.submit(process_repository, repo_name, tasks): repo_name
            for repo_name, tasks in repo_groups.items()
        }

        finished_count = 0
        total_repos = len(repo_groups)

        for future in concurrent.futures.as_completed(future_to_repo):
            repo_name = future_to_repo[future]
            try:
                repo_results = future.result()
                for res in repo_results:
                    results_map[res['instance_id']] = res
                finished_count += 1
                print(f"Progress: {finished_count}/{total_repos} repos processed.")
            except Exception as exc:
                print(f'{repo_name} generated an exception: {exc}')

    # 3. Build results list in order and write to CSV
    print(f"Writing results to {output_file}...")
    results_list = []
    count_missing = 0
    for row in tasks:
        instance_id = row['instance_id']
        if instance_id in results_map:
            results_list.append(results_map[instance_id])
        else:
            print(f"Warning: Missing results for {instance_id}")
            count_missing += 1

    if count_missing > 0:
        print(f"Total missing: {count_missing}")

    write_loc_stats_csv(output_file, results_list, EvalSet.MULTI_SWE_BENCH)

    print("\nDone! Analysis complete.")

if __name__ == "__main__":
    main()
