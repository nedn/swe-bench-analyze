import csv
import os
import json

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
    input_file = "multi_swe_bench_loc_stats.csv"
    output_file = "augmented/multi_swe_bench_loc_stats_augmented.csv"
    base_dir = "Multi-SWE-bench"

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    if not os.path.exists(base_dir):
        print(f"Error: {base_dir} directory not found.")
        print("Please download Multi-SWE-bench first following the instructions "
              "in https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench.")
        return

    # Load all patches from JSONL files into a lookup dictionary
    print(f"Loading patches from {base_dir}...")
    patch_lookup = {}  # instance_id -> fix_patch

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".jsonl"):
                file_path = os.path.join(root, file)
                print(f"  Reading {file_path}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                data = json.loads(line)
                                instance_id = data.get('instance_id')
                                fix_patch = data.get('fix_patch', '')
                                if instance_id:
                                    patch_lookup[instance_id] = fix_patch
                            except json.JSONDecodeError as e:
                                print(f"  Error decoding json in {file_path}: {e}")

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
                instance_id = row['instance_id']

                # Get the patch from the lookup
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
                    missing_patches += 1

                writer.writerow(row)
                rows_processed += 1

    print(f"\nDone! Augmented data saved to {output_file}")
    print(f"Processed {rows_processed} rows.")
    if missing_patches > 0:
        print(f"Warning: {missing_patches} rows had missing patches.")

if __name__ == "__main__":
    main()
