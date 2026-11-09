---
name: autonomous-pipeline
description: Orchestrates end-to-end autonomous software development in TAIDE, taking a project from initial concept through research, architectural design, task backlog, implementation, automated testing, self-healing debugging, and GitHub PR delivery.
---

# TAIDE Autonomous Development Pipeline

Use this skill whenever you need to execute an autonomous development cycle for a new project, feature, or refactoring milestone.

## Pipeline Phases

### Phase 1: Intake & Research
1. Ingest user requirements or prompt.
2. Dispatch `researcher` subagent:
   - Identify recommended libraries, framework versions, and architectural precedents.
   - Output findings to `scratch/research_brief.md`.

### Phase 2: Architecture & Technical Specification
1. Dispatch `architect` subagent:
   - Formulate module boundaries, directory structure, data models, and API interfaces.
   - Update `architecture.md` with system overview and Mermaid diagrams.
2. Dispatch `planner` subagent:
   - Create/update `prd.json` with user stories and acceptance criteria.
   - Break requirements into single-responsibility tasks in `task_backlog.json`.

### Phase 3: The GSD / Ralph Iterative Construction Loop
For each pending task in `task_backlog.json`:
1. **Branch Checkpoint**:
   - Ensure a clean git branch: `git checkout -b feature/<task-id>`.
2. **Implementation**:
   - Dispatch `coder` subagent in a fresh context with the specific task requirements.
   - `coder` writes modular code and appends progress to `progress.txt`.
3. **Automated Verification**:
   - Dispatch `tester` subagent to write/run test suites (`npm test`, `pytest`, etc.).
4. **Self-Healing Loop (Red-Green)**:
   - If tests fail, dispatch `debugger` subagent with test error output.
   - `debugger` uses Sequential Thinking to diagnose root cause, applies patch, and re-runs `tester`.
   - Iterate up to 3 self-healing attempts until green.
5. **Atomic Commit**:
   - Commit verified changes: `git commit -m "feat(<task-id>): <task title> - verified by tests"`.
   - Update task status to `"completed"` in `task_backlog.json`.

### Phase 4: Security, Documentation & Delivery
1. Dispatch `security-auditor` subagent:
   - Scan modified code for hardcoded secrets, injection vectors, and dependency vulnerabilities.
2. Dispatch `doc-writer` subagent:
   - Update `README.md`, docstrings, and `CHANGELOG.md`.
3. Dispatch `github-ops` subagent:
   - Push branch and create a structured GitHub Pull Request using `gh pr create`.
   - Human approval checkpoint for final merge.
