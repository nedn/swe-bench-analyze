import csv
import os
import shutil
import subprocess

def parse_patch_stats(patch_text):
    """
    Parses a git diff/patch string to count lines added and removed.

    Returns:
        tuple: (lines_added, lines_removed)
    """
    if not patch_text:
        return 0, 0

    added = 0
    removed = 0

    lines = patch_text.splitlines()
    for line in lines:
        # Check for additions (starts with + but not +++)
        if line.startswith('+') and not line.startswith('+++'):
            added += 1
        # Check for deletions (starts with - but not ---)
        elif line.startswith('-') and not line.startswith('---'):
            removed += 1

    return added, removed

def main():
    input_file = "swe_lancer_loc_stats.csv"
    output_file = "augmented/swe_lancer_loc_stats_augmented.csv"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # Clone frontier-evals to get patch data
    print("Cloning/Updating frontier-evals...")
    frontier_evals_dir = "temp_frontier_evals"
    if os.path.exists(frontier_evals_dir):
        shutil.rmtree(frontier_evals_dir, ignore_errors=True)

    # Clone with sparse checkout to save time/space
    subprocess.run(
        ["git", "clone", "--filter=blob:none", "--sparse",
         "https://github.com/openai/frontier-evals", frontier_evals_dir],
        check=True
    )
    subprocess.run(
        ["git", "sparse-checkout", "set", "project/swelancer/issues"],
        cwd=frontier_evals_dir,
        check=True
    )

    issues_dir = os.path.join(frontier_evals_dir, "project", "swelancer", "issues")

    # Build a lookup from task_id to patch content
    print("Loading patches from frontier-evals...")
    patch_lookup = {}  # task_id -> patch_content

    if os.path.exists(issues_dir):
        for item in os.listdir(issues_dir):
            item_path = os.path.join(issues_dir, item)
            if os.path.isdir(item_path):
                patch_file = os.path.join(item_path, "bug_reintroduce.patch")
                if os.path.exists(patch_file):
                    with open(patch_file, "r", encoding='utf-8', errors='replace') as f:
                        patch_content = f.read()
                    patch_lookup[item] = patch_content

    print(f"Loaded {len(patch_lookup)} patches.")

    # Read the input CSV and augment it
    print(f"Reading {input_file} and appending patch statistics...")

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Define new columns
        new_cols = ['golden_patch_added', 'golden_patch_deleted', 'golden_patch_total']

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Prepare output file
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames + new_cols)
            writer.writeheader()

            rows_processed = 0
            missing_patches = 0
            for row in reader:
                task_id = row['swe_lancer_task_id']

                # Get the patch from the lookup
                patch_content = patch_lookup.get(task_id)

                if patch_content:
                    added, deleted = parse_patch_stats(patch_content)
                    row['golden_patch_added'] = added
                    row['golden_patch_deleted'] = deleted
                    row['golden_patch_total'] = added + deleted
                else:
                    print(f"Warning: No patch found for task {task_id}")
                    row['golden_patch_added'] = 0
                    row['golden_patch_deleted'] = 0
                    row['golden_patch_total'] = 0
                    missing_patches += 1

                writer.writerow(row)
                rows_processed += 1

    # Cleanup
    print("Cleaning up...")
    if os.path.exists(frontier_evals_dir):
        shutil.rmtree(frontier_evals_dir)

    print(f"\nDone! Augmented data saved to {output_file}")
    print(f"Processed {rows_processed} rows.")
    if missing_patches > 0:
        print(f"Warning: {missing_patches} rows had missing patches.")

if __name__ == "__main__":
    main()
