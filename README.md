# SWE-bench Code Analysis

This project analyzes the [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) dataset. For every repository and commit in the benchmark, it performs a git checkout and calculates Lines of Code (LOC) for specific programming languages using the `scc` tool.

## Prerequisites

1.  **Git**: Ensure git is installed and configured.
2.  **uv**: An extremely fast Python package installer and resolver.
3.  **scc**: Sloc, Cloc and Code. A very fast line counting tool.

## Installation

### 1. Install `scc`

You must have `scc` installed and available in your system PATH.

**macOS (Homebrew):**
```bash
brew install scc
````

**Linux (Snap):**

```bash
sudo snap install scc
```

**Go (Direct):**

```bash
go install [github.com/boyter/scc/v3@latest](https://github.com/boyter/scc/v3@latest)
```

**Manual Binary Download:**
Download the binary for your system from the [scc releases page](https://github.com/boyter/scc/releases) and place it in your `/usr/local/bin` or add it to your PATH.

### 2\. Python Environment Setup (using uv)

This project uses `uv` for dependency management.

First, initialize a virtual environment and install the dependencies:

```bash
# 1. Sync the virtual environment
```
uv sync
```

## Usage

Run the analysis script:

```bash
uv run analyze_swe_bench.py
```

### What happens next?

1.  The script will download the SWE-bench Verified dataset.
2.  It creates a folder named `repo_cache/`.
3.  For each row in the dataset:
      * It checks if the repo is cloned in `repo_cache`. If not, it clones it.
      * It performs a `git checkout` of the `base_commit`.
      * It runs `scc` to count lines of code.
4.  Results are streamed to `swe_bench_loc_stats.csv`.

### Output Format

The output CSV contains the following columns:

  * `swe_bench_test_id`: The unique instance ID.
  * `repo`: The GitHub repository name.
  * `commit`: The base commit hash used for analysis.
  * `C`, `C++`, `Java`, `Kotlin`, `Python`, `Go`, `Rust`, `JavaScript`, `HTML`: The Line of Code (LOC) counts for each language.

