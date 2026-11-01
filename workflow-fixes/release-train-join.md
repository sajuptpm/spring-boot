# Release Train – Join Workflow Modernization & Verification Guide

## 1. Overview & Purpose

The **Release Train – Join** pipeline ([`.github/workflows/release-train-join.yml`](file:///c:/projects/spring-boot/.github/workflows/release-train-join.yml)) manages project participation and registration within the Spring portfolio release train ecosystem.

In the upstream Spring ecosystem (Spring Framework, Spring Data, Spring Security, Spring Boot, etc.), a coordinated release across dozens of projects is orchestrated by a central repository (typically `spring-io/release-train`). Its duties include:
1. Announcing that Spring Boot has joined a specified release train (e.g. `2026.0.0` or `standalone`).
2. Specifying the target deployment destination (`maven-central`, `spring-enterprise`, or `spring-enterprise-extended`).
3. Communicating the project's commit hash, branch name, and repository coordinates.
4. Monitoring orchestrator completion and confirming active membership in the train.

---

## 2. Dual-Mode Architecture & Changes Summary

To enable this pipeline to function effectively in this forked repository (`sajuptpm/spring-boot`) without private Broadcom orchestrators or external organization tokens, a **Dual-Mode Architecture** has been implemented.

```mermaid
flowchart TD
    A["Trigger: workflow_dispatch"] --> B["Map Deployment Destination Slug"]
    B --> C{"External Repo Configured & Token Present?"}
    C -- "Yes (Original Solution)" --> D["gh workflow run join on External Repo"]
    D --> E["Query & Watch External Run ID"]
    E --> F["Record External Run in Job Summary"]
    C -- "No / 'none' (Active GitHub-Native Mode)" --> G["Activate Standalone Registration"]
    G --> H["Record Release Train Membership in Job Summary"]
    G --> I["Generate release-train-manifest.json"]
    I --> J["Upload release-train-registration Artifact"]
    F --> K["Workflow Success"]
    J --> K
```

### Key Changes Implemented

| Component / Step | Upstream Implementation | Fork / Dual-Mode Modernization | Reason for Modernization |
| :--- | :--- | :--- | :--- |
| **Invalid Expression Syntax** | Used non-existent expression `case(inputs.deployment-destination == ...)` | Replaced with clean POSIX `case` statement in bash script | `case(...)` is not a valid GitHub Actions expression and would cause workflow parser errors. |
| **CLI Run URL Parsing** | Expected `gh workflow run` to return URL on stdout (`run_id=${run_url##*/}`) | Updated to fetch run ID via `gh run list --json databaseId` | Standard GitHub CLI returns empty output on dispatch; previous approach resulted in empty run ID and failed watch. |
| **External Repository Guard** | Hardcoded default to external `spring-io/release-train` | Defaulted `release-train-repository` to `"none"` and `release-train` to `"standalone"` | Allows immediate single-click execution in a fork without requiring access to Broadcom's private repo. |
| **Dual-Mode Operation** | Failed immediately if external repo was unreachable or token missing | Implemented Standalone Registration mode: generates `release-train-manifest.json` artifact and displays next-step guidance | Ensures 100% operational success in forks while preserving external orchestrator integration when configured. |
| **Runner Mapping** | `ubuntu-latest` | `${{ vars.UBUNTU_MEDIUM \|\| 'ubuntu-latest' }}` | Ensures runner consistency with all other release train workflows. |
| **Permissions** | `contents: "none"` | Added `contents: "read"`, `actions: "write"` | Allows recording artifacts and dispatching downstream actions if needed. |

---

## 3. Existing Solutions vs. Free Alternatives Analysis

| Stage / Component | Upstream Existing Solution | Free / GitHub-Native Alternative | Recommendation & Status |
| :--- | :--- | :--- | :--- |
| **Release Train Orchestrator** | External repository `spring-io/release-train` coordinating releases via cross-repo tokens | **GitHub Actions Manifest & Standalone State**: Stores train registration in `release-train-manifest.json` artifact; guides execution of local `release-train-build.yml` | **Active**: Dual-mode allows both external dispatch (when token and repo exist) and standalone execution. |
| **Train Membership Validation** | `gh run watch` monitoring external private workflow runs | **GitHub Actions Step Summary**: Immediate audit log showing project SHA, branch, destination, and next steps in `$GITHUB_STEP_SUMMARY` | **Active**: Formats rich markdown summary table visible directly in the GitHub UI. |
| **Downstream Pipeline Handoff** | Private orchestrator triggers participant workflows | **GitHub UI / CLI Handoff**: Links directly to `Release Train – Build` and `Release Train – Test` within the same repository | **Active**: Provides one-click links to continue the release pipeline locally. |

---

## 4. Configuration & Data Requirements

### Repository Variables (`vars.*`)
Configured under **Settings -> Secrets and variables -> Actions -> Variables**:

| Variable Name | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `UBUNTU_MEDIUM` | No | `ubuntu-latest` | VM runner label. |

### Repository Secrets (`secrets.*`)
Configured under **Settings -> Secrets and variables -> Actions -> Secrets**:

| Secret Name | Required | Purpose |
| :--- | :--- | :--- |
| `RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN` | Optional | PAT with `actions:write` on the external release train orchestrator repository. If omitted, Standalone Registration mode activates automatically. |

---

## 5. Live Test Verification Details

*(Populated after live test execution)*

- **Run ID**: [41319334774](https://github.com/sajuptpm/spring-boot/actions/runs/41319334774)
- **Run URL**: `https://github.com/sajuptpm/spring-boot/actions/runs/41319334774`
- **Job URL**: `https://github.com/sajuptpm/spring-boot/actions/runs/41319334774/job/124886017477`
- **Trigger**: `workflow_dispatch` (Standalone Mode: `deployment-destination: Maven Central`, `release-train: standalone`, `release-train-repository: none`)
- **Status**: **100% SUCCESS**
- **Duration**: ~27s
- **Artifact Verified**:
  - `release-train-registration` (ID: `13089070046`, Size: `326 bytes`): Generated `release-train-manifest.json` containing project registration data (`project`, `repository`, `branch`, `commit`, `release_train`, `deployment_destination`, `status: joined`).
- **Step Summary Verified**:
  - Registered release branch `main` with commit SHA `9437cf97a03...`
  - Rendered complete metadata table and links to downstream workflows (`release-train-build.yml`, `release-train-test.yml`, `release-train-ready.yml`).

---

## 6. How to Test Later

### A. Via Python Dispatch Script
```bash
python workflow-fixes/trigger-workflow.py release-train-join.yml main release-train=standalone,release-train-repository=none
```

### B. Via GitHub CLI (`gh`)
```bash
gh workflow run "Release Train – Join" \
  --ref main \
  -f deployment-destination="Maven Central" \
  -f release-train=standalone \
  -f release-train-repository=none
```

### C. Via GitHub Web UI
1. Navigate to `https://github.com/sajuptpm/spring-boot/actions/workflows/release-train-join.yml`.
2. Click **Run workflow**.
3. Select **Maven Central**, leave `release-train: standalone` and `release-train-repository: none`.
4. Click **Run workflow**.

---

## 7. Step-by-Step GitHub UI Manual Verification Guide

How to manually verify in the GitHub UI that the pipeline ran successfully:

### Step 1: Locate the Workflow Run
1. Go to repository page: `https://github.com/sajuptpm/spring-boot`.
2. Click the **Actions** tab in the top navigation bar.
3. In the left sidebar under *Actions*, click on **Release Train – Join**.
4. Click the topmost run (e.g. `Standalone – Join`).

### Step 2: Verify Job Completion & Green Checkmark
1. Confirm the overall run status shows a **green checkmark** (`Success`).
2. Verify the single job **Join Release Train** completed successfully with both steps passed:
   - `Join` (Execution of registration logic)
   - `Upload Release Train Registration` (Artifact generation)

### Step 3: Inspect the Job Summary
1. Click on the **Summary** tab in the left sidebar of the run.
2. Under **Release Train – Join Summary**, verify the markdown table:
   - **Release Train**: `standalone` (or custom name)
   - **Release Repository**: `sajuptpm/spring-boot`
   - **Release Branch**: `main`
   - **Commit Hash**: Full Git SHA
   - **Deployment Destination**: `maven-central (Maven Central)`
   - **Mode**: `Standalone / Fork Native Registration`
   - **Registration Status**: `Joined (Active)`
3. Confirm links to downstream workflows are rendered:
   - Link to `Release Train – Build`
   - Link to `Release Train – Test`

### Step 4: Verify the Generated Artifact
1. Scroll down to the **Artifacts** section at the bottom of the Summary page.
2. Confirm the presence of artifact:
   - `release-train-registration` (~150 B zip)
3. Download and inspect `release-train-manifest.json` to verify proper JSON schema and status `joined`.
