# Spring Boot Enterprise Release Readiness & Risk Assessment

## 1. Executive Summary

All 15 GitHub Actions workflow pipelines in [`.github/workflows/`](file:///c:/projects/spring-boot/.github/workflows/) have been modernized, executed live, and verified on GitHub Actions in this repository (`sajuptpm/spring-boot`).

The pipelines currently operate under a **Dual-Mode Architecture**:
* **Active GitHub-Native Mode**: In the absence of proprietary Broadcom/enterprise credentials, workflows automatically fall back to 100% free, GitHub-native alternatives (GitHub Releases, GitHub Packages / Maven, Actions Artifacts, and built-in smoke tests).
* **Enterprise Production Mode**: When enterprise secrets and configuration variables are populated, the pipelines dynamically route artifacts, signatures, and notifications to enterprise infrastructure (JFrog Artifactory, internal Maven repositories, Gradle Plugin Portal, SDKMAN, and external verification suites).

This document outlines the **architectural, operational, and security risks** when promoting these pipelines to an **Enterprise / Commercial Production Release**, along with mitigation strategies, required configuration, and a pre-release verification checklist.

---

## 2. Current State vs. Enterprise Production Target

```
                       Pipeline Trigger (workflow_dispatch / push)
                                           │
                              [Resolve Target & Mode]
                                           │
             ┌─────────────────────────────┴─────────────────────────────┐
             ▼                                                           ▼
   [Current Active Native Mode]                                [Enterprise Production Mode]
 • Artifacts: GitHub Releases & Packages                     • Artifacts: JFrog Artifactory / Nexus
 • Signing: Unsigned zips & jars                             • Signing: PGP/GPG Key & Passphrase
 • Verification: Built-in Simple Smoke Tests                 • Verification: Exhaustive RVT Suite
 • Release Train: Standalone Manifest Mode                   • Release Train: Multi-Repo Orchestrator
 • Runners: Standard 2-vCPU GitHub-hosted                    • Runners: Dedicated 8-vCPU / Self-hosted
 • Cost / Prereqs: Zero external accounts                    • Cost / Prereqs: Enterprise Infra & Secrets
```

---

## 3. Comprehensive Risk & Gap Analysis

### Risk 1: Cryptographic Artifact Signing & Supply Chain Provenance
* **Severity**: **Critical**
* **Current State**: Artifacts packaged in Native Mode (such as `spring-boot-4.2.0-SNAPSHOT-snapshot.zip` and GitHub Packages Maven jars) are published without PGP/GPG signatures.
* **Enterprise Impact**:
  * Public registries (Maven Central, Gradle Plugin Portal) and enterprise artifact firewalls (JFrog Xray, Sonatype Nexus Firewall) require ASCII-armored PGP signatures (`.asc` files) and SHA-256/SHA-512 checksums.
  * Enterprise regulatory frameworks (SLSA, NIST SSDF, SOC2, FedRAMP) mandate verifiable build provenance.
* **Mitigation**:
  * Set repository secrets `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE` before triggering release pipelines.
  * Enable GitHub Actions build attestations (`actions/attest-build-provenance`) for signed SLSA Level 3 supply-chain integrity.

---

### Risk 2: Enterprise Target Registry Credentials & Dual-Mode Routing
* **Severity**: **High**
* **Current State**: Workflows automatically detect whether `ARTIFACTORY_USERNAME` or `COMMERCIAL_ARTIFACTORY_USERNAME` is populated. When empty, they deploy directly to GitHub Releases.
* **Enterprise Impact**: If an enterprise operator runs `build-and-deploy-snapshot.yml` or `publicize-release.yml` without setting up secrets, artifacts will be published exclusively to GitHub rather than the internal corporate repository.
* **Mitigation**:
  * Ensure the following secrets are configured in **Repository Settings → Secrets and variables → Actions**:
    * `ARTIFACTORY_USERNAME` / `ARTIFACTORY_PASSWORD`
    * `COMMERCIAL_ARTIFACTORY_USERNAME` / `COMMERCIAL_ARTIFACTORY_PASSWORD`
    * `COMMERCIAL_DEPLOY_REPO_URL` / `COMMERCIAL_RELEASE_REPO_URL`
    * Set repository variable `COMMERCIAL=true` if building Broadcom commercial enterprise distributions.

---

### Risk 3: Verification Test Suite Coverage (RVT vs. Built-in Smoke Tests)
* **Severity**: **Medium**
* **Current State**: Upstream Spring Boot delegates release verification to a private Broadcom repository (`spring-projects/spring-boot-release-verification`). In our fork, `verify.yml` detects the HTTP 404 and runs the built-in smoke test `:smoke-test:spring-boot-smoke-test-simple:test` on JDK 25.
* **Enterprise Impact**:
  * The built-in smoke test verifies container startup, auto-configuration, and web endpoints.
  * However, it does not exhaustively test external repository resolution against Artifactory staging repositories, Homebrew formula installations, or multi-version Maven/Gradle plugin consumers.
* **Mitigation**:
  * If your organization maintains a dedicated Release Verification Test (RVT) repository, provide a GitHub PAT (`secrets.GH_ACTIONS_REPO_TOKEN` or `secrets.token`) granting read access to that repository.
  * If using Spring Boot internally within an enterprise, the built-in smoke test provides functional verification of core container startup and framework endpoints.

---

### Risk 4: Runner Sizing, Performance & Windows Build Timeouts
* **Severity**: **Medium**
* **Current State**: All workflows default to standard GitHub-hosted free runners (`ubuntu-latest` and `windows-latest` with 2 vCPUs and 7 GB RAM).
* **Enterprise Impact**:
  * During verification, full matrix CI on Windows took 22 to 35 minutes, with Windows I/O contention occasionally causing test timeouts.
  * Full snapshot and release builds require 9 to 15 minutes on standard 2-vCPU runners.
* **Mitigation**:
  * In **Repository Settings → Variables**, configure custom or larger runner tiers:
    * `UBUNTU_MEDIUM`: Point to `ubuntu-8-core` or dedicated self-hosted Linux runners.
    * `UBUNTU_SMALL`: Point to `ubuntu-4-core` or `ubuntu-latest`.
    * Windows CI: Allocate dedicated self-hosted Windows runners with NVMe storage.

---

### Risk 5: Multi-Project Release Train Orchestration
* **Severity**: **Low to Medium**
* **Current State**: Workflows `release-train-build`, `release-train-join`, `release-train-leave`, `release-train-ready`, `release-train-retry`, and `release-train-test` operate in **Standalone Mode** (`callback: none`).
* **Enterprise Impact**:
  * In the public/Broadcom Spring portfolio, Spring Boot is one part of a multi-project train (Spring Framework → Spring Data → Spring Security → Spring Boot → Spring Cloud) coordinated by a central orchestrator repository (`spring-io/release-train`).
* **Mitigation**:
  * **For Standalone Enterprise Distribution**: Standalone mode is the correct, self-contained architecture. No action needed.
  * **For Multi-Project Enterprise Trains**: If your organization orchestrates multiple internal Spring libraries together, configure `release-train-repository` to point to your enterprise orchestrator and set `RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN`.

---

### Risk 6: Automated `push:` Triggers Disabled
* **Severity**: **Operational / Informational**
* **Current State**: To prevent exhausting GitHub Actions runner minutes during development, automatic `push:` triggers were commented out on:
  * `ci.yml`
  * `build-and-deploy-snapshot.yml`
  * `run-system-tests.yml`
  * `run-codeql-analysis.yml`
* **Enterprise Impact**: Pull requests and commits merged to `main` will not automatically trigger CI or snapshot builds unless triggered manually via `workflow_dispatch`.
* **Mitigation**:
  * Before promoting to active team development, uncomment the `push:` triggers on `ci.yml` and `build-and-deploy-snapshot.yml`.
  * Add path filters (e.g. `paths-ignore: ['workflow-fixes/**', '**.md']`) to avoid rebuilding on documentation changes.

---

### Risk 7: Release Governance, Git Tagging & Rollback Procedures
* **Severity**: **Medium**
* **Current State**: `publicize-release.yml` and `publicize-milestone.yml` automatically create Git tags (`v4.2.0`, `v4.2.0-M2`) and GitHub Releases with release notes.
* **Enterprise Impact**:
  * Without branch and tag protection, an accidental workflow dispatch could push a release tag prematurely.
  * Release tags are immutable once published to downstream consumers.
* **Mitigation**:
  * Configure **GitHub Branch Protection Rules** for branch `main` (require pull request reviews, status check approvals).
  * Configure **GitHub Tag Protection Rules** (`v*`) requiring admin authorization for tag creation.

---

## 4. Configuration Reference for Enterprise Production

To transition from GitHub-Native Mode to full Enterprise Production Mode, configure the following:

### Repository Secrets (`Settings → Secrets and variables → Actions → Secrets`)
| Secret Name | Description | Required For |
| :--- | :--- | :---: |
| `ARTIFACTORY_USERNAME` | OSS / Enterprise Artifactory username | Artifactory Deployment |
| `ARTIFACTORY_PASSWORD` | OSS / Enterprise Artifactory API key / token | Artifactory Deployment |
| `COMMERCIAL_ARTIFACTORY_USERNAME` | Commercial Artifactory username | Commercial Builds (`COMMERCIAL=true`) |
| `COMMERCIAL_ARTIFACTORY_PASSWORD` | Commercial Artifactory API key / token | Commercial Builds (`COMMERCIAL=true`) |
| `GPG_PRIVATE_KEY` | ASCII-armored PGP private key for artifact signing | Production Releases |
| `GPG_PASSPHRASE` | Passphrase for the PGP private key | Production Releases |
| `GRADLE_PLUGIN_PUBLISH_KEY` | Gradle Plugin Portal API key | Public Plugin Publishing |
| `GRADLE_PLUGIN_PUBLISH_SECRET`| Gradle Plugin Portal secret | Public Plugin Publishing |
| `SDKMAN_KEY` | SDKMAN release consumer key | Spring Boot CLI Publishing |
| `SDKMAN_TOKEN` | SDKMAN release consumer token | Spring Boot CLI Publishing |
| `GOOGLE_CHAT_WEBHOOK_URL` | Webhook URL for CI/CD status notifications | Build Notifications |
| `DEVELOCITY_ACCESS_KEY` | Access key for Gradle Develocity build scans | Build Scans & Cache Acceleration |

### Repository Variables (`Settings → Secrets and variables → Actions → Variables`)
| Variable Name | Enterprise Value | Description |
| :--- | :--- | :--- |
| `COMMERCIAL` | `true` or `false` | Sets release branding to VMware/Broadcom commercial vs. OSS. |
| `COMMERCIAL_DEPLOY_REPO_URL` | `https://repo.spring.io` (or corporate URL) | Target repository URL for commercial snapshots. |
| `COMMERCIAL_RELEASE_REPO_URL`| `https://repo.spring.io` (or corporate URL) | Target repository URL for commercial GA releases. |
| `ARTIFACTORY_PROJECT` | `spring` (or internal project name) | Artifactory project identifier. |
| `ARTIFACTORY_REPOSITORY` | `libs-snapshot-local` (or internal repo) | Target Artifactory repository key. |
| `UBUNTU_MEDIUM` | `ubuntu-8-core` (or custom runner label) | High-performance runner for snapshot and release builds. |
| `UBUNTU_SMALL` | `ubuntu-4-core` (or `ubuntu-latest`) | Standard runner for utility jobs. |
| `ENABLE_SNAPSHOT_BUILD` | `true` | Allows snapshot pipeline execution on forked repos. |
| `ENABLE_CI` | `true` | Allows CI matrix pipeline execution on forked repos. |

---

## 5. Pre-Enterprise Release Checklist

Before dispatching `publicize-release.yml` or `build-and-deploy-snapshot.yml` for an official enterprise release, complete this verification checklist:

- [ ] **1. Version Property Set**: Verify `version` in [`gradle.properties`](file:///c:/projects/spring-boot/gradle.properties) matches the target release (e.g. `4.2.0` for GA, `4.2.0-SNAPSHOT` for snapshot).
- [ ] **2. Toolchain Verified**: Confirm JDK 25 is installed and active on build runners.
- [ ] **3. Credentials Populated**: Verify `ARTIFACTORY_*` and `GPG_*` secrets are configured in GitHub Settings.
- [ ] **4. CI Green**: Confirm that [`CI`](file:///c:/projects/spring-boot/.github/workflows/ci.yml) and [`Run System Tests`](file:///c:/projects/spring-boot/.github/workflows/run-system-tests.yml) pass cleanly on the release commit.
- [ ] **5. CodeQL Scan Clear**: Confirm [`Run CodeQL Analysis`](file:///c:/projects/spring-boot/.github/workflows/run-codeql-analysis.yml) reports 0 security vulnerabilities.
- [ ] **6. Runner Capacity Checked**: Ensure custom runner labels (`UBUNTU_MEDIUM`) have active, idle runners available.
- [ ] **7. Tag Protection Active**: Ensure git tag protection rules prevent accidental tag overwrites.

---

## 6. Step-by-Step Enterprise Release Execution Runbook

When you are ready to publish an official release:

1. **Step 1: Run Pre-Flight Validation**:
   ```bash
   python workflow-fixes/trigger-workflow.py verify.yml main version=4.2.0,verification-mode=auto
   ```
2. **Step 2: Run Full System Tests**:
   ```bash
   python workflow-fixes/trigger-workflow.py run-system-tests.yml main java-version=all,system-test-target=all
   ```
3. **Step 3: Trigger the Release Pipeline**:
   * For a **Milestone / RC**:
     ```bash
     python workflow-fixes/trigger-workflow.py publicize-milestone.yml main milestone=4.2.0-RC1
     ```
   * For a **General Availability (GA) Release**:
     ```bash
     python workflow-fixes/trigger-workflow.py publicize-release.yml main milestone=4.2.0,latest=true
     ```
4. **Step 4: Verify Published Deliverables**:
   * Inspect the newly created GitHub Release at `https://github.com/sajuptpm/spring-boot/releases`.
   * Verify uploaded assets: documentation bundle (`.zip`), CLI binary (`.zip`), Homebrew formula, and Gradle plugin packages.
   * Verify repository publications in Artifactory / Nexus (if enterprise credentials were provided).
