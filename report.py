#!/usr/bin/env python3
"""
SWE-Bench Complexity Report Generator

Analyzes augmented benchmark data and generates complexity statistics
for each benchmark dataset. Outputs to console, CSV, and Markdown.
"""

import pandas as pd
from pathlib import Path
from common import TARGET_LANGUAGES

AUGMENTED_DIR = Path("augmented")
REPORTS_DIR = Path("reports")


def load_benchmark_data() -> dict[str, pd.DataFrame]:
    """Load all augmented CSV files from the augmented directory."""
    benchmarks = {}
    for csv_file in sorted(AUGMENTED_DIR.glob("*_augmented.csv")):
        # Extract benchmark name from filename
        # e.g., "swe_bench_verified_loc_stats_augmented.csv" -> "swe_bench_verified"
        name = csv_file.stem.replace("_loc_stats_augmented", "")
        df = pd.read_csv(csv_file)
        benchmarks[name] = df
    return benchmarks


def get_primary_language(row: pd.Series) -> str:
    """Determine the primary language for a task based on max LOC."""
    lang_cols = [col for col in TARGET_LANGUAGES if col in row.index]
    loc_values = {lang: row[lang] for lang in lang_cols}
    primary = max(loc_values, key=loc_values.get)
    return primary if loc_values[primary] > 0 else "Unknown"


def compute_stats(series: pd.Series) -> dict:
    """Compute standard statistics for a numeric series."""
    return {
        "mean": series.mean(),
        "median": series.median(),
        "std": series.std(),
        "min": series.min(),
        "25%": series.quantile(0.25),
        "75%": series.quantile(0.75),
        "max": series.max(),
    }


def analyze_benchmark(name: str, df: pd.DataFrame) -> dict:
    """Analyze a single benchmark dataset and return stats."""
    results = {
        "name": name,
        "task_count": len(df),
    }

    # Compute total LOC per task
    lang_cols = [col for col in TARGET_LANGUAGES if col in df.columns]
    df["total_loc"] = df[lang_cols].sum(axis=1)

    # Repository size stats
    results["repo_size_stats"] = compute_stats(df["total_loc"])

    # LOC stats by language
    loc_by_lang = {}
    for lang in lang_cols:
        tasks_with_code = df[df[lang] > 0]
        if len(tasks_with_code) > 0:
            loc_by_lang[lang] = {
                "tasks_with_code": len(tasks_with_code),
                **compute_stats(tasks_with_code[lang]),
            }
    results["loc_by_language"] = loc_by_lang

    # Determine primary language for each task
    df["primary_language"] = df.apply(get_primary_language, axis=1)

    # Patch complexity stats per primary language
    patch_cols = ["golden_patch_added", "golden_patch_deleted", "golden_patch_total"]
    patch_by_lang = {}
    for lang in df["primary_language"].unique():
        lang_df = df[df["primary_language"] == lang]
        if len(lang_df) > 0:
            patch_by_lang[lang] = {
                "task_count": len(lang_df),
                "added": compute_stats(lang_df["golden_patch_added"]),
                "deleted": compute_stats(lang_df["golden_patch_deleted"]),
                "total": compute_stats(lang_df["golden_patch_total"]),
            }
    results["patch_by_language"] = patch_by_lang

    # Overall patch complexity stats
    results["patch_overall"] = {
        "added": compute_stats(df["golden_patch_added"]),
        "deleted": compute_stats(df["golden_patch_deleted"]),
        "total": compute_stats(df["golden_patch_total"]),
    }

    # Repository-level stats
    results["repositories"] = analyze_repositories(df, lang_cols)

    return results


def analyze_repositories(df: pd.DataFrame, lang_cols: list[str]) -> list[dict]:
    """Analyze stats per repository."""
    repos = []
    for repo_name, repo_df in df.groupby("repo"):
        # Get max LOC for each language across tasks
        lang_max = {lang: repo_df[lang].max() for lang in lang_cols}

        # Max repo size (max total_loc across all tasks for this repo)
        max_repo_size = repo_df["total_loc"].max()

        # Filter languages with LOC >= 5% of total and sort by LOC descending
        threshold = max_repo_size * 0.05
        main_langs = [
            (lang, loc) for lang, loc in sorted(lang_max.items(), key=lambda x: x[1], reverse=True)
            if loc >= threshold
        ]

        # Number of tasks
        task_count = len(repo_df)

        # Median task complexity (median of golden_patch_total)
        median_complexity = repo_df["golden_patch_total"].median()

        repos.append({
            "name": repo_name,
            "main_languages": main_langs,  # List of (lang, loc) tuples
            "max_repo_size": max_repo_size,
            "task_count": task_count,
            "median_complexity": median_complexity,
        })

    # Sort by task count descending
    repos.sort(key=lambda x: x["task_count"], reverse=True)
    return repos


def format_number(val, decimals=1) -> str:
    """Format a number for display."""
    if pd.isna(val):
        return "N/A"
    if abs(val) >= 1_000_000:
        return f"{val/1_000_000:.{decimals}f}M"
    if abs(val) >= 1_000:
        return f"{val/1_000:.{decimals}f}K"
    if isinstance(val, float):
        return f"{val:.{decimals}f}"
    return str(int(val))


def print_benchmark_report(results: dict):
    """Print formatted report for a single benchmark to console."""
    print(f"\n{'='*70}")
    print(f"  Benchmark: {results['name']}")
    print(f"{'='*70}")
    print(f"\nTask Count: {results['task_count']}")

    # Repository Size Stats
    print(f"\n--- Repository Size Stats (Total LOC) ---")
    stats = results["repo_size_stats"]
    print(f"  Mean: {format_number(stats['mean']):>10}  |  Median: {format_number(stats['median']):>10}  |  Std: {format_number(stats['std']):>10}")
    print(f"  Min:  {format_number(stats['min']):>10}  |  25%:    {format_number(stats['25%']):>10}  |  75%: {format_number(stats['75%']):>10}  |  Max: {format_number(stats['max']):>10}")

    # LOC Stats by Language
    print(f"\n--- LOC Stats by Language ---")
    print(f"  {'Language':<12} {'Tasks':>7} {'Mean':>10} {'Median':>10} {'Std':>10} {'Min':>8} {'Max':>10}")
    print(f"  {'-'*12} {'-'*7} {'-'*10} {'-'*10} {'-'*10} {'-'*8} {'-'*10}")

    # Sort by task count descending
    sorted_langs = sorted(
        results["loc_by_language"].items(),
        key=lambda x: x[1]["tasks_with_code"],
        reverse=True,
    )
    for lang, stats in sorted_langs:
        print(
            f"  {lang:<12} {stats['tasks_with_code']:>7} "
            f"{format_number(stats['mean']):>10} {format_number(stats['median']):>10} "
            f"{format_number(stats['std']):>10} {format_number(stats['min']):>8} "
            f"{format_number(stats['max']):>10}"
        )

    # Patch Complexity Stats per Primary Language
    print(f"\n--- Patch Complexity by Primary Language ---")
    print(f"  {'Primary Lang':<12} {'Tasks':>6} {'Added':>14} {'Deleted':>14} {'Total':>14}")
    print(f"  {'':<12} {'':<6} {'(mean/med)':>14} {'(mean/med)':>14} {'(mean/med)':>14}")
    print(f"  {'-'*12} {'-'*6} {'-'*14} {'-'*14} {'-'*14}")

    # Sort by task count descending
    sorted_patch = sorted(
        results["patch_by_language"].items(),
        key=lambda x: x[1]["task_count"],
        reverse=True,
    )
    for lang, stats in sorted_patch:
        added = f"{stats['added']['mean']:.1f}/{stats['added']['median']:.0f}"
        deleted = f"{stats['deleted']['mean']:.1f}/{stats['deleted']['median']:.0f}"
        total = f"{stats['total']['mean']:.1f}/{stats['total']['median']:.0f}"
        print(f"  {lang:<12} {stats['task_count']:>6} {added:>14} {deleted:>14} {total:>14}")

    # Overall Patch Complexity
    print(f"\n--- Overall Patch Complexity ---")
    print(f"  {'Metric':<15} {'Mean':>8} {'Median':>8} {'Std':>8} {'Min':>6} {'25%':>8} {'75%':>8} {'Max':>8}")
    print(f"  {'-'*15} {'-'*8} {'-'*8} {'-'*8} {'-'*6} {'-'*8} {'-'*8} {'-'*8}")
    for metric_name, key in [("Lines Added", "added"), ("Lines Deleted", "deleted"), ("Total Changed", "total")]:
        s = results["patch_overall"][key]
        print(
            f"  {metric_name:<15} {s['mean']:>8.1f} {s['median']:>8.0f} {s['std']:>8.1f} "
            f"{s['min']:>6.0f} {s['25%']:>8.0f} {s['75%']:>8.0f} {s['max']:>8.0f}"
        )


def generate_summary_csv(all_results: list[dict], output_path: Path):
    """Generate a summary CSV with key stats for all benchmarks."""
    rows = []
    for res in all_results:
        row = {
            "benchmark": res["name"],
            "task_count": res["task_count"],
            # Repo size stats
            "repo_loc_mean": res["repo_size_stats"]["mean"],
            "repo_loc_median": res["repo_size_stats"]["median"],
            "repo_loc_std": res["repo_size_stats"]["std"],
            "repo_loc_min": res["repo_size_stats"]["min"],
            "repo_loc_25pct": res["repo_size_stats"]["25%"],
            "repo_loc_75pct": res["repo_size_stats"]["75%"],
            "repo_loc_max": res["repo_size_stats"]["max"],
            # Patch stats - added
            "patch_added_mean": res["patch_overall"]["added"]["mean"],
            "patch_added_median": res["patch_overall"]["added"]["median"],
            "patch_added_std": res["patch_overall"]["added"]["std"],
            "patch_added_min": res["patch_overall"]["added"]["min"],
            "patch_added_max": res["patch_overall"]["added"]["max"],
            # Patch stats - deleted
            "patch_deleted_mean": res["patch_overall"]["deleted"]["mean"],
            "patch_deleted_median": res["patch_overall"]["deleted"]["median"],
            "patch_deleted_std": res["patch_overall"]["deleted"]["std"],
            "patch_deleted_min": res["patch_overall"]["deleted"]["min"],
            "patch_deleted_max": res["patch_overall"]["deleted"]["max"],
            # Patch stats - total
            "patch_total_mean": res["patch_overall"]["total"]["mean"],
            "patch_total_median": res["patch_overall"]["total"]["median"],
            "patch_total_std": res["patch_overall"]["total"]["std"],
            "patch_total_min": res["patch_overall"]["total"]["min"],
            "patch_total_max": res["patch_overall"]["total"]["max"],
        }

        # Add top 3 languages by task count
        sorted_langs = sorted(
            res["loc_by_language"].items(),
            key=lambda x: x[1]["tasks_with_code"],
            reverse=True,
        )[:3]
        for i, (lang, stats) in enumerate(sorted_langs, 1):
            row[f"top{i}_language"] = lang
            row[f"top{i}_tasks"] = stats["tasks_with_code"]
            row[f"top{i}_loc_mean"] = stats["mean"]

        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"\nSummary CSV saved to: {output_path}")


def generate_markdown_report(all_results: list[dict], output_path: Path):
    """Generate a detailed Markdown report."""
    lines = []
    lines.append("# SWE-Bench Complexity Report\n")
    lines.append("This report analyzes the complexity of tasks across various SWE benchmark datasets.\n")

    # Summary table
    lines.append("## Summary\n")
    lines.append("| Benchmark | Tasks | Repo LOC (mean) | Patch Total (mean) | Patch Total (median) |")
    lines.append("|-----------|-------|-----------------|--------------------|--------------------|")
    for res in all_results:
        lines.append(
            f"| {res['name']} | {res['task_count']} | "
            f"{format_number(res['repo_size_stats']['mean'])} | "
            f"{res['patch_overall']['total']['mean']:.1f} | "
            f"{res['patch_overall']['total']['median']:.0f} |"
        )
    lines.append("")

    # Detailed sections for each benchmark
    for res in all_results:
        lines.append(f"## {res['name']}\n")
        lines.append(f"**Task Count:** {res['task_count']}\n")

        # Repository Size Stats
        lines.append("### Repository Size Stats (Total LOC)\n")
        stats = res["repo_size_stats"]
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Mean | {format_number(stats['mean'])} |")
        lines.append(f"| Median | {format_number(stats['median'])} |")
        lines.append(f"| Std Dev | {format_number(stats['std'])} |")
        lines.append(f"| Min | {format_number(stats['min'])} |")
        lines.append(f"| 25th Percentile | {format_number(stats['25%'])} |")
        lines.append(f"| 75th Percentile | {format_number(stats['75%'])} |")
        lines.append(f"| Max | {format_number(stats['max'])} |")
        lines.append("")

        # LOC by Language
        lines.append("### LOC Stats by Language\n")
        lines.append("| Language | Tasks w/ Code | Mean | Median | Std | Min | Max |")
        lines.append("|----------|---------------|------|--------|-----|-----|-----|")
        sorted_langs = sorted(
            res["loc_by_language"].items(),
            key=lambda x: x[1]["tasks_with_code"],
            reverse=True,
        )
        for lang, stats in sorted_langs:
            lines.append(
                f"| {lang} | {stats['tasks_with_code']} | "
                f"{format_number(stats['mean'])} | {format_number(stats['median'])} | "
                f"{format_number(stats['std'])} | {format_number(stats['min'])} | "
                f"{format_number(stats['max'])} |"
            )
        lines.append("")

        # Patch Complexity by Primary Language
        lines.append("### Patch Complexity by Primary Language\n")
        lines.append("| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |")
        lines.append("|------------------|-------|---------------------|----------------------|---------------------|")
        sorted_patch = sorted(
            res["patch_by_language"].items(),
            key=lambda x: x[1]["task_count"],
            reverse=True,
        )
        for lang, stats in sorted_patch:
            lines.append(
                f"| {lang} | {stats['task_count']} | "
                f"{stats['added']['mean']:.1f} / {stats['added']['median']:.0f} | "
                f"{stats['deleted']['mean']:.1f} / {stats['deleted']['median']:.0f} | "
                f"{stats['total']['mean']:.1f} / {stats['total']['median']:.0f} |"
            )
        lines.append("")

        # Overall Patch Complexity
        lines.append("### Overall Patch Complexity\n")
        lines.append("| Metric | Mean | Median | Std | Min | 25% | 75% | Max |")
        lines.append("|--------|------|--------|-----|-----|-----|-----|-----|")
        for metric_name, key in [("Lines Added", "added"), ("Lines Deleted", "deleted"), ("Total Changed", "total")]:
            s = res["patch_overall"][key]
            lines.append(
                f"| {metric_name} | {s['mean']:.1f} | {s['median']:.0f} | "
                f"{s['std']:.1f} | {s['min']:.0f} | {s['25%']:.0f} | "
                f"{s['75%']:.0f} | {s['max']:.0f} |"
            )
        lines.append("")

        # Repositories
        lines.append("### Repositories\n")
        lines.append("| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |")
        lines.append("|------------|----------------|---------------|-------|-------------------|")
        for repo in res["repositories"]:
            # Format languages with LOC: "Python (1.1M), JavaScript (10.1K)"
            if repo["main_languages"]:
                langs_str = ", ".join(
                    f"{lang} ({format_number(loc)})" for lang, loc in repo["main_languages"]
                )
            else:
                langs_str = "N/A"
            lines.append(
                f"| {repo['name']} | {langs_str} | "
                f"{format_number(repo['max_repo_size'])} | {repo['task_count']} | "
                f"{repo['median_complexity']:.0f} |"
            )
        lines.append("")

    output_path.write_text("\n".join(lines))
    print(f"Markdown report saved to: {output_path}")


def main():
    print("SWE-Bench Complexity Report Generator")
    print("=" * 40)

    # Load all benchmark data
    print(f"\nLoading data from {AUGMENTED_DIR}/...")
    benchmarks = load_benchmark_data()
    print(f"Found {len(benchmarks)} benchmarks: {', '.join(benchmarks.keys())}")

    # Analyze each benchmark
    all_results = []
    for name, df in benchmarks.items():
        results = analyze_benchmark(name, df)
        all_results.append(results)
        print_benchmark_report(results)

    # Create reports directory
    REPORTS_DIR.mkdir(exist_ok=True)

    # Generate output files
    generate_summary_csv(all_results, REPORTS_DIR / "complexity_summary.csv")
    generate_markdown_report(all_results, REPORTS_DIR / "complexity_report.md")

    print(f"\nReport generation complete!")


if __name__ == "__main__":
    main()
