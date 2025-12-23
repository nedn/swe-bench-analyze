# SWE-Bench Complexity Report

This report analyzes the complexity of tasks across various SWE benchmark datasets.

## Summary

| Benchmark | Org | Tasks | Repo LOC (mean) | Patch Total (mean) | Patch Total (median) | Main Languages |
|-----------|-----|-------|-----------------|--------------------|--------------------|----------------|
| Multi-SWE-bench | ByteDance | 1632 | 180.3K | 163.2 | 33 | JavaScript (38.2%), HTML (24.6%), Go (12.1%) |
| SWE-Bench Multilingual | SWE-bench | 300 | 173.4K | 47.8 | 10 | Java (29.9%), PHP (16.8%), Ruby (10.5%) |
| SWE-Bench Pro | Scale AI | 731 | 276.1K | 169.6 | 94 | Go (42.4%), Python (22.0%), TypeScript (21.2%) |
| SWE-Bench Verified | OpenAI | 500 | 292.9K | 14.3 | 7 | Python (90.0%), JavaScript (4.6%), C (3.9%) |
| SWE-Lancer | OpenAI | 198 | 536.8K | 33.4 | 14 | TypeScript (55.9%), JavaScript (43.8%) |
| SWE-PolyBench | Amazon | 2110 | 257.9K | 51.2 | 19 | TypeScript (37.8%), JavaScript (34.4%), Python (17.5%) |

## Multi-SWE-bench

**Organization:** ByteDance  
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

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| JavaScript | 38.2% | 768 | 146.3K | 65.3K | 217.3K | 1 | 661.7K |
| HTML | 24.6% | 777 | 93.3K | 408.0 | 792.2K | 1 | 7.7M |
| Go | 12.1% | 481 | 74.0K | 76.1K | 49.3K | 62 | 158.8K |
| TypeScript | 10.0% | 515 | 57.3K | 4.5K | 69.7K | 38 | 249.4K |
| Java | 4.2% | 138 | 90.3K | 61.4K | 80.9K | 69 | 418.9K |
| Rust | 3.9% | 239 | 48.0K | 38.9K | 41.8K | 3.0K | 229.6K |
| C | 3.5% | 305 | 33.9K | 27.0K | 29.8K | 14 | 100.7K |
| C++ | 2.6% | 253 | 30.4K | 23.6K | 24.2K | 122 | 98.0K |

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

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| cli/cli | Go (158.8K), JavaScript (33.6K) | 158.8K | 397 | 34 |
| sveltejs/svelte | JavaScript (80.3K), TypeScript (4.7K) | 85.4K | 272 | 32 |
| mui/material-ui | JavaScript (661.7K), TypeScript (249.4K) | 911.1K | 174 | 36 |
| clap-rs/clap | Rust (75.9K) | 76.6K | 132 | 51 |
| ponylang/ponyc | C (82.0K), C++ (37.4K) | 121.5K | 82 | 36 |
| iamkun/dayjs | JavaScript (15.8K) | 15.8K | 56 | 6 |
| nlohmann/json | C++ (98.0K), C (7.4K), Python (5.9K) | 106.7K | 55 | 106 |
| vuejs/core | TypeScript (116.5K) | 120.6K | 48 | 10 |
| fasterxml/jackson-databind | HTML (7.7M) | 7.8M | 42 | 18 |
| fmtlib/fmt | C (33.8K), C++ (20.1K) | 50.4K | 41 | 18 |
| elastic/logstash | Ruby (53.4K), Java (45.8K) | 100.7K | 38 | 88 |
| facebook/zstd | C (87.7K), C++ (5.9K) | 98.1K | 29 | 42 |
| tokio-rs/tokio | Rust (87.0K) | 87.0K | 25 | 116 |
| tokio-rs/tracing | Rust (39.5K) | 39.5K | 21 | 123 |
| simdjson/simdjson | C (100.7K), C++ (67.2K) | 168.7K | 20 | 218 |
| anuraghazra/github-readme-stats | JavaScript (10.2K) | 10.2K | 19 | 60 |
| fasterxml/jackson-core | HTML (2.2M) | 2.2M | 18 | 25 |
| jqlang/jq | C (34.0K) | 34.7K | 17 | 10 |
| grpc/grpc-go | Go (88.3K) | 88.3K | 16 | 29 |
| zeromicro/go-zero | Go (90.6K) | 90.6K | 15 | 31 |
| BurntSushi/ripgrep | Rust (30.9K) | 32.2K | 14 | 28 |
| nushell/nushell | Rust (229.6K) | 229.8K | 14 | 38 |
| sharkdp/fd | Rust (4.0K) | 4.0K | 14 | 46 |
| catchorg/Catch2 | C++ (51.5K), C (4.3K) | 53.3K | 12 | 88 |
| sharkdp/bat | Rust (11.4K), Python (6.9K), JavaScript (6.9K) | 26.9K | 10 | 76 |
| alibaba/fastjson2 | Java (418.9K) | 420.6K | 6 | 6 |
| mockito/mockito | Java (62.5K) | 63.3K | 6 | 52 |
| fasterxml/jackson-dataformat-xml | HTML (655.9K) | 672.3K | 5 | 23 |
| google/gson | Java (27.9K), HTML (23.2K) | 48.6K | 5 | 22 |
| googlecontainertools/jib | Java (56.1K) | 56.4K | 5 | 6 |
| tokio-rs/bytes | Rust (5.8K) | 5.8K | 5 | 37 |
| axios/axios | JavaScript (21.5K) | 22.9K | 4 | 33 |
| expressjs/express | JavaScript (16.9K) | 17.0K | 4 | 7 |
| apache/dubbo | Java (214.5K) | 214.5K | 3 | 4 |
| darkreader/darkreader | TypeScript (18.7K), JavaScript (2.1K) | 20.9K | 2 | 13 |
| rayon-rs/rayon | Rust (25.5K) | 25.5K | 2 | 638 |
| serde-rs/serde | Rust (30.3K) | 30.3K | 2 | 72 |
| Kong/insomnia | TypeScript (98.8K), JavaScript (93.6K) | 192.5K | 1 | 1 |
| yhirose/cpp-httplib | C++ (15.0K), C (13.6K) | 28.6K | 1 | 1 |

## SWE-Bench Multilingual

**Organization:** SWE-bench  
**Task Count:** 300

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 173.4K |
| Median | 122.0K |
| Std Dev | 208.3K |
| Min | 3.1K |
| 25th Percentile | 39.8K |
| 75th Percentile | 215.4K |
| Max | 1.3M |

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| Java | 29.9% | 57 | 272.5K | 90.1K | 386.5K | 69 | 1.2M |
| PHP | 16.8% | 69 | 126.4K | 166.3K | 102.7K | 3 | 264.3K |
| Ruby | 10.5% | 78 | 69.8K | 17.3K | 85.7K | 2 | 224.1K |
| C | 9.9% | 73 | 70.6K | 26.3K | 97.7K | 30 | 308.2K |
| Go | 9.4% | 49 | 99.8K | 53.9K | 113.3K | 117 | 398.3K |
| Rust | 8.6% | 43 | 104.2K | 83.3K | 95.1K | 3.1K | 261.1K |
| JavaScript | 5.8% | 183 | 16.5K | 230.0 | 52.0K | 1 | 362.5K |
| TypeScript | 3.4% | 67 | 26.7K | 2.6K | 37.8K | 221 | 116.5K |
| HTML | 2.6% | 205 | 6.5K | 575.0 | 38.1K | 18 | 328.3K |
| Python | 2.6% | 85 | 15.6K | 1.2K | 35.9K | 39 | 128.6K |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| Ruby | 44 | 14.5 / 6 | 2.6 / 1 | 17.1 / 8 |
| Java | 43 | 14.4 / 8 | 6.6 / 2 | 21.0 / 11 |
| Rust | 43 | 29.6 / 12 | 13.6 / 4 | 43.2 / 18 |
| PHP | 43 | 15.5 / 7 | 6.4 / 2 | 21.9 / 10 |
| Go | 42 | 31.6 / 8 | 21.5 / 2 | 53.2 / 10 |
| C | 41 | 88.0 / 7 | 81.9 / 2 | 169.9 / 13 |
| JavaScript | 31 | 12.8 / 5 | 2.5 / 1 | 15.4 / 6 |
| TypeScript | 12 | 11.1 / 9 | 5.5 / 5 | 16.6 / 10 |
| C++ | 1 | 4.0 / 4 | 2.0 / 2 | 6.0 / 6 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 28.9 | 7 | 112.5 | 1 | 3 | 18 | 1561 |
| Lines Deleted | 18.9 | 2 | 111.6 | 0 | 1 | 6 | 1617 |
| Total Changed | 47.8 | 10 | 222.9 | 1 | 4 | 24 | 3178 |

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| preactjs/preact | JavaScript (34.8K) | 36.9K | 17 | 7 |
| projectlombok/lombok | Java (98.0K) | 102.0K | 17 | 11 |
| rubocop/rubocop | Ruby (224.1K) | 224.7K | 16 | 10 |
| caddyserver/caddy | Go (55.4K) | 56.5K | 14 | 16 |
| laravel/framework | PHP (264.3K) | 264.4K | 13 | 4 |
| fluent/fluentd | Ruby (82.7K) | 82.7K | 12 | 8 |
| redis/redis | C (207.6K) | 216.6K | 12 | 14 |
| fmtlib/fmt | C (31.4K), C++ (19.7K) | 48.2K | 11 | 8 |
| briannesbitt/carbon | PHP (166.3K) | 166.3K | 10 | 16 |
| php-cs-fixer/php-cs-fixer | PHP (207.4K) | 207.4K | 10 | 10 |
| phpoffice/phpspreadsheet | PHP (196.5K) | 196.9K | 10 | 12 |
| apache/lucene | Java (868.5K) | 882.7K | 9 | 7 |
| google/gson | Java (33.6K), HTML (23.2K) | 48.0K | 9 | 9 |
| jqlang/jq | C (33.9K) | 34.3K | 9 | 32 |
| tokio-rs/tokio | Rust (87.3K) | 87.3K | 9 | 7 |
| gin-gonic/gin | Go (15.0K) | 15.0K | 8 | 2 |
| prometheus/prometheus | Go (198.8K), TypeScript (33.9K), JavaScript (13.2K) | 236.3K | 8 | 29 |
| sharkdp/bat | Rust (10.8K), Python (6.9K), JavaScript (6.9K) | 26.3K | 8 | 18 |
| astral-sh/ruff | Rust (261.1K), Python (128.6K) | 391.6K | 7 | 14 |
| fastlane/fastlane | Ruby (124.6K) | 125.7K | 7 | 5 |
| gohugoio/hugo | Go (140.6K) | 148.8K | 7 | 4 |
| tokio-rs/axum | Rust (24.5K) | 24.5K | 7 | 64 |
| axios/axios | JavaScript (25.3K) | 26.8K | 6 | 5 |
| apache/druid | Java (1.2M) | 1.3M | 5 | 11 |
| babel/babel | JavaScript (174.6K), TypeScript (95.5K) | 270.2K | 5 | 2 |
| facebook/docusaurus | TypeScript (77.5K), JavaScript (67.9K) | 145.8K | 5 | 23 |
| hashicorp/terraform | Go (398.3K) | 398.3K | 5 | 43 |
| jekyll/jekyll | Ruby (17.5K), JavaScript (1.1K), HTML (1.0K) | 19.6K | 5 | 10 |
| micropython/micropython | C (308.2K), Python (56.2K) | 366.1K | 5 | 8 |
| nushell/nushell | Rust (228.8K) | 229.0K | 5 | 15 |
| uutils/coreutils | Rust (128.0K) | 128.5K | 5 | 24 |
| vuejs/core | TypeScript (116.5K) | 120.6K | 5 | 11 |
| valkey-io/valkey | C (218.8K) | 228.3K | 4 | 7 |
| mrdoob/three.js | JavaScript (362.5K), HTML (328.3K) | 683.3K | 3 | 6 |
| burntsushi/ripgrep | Rust (30.1K) | 31.4K | 2 | 44 |
| faker-ruby/faker | Ruby (20.9K) | 20.9K | 2 | 3 |
| immutable-js/immutable-js | TypeScript (11.1K), JavaScript (7.3K) | 18.3K | 2 | 9 |
| javaparser/javaparser | Java (214.4K) | 214.4K | 2 | 82 |
| jordansissel/fpm | Ruby (8.6K) | 8.7K | 2 | 28 |
| nlohmann/json | C++ (96.9K), C (6.8K) | 104.5K | 1 | 6 |
| reactivex/rxjava | Java (315.3K) | 315.3K | 1 | 5 |

## SWE-Bench Pro

**Organization:** Scale AI  
**Task Count:** 731

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 276.1K |
| Median | 105.3K |
| Std Dev | 401.7K |
| Min | 13.0K |
| 25th Percentile | 76.9K |
| 75th Percentile | 228.5K |
| Max | 2.1M |

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| Go | 42.4% | 376 | 227.7K | 37.0K | 427.3K | 61 | 1.8M |
| Python | 22.0% | 484 | 91.8K | 54.3K | 214.5K | 23 | 1.7M |
| TypeScript | 21.2% | 212 | 202.0K | 197.9K | 179.7K | 8.3K | 786.7K |
| C | 8.0% | 149 | 108.4K | 108.2K | 98.3K | 8 | 276.4K |
| JavaScript | 5.2% | 621 | 17.0K | 10.8K | 25.1K | 4 | 125.2K |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| Go | 280 | 149.7 / 88 | 57.0 / 25 | 206.8 / 138 |
| Python | 266 | 102.8 / 46 | 42.7 / 15 | 145.5 / 74 |
| TypeScript | 133 | 100.4 / 59 | 50.6 / 22 | 151.1 / 94 |
| JavaScript | 45 | 107.4 / 57 | 35.1 / 16 | 142.5 / 76 |
| C | 7 | 72.4 / 56 | 51.4 / 32 | 123.9 / 88 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 120.3 | 63 | 152.5 | 20 | 33 | 135 | 1467 |
| Lines Deleted | 49.2 | 20 | 89.5 | 0 | 7 | 52 | 805 |
| Total Changed | 169.6 | 94 | 213.7 | 20 | 50 | 207 | 2028 |

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| ansible/ansible | Python (1.7M) | 1.7M | 96 | 86 |
| internetarchive/openlibrary | Python (63.6K), HTML (15.1K), JavaScript (11.7K) | 90.0K | 91 | 97 |
| flipt-io/flipt | Go (87.0K), TypeScript (16.6K) | 103.5K | 85 | 153 |
| qutebrowser/qutebrowser | Python (88.9K), JavaScript (19.8K) | 113.8K | 79 | 52 |
| gravitational/teleport | Go (1.8M), C (276.4K), TypeScript (132.8K) | 2.1M | 76 | 113 |
| protonmail/webclients | TypeScript (786.7K), JavaScript (125.2K) | 912.9K | 65 | 103 |
| future-architect/vuls | Go (73.8K) | 73.8K | 62 | 160 |
| navidrome/navidrome | Go (48.0K), JavaScript (15.8K) | 54.1K | 57 | 109 |
| element-hq/element-web | TypeScript (246.1K), JavaScript (53.9K) | 252.2K | 56 | 82 |
| NodeBB/NodeBB | JavaScript (108.2K) | 108.4K | 44 | 74 |
| tutao/tutanota | TypeScript (214.7K), C (210.9K), JavaScript (56.0K) | 487.6K | 20 | 110 |

## SWE-Bench Verified

**Organization:** OpenAI  
**Task Count:** 500

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 292.9K |
| Median | 307.4K |
| Std Dev | 139.5K |
| Min | 8.1K |
| 25th Percentile | 179.2K |
| 75th Percentile | 392.3K |
| Max | 597.4K |

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| Python | 90.0% | 500 | 263.6K | 278.1K | 138.6K | 7.9K | 597.3K |
| JavaScript | 4.6% | 373 | 18.0K | 19.7K | 11.5K | 2 | 52.4K |
| C | 3.9% | 132 | 43.5K | 3.8K | 72.0K | 1 | 235.7K |

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

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| django/django | Python (376.5K), JavaScript (20.5K) | 401.9K | 231 | 6 |
| sympy/sympy | Python (597.3K) | 597.4K | 75 | 7 |
| sphinx-doc/sphinx | Python (84.4K), JavaScript (52.4K) | 131.0K | 44 | 8 |
| matplotlib/matplotlib | Python (185.9K), C (59.4K), C++ (29.8K) | 257.3K | 34 | 7 |
| scikit-learn/scikit-learn | Python (275.8K) | 283.0K | 32 | 8 |
| astropy/astropy | Python (284.8K), C (235.7K) | 533.9K | 22 | 8 |
| pydata/xarray | Python (114.0K) | 114.0K | 22 | 7 |
| pytest-dev/pytest | Python (66.7K) | 66.9K | 19 | 7 |
| pylint-dev/pylint | Python (79.1K) | 79.2K | 10 | 11 |
| psf/requests | Python (14.3K) | 14.5K | 8 | 4 |
| mwaskom/seaborn | Python (39.6K) | 39.7K | 2 | 14 |
| pallets/flask | Python (12.8K) | 13.1K | 1 | 3 |

## SWE-Lancer

**Organization:** OpenAI  
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

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| TypeScript | 55.9% | 198 | 300.0K | 300.9K | 27.0K | 26.6K | 337.4K |
| JavaScript | 43.8% | 198 | 235.0K | 219.1K | 141.8K | 204.7K | 1.6M |

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

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| Expensify/App | JavaScript (1.6M), TypeScript (337.4K) | 2.0M | 198 | 14 |

## SWE-PolyBench

**Organization:** Amazon  
**Task Count:** 2110

### Repository Size Stats (Total LOC)

| Metric | Value |
|--------|-------|
| Mean | 257.9K |
| Median | 72.2K |
| Std Dev | 323.6K |
| Min | 2.0K |
| 25th Percentile | 39.2K |
| 75th Percentile | 375.9K |
| Max | 1.1M |

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| TypeScript | 37.8% | 1446 | 142.2K | 17.1K | 279.7K | 3 | 942.4K |
| JavaScript | 34.4% | 1890 | 99.0K | 46.5K | 149.7K | 9 | 672.0K |
| Python | 17.5% | 801 | 119.0K | 144.0 | 280.1K | 2 | 1.1M |
| Java | 9.0% | 678 | 72.4K | 462.0 | 185.4K | 23 | 840.7K |

### Patch Complexity by Primary Language

| Primary Language | Tasks | Added (mean/median) | Deleted (mean/median) | Total (mean/median) |
|------------------|-------|---------------------|----------------------|---------------------|
| JavaScript | 1492 | 34.2 / 13 | 14.7 / 3 | 48.9 / 19 |
| TypeScript | 254 | 23.9 / 8 | 12.7 / 3 | 36.6 / 12 |
| Python | 199 | 47.1 / 13 | 23.0 / 4 | 70.1 / 18 |
| Java | 165 | 47.7 / 22 | 23.6 / 7 | 71.3 / 35 |

### Overall Patch Complexity

| Metric | Mean | Median | Std | Min | 25% | 75% | Max |
|--------|------|--------|-----|-----|-----|-----|-----|
| Lines Added | 35.2 | 13 | 76.5 | 0 | 4 | 36 | 1306 |
| Lines Deleted | 15.9 | 4 | 43.6 | 0 | 1 | 12 | 1018 |
| Total Changed | 51.2 | 19 | 109.8 | 1 | 6 | 50 | 2144 |

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| sveltejs/svelte | JavaScript (32.8K), TypeScript (24.6K), HTML (11.7K) | 57.9K | 496 | 10 |
| mui/material-ui | JavaScript (672.0K), TypeScript (257.8K) | 920.6K | 488 | 22 |
| serverless/serverless | JavaScript (90.9K) | 93.5K | 307 | 20 |
| microsoft/vscode | TypeScript (942.4K) | 1.0M | 205 | 11 |
| prettier/prettier | JavaScript (72.1K) | 78.2K | 196 | 31 |
| huggingface/transformers | Python (1.1M) | 1.1M | 126 | 18 |
| trinodb/trino | Java (840.7K), JavaScript (100.4K) | 941.8K | 46 | 40 |
| apache/rocketmq | Java (227.5K) | 227.8K | 42 | 22 |
| keras-team/keras | Python (161.7K) | 161.7K | 38 | 18 |
| apache/dubbo | Java (266.0K) | 266.0K | 37 | 19 |
| google/gson | Java (36.1K), HTML (23.2K) | 47.0K | 30 | 39 |
| langchain-ai/langchain | Python (360.1K) | 361.8K | 22 | 16 |
| tailwindlabs/tailwindcss | JavaScript (6.9K) | 6.9K | 20 | 8 |
| mrdoob/three.js | JavaScript (419.7K), HTML (234.2K) | 653.9K | 18 | 31 |
| coder/code-server | TypeScript (695.9K), JavaScript (44.3K) | 745.4K | 14 | 17 |
| yt-dlp/yt-dlp | Python (207.7K) | 207.7K | 10 | 37 |
| apolloconfig/apollo | Java (57.9K), JavaScript (14.3K), HTML (6.5K) | 78.7K | 6 | 50 |
| google/guava | Java (518.4K) | 518.4K | 4 | 111 |
| angular/angular | TypeScript (470.3K), JavaScript (171.7K) | 653.9K | 2 | 32 |
| tensorflow/models | Python (200.9K), C++ (22.0K) | 236.8K | 2 | 378 |
| Significant-Gravitas/AutoGPT | Python (10.3K) | 10.3K | 1 | 54 |
