import os
import subprocess
import json
import shutil
import tempfile
from collections import defaultdict
from datasets import load_dataset
import argparse


from common import check_scc_installed, get_loc_counts, write_loc_stats_csv, EvalSet, clone_repo_with_retry



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

def run_analysis(eval_set, dataset_name, output_file, max_workers):
    """Run LOC analysis for a single eval set."""
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
    print(f"Starting parallel analysis with {max_workers} workers...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
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
    for row in dataset:
        instance_id = row['instance_id']
        if instance_id in results_map:
            results_list.append(results_map[instance_id])
        else:
            print(f"Warning: Missing results for {instance_id}")
            count_missing += 1

    if count_missing > 0:
        print(f"Total missing: {count_missing}")

    write_loc_stats_csv(output_file, results_list, eval_set)

    print(f"\nDone! Analysis complete for {dataset_name}.\n")


def main():
    parser = argparse.ArgumentParser(description="Analyze LOC statistics for SWE-bench datasets.")
    parser.add_argument("--eval-set", choices=["verified", "multilingual", "pro", "polybench", "all"], default="verified", help="Type of SWE-bench dataset to use.")
    parser.add_argument("--max-workers", type=int, default=8, help="Number of parallel workers.")
    args = parser.parse_args()

    EVAL_SET_CONFIG = {
        "verified": {
            "eval_set": EvalSet.SWE_BENCH_VERIFIED,
            "dataset_name": "SWE-bench/SWE-bench_Verified",
            "output_file": "swe_bench_verified_loc_stats.csv",
        },
        "multilingual": {
            "eval_set": EvalSet.SWE_BENCH_MULTILINGUAL,
            "dataset_name": "SWE-bench/SWE-bench_Multilingual",
            "output_file": "swe_bench_multilingual_loc_stats.csv",
        },
        "pro": {
            "eval_set": EvalSet.SWE_BENCH_PRO,
            "dataset_name": "ScaleAI/SWE-bench_Pro",
            "output_file": "swe_bench_pro_loc_stats.csv",
        },
        "polybench": {
            "eval_set": EvalSet.SWE_POLYBENCH,
            "dataset_name": "AmazonScience/SWE-PolyBench",
            "output_file": "swe_polybench_loc_stats.csv",
        },
    }

    check_scc_installed()

    if args.eval_set == "all":
        eval_sets_to_run = list(EVAL_SET_CONFIG.keys())
    else:
        eval_sets_to_run = [args.eval_set]

    for eval_set_name in eval_sets_to_run:
        config = EVAL_SET_CONFIG[eval_set_name]
        run_analysis(
            config["eval_set"],
            config["dataset_name"],
            config["output_file"],
            args.max_workers
        )

if __name__ == "__main__":
    main()
