# Workflow Documentation & Fix: `build-pull-request.yml`

## 1. Overview
- **Workflow File**: [`.github/workflows/build-pull-request.yml`](file:///c:/projects/spring-boot/.github/workflows/build-pull-request.yml)
- **Target Repository**: [`https://github.com/sajuptpm/spring-boot`](https://github.com/sajuptpm/spring-boot)
- **Purpose**: Runs verification builds and test suites on pull requests (compile, unit tests, integration tests) without deploying artifacts.

---

## 2. Issues in the Fork & Changes Made

### A. Problems Identified
1. **Repository Guard Skipping All PRs**: Upstream hardcoded `if: ${{ github.repository == 'spring-projects/spring-boot' }}`. In the fork `sajuptpm/spring-boot`, all pull requests were automatically skipped.
2. **Missing Manual Dispatch**: The workflow only listened to `on: pull_request`. It could not be manually triggered (`workflow_dispatch`) from the GitHub Actions web UI or CLI for testing without opening a real PR.
3. **Missing Develocity Configuration**: While the build composite action supports `develocity-access-key`, it was not wired into the build step inputs.

### B. Summary of Changes Made

| Component | Upstream State | Fork State (Updated) | Reason |
| :--- | :--- | :--- | :--- |
| **Triggers (`on`)** | `on: pull_request` | `on: [pull_request, workflow_dispatch]` | Allows manual testing and execution on-demand without opening a PR. |
| **Job Guard (`if`)** | `github.repository == 'spring-projects/spring-boot'` | `github.repository == 'sajuptpm/spring-boot' \|\| github.repository == 'spring-projects/spring-boot' \|\| vars.ENABLE_PR_BUILD == 'true'` | Enables the PR build to run in your forked repo. |
| **Develocity Key** | Not passed. | Added `develocity-access-key: ${{ secrets.DEVELOCITY_ACCESS_KEY }}`. | Publishes build scans to Develocity (`ge.spring.io`) if configured; otherwise gracefully omitted. |
| **Cancellation Diagnostics** | Unchanged. | `actions/print-jvm-thread-dumps` if cancelled. | Preserves upstream thread dump diagnostic on timeout/cancellation. |
| **Failure Diagnostics** | Unchanged. | `actions/upload-artifact@v7` for `**/build/reports/` if failure. | Preserves upstream build report artifact upload on test failures. |

---

## 3. Data Requirements (Secrets, Variables & Permissions)

Pull request workflows are isolated validation builds and **do not require any sensitive deployment credentials**.

### A. Repository Secrets (`secrets`)

| Secret Name | Required? | Description |
| :--- | :--- | :--- |
| `DEVELOCITY_ACCESS_KEY` | **Optional** | Access key for Gradle Develocity (`ge.spring.io` or self-hosted) to generate and publish build scan URLs. |

> **Note**: For security, GitHub Actions limits access to secrets on pull requests opened from external forks. This workflow does not require any secrets to compile and run tests.

---

### B. Repository Variables (`vars`)

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `UBUNTU_MEDIUM` | `ubuntu-latest` | Custom runner label if using self-hosted or larger GitHub-hosted runners. |
| `ENABLE_PR_BUILD` | *(empty / false)* | Optional fallback flag to enable PR builds if the repository name is changed. |

---

### C. GitHub Repository Settings & Permissions
- **Permissions**: `contents: read` is declared at the workflow level (standard least-privilege for PR builds).
- Under **Settings > Actions > General**:
  - Ensure **Allow GitHub Actions to run workflows from pull request forks** is set according to your collaboration preference (e.g., "Require approval for first-time contributors").

---

## 4. How to Test and Run

### Method 1: On-Demand Manual Trigger (Workflow Dispatch)
1. Commit and push the workflow to `main`.
2. Navigate to `https://github.com/sajuptpm/spring-boot/actions/workflows/build-pull-request.yml`.
3. Click **Run workflow** -> select branch `main` -> Click **Run workflow**.

### Method 2: Automatic Pull Request Trigger
1. Create a feature branch, make a change, and open a Pull Request targeting `main` in `sajuptpm/spring-boot`.
2. The `Build Pull Request` check will automatically trigger and report its pass/fail status directly on the PR.
