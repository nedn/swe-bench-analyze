import csv
import os
from datasets import load_dataset

# Configuration
INPUT_FILE = "swe_bench_loc_stats.csv"
OUTPUT_FILE = "swe_bench_loc_stats_augmented.csv"

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
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Please run the previous script first.")
        return

    print("Loading SWE-bench Verified dataset to retrieve patches...")
    # Loading the same split used in the original script
    dataset = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")

    # Create a quick lookup dictionary: instance_id -> patch_content
    print("Creating patch lookup table...")
    patch_lookup = {item['instance_id']: item['patch'] for item in dataset}

    print(f"Reading {INPUT_FILE} and appending data...")

    with open(INPUT_FILE, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Define new columns
        new_cols = ['golden_patch_added', 'golden_patch_deleted', 'golden_patch_total']

        # Prepare output file
        with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames + new_cols)
            writer.writeheader()

            rows_processed = 0
            for row in reader:
                instance_id = row['swe_bench_test_id']

                # Get the patch from the dataset
                patch_content = patch_lookup.get(instance_id)

                if patch_content:
                    added, deleted = parse_patch_stats(patch_content)
                    row['golden_patch_added'] = added
                    row['golden_patch_deleted'] = deleted
                    row['golden_patch_total'] = added + deleted
                else:
                    print(f"Warning: No patch found for ID {instance_id}")
                    row['golden_patch_added'] = 0
                    row['golden_patch_deleted'] = 0
                    row['golden_patch_total'] = 0

                writer.writerow(row)
                rows_processed += 1

    print(f"Done! Augmented data saved to {OUTPUT_FILE}")
    print(f"Processed {rows_processed} rows.")

if __name__ == "__main__":
    main()
