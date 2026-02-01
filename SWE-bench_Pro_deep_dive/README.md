# SWE-bench Pro Deep Dive

A static, client-side deep-dive UI for the [SWE-bench Pro](https://huggingface.co/datasets/ScaleAI/SWE-bench_Pro) public dataset, focused on problem statement, requirements, and interface.

See the render page directly [here](https://html-preview.github.io/?url=https://github.com/nedn/swe-bench-analyze/blob/main/SWE-bench_Pro_deep_dive/index.html).

## How Problem Statement, Requirements, and Interface Are Used

SWE-bench Pro gives each agent a codebase and a combined prompt constructed from three dataset fields. The official harness ([`SWE-bench_Pro-os`](https://github.com/scaleapi/SWE-bench_Pro-os)) assembles the prompt in [`helper_code/create_problem_statement.py`](https://github.com/scaleapi/SWE-bench_Pro-os/blob/main/helper_code/create_problem_statement.py):

```python
def create_problem_statement(row):
    problem_statement = row['problem_statement']
    requirement = row['requirements']
    interface = row['interface']

    return f"""{problem_statement}

Requirements:
{requirement}

New interfaces introduced:
{interface}"""
```

The three fields serve distinct roles:

- **Problem Statement** — describes the issue or feature request the agent must resolve. This is the core task description.
- **Requirements** — specifies the concrete conditions the solution must satisfy.
- **Interface** — lists new interfaces (functions, classes, API endpoints, etc.) that the solution should introduce.

The combined text is then passed as the `problem_statement` field in a SWE-agent instance YAML file (see [`helper_code/generate_sweagent_instances.py`](https://github.com/scaleapi/SWE-bench_Pro-os/blob/main/helper_code/generate_sweagent_instances.py)), which is what the agent actually receives as its task input. The agent never sees the three fields separately — it gets a single prompt with the requirements and interfaces appended below the problem statement.

## Usage

Open `index.html` directly in a browser. No build step or server required.

To refresh the dataset:

```bash
cd SWE-bench_Pro_deep_dive/
python fetch_data.py
```

This fetches the `ScaleAI/SWE-bench_Pro:test` split from HuggingFace and writes `data/swe_bench_pro_data.js`.
