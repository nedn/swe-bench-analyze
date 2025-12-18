# SWE-Bench Complexity Report

This report analyzes the complexity of tasks across various SWE benchmark datasets.

## Summary

| Benchmark | Tasks | Repo LOC (mean) | Patch Total (mean) | Patch Total (median) | Main Languages |
|-----------|-------|-----------------|--------------------|--------------------|----------------|
| multi_swe_bench | 1632 | 180.3K | 163.2 | 33 | JavaScript (38.2%), HTML (24.6%), Go (12.1%) |
| swe_bench_multilingual | 300 | 169.2K | 47.8 | 10 | Java (30.6%), PHP (17.2%), Ruby (10.7%) |
| swe_bench_pro | 731 | 266.5K | 169.6 | 94 | Go (43.9%), Python (22.8%), TypeScript (22.0%) |
| swe_bench_verified | 500 | 290.2K | 14.3 | 7 | Python (90.2%), JavaScript (4.4%), C (4.0%) |
| swe_lancer | 198 | 536.8K | 33.4 | 14 | TypeScript (55.9%), JavaScript (43.8%) |

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

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| Java | 30.6% | 57 | 272.5K | 90.1K | 386.5K | 69 | 1.2M |
| PHP | 17.2% | 69 | 126.4K | 166.3K | 102.7K | 3 | 264.3K |
| Ruby | 10.7% | 78 | 69.8K | 17.3K | 85.7K | 2 | 224.1K |
| Go | 9.6% | 49 | 99.8K | 53.9K | 113.3K | 117 | 398.3K |
| Rust | 8.8% | 43 | 104.2K | 83.3K | 95.1K | 3.1K | 261.1K |
| C | 7.8% | 56 | 70.7K | 28.9K | 83.9K | 12 | 214.5K |
| JavaScript | 6.0% | 183 | 16.5K | 230.0 | 52.0K | 1 | 362.5K |
| TypeScript | 3.5% | 67 | 26.7K | 2.6K | 37.8K | 221 | 116.5K |
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

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| preactjs/preact | JavaScript (34.8K) | 36.9K | 17 | 7 |
| projectlombok/lombok | Java (98.0K) | 101.9K | 17 | 11 |
| rubocop/rubocop | Ruby (224.1K) | 224.7K | 16 | 10 |
| caddyserver/caddy | Go (55.4K) | 56.5K | 14 | 16 |
| laravel/framework | PHP (264.3K) | 264.4K | 13 | 4 |
| fluent/fluentd | Ruby (82.7K) | 82.7K | 12 | 8 |
| redis/redis | C (179.4K) | 188.4K | 12 | 14 |
| fmtlib/fmt | C++ (19.7K), Python (1.3K) | 21.2K | 11 | 8 |
| briannesbitt/carbon | PHP (166.3K) | 166.3K | 10 | 16 |
| php-cs-fixer/php-cs-fixer | PHP (207.4K) | 207.4K | 10 | 10 |
| phpoffice/phpspreadsheet | PHP (196.5K) | 196.9K | 10 | 12 |
| apache/lucene | Java (868.5K) | 882.7K | 9 | 7 |
| google/gson | Java (33.6K), HTML (23.2K) | 48.0K | 9 | 9 |
| jqlang/jq | C (29.7K) | 30.1K | 9 | 32 |
| tokio-rs/tokio | Rust (87.3K) | 87.3K | 9 | 7 |
| gin-gonic/gin | Go (15.0K) | 15.0K | 8 | 2 |
| prometheus/prometheus | Go (198.8K), TypeScript (33.9K), JavaScript (13.2K) | 236.3K | 8 | 29 |
| sharkdp/bat | Rust (10.8K), Python (6.9K), JavaScript (6.9K) | 26.3K | 8 | 18 |
| astral-sh/ruff | Rust (261.1K), Python (128.6K) | 391.6K | 7 | 14 |
| fastlane/fastlane | Ruby (124.6K) | 125.6K | 7 | 5 |
| gohugoio/hugo | Go (140.6K) | 148.8K | 7 | 4 |
| tokio-rs/axum | Rust (24.5K) | 24.5K | 7 | 64 |
| axios/axios | JavaScript (25.3K) | 26.8K | 6 | 5 |
| apache/druid | Java (1.2M) | 1.3M | 5 | 11 |
| babel/babel | JavaScript (174.6K), TypeScript (95.5K) | 270.2K | 5 | 2 |
| facebook/docusaurus | TypeScript (77.5K), JavaScript (67.9K) | 145.8K | 5 | 23 |
| hashicorp/terraform | Go (398.3K) | 398.3K | 5 | 43 |
| jekyll/jekyll | Ruby (17.5K), JavaScript (1.1K), HTML (1.0K) | 19.6K | 5 | 10 |
| micropython/micropython | C (214.5K), Python (56.2K) | 272.5K | 5 | 8 |
| nushell/nushell | Rust (228.8K) | 229.0K | 5 | 15 |
| uutils/coreutils | Rust (128.0K) | 128.5K | 5 | 24 |
| vuejs/core | TypeScript (116.5K) | 120.6K | 5 | 11 |
| valkey-io/valkey | C (185.7K) | 195.3K | 4 | 7 |
| mrdoob/three.js | JavaScript (362.5K), HTML (328.3K) | 683.3K | 3 | 6 |
| burntsushi/ripgrep | Rust (30.1K) | 31.4K | 2 | 44 |
| faker-ruby/faker | Ruby (20.9K) | 20.9K | 2 | 3 |
| immutable-js/immutable-js | TypeScript (11.1K), JavaScript (7.3K) | 18.3K | 2 | 9 |
| javaparser/javaparser | Java (214.4K) | 214.4K | 2 | 82 |
| jordansissel/fpm | Ruby (8.6K) | 8.7K | 2 | 28 |
| nlohmann/json | C++ (45.7K) | 46.5K | 1 | 6 |
| reactivex/rxjava | Java (315.3K) | 315.3K | 1 | 5 |

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

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| Go | 43.9% | 376 | 227.7K | 37.0K | 427.3K | 61 | 1.8M |
| Python | 22.8% | 484 | 91.8K | 54.3K | 214.5K | 23 | 1.7M |
| TypeScript | 22.0% | 212 | 202.0K | 197.9K | 179.7K | 8.3K | 786.7K |
| JavaScript | 5.4% | 621 | 17.0K | 10.8K | 25.1K | 4 | 125.2K |
| C | 4.7% | 98 | 93.6K | 163.8K | 84.6K | 8 | 180.8K |

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

### Repositories

| Repository | Main Languages | Max Repo Size | Tasks | Median Complexity |
|------------|----------------|---------------|-------|-------------------|
| ansible/ansible | Python (1.7M) | 1.7M | 96 | 86 |
| internetarchive/openlibrary | Python (63.6K), HTML (15.1K), JavaScript (11.7K) | 90.0K | 91 | 97 |
| flipt-io/flipt | Go (87.0K), TypeScript (16.6K) | 103.5K | 85 | 153 |
| qutebrowser/qutebrowser | Python (88.9K), JavaScript (19.8K) | 113.8K | 79 | 52 |
| gravitational/teleport | Go (1.8M), C (180.8K), TypeScript (132.8K) | 2.0M | 76 | 113 |
| protonmail/webclients | TypeScript (786.7K), JavaScript (125.2K) | 912.9K | 65 | 103 |
| future-architect/vuls | Go (73.8K) | 73.8K | 62 | 160 |
| navidrome/navidrome | Go (48.0K), JavaScript (15.8K) | 54.1K | 57 | 109 |
| element-hq/element-web | TypeScript (246.1K), JavaScript (53.9K) | 252.2K | 56 | 82 |
| NodeBB/NodeBB | JavaScript (108.2K) | 108.4K | 44 | 74 |
| tutao/tutanota | TypeScript (214.7K), C (163.8K), JavaScript (56.0K) | 440.5K | 20 | 110 |

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

### LOC Stats by Language (>= 2% of codebase)

| Language | % | Tasks w/ Code | Mean | Median | Std | Min | Max |
|----------|---|---------------|------|--------|-----|-----|-----|
| Python | 90.2% | 500 | 261.7K | 277.9K | 135.9K | 7.9K | 581.2K |
| JavaScript | 4.4% | 373 | 17.0K | 18.2K | 11.4K | 2 | 52.3K |
| C | 4.0% | 132 | 43.5K | 3.8K | 72.0K | 1 | 235.7K |

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
| django/django | Python (375.8K) | 399.8K | 231 | 6 |
| sympy/sympy | Python (581.2K) | 581.2K | 75 | 7 |
| sphinx-doc/sphinx | Python (84.3K), JavaScript (52.3K) | 130.9K | 44 | 8 |
| matplotlib/matplotlib | Python (184.8K), C (59.4K), C++ (29.8K) | 257.0K | 34 | 7 |
| scikit-learn/scikit-learn | Python (275.3K) | 282.6K | 32 | 8 |
| astropy/astropy | Python (283.6K), C (235.7K) | 530.1K | 22 | 8 |
| pydata/xarray | Python (113.9K) | 113.9K | 22 | 7 |
| pytest-dev/pytest | Python (66.6K) | 66.7K | 19 | 7 |
| pylint-dev/pylint | Python (79.4K) | 79.5K | 10 | 11 |
| psf/requests | Python (14.3K) | 14.5K | 8 | 4 |
| mwaskom/seaborn | Python (39.9K) | 39.9K | 2 | 14 |
| pallets/flask | Python (12.8K) | 13.1K | 1 | 3 |

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
