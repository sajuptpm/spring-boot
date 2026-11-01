# CodeQL Security Analysis: Run CodeQL Analysis (`run-codeql-analysis.yml`)

## 1. Overview & Purpose

The `Run CodeQL Analysis` workflow ([`.github/workflows/run-codeql-analysis.yml`](file:///c:/projects/spring-boot/.github/workflows/run-codeql-analysis.yml)) is responsible for automated security vulnerability, bug, and quality scanning using GitHub's CodeQL engine.

In Spring Boot, this workflow calls the reusable workflow [`spring-io/github-actions/.github/workflows/codeql-analysis.yml`](https://github.com/spring-io/github-actions/blob/main/.github/workflows/codeql-analysis.yml) at pinned commit `5caba18f0b4141f3a32b1bc9f5f3f82169b0b6ac`. It targets `languages: 'actions'`, analyzing GitHub Actions workflow definitions and composite actions for security vulnerabilities, untrusted script injections, and malformed configurations without requiring a full Java project build.

---

## 2. Architecture & Changes Summary

```
                      run-codeql-analysis.yml
                                 │
                   (workflow_dispatch / pull_request)
                                 │
                                 ▼
                     [spring-io/codeql-analysis]
                                 │
               ┌─────────────────┴─────────────────┐
               ▼                                   ▼
      [actions/checkout]                  [Initialize CodeQL]
 • Checks out repository              • Configures CodeQL v4.39.1
   workflows and action code          • Languages: 'actions'
                                      • Packs: security-extended,
                                        security-and-quality
                                                   │
                                                   ▼
                                       [Perform CodeQL Analysis]
                                      • Evaluates action rules
                                      • Publishes security alerts
                                        to GitHub Security tab
```

### Changes Implemented
1. **Conserve Runner Minutes**:
   - Temporarily commented out the automatic `push:` trigger to prevent redundant CodeQL scans during intensive workflow testing.
   - Preserved `pull_request:` and `workflow_dispatch:` for full automated PR scanning and on-demand manual verification.
2. **Pinned Action Versions**:
   - Uses verified action SHAs for `actions/checkout` and `github/codeql-action`.

---

## 3. Existing Solutions vs. Free Alternatives Analysis

| Feature / Step | Spring Upstream Solution | Fork / Alternative Solution |
| :--- | :--- | :--- |
| **CodeQL Engine** | GitHub CodeQL action (`github/codeql-action@v4`) targeting `languages: 'actions'`. | Built into GitHub Actions free tier for all public repositories without license fees. |
| **Analysis Scope** | Scans workflow definitions, composite actions, and action inputs/outputs for script injection vulnerabilities. | Directly reports findings to the repository's GitHub Security tab (`security-events: write`). |
| **Execution Overhead** | Does not compile the Java codebase (`build-mode: 'none'`), completing in under 45 seconds. | Extremely fast, zero external credential dependencies. |

---

## 4. Configuration & Data Requirements

### Repository Secrets
*No secrets required.* Uses default `GITHUB_TOKEN` provided by the GitHub Actions runner.

### Repository Variables
*No variables required.*

### Permissions
| Permission | Level | Reason |
| :--- | :--- | :--- |
| `actions` | `read` | Inspects workflow runs and action definitions. |
| `contents` | `read` | Checks out repository workflows and source files. |
| `security-events` | `write` | Publishes CodeQL SARIF results to the repository Security Advisory tab. |

---

## 5. Live Test Verification Details

The `Run CodeQL Analysis` workflow was dispatched and verified live on GitHub Actions on branch `main`.

| Parameter | Value |
| :--- | :--- |
| **Workflow Run ID** | `41327162382` |
| **Workflow Run URL** | [Run #41327162382](https://github.com/sajuptpm/spring-boot/actions/runs/41327162382) |
| **Job Details** | [Analyze Job #124909409929](https://github.com/sajuptpm/spring-boot/actions/runs/41327162382/job/124909409929) |
| **Trigger Type** | `workflow_dispatch` |
| **Branch** | `main` |
| **CodeQL Language** | `actions` |
| **Queries** | `security-extended`, `security-and-quality` |
| **Duration** | 41 seconds |
| **Outcome** | **`completed / success`** (100% Success) |

### Step Execution Timeline
```
STEP STATUS         CONCLUSION   NAME
--------------------------------------------------------------------------------
1    completed      success      Set up job
2    completed      success      Checkout
3    completed      success      Initialize CodeQL (v4.39.1)
4    completed      success      Perform CodeQL Analysis
6    completed      success      Post Perform CodeQL Analysis
7    completed      success      Post Initialize CodeQL
8    completed      success      Post Checkout
9    completed      success      Complete job
```

---

## 6. How to Test Later

### Option A: Using the Workflow Dispatch Python Helper
```powershell
python workflow-fixes/trigger-workflow.py run-codeql-analysis.yml main
```

### Option B: Using the GitHub CLI (`gh`)
```bash
gh workflow run run-codeql-analysis.yml
```

---

## 7. Step-by-Step GitHub UI Manual Verification Guide

1. **Navigate to Actions**:
   - Open your web browser and go to `https://github.com/sajuptpm/spring-boot/actions`.
2. **Select the Workflow**:
   - Under "All workflows" in the left sidebar, click on **`Run CodeQL Analysis`**.
3. **Trigger Workflow**:
   - Click the blue **"Run workflow"** button on the right.
   - Select branch `main`.
   - Click the green **"Run workflow"** button.
4. **Inspect Execution**:
   - Click on the new run (e.g. `Run CodeQL Analysis #...`).
   - Click the **`run-analysis / Analyze`** job.
   - Verify that all steps (`Initialize CodeQL`, `Perform CodeQL Analysis`) pass with green checkmarks.
5. **View Security Alerts (Optional)**:
   - Go to the **Security** tab -> **Code scanning** to see CodeQL analysis reports.
