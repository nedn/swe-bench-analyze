import subprocess
import os
import json
from collections import defaultdict

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
