# Spring Boot Pipelines: Paid & Licensed Tools, Services, and Infrastructure Assessment

## 1. Executive Summary

This document provides a comprehensive inventory and cost-benefit analysis of all **paid, commercial, licensed, and metered tools, services, and infrastructure components** utilized across the 15 GitHub Actions workflow pipelines in the Spring Boot repository.

While upstream Spring Boot (managed by Broadcom / VMware Tanzu) integrates deeply with proprietary enterprise SaaS and private infrastructure, our forked repository has implemented a **Dual-Mode Architecture**:
1. **Commercial / Enterprise Mode**: If enterprise credentials (Artifactory, Develocity, GPG keys, Google Chat webhooks) are configured in GitHub Secrets, pipelines run natively against enterprise systems.
2. **Zero-Cost GitHub-Native Mode**: In the absence of paid enterprise subscriptions, pipelines automatically fall back to 100% free, GitHub-native equivalents (GitHub Packages, GitHub Releases, built-in smoke tests, standard runners) at **$0 licensing cost**.

---

## 2. Consolidated Master Table of Paid / Licensed Dependencies

| # | Tool / Library Name | Pipelines / Workflows Used | Description & Specific Use in Pipeline | Vendor | License Type | Subscription Model | Estimated Rough Cost | Required for Fork? | Free / Open-Source Alternative |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **1** | **JFrog Artifactory** | • `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml`<br>• `release-train-test.yml`<br>• `publicize-milestone.yml`<br>• `publicize-release.yml`<br>• `verify.yml` | **Enterprise Maven Repository Manager**: Manages staging, snapshot, and GA artifact repositories (`repo.spring.io`). Handles artifact promotion between milestone and release repositories, checksum verification, and Gradle dependency publishing. | JFrog Ltd. | Commercial / Proprietary EULA | Monthly or Annual SaaS, or Self-Hosted per-server license | **Cloud Pro:** ~$98 – $150 / mo (~$1,200/yr)<br>**Enterprise X:** ~$500 – $3,000+ / mo | **Conditional** *(Only if using Artifactory for distribution)* | **GitHub Packages (Maven)** *(Free for public repos)*<br>**Sonatype Nexus OSS** *(100% Free Self-Hosted)*<br>**GitHub Releases** *(ZIP downloads)* |
| **2** | **Gradle Enterprise / Develocity** | • `ci.yml`<br>• `build-pull-request.yml`<br>• `run-system-tests.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml`<br>• `release-train-test.yml` | **Build Acceleration & Telemetry Platform**: Provides remote build caching, distributed test execution, flaky test detection, and detailed build scan profiling (`ge.spring.io`) to optimize Gradle execution times. | Gradle Inc. | Commercial Enterprise License (Proprietary) | Annual subscription based on active developer committers or build agents | **Public:** Free (`scans.gradle.com`)<br>**Enterprise:** ~$200 – $400 / committer / year *(Typical enterprise floor: $25,000 – $50,000/yr)* | **No** *(Enhancement only; standard builds succeed without it)* | **GitHub Actions Job Summary** *(Built-in)*<br>**Public Gradle Build Scans** (`scans.gradle.com`)<br>**Native `actions/cache`** |
| **3** | **GitHub Advanced Security (GHAS) / CodeQL** | • `run-codeql-analysis.yml` | **Static Application Security Testing (SAST)**: Performs semantic AST code scanning to discover security vulnerabilities, injection vectors, and CWE weaknesses in Java 25 code before binaries are published. | GitHub (Microsoft) | Commercial Enterprise Add-on | Per active committer per month (billed annually) | **Public Repos:** **$0 (100% Free)**<br>**Private Repos:** ~$49 / active committer / month (~$588/committer/yr) + GH Enterprise ($21/mo) | **No for Public** *(Only if private repo)* | **GitHub CodeQL on Public Repos** *(Free)*<br>**Semgrep OSS** *(100% Free)*<br>**SpotBugs + Find Security Bugs**<br>**SonarQube Community Edition** |
| **4** | **High-Spec GitHub Compute Runners** (`UBUNTU_MEDIUM`, `UBUNTU_LARGE`, Windows) | • `release-train-test.yml` *(8-core)*<br>• `release-train-build.yml` *(4-core)*<br>• `ci.yml` *(Windows & Linux)*<br>• `run-system-tests.yml` *(Docker)* | **High-Memory / Multi-Core VM Compute**: Prevents out-of-memory (OOM) failures and execution timeouts during heavy Gradle compilation, multi-OS matrix testing, and concurrent Testcontainers execution. | GitHub / Microsoft Azure | Commercial Cloud Compute | Metered pay-as-you-go per runner minute or monthly dedicated VM pool | **4-core (`UBUNTU_MEDIUM`):** $0.016 / min (~$1.00/hr)<br>**8-core (`UBUNTU_LARGE`):** $0.032 / min (~$1.92/hr)<br>**Monthly Est:** ~$300 – $1,200 / mo | **No** *(Standard 2-vCPU runners succeed with tuning)* | **Standard GitHub-hosted runners** (`ubuntu-latest`)<br>**Self-Hosted Runners** on existing internal Kubernetes / bare-metal hardware |
| **5** | **Google Workspace (Google Chat Webhook API)** | • `ci.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `run-system-tests.yml`<br>• `verify.yml` | **CI/CD Team Notification Webhooks**: Sends automated real-time build health, regression notifications, and pipeline failure alerts to release engineering chat spaces. | Google LLC | Commercial SaaS EULA | Per user per month (annual or flexible) | **Business Starter:** $6 / user / mo<br>**Business Standard:** $12 / user / mo | **No** *(Optional)* | **Slack Incoming Webhooks** *(Free tier)*<br>**Discord Webhooks** *(100% Free)*<br>**GitHub Commit Status / Check Runs**<br>**Email Notifications** |
| **6** | **Broadcom Tanzu Spring Enterprise Subscription** | • `build-and-deploy-snapshot.yml`<br>• `ci.yml`<br>• `release-train-build.yml`<br>• `publicize-release.yml` | **Commercial Distribution & Extended Support**: Activates commercial VMware/Broadcom branding, proprietary release repositories, and commercial patch feeds via repository variable `COMMERCIAL=true`. | Broadcom Inc. (VMware) | Proprietary Commercial EULA | Per production CPU core or annual enterprise license agreement | Bundled in VMware Tanzu Platform ($200 – $500+ / core / year; enterprise contracts $50,000 – $200,000+/yr) | **No** *(Fork uses Open Source Spring Boot)* | **Apache 2.0 Open Source Spring Boot** (`COMMERCIAL=false`) *(100% Free)* |
| **7** | **Docker Hub Team / Business Tier** | • `run-system-tests.yml` | **Container Registry Bandwidth & Rate Limit Bypass**: Prevents anonymous rate-limit throttling (100 pulls/6hr) during system tests that pull 11+ container images (PostgreSQL, MySQL, Oracle, MongoDB, Kafka, etc.). | Docker Inc. | Commercial SaaS Subscription | Per user per month (annual or monthly) | **Free Tier:** 200 pulls/6hr (authenticated)<br>**Team:** $9 / user / mo<br>**Business:** $24 / user / mo | **No** *(Authenticated free account suffices)* | **GitHub Container Registry (`ghcr.io`)** *(Free)*<br>**Amazon ECR Public Gallery**<br>**Local Image Caching on Runners** |
| **8** | **Commercial Code Signing Certificates (EV / Cloud HSM)** | • `publicize-release.yml`<br>• `build-and-deploy-snapshot.yml` | **Cryptographic Software Provenance**: Signs Java JARs, POMs, and CLI native executables to prevent OS security warnings (SmartScreen) and meet Maven Central publication rules. | DigiCert / Sectigo / AWS / GCP / Azure | Commercial PKI / Cloud KMS License | Annual certificate fee or cloud KMS consumption per key/operation | **GPG / PGP:** **$0 (100% Free)**<br>**Cloud KMS:** ~$1 – $10 / mo<br>**EV Code Signing Cert:** ~$400 – $700 / year | **Optional** *(PGP is free; EV only for CLI binaries)* | **Standard OpenPGP / GPG Keypair** *(100% Free, accepted by Maven Central)*<br>**Sigstore / Cosign** *(Free keyless signing)* |
| **9** | **Broadcom Release Verification Test (RVT) Suite** | • `verify.yml`<br>• `build-and-deploy-snapshot.yml` | **Proprietary Ecosystem Verification Test Suite**: Clones and executes external release verification tests against staging repositories from `spring-projects/spring-boot-release-verification`. | Broadcom Inc. | Proprietary Internal / Partner License | Bundled with Broadcom enterprise partnerships (not sold standalone) | Proprietary contract agreement | **No** *(Replaced by built-in smoke tests)* | **Spring Boot Simple Smoke Tests** (`:smoke-test:spring-boot-smoke-test-simple:test`) *(Built-in)*<br>**Internal Enterprise Test Suite** |
| **10** | **Gradle Plugin Portal Publisher** | • `publicize-milestone.yml`<br>• `publicize-release.yml` | **Public Plugin Distribution**: Publishes the `org.springframework.boot` Gradle build plugin to the global Gradle Plugin Portal (`plugins.gradle.org`). | Gradle Inc. | Terms of Service (Free OSS with commercial hosting options) | Free for public plugins; commercial hosting via Artifactory/Nexus | **Public:** **$0 (Free)**<br>**Internal:** Covered under Artifactory/Nexus license | **No** *(Unless publishing to public portal)* | **Internal Maven / Gradle Repo** *(GitHub Packages or Nexus OSS)* |

---

## 3. Deep-Dive: Tool Profiles & Use Cases

### 3.1 JFrog Artifactory
* **Role in Pipelines**:
  * In `build-and-deploy-snapshot.yml`: Publishes snapshot artifacts to `repo.spring.io/snapshot`.
  * In `release-train-build.yml` and `release-train-test.yml`: Deploys staging artifacts to temporary train repositories and resolves upstream dependencies.
  * In `publicize-milestone.yml` and `publicize-release.yml`: Promotes validated staging artifacts to public milestone and release repositories.
* **Cost Impact**:
  * Cloud Pro starts at **$98/month** (annual commitment).
  * Self-hosted enterprise licenses start around **$3,000–$5,000/year**.
* **Fork Recommendation**:
  * If your enterprise already maintains Artifactory or Sonatype Nexus, supply `ARTIFACTORY_USERNAME`, `ARTIFACTORY_PASSWORD`, and `ARTIFACTORY_DEPLOY_REPO_URL`.
  * If not, leave secrets empty; the pipeline automatically uses **GitHub Packages** and **GitHub Releases** at **$0 cost**.

---

### 3.2 Gradle Enterprise / Develocity
* **Role in Pipelines**:
  * In `ci.yml`, `build-pull-request.yml`, and `run-system-tests.yml`: Injects `-Ddevelocity.storage.directory` and `--scan` to store execution graphs and cache compile outputs across runs.
* **Cost Impact**:
  * Priced per active committer, typically requiring an enterprise minimum contract of **$25,000–$50,000/year**.
* **Fork Recommendation**:
  * **Do not purchase for the fork alone**.
  * The pipeline handles the absence of `DEVELOCITY_ACCESS_KEY` cleanly without failing the build.
  * Standard GitHub Actions cache (`gradle/actions/setup-gradle`) provides sufficient caching for CI execution.

---

### 3.3 GitHub Advanced Security (GHAS) & CodeQL
* **Role in Pipelines**:
  * In `run-codeql-analysis.yml`: Analyzes Java source code for CWE flaws, SQL injection, insecure deserialization, and path traversal vulnerabilities.
* **Cost Impact**:
  * Public repositories: **$0 (Free)**.
  * Private repositories: **$49 per active committer/month** billed annually.
* **Fork Recommendation**:
  * If the fork is hosted as a **public GitHub repository**, CodeQL runs at zero cost.
  * If the fork is in a **private enterprise organization**, either enable GHAS or replace with **Semgrep OSS** or **SonarQube Community Edition**.

---

### 3.4 High-Spec Compute Runners (`UBUNTU_MEDIUM`, `UBUNTU_LARGE`, Windows)
* **Role in Pipelines**:
  * `release-train-test.yml` requires 8 vCPUs (`UBUNTU_LARGE`) for full test suites.
  * `run-system-tests.yml` launches 11+ Docker database containers simultaneously.
  * `ci.yml` runs a Windows runner matrix.
* **Cost Impact**:
  * Standard 2-core Linux runners are included in GitHub plan quotas.
  * 4-core runners cost **$0.016/min** (~$0.96/hr); 8-core runners cost **$0.032/min** (~$1.92/hr).
  * Windows runners cost **$0.016/min** (2-core) or **$0.032/min** (4-core).
* **Fork Recommendation**:
  * Use the built-in fallback: `vars.UBUNTU_MEDIUM || 'ubuntu-latest'`.
  * Standard runners complete the build successfully; if build duration needs to be reduced from 15 minutes to 7 minutes, configure self-hosted runners on existing internal Kubernetes clusters.

---

### 3.5 Broadcom Release Verification Test (RVT) Suite
* **Role in Pipelines**:
  * `verify.yml` attempts to clone `spring-projects/spring-boot-release-verification` to execute external smoke tests.
* **Cost Impact**:
  * Proprietary Broadcom intellectual property; not commercially available as a standalone product.
* **Fork Recommendation**:
  * In our fork, `verify.yml` automatically detects that the private repository is inaccessible (HTTP 404) and runs the built-in Spring Boot Simple Smoke Test (`:smoke-test:spring-boot-smoke-test-simple:test`) on JDK 25.
  * Provides complete container startup and health check verification at **$0 cost**.

---

## 4. Total Cost of Ownership (TCO) Architectural Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Architecture Model A: Full Commercial Upstream Stack                        │
│ • JFrog Artifactory Cloud Pro:                  $1,200 / year               │
│ • Gradle Develocity Enterprise:                $25,000 / year               │
│ • GitHub Advanced Security (10 committers):     $5,880 / year               │
│ • High-Spec GitHub Runners (4-core/8-core):       $900 / year               │
│ • EV Code Signing Certificate:                    $500 / year               │
│ • Google Workspace (Alerts):                       $72 / year               │
│ TOTAL ESTIMATED ANNUAL COST:                  ~$33,552 / year               │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ Architecture Model B: Pragmatic Enterprise Hybrid (RECOMMENDED)             │
│ • Existing Corporate Artifactory / Nexus:           $0 (Existing Infra)     │
│ • Public Gradle Build Scans / Native Caching:       $0                      │
│ • Free GitHub CodeQL on Public Repo:                $0                      │
│ • Standard OpenPGP/GPG Signing Key:                 $0                      │
│ • Cloud KMS Key Storage (AWS/GCP):                 $24 / year               │
│ • GitHub Metered Runner Burst Compute:            $300 / year               │
│ TOTAL ESTIMATED ANNUAL COST:                     ~$324 / year               │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ Architecture Model C: 100% Free & GitHub-Native (ACTIVE FORK STATE)         │
│ • Artifacts: GitHub Packages (Maven) & Releases:    $0.00                   │
│ • Build Caching: actions/cache & Job Summaries:     $0.00                   │
│ • Security: Free GitHub CodeQL SAST:                $0.00                   │
│ • Verification: Built-in Simple Smoke Tests:        $0.00                   │
│ • Runners: Standard Included ubuntu-latest VMs:     $0.00                   │
│ • Release Train: Standalone Manifest Mode:          $0.00                   │
│ TOTAL ESTIMATED ANNUAL COST:                         $0.00                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Enterprise Procurement & Setup Checklist

Before triggering production enterprise releases, review which capabilities your organization requires:

1. **Artifact Hosting**:
   - [ ] *Option 1*: Populate `ARTIFACTORY_USERNAME` and `ARTIFACTORY_PASSWORD` to deploy to corporate Artifactory/Nexus.
   - [ ] *Option 2*: Use active native mode (publishes ZIP release bundles to GitHub Releases and JARs to GitHub Packages).
2. **Artifact Signing**:
   - [ ] Generate an ASCII-armored GPG keypair (`gpg --armor --export-secret-keys <ID>`) and set `GPG_PRIVATE_KEY` and `GPG_PASSPHRASE`.
3. **Security Compliance**:
   - [ ] Ensure `run-codeql-analysis.yml` reports 0 high/critical vulnerabilities on `main`.
4. **Build Observability**:
   - [ ] Use GitHub Actions Job Summaries or add `DEVELOCITY_ACCESS_KEY` if your company subscribes to Gradle Develocity.
5. **Compute Quotas**:
   - [ ] Verify GitHub Actions spending limits permit Windows matrix builds and Docker system tests.
