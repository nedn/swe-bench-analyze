# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Environment Setup
```bash
# Install dependencies using uv (fast Python package manager)
uv sync

# Run any script with uv
uv run <script_name>.py
```

### Main Analysis Scripts
```bash
# Analyze SWE-bench Verified dataset
uv run analyze_swe_bench.py

# Analyze Multi-SWE-bench dataset  
uv run analyze_multi_swe_bench.py

# Analyze SWE-lancer dataset
uv run analyze_swe_lancer.py

# Augment existing stats with patch analysis
uv run augment_swe_bench_stats.py --eval_set verified
```

### Prerequisites
- **scc**: Line counting tool must be installed (`brew install scc` on macOS, `sudo snap install scc` on Linux)
- **git**: For repository cloning and checkout operations
- **uv**: Python package manager for dependency management

## Architecture Overview

This is a code analysis project that examines SWE-bench and related datasets to calculate Lines of Code (LOC) statistics.

### Core Components

**common.py**: Shared utilities
- `check_scc_installed()`: Verifies scc tool availability
- `get_loc_counts(repo_path)`: Runs scc and parses JSON output
- `TARGET_LANGUAGES`: Defines languages to analyze (C, C++, Java, Python, etc.)

**analyze_swe_bench.py**: Main analysis script for SWE-bench Verified
- Downloads Hugging Face dataset using `datasets` library  
- Parallel processing of repositories using `concurrent.futures`
- Clones repos with `--filter=blob:none` (blobless clone) for efficiency
- Checks out specific commits and runs scc analysis
- Outputs results to `swe_bench_verified_loc_stats.csv`

**analyze_multi_swe_bench.py**: Analyzes Multi-SWE-bench across multiple languages
- Processes JSONL files from `Multi-SWE-bench/` directory structure
- Similar parallel processing approach as main script
- Outputs to `multi_swe_bench_loc_stats.csv`

**augment_swe_bench_stats.py**: Patch analysis enhancement
- Parses git diff patches to count added/removed lines
- Augments existing CSV files with patch statistics
- Supports multiple eval sets via argparse (verified, pro, etc.)

### Data Flow
1. Scripts download/load benchmark datasets
2. Group tasks by repository to minimize cloning
3. Use temporary directories with parallel processing
4. Clone repos with blobless strategy for speed
5. Checkout specific commits and run scc analysis
6. Parse scc JSON output into language-specific LOC counts
7. Write results to CSV files with standardized columns

### Output Format
CSV files contain: `instance_id`, `repo`, `commit`, and LOC counts for each target language.