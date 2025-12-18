# SWE-Bench Complexity Report

This report analyzes the complexity of tasks across various SWE benchmark datasets.

## Summary

| Benchmark | Tasks | Repo LOC (mean) | Patch Total (mean) | Patch Total (median) |
|-----------|-------|-----------------|--------------------|--------------------|
| multi_swe_bench | 1632 | 180.3K | 163.2 | 33 |
| swe_bench_multilingual | 300 | 169.2K | 47.8 | 10 |
| swe_bench_pro | 731 | 266.5K | 169.6 | 94 |
| swe_bench_verified | 500 | 290.2K | 14.3 | 7 |
| swe_lancer | 198 | 536.8K | 33.4 | 14 |

## multi_swe_bench

**Task Count:** 1632

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 180.3K |
| Median | 80.0K |
| Std Dev | 581.7K |
| Min | 1.2K |
| 25th Percentile | 46.2K |
| 75th Percentile | 109.0K |
| Max | 7.8M |

### LOC Stats by Language

| Language | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---------------|------|--------|-----|-----|-----|
| HTML | 777 | 93.3K | 408.0 | 792.2K | 1 | 7.7M |
| JavaScript | 768 | 146.3K | 65.3K | 217.3K | 1 | 661.7K |
| TypeScript | 515 | 57.3K | 4.5K | 69.7K | 38 | 249.4K |
| Go | 481 | 74.0K | 76.1K | 49.3K | 62 | 158.8K |
| Python | 348 | 1.2K | 941.5 | 1.6K | 3 | 6.9K |
| C | 305 | 33.9K | 27.0K | 29.8K | 14 | 100.7K |
| C++ | 253 | 30.4K | 23.6K | 24.2K | 122 | 98.0K |
| Rust | 239 | 48.0K | 38.9K | 41.8K | 3.0K | 229.6K |
| Java | 138 | 90.3K | 61.4K | 80.9K | 69 | 418.9K |
| Ruby | 87 | 22.1K | 146.0 | 25.2K | 15 | 53.4K |
| Kotlin | 27 | 535.1 | 153.0 | 535.0 | 133 | 1.5K |
| PHP | 10 | 165.0 | 165.0 | 0.0 | 165 | 165 |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| JavaScript | 530 | 118.0 / 21 | 35.8 / 4 | 153.8 / 28 |
| Go | 427 | 77.5 / 27 | 23.9 / 5 | 101.4 / 34 |
| Rust | 239 | 185.3 / 38 | 86.2 / 7 | 271.5 / 53 |
| C | 180 | 101.3 / 24 | 21.1 / 5 | 122.4 / 31 |
| C++ | 77 | 360.8 / 92 | 185.1 / 27 | 545.9 / 118 |
| Java | 76 | 27.6 / 18 | 7.2 / 2 | 34.9 / 20 |
| TypeScript | 51 | 15.7 / 7 | 6.3 / 2 | 22.1 / 9 |
| Ruby | 38 | 163.3 / 63 | 45.9 / 10 | 209.2 / 88 |
| HTML | 14 | 54.1 / 18 | 5.1 / 4 | 59.1 / 20 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 120.0 | 24 | 482.4 | 0 | 9 | 72 | 12751 |
| Lines Deleted | 43.2 | 5 | 232.8 | 0 | 1 | 20 | 6151 |
| Total Changed | 163.2 | 33 | 688.2 | 1 | 12 | 95 | 18902 |

## swe_bench_multilingual

**Task Count:** 300

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 169.2K |
| Median | 121.8K |
| Std Dev | 208.1K |
| Min | 3.1K |
| 25th Percentile | 33.3K |
| 75th Percentile | 212.4K |
| Max | 1.3M |

### LOC Stats by Language

| Language | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---------------|------|--------|-----|-----|-----|
| HTML | 205 | 6.5K | 575.0 | 38.1K | 18 | 328.3K |
| JavaScript | 183 | 16.5K | 230.0 | 52.0K | 1 | 362.5K |
| Python | 85 | 15.6K | 1.2K | 35.9K | 39 | 128.6K |
| Ruby | 78 | 69.8K | 17.3K | 85.7K | 2 | 224.1K |
| PHP | 69 | 126.4K | 166.3K | 102.7K | 3 | 264.3K |
| TypeScript | 67 | 26.7K | 2.6K | 37.8K | 221 | 116.5K |
| Java | 57 | 272.5K | 90.1K | 386.5K | 69 | 1.2M |
| C | 56 | 70.7K | 28.9K | 83.9K | 12 | 214.5K |
| Go | 49 | 99.8K | 53.9K | 113.3K | 117 | 398.3K |
| Rust | 43 | 104.2K | 83.3K | 95.1K | 3.1K | 261.1K |
| C++ | 41 | 6.3K | 402.0 | 10.4K | 27 | 45.7K |
| Kotlin | 7 | 134.0 | 134.0 | 0.0 | 134 | 134 |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| Ruby | 44 | 14.5 / 6 | 2.6 / 1 | 17.1 / 8 |
| Java | 43 | 14.4 / 8 | 6.6 / 2 | 21.0 / 11 |
| Rust | 43 | 29.6 / 12 | 13.6 / 4 | 43.2 / 18 |
| PHP | 43 | 15.5 / 7 | 6.4 / 2 | 21.9 / 10 |
| Go | 42 | 31.6 / 8 | 21.5 / 2 | 53.2 / 10 |
| JavaScript | 31 | 12.8 / 5 | 2.5 / 1 | 15.4 / 6 |
| C | 30 | 114.0 / 8 | 109.9 / 2 | 223.9 / 14 |
| TypeScript | 12 | 11.1 / 9 | 5.5 / 5 | 16.6 / 10 |
| C++ | 12 | 15.8 / 5 | 5.2 / 2 | 21.0 / 8 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 28.9 | 7 | 112.5 | 1 | 3 | 18 | 1561 |
| Lines Deleted | 18.9 | 2 | 111.6 | 0 | 1 | 6 | 1617 |
| Total Changed | 47.8 | 10 | 222.9 | 1 | 4 | 24 | 3178 |

## swe_bench_pro

**Task Count:** 731

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 266.5K |
| Median | 105.3K |
| Std Dev | 383.9K |
| Min | 13.0K |
| 25th Percentile | 76.9K |
| 75th Percentile | 228.5K |
| Max | 2.0M |

### LOC Stats by Language

| Language | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---------------|------|--------|-----|-----|-----|
| HTML | 645 | 2.8K | 252.0 | 5.0K | 4 | 15.1K |
| JavaScript | 621 | 17.0K | 10.8K | 25.1K | 4 | 125.2K |
| Python | 484 | 91.8K | 54.3K | 214.5K | 23 | 1.7M |
| Go | 376 | 227.7K | 37.0K | 427.3K | 61 | 1.8M |
| TypeScript | 212 | 202.0K | 197.9K | 179.7K | 8.3K | 786.7K |
| C++ | 130 | 63.1 | 22.0 | 59.9 | 22 | 192 |
| C | 98 | 93.6K | 163.8K | 84.6K | 8 | 180.8K |
| Rust | 52 | 4.8K | 4.2K | 3.5K | 230 | 9.6K |
| Ruby | 27 | 49.4 | 36.0 | 27.8 | 24 | 82 |
| Java | 20 | 2.0K | 53.0 | 2.7K | 53 | 5.7K |
| Kotlin | 13 | 6.2K | 6.4K | 313.8 | 5.5K | 6.6K |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| Go | 280 | 149.7 / 88 | 57.0 / 25 | 206.8 / 138 |
| Python | 266 | 102.8 / 46 | 42.7 / 15 | 145.5 / 74 |
| TypeScript | 140 | 99.0 / 58 | 50.7 / 23 | 149.7 / 94 |
| JavaScript | 45 | 107.4 / 57 | 35.1 / 16 | 142.5 / 76 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 120.3 | 63 | 152.5 | 20 | 33 | 135 | 1467 |
| Lines Deleted | 49.2 | 20 | 89.5 | 0 | 7 | 52 | 805 |
| Total Changed | 169.6 | 94 | 213.7 | 20 | 50 | 207 | 2028 |

## swe_bench_verified

**Task Count:** 500

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 290.2K |
| Median | 305.8K |
| Std Dev | 136.7K |
| Min | 8.1K |
| 25th Percentile | 178.8K |
| 75th Percentile | 389.8K |
| Max | 581.2K |

### LOC Stats by Language

| Language | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---------------|------|--------|-----|-----|-----|
| Python | 500 | 261.7K | 277.9K | 135.9K | 7.9K | 581.2K |
| HTML | 491 | 2.4K | 1.2K | 2.2K | 2 | 5.0K |
| JavaScript | 373 | 17.0K | 18.2K | 11.4K | 2 | 52.3K |
| C | 132 | 43.5K | 3.8K | 72.0K | 1 | 235.7K |
| C++ | 48 | 20.7K | 26.9K | 10.9K | 364 | 29.8K |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| Python | 494 | 9.9 / 4 | 4.4 / 2 | 14.3 / 6 |
| C | 6 | 15.0 / 6 | 4.5 / 5 | 19.5 / 10 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 9.9 | 4 | 17.9 | 0 | 2 | 10 | 202 |
| Lines Deleted | 4.4 | 2 | 8.3 | 0 | 1 | 4 | 89 |
| Total Changed | 14.3 | 7 | 23.9 | 1 | 3 | 13 | 232 |

## swe_lancer

**Task Count:** 198

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 536.8K |
| Median | 521.7K |
| Std Dev | 145.4K |
| Min | 396.6K |
| 25th Percentile | 521.7K |
| 75th Percentile | 521.7K |
| Max | 2.0M |

### LOC Stats by Language

| Language | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---------------|------|--------|-----|-----|-----|
| C | 198 | 31.7 | 32.0 | 0.8 | 27 | 32 |
| Java | 198 | 707.4 | 708.0 | 32.5 | 614 | 982 |
| JavaScript | 198 | 235.0K | 219.1K | 141.8K | 204.7K | 1.6M |
| HTML | 198 | 873.2 | 758.0 | 254.3 | 746 | 1.4K |
| TypeScript | 198 | 300.0K | 300.9K | 27.0K | 26.6K | 337.4K |
| Kotlin | 196 | 142.0 | 141.0 | 4.8 | 135 | 186 |
| Ruby | 196 | 87.1 | 77.0 | 26.4 | 21 | 141 |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| TypeScript | 194 | 17.0 / 4 | 16.9 / 6 | 33.9 / 14 |
| JavaScript | 4 | 2.2 / 2 | 6.2 / 4 | 8.5 / 6 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 16.7 | 4 | 37.1 | 0 | 1 | 15 | 281 |
| Lines Deleted | 16.7 | 6 | 30.9 | 0 | 2 | 18 | 216 |
| Total Changed | 33.4 | 14 | 54.7 | 1 | 4 | 33 | 308 |
