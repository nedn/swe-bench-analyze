import os
import subprocess
import csv
import json
import shutil
import tempfile
from collections import defaultdict
from datasets import load_dataset

# Configuration
OUTPUT_FILE = "swe_bench_loc_stats.csv"
TARGET_LANGUAGES = [
    "C", "C++", "Java", "Kotlin", "Python", "Go", "Rust", "JavaScript", "HTML"
]

def check_scc_installed():
    """Verifies that scc is installed and accessible."""
    if shutil.which("scc") is None:
        raise EnvironmentError(
            "The 'scc' tool is not found in your PATH. "
            "Please install it before running this script."
        )

def get_loc_counts(repo_path):
    """Runs scc on the specific path and returns a dict of {Language: CodeCount}."""
    try:
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
    except subprocess.CalledProcessError as e:
        print(f"Error running scc: {e}")
        return {}
    except json.JSONDecodeError:
        print("Error parsing scc output")
        return {}

def analyze_commit_in_temp(repo_name, commit_sha):
    """
    Creates a temp dir, shallow fetches ONLY the specific commit,
    runs analysis, and auto-cleans up.
    """
    repo_url = f"https://github.com/{repo_name}.git"

    # Create a temporary directory that cleans itself up automatically
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # 1. Initialize empty git repo
            subprocess.run(
                ["git", "init"],
                cwd=temp_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # 2. Add remote
            subprocess.run(
                ["git", "remote", "add", "origin", repo_url],
                cwd=temp_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # 3. Fetch ONLY the specific commit with depth 1 (Shallow Fetch)
            # This avoids downloading the whole repo history
            subprocess.run(
                ["git", "fetch", "--depth", "1", "origin", commit_sha],
                cwd=temp_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # 4. Checkout the fetched content (FETCH_HEAD)
            subprocess.run(
                ["git", "checkout", "FETCH_HEAD"],
                cwd=temp_dir,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # 5. Run Analysis
            return get_loc_counts(temp_dir)

        except subprocess.CalledProcessError as e:
            print(f"Git error for {repo_name} at {commit_sha}: {e}")
            return {}

def main():
    check_scc_installed()

    print("Loading SWE-bench Verified dataset...")
    dataset = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")

    # Prepare CSV Header
    header = ["swe_bench_test_id", "repo", "commit"] + TARGET_LANGUAGES

    print(f"Starting analysis. Output will be saved to {OUTPUT_FILE}")

    with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # Iterate through the dataset
        for i, row in enumerate(dataset):
            instance_id = row['instance_id']
            repo = row['repo']
            commit = row['base_commit']

            print(f"[{i+1}/{len(dataset)}] Processing {instance_id} ({repo})...")

            # Analyzes inside a temp dir and returns stats
            stats = analyze_commit_in_temp(repo, commit)

            if stats:
                # Build CSV Row
                csv_row = [instance_id, repo, commit]
                for lang in TARGET_LANGUAGES:
                    count = stats.get(lang, 0)
                    csv_row.append(count)

                writer.writerow(csv_row)
                f.flush()

    print("\nDone! Analysis complete.")

if __name__ == "__main__":
    main()
