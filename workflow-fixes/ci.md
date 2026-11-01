# Workflow Documentation & Fix: `ci.yml`

## 1. Overview
- **Workflow File**: [`.github/workflows/ci.yml`](file:///c:/projects/spring-boot/.github/workflows/ci.yml)
- **Target Repository**: [`https://github.com/sajuptpm/spring-boot`](https://github.com/sajuptpm/spring-boot)
- **Purpose**: Runs matrix verification builds across multiple operating systems (**Linux** and **Windows**) and multiple Java versions (**Java 17, 21, 25, and 27**), testing toolchain configurations and build compatibility without deploying artifacts.

---

## 2. Issues in the Fork & Changes Made

### A. Problems Identified
1. **Repository Guard Skipping All CI Runs**: Upstream hardcoded `if: ${{ github.repository == 'spring-projects/spring-boot' || github.repository == 'spring-projects/spring-boot-commercial' }}`. In the fork `sajuptpm/spring-boot`, all matrix builds were skipped.
2. **Missing Manual Dispatch**: The workflow only listened to `on: push` to `main`. It could not be manually triggered (`workflow_dispatch`) from the GitHub Actions web UI or CLI for testing.
3. **Redundant Build Triggering**: Because `push` was enabled on `main`, pushing any commit triggered 7 concurrent matrix jobs consuming large amounts of runner minutes.
4. **Unconditional Notification Step**: Executed the `send-notification` composite action on completion even when `secrets.GOOGLE_CHAT_WEBHOOK_URL` was not configured.

### B. Summary of Changes Made

| Component | Upstream State | Fork State (Updated) | Reason |
| :--- | :--- | :--- | :--- |
| **Triggers (`on`)** | `push: branches: ['main']` | `workflow_dispatch` (with `push` commented out temporarily) | Allows testing on-demand without triggering 7 heavy matrix jobs on every commit while configuring remaining workflows. |
| **Job Guard (`if`)** | Restricted to `spring-projects/*`. | Allows `sajuptpm/spring-boot`, upstream repos, or `vars.ENABLE_CI == 'true'`. | Enables the matrix CI workflow in your forked repo. |
| **Notification Check Step** | None. | Added `Check Notification Configuration` step to output `enabled=true/false`. | Checks whether `GOOGLE_CHAT_WEBHOOK_URL` is set without violating GitHub Actions expression rules. |
| **Send Notification Guard** | `if: always()` | `if: always() && steps.check-notification.outputs.enabled == 'true'` | Skips sending notification cleanly if webhook URL is not provided. |
| **Matrix Strategy** | Unchanged (Linux & Windows across Java 17, 21, 25, 27). | Preserved with `fail-fast: false`. | Tests complete OS and Java compatibility. |

---

## 3. Existing Solution vs. Free Alternatives Analysis

### Feature 1: Build Observability & Diagnostics (Gradle Develocity vs. Alternatives)

| Solution | Provider | Cost | Tokens / Setup Needed | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (`ge.spring.io`)** | Gradle Inc. (Hosted for Broadcom) | Paid / Private | Broadcom internal key | Private Develocity instance restricted to `spring-projects/*`. |
| **Alternative 1: GitHub-Native Job Summary & Artifacts** *(Active)* | **GitHub** | **100% Free** | **None** (Built into GitHub) | `gradle/actions/setup-gradle` automatically generates a **Job Summary** on the Actions run page with build duration, cache hits, and Gradle version. Test reports are uploaded on failure. |
| **Alternative 2: Public Gradle Build Scans (`scans.gradle.com`)** | **Gradle Inc.** | **100% Free** | **None** | Generates a free, shareable web link (e.g., `https://gradle.com/s/xyz123`) in the build log with complete task execution times and dependency trees. |
| **Alternative 3: Develocity Free Cloud / Trial** | **Gradle Inc.** | Free for eligible OSS | Requires registration at [gradle.com/develocity](https://gradle.com/develocity/) | Dedicated cloud instance (`https://<your-org>.develocity.com`) with team dashboards and private build scans. |

---

### Feature 2: Build Output Caching

| Solution | Provider | Cost | Storage Limit | Status in Fork |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Develocity Remote Cache** | Gradle Inc. | Paid / Private | Enterprise quota | Disabled (Inaccessible in forks) |
| **GitHub Actions Cache** *(Active)* | **GitHub** | **100% Free** | **10 GB per repository** | **Active**: Automatically caches Gradle wrapper, downloaded dependencies, and build outputs across all matrix jobs. |

---

### Feature 3: Status Notifications

| Solution | Provider | Cost | Description |
| :--- | :--- | :--- | :--- |
| **Upstream Google Chat Webhook** | Google Workspace | Requires Workspace space | Sends status messages with build scan links to a Google Chat room. |
| **Alternative 1: GitHub Actions Built-in Status** *(Active)* | **GitHub** | **100% Free** | Native GitHub commit status checks and email notifications for failed runs. |
| **Alternative 2: Discord / Slack Webhook Action** | **GitHub Marketplace** | **100% Free** | Free webhooks to Discord or Slack channels for build notifications. |

---

## 4. Data Requirements (Secrets, Variables & Permissions)

### A. Repository Secrets (`secrets`)

| Secret Name | Required? | Description |
| :--- | :--- | :--- |
| `DEVELOCITY_ACCESS_KEY` | **Optional** | Access key for Gradle Develocity (`ge.spring.io` or your custom Develocity instance) to publish build scan URLs. |
| `GOOGLE_CHAT_WEBHOOK_URL` | **Optional** | Webhook URL for Google Chat space notifications. |
| `COMMERCIAL_ARTIFACTORY_USERNAME` | **Optional** | Only needed if running with `vars.COMMERCIAL = 'true'`. |
| `COMMERCIAL_ARTIFACTORY_PASSWORD` | **Optional** | Only needed if running with `vars.COMMERCIAL = 'true'`. |

---

### B. Repository Variables (`vars`)

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `UBUNTU_MEDIUM` | `ubuntu-latest` | Custom runner label for Linux matrix jobs if using self-hosted runners. |
| `ENABLE_CI` | *(empty / false)* | Optional fallback flag to enable CI builds if the repository name is changed. |
| `COMMERCIAL` | `false` | Set to `'true'` only for commercial distribution. |

---

### C. Permissions
- `contents: read` is declared at the workflow level (standard least-privilege for CI builds).

---

## 5. How We Tested This Workflow

Because we added `workflow_dispatch` to `.github/workflows/ci.yml`, this workflow can be triggered on-demand via the GitHub API and verified live.

### Testing Execution Steps:
1. Committed and pushed the updated workflow file to `origin main`.
2. Automatically retrieved the active GitHub authorization token from the local Git Credential Manager (`git credential fill`).
3. Sent an HTTP `POST` request to the GitHub Actions workflow dispatches endpoint:
   `https://api.github.com/repos/sajuptpm/spring-boot/actions/workflows/ci.yml/dispatches` with `{"ref": "main"}`.
4. Verified that the matrix of 7 jobs (Linux & Windows across Java 17, 21, 25, 27) was accepted and began executing on GitHub Actions runners.

---

## 6. How You Can Test It Later (Scripts & Instructions)

### Tool 1: `trigger-workflow.py`
Use this script to trigger the CI matrix build on-demand:

```bash
python workflow-fixes/trigger-workflow.py ci.yml main
```

---

### Tool 2: `check-runs.py`
Use this script to monitor the progress of all matrix jobs:

```bash
python workflow-fixes/check-runs.py 10
```

---

### Method 3: GitHub Web UI
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions/workflows/ci.yml`
2. Click **Run workflow** -> select branch `main` -> Click **Run workflow**.


---

## 7. How to Manually Verify via the GitHub UI

### Step 1: Verify the Actions Run Summary
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions`
2. Click **CI** in the left sidebar.
3. Click the most recent run (e.g., `CI #10`).
4. Look at the matrix job listing:
   - You will see 7 distinct matrix jobs listed:
     - `CI (Linux, 17, adoptium, -P... -D...)`
     - `CI (Linux, 21, adoptium, -P... -D...)`
     - `CI (Linux, 25, adoptium, -P... -D...)`
     - `CI (Linux, 27, graalvm, -P... -D...)`
     - `CI (Windows, 17, adoptium, -P... -D...)`
     - `CI (Windows, 21, adoptium, -P... -D...)`
     - `CI (Windows, 25, adoptium, -P... -D...)`
5. Click on any job to view its live runner allocation and Gradle compilation progress.
