"""Fetch SWE-bench Pro dataset from HuggingFace and save as a JS data file."""
import json
import sys
sys.path.insert(0, '..')
from datasets import load_dataset


def main():
    print("Loading SWE-bench Pro dataset...")
    dataset = load_dataset("ScaleAI/SWE-bench_Pro", split="test")
    print(f"Loaded {len(dataset)} instances")

    # Convert to list of dicts, keeping fields relevant for the deep dive
    records = []
    for row in dataset:
        record = {
            "instance_id": row["instance_id"],
            "repo": row["repo"],
            "repo_language": row["repo_language"],
            "base_commit": row["base_commit"],
            "problem_statement": row["problem_statement"],
            "requirements": row["requirements"],
            "interface": row["interface"],
            "patch": row["patch"],
            "test_patch": row["test_patch"],
            "fail_to_pass": row["fail_to_pass"],
            "pass_to_pass": row["pass_to_pass"],
            "issue_specificity": row["issue_specificity"],
            "issue_categories": row["issue_categories"],
            "selected_test_files_to_run": row["selected_test_files_to_run"],
        }
        records.append(record)

    # Sort by repo then instance_id for consistent ordering
    records.sort(key=lambda r: (r["repo"], r["instance_id"]))

    # Write as a JS file that assigns data to a global variable
    output_path = "data/swe_bench_pro_data.js"
    import os
    os.makedirs("data", exist_ok=True)

    with open(output_path, "w") as f:
        f.write("// SWE-bench Pro dataset - auto-generated\n")
        f.write("// Source: ScaleAI/SWE-bench_Pro on HuggingFace\n")
        f.write(f"// Total instances: {len(records)}\n")
        f.write("const SWE_BENCH_PRO_DATA = ")
        json.dump(records, f, indent=None, ensure_ascii=False)
        f.write(";\n")

    file_size = os.path.getsize(output_path)
    print(f"Saved {len(records)} instances to {output_path} ({file_size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
