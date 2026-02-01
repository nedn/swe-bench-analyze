// SWE-bench Pro Deep Dive - Application Logic
(function () {
    "use strict";

    const data = SWE_BENCH_PRO_DATA.map(d => ({
        ...d,
        issue_specificity: normalizeList(d.issue_specificity),
        issue_categories: normalizeList(d.issue_categories),
        selected_test_files_to_run: normalizeList(d.selected_test_files_to_run),
        fail_to_pass: normalizeList(d.fail_to_pass),
        pass_to_pass: normalizeList(d.pass_to_pass),
    }));

    function normalizeList(value) {
        if (Array.isArray(value)) return value;
        if (value == null || value === "") return [];
        if (typeof value === "string") {
            try {
                const parsed = JSON.parse(value);
                if (Array.isArray(parsed)) return parsed;
            } catch {
                return [value];
            }
            return [value];
        }
        return [value];
    }

    // Precompute metadata
    const repos = [...new Set(data.map(d => d.repo))].sort();
    const languages = [...new Set(data.map(d => d.repo_language))].sort();

    // State
    let filteredData = data;
    let selectedIndex = -1;
    let activeTab = "problem";

    // --- Render the app shell ---
    function renderApp() {
        const app = document.getElementById("app");
        app.className = "";
        app.innerHTML = `
            <div class="header">
                <div class="header-content">
                    <h1>SWE-bench Pro <span>Deep Dive</span></h1>
                    <div class="stats-bar">
                        <span><span class="stat-value">${data.length}</span> instances</span>
                        <span><span class="stat-value">${repos.length}</span> repos</span>
                        <span><span class="stat-value">${languages.length}</span> languages</span>
                    </div>
                </div>
            </div>
            <div class="container">
                <div class="sidebar">
                    <div class="filters">
                        <input type="text" class="search-box" id="searchBox"
                               placeholder="Search problem statements, repos, IDs...">
                        <div class="filter-row">
                            <select class="filter-select" id="repoFilter">
                                <option value="">All repos (${repos.length})</option>
                                ${repos.map(r => `<option value="${esc(r)}">${esc(r)}</option>`).join("")}
                            </select>
                            <select class="filter-select" id="langFilter">
                                <option value="">All languages</option>
                                ${languages.map(l => `<option value="${esc(l)}">${esc(l)}</option>`).join("")}
                            </select>
                        </div>
                    </div>
                    <div class="nav-hint">
                        <span class="kbd">&uarr;</span> <span class="kbd">&darr;</span> navigate
                        &nbsp;&middot;&nbsp;
                        <span class="kbd">Enter</span> select
                    </div>
                    <div class="results-count" id="resultsCount"></div>
                    <div class="instance-list" id="instanceList"></div>
                </div>
                <div class="detail-panel" id="detailPanel">
                    <div class="detail-empty">Select an instance to view details</div>
                </div>
            </div>
        `;

        // Bind events
        document.getElementById("searchBox").addEventListener("input", debounce(applyFilters, 200));
        document.getElementById("repoFilter").addEventListener("change", applyFilters);
        document.getElementById("langFilter").addEventListener("change", applyFilters);
        document.addEventListener("keydown", handleKeyDown);

        applyFilters();
    }

    // --- Filtering ---
    function applyFilters() {
        const query = document.getElementById("searchBox").value.toLowerCase().trim();
        const repo = document.getElementById("repoFilter").value;
        const lang = document.getElementById("langFilter").value;

        filteredData = data.filter(d => {
            if (repo && d.repo !== repo) return false;
            if (lang && d.repo_language !== lang) return false;
            if (query) {
                const haystack = (
                    d.instance_id + " " +
                    d.repo + " " +
                    d.problem_statement + " " +
                    d.requirements + " " +
                    d.interface
                ).toLowerCase();
                // Support multi-word search
                const terms = query.split(/\s+/);
                for (const term of terms) {
                    if (!haystack.includes(term)) return false;
                }
            }
            return true;
        });

        selectedIndex = -1;
        renderList();
        renderDetail();
    }

    // --- List rendering with virtual scroll ---
    function renderList() {
        const container = document.getElementById("instanceList");
        const countEl = document.getElementById("resultsCount");
        countEl.textContent = `${filteredData.length} of ${data.length} instances`;

        // For performance with 731 items, render all (it's manageable)
        const html = filteredData.map((d, i) => {
            const langClass = getLangClass(d.repo_language);
            const isActive = i === selectedIndex ? " active" : "";
            // Truncate problem statement for preview
            const preview = (d.problem_statement || "").substring(0, 80).replace(/\n/g, " ");
            return `<div class="instance-item${isActive}" data-index="${i}">
                <div class="instance-repo">${esc(d.repo)}</div>
                <div class="instance-id">${esc(shortId(d.instance_id))}</div>
                <div class="instance-meta">
                    <span class="lang-badge ${langClass}">${esc(d.repo_language)}</span>
                    <span style="color: var(--text-muted)">${esc(preview)}...</span>
                </div>
            </div>`;
        }).join("");

        container.innerHTML = html;

        // Click handlers
        container.querySelectorAll(".instance-item").forEach(el => {
            el.addEventListener("click", () => {
                selectedIndex = parseInt(el.dataset.index);
                renderList();
                renderDetail();
            });
        });
    }

    // --- Detail rendering ---
    function renderDetail() {
        const panel = document.getElementById("detailPanel");
        if (selectedIndex < 0 || selectedIndex >= filteredData.length) {
            panel.innerHTML = '<div class="detail-empty">Select an instance to view details</div>';
            return;
        }

        const d = filteredData[selectedIndex];
        const langClass = getLangClass(d.repo_language);
        const ghUrl = `https://github.com/${d.repo}/commit/${d.base_commit}`;

        panel.innerHTML = `
            <div class="detail-header">
                <h2>${esc(d.repo)} &mdash; ${esc(shortId(d.instance_id))}</h2>
                <div class="detail-meta">
                    <span class="lang-badge ${langClass}">${esc(d.repo_language)}</span>
                    <span>Commit: <a href="${esc(ghUrl)}" target="_blank">${esc(d.base_commit.substring(0, 10))}</a></span>
                    <span>Instance: <code>${esc(d.instance_id)}</code></span>
                </div>
                <div style="margin-top: 8px;">
                    <div class="tag-list">
                        ${(d.issue_specificity || []).map(t => `<span class="tag tag-specificity">${esc(t)}</span>`).join("")}
                        ${(d.issue_categories || []).map(t => `<span class="tag tag-category">${esc(t)}</span>`).join("")}
                    </div>
                </div>
            </div>
            <div class="detail-nav" id="detailNav">
                <button data-tab="problem" class="${activeTab === "problem" ? "active" : ""}">Problem Statement</button>
                <button data-tab="requirements" class="${activeTab === "requirements" ? "active" : ""}">Requirements</button>
                <button data-tab="interface" class="${activeTab === "interface" ? "active" : ""}">Interface</button>
                <button data-tab="patch" class="${activeTab === "patch" ? "active" : ""}">Gold Patch</button>
                <button data-tab="tests" class="${activeTab === "tests" ? "active" : ""}">Tests</button>
            </div>
            <div class="detail-body" id="detailBody"></div>
        `;

        // Tab click handlers
        document.getElementById("detailNav").querySelectorAll("button").forEach(btn => {
            btn.addEventListener("click", () => {
                activeTab = btn.dataset.tab;
                document.getElementById("detailNav").querySelectorAll("button").forEach(b => b.classList.remove("active"));
                btn.classList.add("active");
                renderTabContent(d);
            });
        });

        renderTabContent(d);
    }

    function renderTabContent(d) {
        const body = document.getElementById("detailBody");

        switch (activeTab) {
            case "problem":
                body.innerHTML = `
                    <div class="section">
                        <div class="section-title">Problem Statement</div>
                        <div class="section-content">${esc(d.problem_statement || "N/A")}</div>
                    </div>
                `;
                break;

            case "requirements":
                body.innerHTML = `
                    <div class="section">
                        <div class="section-title">Requirements</div>
                        <div class="section-content">${esc(d.requirements || "N/A")}</div>
                    </div>
                `;
                break;

            case "interface":
                body.innerHTML = `
                    <div class="section">
                        <div class="section-title">Interface</div>
                        <div class="section-content">${esc(d.interface || "N/A")}</div>
                    </div>
                `;
                break;

            case "patch":
                body.innerHTML = `
                    <div class="section">
                        <div class="section-title">Golden Patch</div>
                        <div class="diff-view">${renderDiff(d.patch || "")}</div>
                    </div>
                    ${d.test_patch ? `
                    <div class="section">
                        <div class="section-title">Test Patch</div>
                        <div class="diff-view">${renderDiff(d.test_patch)}</div>
                    </div>
                    ` : ""}
                `;
                break;

            case "tests":
                const failTests = d.fail_to_pass || [];
                const passTests = d.pass_to_pass || [];
                const testFiles = d.selected_test_files_to_run || [];

                body.innerHTML = `
                    <div class="section">
                        <div class="section-title">Selected Test Files</div>
                        <ul class="test-file-list">
                            ${testFiles.map(f => `<li>${esc(f)}</li>`).join("")}
                        </ul>
                    </div>
                    <div class="section">
                        <div class="section-title">Fail to Pass (${failTests.length})</div>
                        ${failTests.map(t => `<div class="test-item">${esc(t)}</div>`).join("") || '<span style="color: var(--text-muted)">None</span>'}
                    </div>
                    <div class="section">
                        <div class="section-title">Pass to Pass (${passTests.length})</div>
                        ${passTests.map(t => `<div class="test-item pass">${esc(t)}</div>`).join("") || '<span style="color: var(--text-muted)">None</span>'}
                    </div>
                `;
                break;
        }
    }

    // --- Diff renderer ---
    function renderDiff(patch) {
        if (!patch) return '<div class="diff-line" style="color: var(--text-muted)">No patch data</div>';

        const lines = patch.split("\n");
        return lines.map(line => {
            let cls = "diff-line";
            if (line.startsWith("+++") || line.startsWith("---")) {
                cls += " diff-line-file";
            } else if (line.startsWith("@@")) {
                cls += " diff-line-hunk";
            } else if (line.startsWith("+")) {
                cls += " diff-line-add";
            } else if (line.startsWith("-")) {
                cls += " diff-line-del";
            }
            return `<div class="${cls}">${esc(line)}</div>`;
        }).join("");
    }

    // --- Keyboard navigation ---
    function handleKeyDown(e) {
        // Don't capture when typing in search
        if (document.activeElement.tagName === "INPUT" || document.activeElement.tagName === "SELECT") {
            if (e.key === "Escape") {
                document.activeElement.blur();
            }
            return;
        }

        if (e.key === "ArrowDown" || e.key === "j") {
            e.preventDefault();
            if (selectedIndex < filteredData.length - 1) {
                selectedIndex++;
                renderList();
                renderDetail();
                scrollSelectedIntoView();
            }
        } else if (e.key === "ArrowUp" || e.key === "k") {
            e.preventDefault();
            if (selectedIndex > 0) {
                selectedIndex--;
                renderList();
                renderDetail();
                scrollSelectedIntoView();
            }
        } else if (e.key === "/") {
            e.preventDefault();
            document.getElementById("searchBox").focus();
        }
    }

    function scrollSelectedIntoView() {
        const active = document.querySelector(".instance-item.active");
        if (active) {
            active.scrollIntoView({ block: "nearest", behavior: "smooth" });
        }
    }

    // --- Utilities ---
    function esc(str) {
        if (str == null) return "";
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }

    function shortId(instanceId) {
        // instance_NodeBB__NodeBB-04998908ba... -> shorten the hash part
        const parts = instanceId.split("-");
        if (parts.length > 2) {
            // Keep everything but truncate long hashes
            return instanceId.replace(/([a-f0-9]{10})[a-f0-9]{30,}/g, "$1...");
        }
        return instanceId;
    }

    function getLangClass(lang) {
        const map = {
            python: "lang-py",
            js: "lang-js",
            javascript: "lang-js",
            typescript: "lang-ts",
            ts: "lang-ts",
            java: "lang-java",
            go: "lang-go",
            rust: "lang-rust",
            c: "lang-c",
            cpp: "lang-cpp",
            "c++": "lang-cpp",
            ruby: "lang-ruby",
        };
        return map[(lang || "").toLowerCase()] || "lang-default";
    }

    function debounce(fn, delay) {
        let timer;
        return function (...args) {
            clearTimeout(timer);
            timer = setTimeout(() => fn.apply(this, args), delay);
        };
    }

    // --- Initialize ---
    if (typeof SWE_BENCH_PRO_DATA !== "undefined") {
        renderApp();
    } else {
        document.getElementById("app").textContent = "Error: SWE-bench Pro data not loaded.";
    }
})();
