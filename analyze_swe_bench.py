import os
import subprocess
import csv
import json
import shutil
import tempfile
from collections import defaultdict
from datasets import load_dataset
import argparse


from common import check_scc_installed, get_loc_counts, TARGET_LANGUAGES



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
            subprocess.run(
                ["git", "clone", "--filter=blob:none", repo_url, temp_dir],
                check=True,
                capture_output=True # Silence git output to avoid messy logs
            )

            # 2. Iterate through commits for this repo
            for task in tasks:
                commit_sha = task['base_commit']
                instance_id = task['instance_id']

                # print(f"  Checking out {commit_sha[:7]} for {instance_id}...")

                # Force checkout the specific commit
                subprocess.run(
                    ["git", "checkout", "-f", commit_sha],
                    cwd=temp_dir,
                    check=True,
                    capture_output=True
                )

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
    parser = argparse.ArgumentParser(description="Analyze LOC statistics for SWE-bench datasets.")
    parser.add_argument("--eval-set", choices=["verified", "multilingual", "pro"], default="verified", help="Type of SWE-bench dataset to use.")
    parser.add_argument("--max-workers", type=int, default=8, help="Number of parallel workers.")
    args = parser.parse_args()

    if args.eval_set == "verified":
      dataset_name = "SWE-bench/SWE-bench_Verified"
      output_file = "swe_bench_verified_loc_stats.csv"
    elif args.eval_set == "multilingual":
        dataset_name = "SWE-bench/SWE-bench_Multilingual"
        output_file = "swe_bench_multilingual_loc_stats.csv"
    elif args.eval_set == "pro":
        dataset_name = "ScaleAI/SWE-bench_Pro"
        output_file = "swe_bench_pro_loc_stats.csv"

    check_scc_installed()

    print(f"Loading {dataset_name} dataset...")
    dataset = load_dataset(dataset_name, split="test")

    # 1. Group data by Repository
    print("Grouping tasks by repository...")
    repo_groups = defaultdict(list)
    for row in dataset:
        repo_groups[row['repo']].append(row)

    print(f"Found {len(repo_groups)} unique repositories across {len(dataset)} tasks.")

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

    # 3. Write to CSV in order
    print(f"Writing results to {output_file}...")
    header = ["swe_bench_test_id", "repo", "commit"] + TARGET_LANGUAGES

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        count_missing = 0
        for row in dataset:
            instance_id = row['instance_id']
            if instance_id in results_map:
                res = results_map[instance_id]
                stats = res['stats']
                csv_row = [instance_id, res['repo'], res['commit']]
                for lang in TARGET_LANGUAGES:
                    csv_row.append(stats.get(lang, 0))
                writer.writerow(csv_row)
            else:
                print(f"Warning: Missing results for {instance_id}")
                count_missing += 1

        if count_missing > 0:
            print(f"Total missing: {count_missing}")

    print("\nDone! Analysis complete.")

if __name__ == "__main__":
    main()
