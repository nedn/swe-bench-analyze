# SWE-bench LOC Analysis

📊 **[View Complexity Report](reports/complexity_report.md)**

A comprehensive toolkit for analyzing Lines of Code (LOC) across multiple SWE-bench-style benchmarks. For every repository and commit in each benchmark, the tools perform a git checkout and calculate LOC for target programming languages using the `scc` tool.

## Supported Benchmarks

| Benchmark | Dataset Source | Organization |
|-----------|----------------|--------------|
| **SWE-Bench Verified** | [HuggingFace](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified) | OpenAI |
| **SWE-Bench Multilingual** | [HuggingFace](https://huggingface.co/datasets/SWE-bench/SWE-bench_Multilingual) | SWE-bench |
| **SWE-Bench Pro** | [HuggingFace](https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro) | Scale AI |
| **SWE-PolyBench** | [HuggingFace](https://huggingface.co/datasets/AmazonScience/SWE-PolyBench) | Amazon |
| **Multi-SWE-bench** | [HuggingFace](https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench) | ByteDance |
| **SWE-Lancer** | [GitHub](https://github.com/openai/frontier-evals) | OpenAI |

## Prerequisites

1. **Git**: Ensure git is installed and configured.
2. **uv**: An extremely fast Python package installer and resolver.
3. **scc**: Sloc, Cloc and Code. A very fast line counting tool.

## Installation

### 1. Install `scc`

**macOS (Homebrew):**
```bash
brew install scc
```

**Linux (Snap):**
```bash
sudo snap install scc
```

**Go (Direct):**
```bash
go install github.com/boyter/scc/v3@latest
```

**Manual Binary Download:**
Download the binary from the [scc releases page](https://github.com/boyter/scc/releases).

### 2. Python Environment Setup

```bash
uv sync
```

## Usage

### Analysis Scripts

#### SWE-Bench Analysis
Analyze LOC statistics for SWE-Bench datasets:

```bash
# Analyze SWE-Bench Verified (default)
uv run analyze_swe_bench.py

# Analyze a specific dataset
uv run analyze_swe_bench.py --eval-set verified|multilingual|pro|polybench|all

# Customize parallelism
uv run analyze_swe_bench.py --max-workers 16
```

#### Multi-SWE-Bench Analysis
Analyze the Multi-SWE-bench dataset (requires downloading data first):

```bash
# Download Multi-SWE-bench data following instructions at:
# https://huggingface.co/datasets/ByteDance-Seed/Multi-SWE-bench

uv run analyze_multi_swe_bench.py --max-workers 8
```

#### SWE-Lancer Analysis
Analyze the SWE-Lancer dataset (Expensify/App):

```bash
uv run analyze_swe_lancer.py

# Limit items for testing
uv run analyze_swe_lancer.py --max-items 10
```

### Augmentation Scripts

Add golden solution patch statistics to existing LOC data:

```bash
# Augment all SWE-Bench datasets
uv run augment_swe_bench_stats.py --eval-set all

# Augment Multi-SWE-bench
uv run augment_multi_swe_bench_stats.py

# Augment SWE-Lancer
uv run augment_swe_lancer_stats.py
```

Augmented files are saved to `augmented/` with columns:
- `golden_patch_added`: Lines added in the golden solution
- `golden_patch_deleted`: Lines deleted in the golden solution
- `golden_patch_total`: Total lines changed

### Report Generation

Generate complexity analysis reports:

```bash
uv run report.py
```

Reports are saved to `reports/`:
- `complexity_summary.csv`: Summary statistics
- `complexity_report.md`: Detailed markdown report

## Output Files

### Raw LOC Stats CSV Files

| File | Description |
|------|-------------|
| `swe_bench_verified_loc_stats.csv` | 500 tasks from SWE-Bench Verified |
| `swe_bench_multilingual_loc_stats.csv` | Multilingual benchmark tasks |
| `swe_bench_pro_loc_stats.csv` | SWE-Bench Pro tasks |
| `swe_polybench_loc_stats.csv` | SWE-PolyBench tasks |
| `multi_swe_bench_loc_stats.csv` | Multi-SWE-bench tasks |
| `swe_lancer_loc_stats.csv` | SWE-Lancer tasks |

### CSV Columns

- `eval_set`: Benchmark name
- `instance_id`: Unique task identifier
- `repo`: GitHub repository name
- `commit`: Base commit hash
- `C`, `C++`, `Java`, `Kotlin`, `Python`, `Go`, `Rust`, `JavaScript`, `HTML`, `Ruby`, `TypeScript`, `PHP`: LOC per language

## Project Structure

```
.
├── analyze_swe_bench.py          # Main SWE-Bench analysis
├── analyze_multi_swe_bench.py    # Multi-SWE-bench analysis
├── analyze_swe_lancer.py         # SWE-Lancer analysis
├── augment_swe_bench_stats.py    # Add patch stats to SWE-Bench CSVs
├── augment_multi_swe_bench_stats.py
├── augment_swe_lancer_stats.py
├── report.py                     # Generate complexity reports
├── common.py                     # Shared utilities
├── augmented/                    # Augmented CSV files
├── reports/                      # Generated reports
└── Multi-SWE-bench/              # Multi-SWE-bench data (download separately)
```

## License

MIT License - See [LICENSE](LICENSE)
