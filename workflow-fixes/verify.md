# Modernization & Dual-Mode Architecture: Verify (`verify.yml`)

## 1. Overview & Purpose

The `Verify` workflow ([`.github/workflows/verify.yml`](file:///c:/projects/spring-boot/.github/workflows/verify.yml)) is responsible for verifying release candidates, snapshots, and GA release artifacts before or during distribution.

In the upstream Spring Boot repository, this workflow operates as a reusable workflow (`workflow_call`) triggered by deployment pipelines (such as [`build-and-deploy-snapshot.yml`](file:///c:/projects/spring-boot/.github/workflows/build-and-deploy-snapshot.yml)). It checks out an external, private repository (`spring-projects/spring-boot-release-verification`), configures Java 17 and Homebrew, and executes the external test suite `spring-boot-release-verification-tests:test` to validate repository publication, Maven/Gradle dependencies, and Homebrew formula installations against Artifactory or staging repositories.

### Upstream Issues in Forked / Non-Enterprise Environments
1. **Private RVT Repository Dependency**: `spring-projects/spring-boot-release-verification` is a private Broadcom repository. In forks and public environments, `actions/checkout` fails with HTTP 404 unless an internal Broadcom PAT (`secrets.token`) with repo read permissions is provided.
2. **Missing Manual Trigger**: The original workflow only defined `workflow_call`, preventing developers from running manual pre-flight or on-demand release verifications.
3. **Java 25 Requirement**: Spring Boot 4.x (`main` branch) requires Java 25 or above. The upstream workflow was pinned to Java 17, failing immediately with `This project should be built with Java 25 or above`.
4. **Mandatory Secrets & Outdated Actions**: Upstream marked `google-chat-webhook-url` and `token` as `required: true`, and referenced `actions/upload-artifact@v7` (an unreleased version) only on test failure (`if: failure()`).
5. **Slow Homebrew Setup**: Homebrew was installed unconditionally for open-source builds, adding unnecessary latency when executing native verification tests.

---

## 2. Dual-Mode Architecture & Changes Summary

To preserve 100% upstream fidelity while enabling complete standalone operation in forked repositories, `verify.yml` implements a **Dual-Mode Architecture**:

```
                                  verify.yml
                                      │
                         [Resolve Verification Mode]
                                      │
               ┌──────────────────────┴──────────────────────┐
               ▼                                             ▼
     [Original Mode (RVT)]                         [Native Mode (GitHub)]
 • Checks out private repo                      • Uses built-in smoke tests
   spring-projects/spring-boot-release-           (:smoke-test:spring-boot-smoke-test-simple)
   verification                                 • Validates project version integrity
 • Sets up Homebrew & external tests            • Uses local Gradle wrapper & Liberica JDK 25
 • Uses RVT Artifactory credentials             • Zero external secrets or private repos needed
               │                                             │
               └──────────────────────┬──────────────────────┘
                                      │
                         [Record Verification Summary]
                                      │
                         [Upload build-reports Artifact]
                                      │
                         [Send Google Chat Notification]
```

### Key Changes Implemented
1. **Dual Trigger Support (`workflow_call` + `workflow_dispatch`)**:
   - Maintains full compatibility with caller workflows (`build-and-deploy-snapshot.yml`).
   - Adds `workflow_dispatch` with customizable parameters (`version`, `staging`, and `verification-mode`).
2. **Dynamic Mode Resolution (`resolve-mode`)**:
   - Defaults to `auto`. Checks whether `spring-projects/spring-boot-release-verification` is accessible via the GitHub REST API.
   - If HTTP 200, uses `original` mode.
   - If HTTP 404 / inaccessible, automatically selects `native` mode.
   - Users can explicitly force `mode=native` or `mode=original` via workflow inputs.
3. **GitHub-Native Verification Test Suite**:
   - In native mode, executes `:smoke-test:spring-boot-smoke-test-simple:test -Pversion="${{ inputs.version }}"`.
   - Confirms that the runtime context, auto-configuration, endpoints, and version metadata function properly without external Artifactory or private repository dependencies.
4. **Upgraded Java Toolchain**:
   - Replaced Java 17 with Liberica JDK 25 (`java-version: '25'`).
5. **Guarded Homebrew Setup**:
   - Homebrew is only installed when running in `original` mode, eliminating redundant minutes during native verification.
6. **Reliable Artifact & Notification Handling**:
   - Upgraded to `actions/upload-artifact@v4` with `if: always()` to capture test reports regardless of pass/fail outcome.
   - Guarded notification delivery, passing both `secrets.google-chat-webhook-url` and fallback repository secret `secrets.GOOGLE_CHAT_WEBHOOK_URL`.

---

## 3. Existing Solutions vs. Free Alternatives Analysis

| Feature / Step | Upstream / Original Solution | Active GitHub-Native Alternative |
| :--- | :--- | :--- |
| **Verification Test Suite** | External private repo `spring-projects/spring-boot-release-verification` (HTTP 404 without internal PAT). | Built-in smoke test `:smoke-test:spring-boot-smoke-test-simple:test` verifying core container startup, context, and web endpoints. |
| **Authentication / Access** | Broadcom personal access token (`secrets.token`) required for checkout. | GitHub default runner token (`GITHUB_TOKEN`) with auto-fallback to native mode. |
| **Repository Artifact Testing** | Requires Artifactory credentials (`COMMERCIAL_REPOSITORY_*`, `OPENSOURCE_REPOSITORY_*`). | Local project compilation and smoke test validation using Gradle caching and local repositories. |
| **Homebrew Installation** | Full Homebrew setup run on every open-source build. | Conditionally skipped in native mode, saving 45+ seconds per run. |
| **Test Report Artifacts** | `actions/upload-artifact@v7` (unreleased/invalid) only uploaded on `failure()`. | `actions/upload-artifact@v4` uploaded on `always()`, publishing HTML and XML test reports. |
| **Execution Flexibility** | Caller-only (`workflow_call`). | Dual-mode: reusable via `workflow_call` and manually dispatchable via `workflow_dispatch`. |

---

## 4. Configuration & Data Requirements

### Repository Secrets
| Secret Name | Required (Original Mode) | Required (Native Mode) | Description |
| :--- | :---: | :---: | :--- |
| `token` / `GH_ACTIONS_REPO_TOKEN` | **Yes** | No | GitHub PAT with read permissions for `spring-projects/spring-boot-release-verification`. |
| `commercial-repository-username` | Optional | No | Username for commercial release repository. |
| `commercial-repository-password` | Optional | No | Password for commercial release repository. |
| `opensource-repository-username` | Optional | No | Username for OSS staging/release repository. |
| `opensource-repository-password` | Optional | No | Password for OSS staging/release repository. |
| `google-chat-webhook-url` | Optional | Optional | Webhook URL for build outcome notifications. |
| `DEVELOCITY_ACCESS_KEY` | Optional | Optional | Gradle Develocity access key for build scans. |

### Repository Variables
| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `UBUNTU_SMALL` | `ubuntu-latest` | Custom runner label for verification jobs. |
| `COMMERCIAL` | `false` / unset | Set to `true` when verifying commercial VMware/Broadcom builds. |

### Permissions
| Permission | Level | Reason |
| :--- | :--- | :--- |
| `contents` | `read` | Checks out repository code and action definitions. |
| `actions` | `write` | Records job summaries and publishes test report artifacts. |

---

## 5. Live Test Verification Details

> *Live test verification in progress...*

| Parameter | Value |
| :--- | :--- |
| **Workflow Run ID** | *Pending* |
| **Workflow Run URL** | *Pending* |
| **Trigger Type** | `workflow_dispatch` |
| **Branch** | `main` |
| **Target Version** | `4.2.0-SNAPSHOT` |
| **Selected Mode** | `native` (auto-detected fallback) |
| **Run Outcome** | *Pending* |
| **Generated Artifacts** | `build-reports` |

---

## 6. How to Test Later

### Option A: Using the Workflow Dispatch Python Helper
```powershell
python workflow-fixes/trigger-workflow.py verify.yml main version=4.2.0-SNAPSHOT,verification-mode=auto
```

### Option B: Using the GitHub CLI (`gh`)
```bash
# Auto mode (auto-detects RVT access)
gh workflow run verify.yml -f version=4.2.0-SNAPSHOT -f verification-mode=auto

# Force Native Mode
gh workflow run verify.yml -f version=4.2.0-SNAPSHOT -f verification-mode=native

# Force Original Mode (requires Broadcom RVT access token)
gh workflow run verify.yml -f version=4.2.0-SNAPSHOT -f verification-mode=original
```

### Option C: Calling as a Reusable Workflow
```yaml
jobs:
  verify:
    uses: ./.github/workflows/verify.yml
    with:
      version: '4.2.0-SNAPSHOT'
      staging: false
      verification-mode: 'auto'
    secrets:
      token: ${{ secrets.GH_ACTIONS_REPO_TOKEN }}
```

---

## 7. Step-by-Step GitHub UI Manual Verification Guide

Follow these steps to manually verify this workflow directly in the GitHub web interface:

1. **Navigate to Actions**:
   - Open your web browser and navigate to `https://github.com/sajuptpm/spring-boot/actions`.
2. **Select the Workflow**:
   - In the left sidebar under "All workflows", click on **`Verify`**.
3. **Open the "Run workflow" Dropdown**:
   - Locate the blue **"Run workflow"** button at the top right of the workflow run list.
4. **Configure the Inputs**:
   - **Use workflow from**: Select branch `main`.
   - **Version to verify**: Enter `4.2.0-SNAPSHOT` (or any target version string).
   - **Whether the release to verify is in the staging repository**: Leave unchecked (`false`).
   - **Verification mode**: Select `auto` (or choose `native` to directly run smoke tests).
5. **Trigger Execution**:
   - Click the green **"Run workflow"** button.
6. **Inspect the Execution**:
   - Refresh the page and click on the newly triggered run (e.g. `Verify #...`).
   - Click on the `Verify` job.
   - Verify that step **`Resolve Verification Mode`** auto-selects `native` (due to external RVT repo being private).
   - Confirm step **`Run Release Verification Tests (Native Mode)`** compiles and passes `:smoke-test:spring-boot-smoke-test-simple:test`.
   - Verify that step **`Record Verification Summary`** writes a complete markdown table to the Job Summary.
   - Confirm step **`Upload Build Reports`** attaches the `build-reports` zip artifact under the run Summary.
