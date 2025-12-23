import csv
import os
import argparse
from datasets import load_dataset

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

def process_eval_set(eval_set):
    """
    Process a single eval set: load dataset, read corresponding CSV, and augment it.
    """
    # Map eval_set to dataset name and file names (matching analyze_swe_bench.py)
    if eval_set == "verified":
        dataset_name = "SWE-bench/SWE-bench_Verified"
        input_file = "swe_bench_verified_loc_stats.csv"
        output_file = "augmented/swe_bench_verified_loc_stats_augmented.csv"
    elif eval_set == "multilingual":
        dataset_name = "SWE-bench/SWE-bench_Multilingual"
        input_file = "swe_bench_multilingual_loc_stats.csv"
        output_file = "augmented/swe_bench_multilingual_loc_stats_augmented.csv"
    elif eval_set == "pro":
        dataset_name = "ScaleAI/SWE-bench_Pro"
        input_file = "swe_bench_pro_loc_stats.csv"
        output_file = "augmented/swe_bench_pro_loc_stats_augmented.csv"
    elif eval_set == "polybench":
        dataset_name = "AmazonScience/SWE-PolyBench"
        input_file = "swe_polybench_loc_stats.csv"
        output_file = "augmented/swe_polybench_loc_stats_augmented.csv"
    else:
        raise ValueError(f"Unknown eval_set: {eval_set}")

    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found. Skipping {eval_set}.")
        return

    print(f"\n{'='*60}")
    print(f"Processing {eval_set.upper()} eval set")
    print(f"{'='*60}")
    print(f"Loading {dataset_name} dataset to retrieve patches...")
    dataset = load_dataset(dataset_name, split="test")

    # Create a quick lookup dictionary: instance_id -> patch_content
    print("Creating patch lookup table...")
    patch_lookup = {item['instance_id']: item['patch'] for item in dataset}

    print(f"Reading {input_file} and appending data...")

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Define new columns
        new_cols = ['golden_patch_added', 'golden_patch_deleted', 'golden_patch_total']

        # Prepare output file
        with open(output_file, mode='w', newline='\n', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames + new_cols)
            writer.writeheader()

            rows_processed = 0
            for row in reader:
                instance_id = row['instance_id']

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

    print(f"Done! Augmented data saved to {output_file}")
    print(f"Processed {rows_processed} rows for {eval_set}.")

def main():
    parser = argparse.ArgumentParser(description="Augment SWE-bench LOC stats CSV files with patch statistics.")
    parser.add_argument(
        "--eval-set",
        choices=["verified", "multilingual", "pro", "polybench", "all"],
        default="all",
        help="Type of SWE-bench dataset to process. Use 'all' to process all available CSV files."
    )
    args = parser.parse_args()

    if args.eval_set == "all":
        # Process all eval sets
        eval_sets = ["verified", "multilingual", "pro", "polybench"]
        for eval_set in eval_sets:
            process_eval_set(eval_set)
        print(f"\n{'='*60}")
        print("All eval sets processed!")
        print(f"{'='*60}")
    else:
        # Process single eval set
        process_eval_set(args.eval_set)

if __name__ == "__main__":
    main()
