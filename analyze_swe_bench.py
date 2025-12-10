import os
import subprocess
import csv
import json
import shutil
import tempfile
from collections import defaultdict
from datasets import load_dataset
import argparse

# Configuration
TARGET_LANGUAGES = [
    "C", "C++", "Java", "Kotlin", "Python", "Go", "Rust", "JavaScript", "HTML",
    "Ruby", "TypeScript", "PHP",
]

def check_scc_installed():
    """Verifies that scc is installed and accessible."""
    result = subprocess.run(
        ["scc", "--version"],
        capture_output=True,
        text=True,
        check=True
    )
    print("SCC Version:", result.stdout.strip())
    if not result.returncode == 0:
        raise EnvironmentError(
            "The 'scc' tool is not found in your PATH. "
            "Please install it before running this script."
        )

def get_loc_counts(repo_path):
    """Runs scc on the specific path and returns a dict of {Language: CodeCount}."""
    assert os.path.exists(repo_path), f"Repo path {repo_path} does not exist"
    assert os.path.isdir(repo_path), f"Repo path {repo_path} is not a directory"
    assert os.listdir(repo_path), f"Repo path {repo_path} is empty"
    print(f"Running scc command: ['scc', '{repo_path}', '--format', 'json']")
    # Run scc outputs JSON which is easy to parse
    result = subprocess.run(
        ["scc", repo_path, "--format", "json"],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(result.stdout)

    # Parse result into a lookup dict
    lang_stats = defaultdict(int)
    for item in data:
        lang_stats[item["Name"]] = item["Code"]

    return lang_stats

def process_repository(repo_name, tasks, writer):
    """
    Clones a repo once, then iterates through all associated tasks/commits.
    """
    repo_url = f"https://github.com/{repo_name}.git"

    print(f"\n--- Processing Repo: {repo_name} ({len(tasks)} items) ---")

    # Create a temporary directory for the repo
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as temp_dir:
        # 1. Clone the repository
        # We use --filter=blob:none (Blobless Clone).
        # This downloads the commit history (so we can checkout any SHA)
        # but doesn't download file contents until we actually checkout.
        # Much faster than a full clone.
        print(f"  Cloning {repo_name}...")
        subprocess.run(
            ["git", "clone", "--filter=blob:none", repo_url, temp_dir],
            check=True
        )

        # 2. Iterate through commits for this repo
        for i, task in enumerate(tasks):
            commit_sha = task['base_commit']
            instance_id = task['instance_id']

            print(f"  [{i+1}/{len(tasks)}] Checking out {commit_sha[:7]}...")

            # Force checkout the specific commit
            subprocess.run(
                ["git", "checkout", "-f", commit_sha],
                cwd=temp_dir,
                check=True
            )

            # 3. Run Analysis
            stats = get_loc_counts(temp_dir)

            # 4. Write to CSV immediately
            csv_row = [instance_id, repo_name, commit_sha]
            for lang in TARGET_LANGUAGES:
                csv_row.append(stats.get(lang, 0))
            print(stats)
            writer.writerow(csv_row)


def main():
    parser = argparse.ArgumentParser(description="Analyze LOC statistics for SWE-bench datasets.")
    parser.add_argument("--type", choices=["verified", "multilingual", "pro"], default="verified", help="Type of SWE-bench dataset to use.")
    args = parser.parse_args()

    if args.type == "verified":
      dataset_name = "SWE-bench/SWE-bench_Verified"
      output_file = "swe_bench_verified_loc_stats.csv"
    elif args.type == "multilingual":
        dataset_name = "SWE-bench/SWE-bench_Multilingual"
        output_file = "swe_bench_multilingual_loc_stats.csv"
    elif args.type == "pro":
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

    # Prepare CSV Header
    header = ["swe_bench_test_id", "repo", "commit"] + TARGET_LANGUAGES

    print(f"Starting analysis. Output will be saved to {output_file}")

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        i = 0
        # 2. Iterate through each repository group
        for repo_name, tasks in repo_groups.items():
            i += 1
            print(f"Processing repository {i}/{len(repo_groups)}: {repo_name}")
            process_repository(repo_name, tasks, writer)
            f.flush()

    print("\nDone! Analysis complete.")

if __name__ == "__main__":
    main()
