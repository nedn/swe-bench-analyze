import os
import shutil
import subprocess
import json
import argparse
import tempfile
from common import check_scc_installed, get_loc_counts, write_loc_stats_csv, EvalSet, clone_repo_with_retry, checkout_with_retry

def main():
    parser = argparse.ArgumentParser(description="Analyze LOC statistics for SWELancer tasks.")
    parser.add_argument("--output-file", default="swe_lancer_loc_stats.csv", help="Output CSV file.")
    parser.add_argument("--max-items", type=int, default=None, help="Max number of items to process (for testing).")
    args = parser.parse_args()

    check_scc_installed()

    # Paths
    # We will use temp directories for cloning to ensure a clean state
    # But to speed up dev/testing, if they exist locally we could reuse?
    # For now, follow the robust pattern of temp dirs or specific dirs in CWD.
    
    # 1. Clone frontier-evals to get issue data
    print("Cloning/Updating frontier-evals...")
    frontier_evals_dir = "temp_frontier_evals"
    if os.path.exists(frontier_evals_dir):
        shutil.rmtree(frontier_evals_dir, ignore_errors=True)
    
    # Clone with sparse checkout to save time/space
    subprocess.run(
        ["git", "clone", "--filter=blob:none", "--sparse", "https://github.com/openai/frontier-evals", frontier_evals_dir],
        check=True
    )
    subprocess.run(
        ["git", "sparse-checkout", "set", "project/swelancer/issues"],
        cwd=frontier_evals_dir,
        check=True
    )

    # 2. Collect tasks/commits
    issues_dir = os.path.join(frontier_evals_dir, "project", "swelancer", "issues")
    tasks = []
    
    print(f"Reading issues from {issues_dir}...")
    if os.path.exists(issues_dir):
        for item in os.listdir(issues_dir):
            item_path = os.path.join(issues_dir, item)
            if os.path.isdir(item_path):
                commit_file = os.path.join(item_path, "commit_id.txt")
                if os.path.exists(commit_file):
                    with open(commit_file, "r") as f:
                        commit_sha = f.read().strip()
                    tasks.append({
                        "task_id": item,
                        "commit": commit_sha
                    })

    print(f"Found {len(tasks)} tasks.")
    
    if args.max_items:
        tasks = tasks[:args.max_items]
        print(f"Processing only first {len(tasks)} tasks.")

    if not tasks:
        print("No tasks found. Exiting.")
        return

    # 3. Clone Expensify/App
    print("Cloning Expensify/App...")
    expensify_dir = "temp_expensify_app"
    if os.path.exists(expensify_dir):
        shutil.rmtree(expensify_dir, ignore_errors=True)

    clone_repo_with_retry("https://github.com/Expensify/App", expensify_dir)

    # 4. Analyze each task
    results = []

    for i, task in enumerate(tasks):
        task_id = task["task_id"]
        commit_sha = task["commit"]
        print(f"Processing {i+1}/{len(tasks)}: {task_id} @ {commit_sha[:7]}")

        # Checkout commit
        checkout_with_retry(expensify_dir, commit_sha)
        
        # Run SCC
        stats = get_loc_counts(expensify_dir)
        
        # Store result
        res = {
            "instance_id": task_id,
            "repo": "Expensify/App",
            "commit": commit_sha,
            "stats": stats
        }
        results.append(res)

    # 5. Write CSV
    write_loc_stats_csv(args.output_file, results, EvalSet.SWE_LANCER)

    # Cleanup
    print("Cleaning up...")
    if os.path.exists(frontier_evals_dir):
        shutil.rmtree(frontier_evals_dir)
    if os.path.exists(expensify_dir):
        shutil.rmtree(expensify_dir)

    print("Done!")

if __name__ == "__main__":
    main()
