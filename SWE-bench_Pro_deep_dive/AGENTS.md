# SWE-bench Pro Deep Dive

Purpose: a static, client-side deep-dive UI for the SWE-bench Pro public dataset, focused on problem statement, requirements, and interface.

## Layout & Data Flow
- `index.html` is the single-page shell and owns all styles.
- `app.js` renders the UI, filters, and detail tabs. It expects a global `SWE_BENCH_PRO_DATA` array.
- `data/swe_bench_pro_data.js` defines `SWE_BENCH_PRO_DATA` and is loaded by `index.html` before `app.js`.

## Updating Dataset
Run from `SWE-bench_Pro_deep_dive/`:
1) `python fetch_data.py`
2) Confirm it writes `data/swe_bench_pro_data.js` and prints the instance count and file size.

Notes:
- The script fetches the HuggingFace split `ScaleAI/SWE-bench_Pro:test`.
- Output is a single JS file (no build step) so the UI stays fully static.
- Records are sorted by `repo`, then `instance_id` for stable ordering.

## Editing Guidelines
- Keep everything static (no bundlers, no frameworks). Changes should remain compatible with `index.html` opening directly in a browser.
- Preserve the contract: `app.js` must be able to run if `SWE_BENCH_PRO_DATA` exists; otherwise it shows an error message.
- If you add fields to the dataset, update both `fetch_data.py` and `app.js` to consume them.

## Dataset Fields
`fetch_data.py` currently exports (with usage in `app.js`):
- `instance_id`: list preview, search, detail header, and instance metadata.
- `repo`: list preview, repo filter, search, detail header, GitHub commit link.
- `repo_language`: language filter, badges, and language count.
- `base_commit`: commit link in the detail header.
- `problem_statement`: search and “Problem Statement” tab.
- `requirements`: search and “Requirements” tab.
- `interface`: search and “Interface” tab.
- `patch`: “Gold Patch” tab diff viewer.
- `test_patch`: optional “Test Patch” tab diff viewer.
- `fail_to_pass`: “Tests” tab (fail list + count).
- `pass_to_pass`: “Tests” tab (pass list + count).
- `issue_specificity`: detail header tags.
- `issue_categories`: detail header tags.
- `selected_test_files_to_run`: “Tests” tab list.

## Testing/Preview
- Open `index.html` directly in a browser to verify search, filters, and tab rendering.

## Troubleshooting
- `ModuleNotFoundError: datasets`: install dependencies per project setup (see repo README), then rerun `python fetch_data.py`.
- Dataset fetch stalls or fails: verify network access and retry; the script relies on HuggingFace availability.
- UI shows “Error: SWE-bench Pro data not loaded.”: ensure `data/swe_bench_pro_data.js` exists and is loaded before `app.js` in `index.html`.
