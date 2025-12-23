import subprocess
import os
import json
import csv
from enum import Enum
from collections import defaultdict


class EvalSet(Enum):
    """Enum representing the different evaluation set benchmarks."""
    SWE_BENCH_VERIFIED = "SWE-Bench Verified"
    SWE_BENCH_MULTILINGUAL = "SWE-Bench Multilingual"
    SWE_BENCH_PRO = "SWE-Bench Pro"
    SWE_POLYBENCH = "SWE-PolyBench"
    MULTI_SWE_BENCH = "Multi-SWE-bench"
    SWE_LANCER = "SWE-Lancer"


EVAL_SET_ORGS = {
    EvalSet.SWE_BENCH_VERIFIED: "OpenAI",
    EvalSet.SWE_BENCH_MULTILINGUAL: "SWE-bench",
    EvalSet.SWE_BENCH_PRO: "Scale AI",
    EvalSet.SWE_POLYBENCH: "Amazon",
    EvalSet.MULTI_SWE_BENCH: "ByteDance",
    EvalSet.SWE_LANCER: "OpenAI",
}


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
    # Run scc outputs JSON which is easy to parse
    result = subprocess.run(
        ["scc", repo_path, "--format", "json"],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(result.stdout)

    # Parse result into a lookup dict
    lang_stats = {lang_name: 0 for lang_name in TARGET_LANGUAGES}
    for item in data:
        lang_name = item["Name"]
        if lang_name == "C Header":
            lang_name = "C"
        elif lang_name == "C++ Header":
            lang_name = "C++"
        if lang_name not in lang_stats:
            continue
        lang_stats[lang_name] += item["Code"]

    return lang_stats


def write_loc_stats_csv(output_file, results, eval_set):
    """
    Writes LOC statistics to a CSV file with a standardized format.

    Args:
        output_file: Path to the output CSV file
        results: List of dicts with keys: 'instance_id', 'repo', 'commit', 'stats'
                 where 'stats' is a dict of {language: line_count}
        eval_set: EvalSet enum value representing the evaluation set
    """
    header = ["eval_set", "instance_id", "repo", "commit"] + TARGET_LANGUAGES
    eval_set_name = eval_set.value if isinstance(eval_set, EvalSet) else eval_set

    with open(output_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for res in results:
            stats = res['stats']
            row = [eval_set_name, res['instance_id'], res['repo'], res['commit']]
            for lang in TARGET_LANGUAGES:
                row.append(stats.get(lang, 0))
            writer.writerow(row)

    print(f"Wrote {len(results)} rows to {output_file}")
