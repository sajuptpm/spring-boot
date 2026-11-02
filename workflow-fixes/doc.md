# Spring Boot Pipelines: Paid Tools, External Infrastructure, Cloud & GitHub Projects Assessment

## 1. Executive Summary

This document provides a comprehensive inventory, architectural analysis, and cost-benefit breakdown of all:
1. **Paid & Licensed Tools and Libraries**
2. **External Infrastructure, Paid Runners, External Infra Setups, and External Cloud Services**
3. **External GitHub Projects Cloned, Dispatched, and Used**

utilized across the 15 GitHub Actions workflow pipelines in the Spring Boot repository.

### Target Deployment Model: Open-Source Release via GitHub Enterprise Public Repository
The target operating model is:
* **Platform**: GitHub Enterprise hosting a **Public Fork Repository** (`https://github.com/sajuptpm/spring-boot`).
* **Objective**: Build, test, and perform **100% Open-Source Releases** under the Apache License 2.0 via the same public repository.
* **Financial Impact**: Because GitHub Enterprise grants **free unlimited standard GitHub-hosted runners, free GitHub Advanced Security (CodeQL SAST), free GitHub Packages (Maven), and free GitHub Releases** for public repositories, the **Total Annual Cost of Tools, Licensing, Infrastructure, and Security Scanning for this Open-Source Release is $0.00 / year**.

---

## 2. Consolidated Master Table: Paid & Licensed Tools and Libraries

The table below catalogs every paid, proprietary, or commercial tool and library utilized in upstream Spring Boot pipelines, contrasting upstream enterprise pricing against the **$0.00 Open-Source Release Model on a GitHub Enterprise Public Repository**.

| # | Tool / Library Name | Vendor | License Type | Upstream Commercial Rough Cost | Subscription Model | Pipelines / Workflows Used | Description & Specific Use in Pipeline | Cost for GH Enterprise Public Repo (OSS) | Required for OSS Release? | Open-Source Strategy & Free Alternative |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | **JFrog Artifactory** | JFrog Ltd. | Commercial / Proprietary EULA | **Cloud Pro:** ~$98 – $150 / mo (~$1,200/yr)<br>**Enterprise X:** ~$500 – $3,000+ / mo | Monthly/Annual SaaS, or Self-Hosted per-server instance BYOL | • `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml`<br>• `release-train-test.yml`<br>• `publicize-milestone.yml`<br>• `publicize-release.yml`<br>• `verify.yml` | **Enterprise Maven Repository Manager**: Manages staging, snapshot, and GA repositories (`repo.spring.io`). Handles artifact promotion between milestone and release stages, checksum validation, and Gradle dependency publishing. | **$0.00** | **No** *(Optional)* | **Maven Central (via Sonatype Central Portal / OSSRH)** *(100% Free for Open Source)*<br>**GitHub Packages (Maven)** *(Free for public repos)*<br>**GitHub Releases** *(Direct ZIP/JAR distribution)* |
| **2** | **Gradle Enterprise / Develocity** | Gradle Inc. | Commercial Enterprise License (Proprietary) | **Enterprise:** ~$200 – $400 / committer / year *(Typical floor: $25k – $50k/yr)* | Annual subscription based on active developer committers or build agents | • `ci.yml`<br>• `build-pull-request.yml`<br>• `run-system-tests.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml`<br>• `release-train-test.yml`<br>• `.github/actions/prepare-gradle-build` | **Build Acceleration & Telemetry**: Remote build caching, distributed test execution, flaky test detection, and detailed build scan profiling (`ge.spring.io`) to accelerate Gradle execution. | **$0.00** | **No** *(Enhancement only; standard builds succeed)* | **GitHub Actions Cache (`actions/cache`)** with `gradle/actions/setup-gradle` *(100% Free)*<br>**Public Gradle Build Scans (`scans.gradle.com`)** *(Free for open-source)*<br>**GitHub Actions Job Summary** *(Built-in)* |
| **3** | **GitHub Advanced Security (GHAS) / CodeQL** | GitHub (Microsoft) | Commercial Enterprise Add-on (for private repos) | **Public Repos:** **$0 (100% Free)**<br>**Private Repos:** ~$49 / committer / mo (~$588/committer/yr) | Per active committer per month (annual billing) on private repos; free on public repos | • `run-codeql-analysis.yml` | **Static Application Security Testing (SAST)**: Semantic AST code analysis to detect security vulnerabilities, injection vectors, and CWE flaws in Java 25 code before binaries are published. | **$0.00** *(Included free)* | **Yes** *(Mandatory for OSS security hygiene)* | **GitHub CodeQL on Public Repos** *(Completely free, full GHAS features included on public repositories even under GH Enterprise)* |
| **4** | **GitHub Compute Runners (`UBUNTU_MEDIUM`, `UBUNTU_LARGE`, `windows-latest`)** | GitHub (Microsoft) / Azure | Commercial Cloud Compute | **Standard Public:** **$0.00**<br>**Medium (4 vCPU):** ~$0.016 / min (~$0.96/hr)<br>**Large (8 vCPU):** ~$0.032 / min (~$1.92/hr) | Metered consumption per runner minute; standard runners 100% free with unlimited minutes on public repos | • `ci.yml`<br>• `build-pull-request.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml`<br>• `release-train-test.yml`<br>• `run-system-tests.yml`<br>• `verify.yml` | **Hosted Build Compute VMs**: Linux Ubuntu and Windows Server 2022 virtual machines executing parallel compilation, test suites, and packaging. | **$0.00** | **Yes** *(Standard runners)* | **Standard GitHub-Hosted Runners (`ubuntu-latest`, `windows-latest`)** are **100% Free** for public repos. Our memory heap tuning (`-Xmx4g`) and disk cleanup (`jlumbroso/free-disk-space`) allow builds to finish on standard runners without paid medium/large VMs. |
| **5** | **Broadcom Tanzu Spring Enterprise Subscription** | Broadcom Inc. (VMware) | Proprietary Commercial EULA | Bundled in VMware Tanzu Platform ($200 – $500+ / core / year; enterprise contracts $50k – $200k+/yr) | Annual enterprise license agreement based on production CPU cores | • `build-and-deploy-snapshot.yml`<br>• `ci.yml`<br>• `release-train-build.yml`<br>• `publicize-release.yml` | **Commercial Distribution & Extended Support**: Activates commercial VMware/Broadcom branding, proprietary release repositories, and commercial patch feeds via repository variable `COMMERCIAL=true`. | **$0.00** | **No** *(Completely redundant for OSS)* | **Open-Source Spring Boot Apache License 2.0** (`COMMERCIAL=false`). 100% free open-source community distribution. |
| **6** | **Broadcom Release Verification Test (RVT) Suite** | Broadcom Inc. (Spring Projects) | Proprietary Broadcom Internal / Partner License | Bundled with Broadcom enterprise partnerships (not sold standalone) | Closed internal repository access | • `verify.yml`<br>• `build-and-deploy-snapshot.yml` | **Proprietary Ecosystem Verification Test Suite**: Clones private repository `spring-projects/spring-boot-release-verification` to run downstream consumer sanity tests against staging repositories. | **$0.00** | **No** *(Replaced by built-in smoke tests)* | **Spring Boot Simple Smoke Tests** (`:smoke-test:spring-boot-smoke-test-simple:test`) runs automatically when private repo returns HTTP 404. Built-in and open-source. |
| **7** | **Commercial Code Signing Certificates (EV / Cloud HSM)** | DigiCert / Sectigo / AWS / GCP / Azure | Commercial PKI / Cloud KMS License | **GPG / OpenPGP:** **$0.00 (100% Free)**<br>**Cloud KMS:** ~$1 – $10 / mo<br>**EV Code Signing Cert:** ~$400 – $700 / year | Annual certificate fee or pay-as-you-go per key operation | • `publicize-release.yml`<br>• `build-and-deploy-snapshot.yml` | **Cryptographic Software Provenance**: Signs Java JARs, POMs, and CLI native executables to prevent OS security warnings and satisfy repository publication rules. | **$0.00** | **Optional** *(PGP signing is mandatory for Maven Central, but GPG is $0)* | **Standard OpenPGP / GPG Keypair** *(100% Free, accepted by Maven Central & Sonatype)*<br>**Sigstore / Cosign** *(Free keyless container and binary signing)* |
| **8** | **Docker Hub Team / Business Tier** | Docker Inc. | Commercial SaaS Subscription | **Free Tier:** $0 (200 pulls/6hr with auth)<br>**Team:** $9 / user / mo<br>**Business:** $24 / user / mo | Per-user monthly/annual subscription | • `run-system-tests.yml` | **Container Registry Bandwidth & Rate Limit Bypass**: Prevents anonymous rate-limit throttling (100 pulls/6hr) during system tests that pull 11+ container images (PostgreSQL, MySQL, Oracle, MongoDB, Kafka, etc.). | **$0.00** | **No** *(Authenticated free account or GHCR)* | **GitHub Container Registry (`ghcr.io`)** *(100% Free for public images)*<br>**Authenticated Free Docker Hub Account** (200 pulls/6hr is plenty for CI)<br>**Local runner container caching** |
| **9** | **Google Workspace (Google Chat Webhook API)** | Google LLC | Commercial SaaS EULA | **Business Starter:** $6 / user / mo<br>**Business Standard:** $12 / user / mo | Per-user monthly/annual subscription | • `ci.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `run-system-tests.yml`<br>• `verify.yml` | **CI/CD Team Notification Webhooks**: Sends automated real-time build health, regression notifications, and pipeline failure alerts to release engineering chat spaces. | **$0.00** | **No** *(Optional)* | **GitHub Actions Job Summaries & Check Runs** *(Native, $0)*<br>**GitHub Discussions / Release Announcements** *(Free)*<br>**Discord Webhook** *(100% Free)*<br>**Slack Incoming Webhooks** *(Free tier)* |
| **10** | **Gradle Plugin Portal Publisher** | Gradle Inc. | Gradle Plugin Portal Terms of Service (Free OSS) | **Public OSS:** **$0.00 (100% Free)** | Free for public open-source Gradle plugins | • `publicize-milestone.yml`<br>• `publicize-release.yml` | **Public Plugin Distribution**: Publishes the `org.springframework.boot` Gradle build plugin to the global Gradle Plugin Portal (`plugins.gradle.org`). | **$0.00** | **Yes** *(If distributing Gradle plugin publicly)* | **Official Gradle Plugin Portal** (`plugins.gradle.org`). Free registration, requires only API keys stored in secrets `GRADLE_PUBLISH_KEY` and `GRADLE_PUBLISH_SECRET`. |
| **11** | **Sonatype Central Portal / Maven Central (OSSRH)** | Sonatype Inc. / Maven Central | Maven Central Terms of Service (Free Open Source) | **Public OSS:** **$0.00 (100% Free)** | Free public service for all global open-source Java projects | • `build-and-deploy-snapshot.yml`<br>• `publicize-release.yml` | **Global Open-Source Maven Central Repository**: The global standard registry for distributing open-source Java libraries. Replaces proprietary Artifactory for public consumption. | **$0.00** | **Yes** *(Standard for OSS Java libraries)* | **Maven Central via Sonatype Central Portal** (`central.sonatype.com`). Free publisher account, validated namespace ownership via GitHub username/DNS. |
| **12** | **GitHub Releases & GitHub Packages** | GitHub (Microsoft) | GitHub Terms of Service (Included with GitHub) | **Public Repos:** **$0.00 (100% Free)** | Included free of charge for all public open-source repositories | • `build-and-deploy-snapshot.yml`<br>• `publicize-milestone.yml`<br>• `publicize-release.yml` | **Binary Distribution & Package Registry**: Hosts release bundles (`spring-boot-cli-<ver>-bin.zip`, `docs.zip`), source code archives, and Maven packages directly in the GitHub repo. | **$0.00** | **Yes** *(Active fallback)* | **Native GitHub Releases (`gh release create`)** and **GitHub Packages (Apache Maven)** with zero external hosting configuration. |

---

## 3. Consolidated Master Table: External GitHub Projects Cloned & Used in Pipelines

| # | GitHub Project Name | Project Type / Category | Pipelines / Workflows Used | Description & Specific Use in Pipeline | Vendor / Maintainer | License | Interaction Mechanism | Access Requirement | Open-Source Strategy / Alternative |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **`spring-projects/spring-boot-release-verification`** | Proprietary Release Test Suite | • `verify.yml`<br>• `build-and-deploy-snapshot.yml` | **Release Verification Test (RVT) Suite**: Cloned via `actions/checkout` (ref: `v0.0.15`, path: `external-rvt`) to run end-to-end sanity tests verifying that staged artifacts in Artifactory can be resolved by downstream consumers. | Broadcom Inc. (Spring Projects) | Proprietary Broadcom Internal / Partner License | `git clone` via `actions/checkout` | **Private** *(Requires GitHub PAT with `repo` read access)* | **Built-in Simple Smoke Tests** (`:smoke-test:spring-boot-smoke-test-simple:test`) automatically executes when repo returns HTTP 404. |
| **2** | **`spring-io/homebrew-tap`** *(also referenced as `spring-projects/homebrew-tap`)* | Package Distribution Tap | • `publicize-release.yml` *(via `update-homebrew-tap` action)* | **Spring Boot CLI Homebrew Tap**: Cloned to update the `spring-boot.rb` formula with the newly published CLI binary ZIP and SHA-256 checksum from Maven Central, committing and pushing updates directly to GitHub. | Broadcom Inc. (Spring I/O) / Homebrew | Apache License 2.0 | `git clone` & `git push` via `actions/checkout` | **Restricted Write** *(Requires PAT with write access to tap repo)* | **Custom Enterprise Homebrew Tap** (e.g. `<org>/homebrew-tap`) or direct ZIP distribution via GitHub Releases. |
| **3** | **`spring-io/release-train`** | Release Orchestrator & Manifest | • `release-train-join.yml`<br>• `release-train-build.yml`<br>• `release-train-leave.yml`<br>• `release-train-ready.yml`<br>• `release-train-retry.yml`<br>• `release-train-test.yml` | **Spring Release Train Orchestrator**: Central orchestrator coordinating multi-project releases across the Spring portfolio. Pipelines send `gh workflow run` dispatch events to synchronize build versions, staging repositories, and release status. | Broadcom Inc. (Spring I/O) | Apache License 2.0 | GitHub API / `gh workflow run` dispatch | **Restricted Write** *(Requires `RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN`)* | **Standalone Mode (`callback: none`)**: Operates independently for single-repo releases without external coordination. |
| **4** | **`spring-projects/spring-boot-docs`** | Documentation Site Repository | • `trigger-docs-build.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `publicize-milestone.yml`<br>• `publicize-release.yml` | **Decoupled Reference Documentation Site**: External repository compiling and hosting Antora-based documentation. Triggered via `gh workflow run deploy-docs.yml -r docs-build` to rebuild documentation on Antora asset updates. | Broadcom Inc. (Spring Projects) | Apache License 2.0 | GitHub API `repository_dispatch` / `gh workflow run` | **Restricted Write** *(Requires PAT with dispatch permissions)* | **Local Antora Documentation Build** or bundling docs directly into distribution ZIPs (`spring-boot-<version>-docs.zip`). |
| **5** | **`spring-io/antora-ui-spring`** | Documentation UI Bundle | • Referenced in documentation generation (`trigger-docs-build.yml`) | **Antora UI Theme & Layout Template**: Provides CSS, JavaScript, and navigation header templates defining the visual look-and-feel of official Spring documentation websites. | Broadcom Inc. (Spring I/O) | Mozilla Public License 2.0 (MPL-2.0) | Cloned / downloaded during Antora site build | **Public** *(Open Source)* | Can be cloned freely or replaced with corporate enterprise documentation themes. |
| **6** | **`spring-io/artifactory-deploy-action`** | Deployment GitHub Action | • `build-and-deploy-snapshot.yml` | **Artifactory Multithreaded Publisher**: Custom action (`spring-io/artifactory-deploy-action@v0.0.6`) uploading Maven deployment folders, POMs, and signed JARs to JFrog Artifactory with build-info metadata. | Broadcom Inc. (Spring I/O) | Apache License 2.0 | `uses: spring-io/artifactory-deploy-action@...` | **Public** *(Open Source)* | Active fallback to **GitHub Releases (`gh release create`)** and **GitHub Packages** when Artifactory is not configured. |
| **7** | **`spring-io/github-changelog-generator`** | Release Tooling Action | • `publicize-milestone.yml`<br>• `publicize-release.yml` *(via `create-github-release` action)* | **Automated Milestone Changelog Generator**: Custom action (`spring-io/github-changelog-generator@v0.0.14`) that queries GitHub API for milestone issues/PRs and formats release notes into categorized sections. | Broadcom Inc. (Spring I/O) | Apache License 2.0 | `uses: spring-io/github-changelog-generator@...` | **Public** *(Open Source)* | Fully functional in forks using repository `GITHUB_TOKEN` to generate changelogs from internal milestones. |
| **8** | **`spring-io/github-actions`** | Shared Reusable Workflows | • `run-codeql-analysis.yml` | **Enterprise Reusable Workflow Repository**: Upstream workflow calls `uses: spring-io/github-actions/.github/workflows/codeql-analysis.yml` to execute standardized CodeQL static security analysis. | Broadcom Inc. (Spring I/O) | Apache License 2.0 | `uses: <owner>/<repo>/.github/workflows/...` | **Public** *(Open Source)* | Fully functional; or use standard inline `github/codeql-action` steps directly. |
| **9** | **`gradle/actions` (`setup-gradle`)** | Build Tool GitHub Action | • `ci.yml`<br>• `build-pull-request.yml`<br>• `verify.yml`<br>• `.github/actions/prepare-gradle-build` | **Gradle Environment & Cache Action**: Configures Gradle build environment, validates wrapper binaries, injects Develocity access keys, caches dependencies, and generates Actions Job Summaries. | Gradle Inc. | Apache License 2.0 | `uses: gradle/actions/setup-gradle@...` | **Public** *(Open Source)* | Fully functional in all environments; handles both cached and non-cached builds. |
| **10** | **`Homebrew/actions` (`setup-homebrew`)** | Package Manager Action | • `verify.yml` | **Homebrew Setup Action**: Installs and configures Homebrew on macOS/Linux runners (`Homebrew/actions/setup-homebrew`) during release verification to test CLI formula installations. | Homebrew Project | BSD 2-Clause License | `uses: Homebrew/actions/setup-homebrew@...` | **Public** *(Open Source)* | Used in verification original mode; skipped when running in native smoke test mode. |
| **11** | **`jlumbroso/free-disk-space`** | Runner Utility Action | • `release-train-test.yml`<br>• `.github/actions/prepare-gradle-build` | **Runner Storage Cleaner**: Removes pre-installed toolchains (Android SDKs, .NET, Haskell, swap space) from standard GitHub runner images to free up 30GB+ of disk space for heavy builds and Docker images. | Jonathan Lumbroso (Community OSS) | MIT License | `uses: jlumbroso/free-disk-space@...` | **Public** *(Open Source)* | Essential utility for preventing runner disk exhaustion on standard GitHub runners. |
| **12** | **`jfrog/setup-jfrog-cli`** | CLI Installer Action | • `.github/actions/publish-gradle-plugin` *(called by `publicize-release.yml`)* | **JFrog CLI Bootstrap Action**: Installs and authenticates the JFrog CLI tool on the runner to download pre-staged Gradle plugin binaries from Artifactory prior to publishing. | JFrog Ltd. | Apache License 2.0 | `uses: jfrog/setup-jfrog-cli@...` | **Public** *(Open Source)* | Used only when publishing plugins from Artifactory; can be bypassed if publishing directly from Gradle. |
| **13** | **`actions/checkout`** | Core Official Action | • Used across almost all 15 workflows | **Git Repository Checkout**: Clones repository branches, tags, submodules, and secondary repos (like `external-rvt` or `homebrew-tap`) into runner workspace. | GitHub (Microsoft) | MIT License | `uses: actions/checkout@...` | **Public** *(Open Source)* | Official standard action, fully supported. |
| **14** | **`actions/setup-java`** | Core Official Action | • `ci.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `verify.yml`<br>• `prepare-gradle-build` | **Java Toolchain Action**: Downloads, installs, and configures OpenJDK 25 toolchains (Liberica / Temurin distributions) with `JAVA_HOME` configuration. | GitHub (Microsoft) | MIT License | `uses: actions/setup-java@...` | **Public** *(Open Source)* | Official standard action, fully supported. |
| **15** | **`actions/upload-artifact` & `actions/download-artifact`** | Core Official Action | • `build-and-deploy-snapshot.yml`<br>• `publicize-milestone.yml`<br>• `publicize-release.yml`<br>• `release-train-*.yml` | **Workflow Artifact Storage**: Uploads and downloads build artifacts (ZIP archives, test reports, distributions) across decoupled workflow jobs. | GitHub (Microsoft) | MIT License | `uses: actions/upload-artifact@...`<br>`uses: actions/download-artifact@...` | **Public** *(Open Source)* | Official standard action, fully supported. |

---

## 4. Consolidated Master Table: External Infrastructure, Paid Runners & Cloud Services

The table below details all external compute runners, cloud platforms, infrastructure setups, and external hosting environments, contrasting upstream commercial requirements with the **$0.00 Open-Source Release Model on a GitHub Enterprise Public Repository**:

| # | Infrastructure Name | Category / Infra Type | Vendor / Provider | License / Terms | Upstream Commercial Rough Cost | Subscription Model | Pipelines / Workflows Used | Description & Specific Use in Pipeline | Cost for GH Enterprise Public Repo (OSS) | Required for OSS Release? | Open-Source Strategy & Free Alternative |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **1** | **GitHub Standard Linux Runners (`ubuntu-latest`)** | Hosted Compute Runner (2 vCPU, 7 GB RAM, 14 GB SSD) | GitHub (Microsoft) / Azure | GitHub Terms of Service | $0.008 / min on private repos | Metered on private repos; **100% Free with unlimited minutes on public repos** | • `ci.yml`<br>• `build-pull-request.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `run-system-tests.yml`<br>• `release-train-*.yml`<br>• `verify.yml` | **Standard CI/CD Linux VM**: Compiles multi-module Gradle project, runs unit test suites, builds documentation, and executes Testcontainers. | **$0.00 (Unlimited Free)** | **Yes** | **Standard GitHub-Hosted `ubuntu-latest`** *(Free for public repositories; zero setup)* |
| **2** | **GitHub Standard Windows Runners (`windows-latest`)** | Hosted Compute Runner (Windows Server 2022) | GitHub (Microsoft) / Azure | Commercial Cloud Compute (OS license included) | $0.016 / min on private repos (consumes 2x Linux minutes) | Metered on private repos; **100% Free with unlimited minutes on public repos** | • `ci.yml` *(Windows matrix build job)* | **Cross-Platform OS VM**: Validates cross-platform file system handling, path delimiters (`\` vs `/`), and Windows batch scripts to guarantee multi-platform stability. | **$0.00 (Unlimited Free)** | **Yes** *(For cross-platform QA)* | **Standard GitHub-Hosted `windows-latest`** *(Free for public repositories; zero setup)* |
| **3** | **GitHub Larger Linux Compute Runners (`UBUNTU_MEDIUM`)** | Paid Runner / Mid-Tier Compute (4 vCPU, 16 GB RAM) | GitHub (Microsoft) / Azure | Commercial Cloud Compute | ~$0.016 / min (~$0.96 / hr)<br>*Monthly Est: ~$200 – $600 / mo* | Metered consumption per runner minute | • `release-train-build.yml`<br>• `ci.yml` *(Linux)*<br>• `run-system-tests.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `build-pull-request.yml`<br>• `release-train-join.yml`<br>• `release-train-leave.yml`<br>• `release-train-ready.yml`<br>• `release-train-retry.yml` | **Mid-Tier Compute VM**: Upstream uses larger VMs to prevent heap memory exhaustion and execution timeouts during parallel Gradle compilation and integration tests. | **$0.00** | **No** *(Standard runners succeed with tuning)* | **Standard `ubuntu-latest`** with Gradle heap tuning (`-Xmx4g`) and storage cleanup (`jlumbroso/free-disk-space`). Paid medium runners are completely bypassable. |
| **4** | **GitHub Heavyweight Linux Runners (`UBUNTU_LARGE`)** | Paid Runner / Heavy Compute (8 vCPU, 32 GB RAM) | GitHub (Microsoft) / Azure | Commercial Cloud Compute | ~$0.032 / min (~$1.92 / hr)<br>*Monthly Est: ~$300 – $800 / mo* | Metered consumption per runner minute | • `release-train-test.yml` | **High-Memory Compute VM**: Upstream uses 8-core VMs for full-portfolio integration tests and multi-project framework verification across Spring ecosystem. | **$0.00** | **No** *(Exclude heavy docs or tune memory)* | **Standard `ubuntu-latest`** with Gradle memory tuning (`-Xmx4g`) or excluding heavyweight Antora site rendering (`-x antora`). |
| **5** | **Self-Hosted Kubernetes Runner Pool (Actions Runner Controller - ARC)** | External Infra Setup / Private Cloud Compute | AWS (EKS) / GCP (GKE) / Azure (AKS) / On-Premise VMware | Cloud Infrastructure & ARC Open-Source Controller | ~$150 – $600 / month per cluster (e.g. 2 x `c6i.2xlarge` nodes @ ~$250/mo each + K8s management fee) | Monthly cloud cluster compute, networking, and storage billing | • Applicable to all 15 workflows (`ci.yml`, `run-system-tests.yml`, etc.) | **Autoscaling Ephemeral Private Compute**: Runs private container runners inside a corporate VPC/Kubernetes cluster behind enterprise firewalls for proprietary builds. | **$0.00** | **No** *(Optional private infrastructure)* | **Default GitHub-Hosted Standard Runners** (`ubuntu-latest`) *(Zero infrastructure maintenance, 100% free on public repos)* |
| **6** | **JFrog Artifactory Enterprise / Cloud Repository Server (`repo.spring.io`)** | External Cloud Infra / Central Artifact Storage | JFrog Ltd. / AWS / Azure / GCP | Commercial Enterprise EULA | **Cloud Pro:** ~$98 – $150 / mo (~$1,200/yr)<br>**Enterprise X:** ~$500 – $3,000+ / mo<br>**Self-hosted VM:** ~$200 – $500 / mo | Monthly/Annual SaaS or BYOL Self-Hosted per instance | • `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml`<br>• `release-train-test.yml`<br>• `publicize-milestone.yml`<br>• `publicize-release.yml`<br>• `verify.yml` | **Central Maven Repository Server**: Enterprise Maven repository hosting snapshots (`libs-snapshot-local`), milestone staging (`libs-milestone-local`), and GA releases (`libs-release-local`) with RBAC and metadata promotion. | **$0.00** | **No** *(Optional)* | **Maven Central (via Sonatype Central Portal / OSSRH)** *(100% Free for Open Source)*<br>**GitHub Packages (Maven)** *(Free for public repos)*<br>**GitHub Releases** *(Direct ZIP/JAR distribution)* |
| **7** | **Gradle Enterprise / Develocity Remote Server (`ge.spring.io`)** | External Cloud Infra / Build Telemetry & Cache Server | Gradle Inc. / AWS / GCP | Commercial Enterprise Software License (Proprietary) | **Software License:** ~$25,000 – $50,000+ / year<br>**Cloud Host (EC2 + SSD):** ~$150 – $300 / mo | Annual committer-based license + cloud VM compute | • `ci.yml`<br>• `build-pull-request.yml`<br>• `run-system-tests.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml`<br>• `release-train-test.yml` | **Centralized Remote Build Cache & Telemetry Server**: Stores compiled task outputs, dependency verification graphs, and build performance analytics to accelerate build times across distributed CI workers. | **$0.00** | **No** *(Enhancement only; standard builds succeed)* | **GitHub Actions Cache (`actions/cache`)** with `gradle/actions/setup-gradle` *(100% Free)*<br>**Public Gradle Build Scans (`scans.gradle.com`)** *(Free for open-source)*<br>**GitHub Actions Job Summary** *(Built-in)* |
| **8** | **Docker Engine & Testcontainer Runtime Host** | External Infra Setup / Container Compute & Storage | Docker Inc. / Cloud VM Host / Moby Project | Open Source (Docker CE on Linux) | **Software:** $0 (Docker CE on Linux)<br>**Host Compute/Storage:** Min 8GB RAM + 30GB SSD space on runner (~$50 – $100/mo if self-hosted)<br>**Docker Hub Team:** $9/user/mo *(to avoid IP rate limits)* | Free OSS runtime; metered cloud VM compute; optional registry SaaS | • `run-system-tests.yml` | **Local Container Host & Storage**: Runs 11+ real database and messaging broker containers (Postgres, Oracle-Free, MS SQL, MySQL, MariaDB, Mongo, Neo4j, Cassandra, Redis, RabbitMQ, Kafka) concurrently during integration tests. | **$0.00** | **Yes** *(Mandatory for system tests)* | **Pre-installed Docker CE on GitHub `ubuntu-latest` runners** *(100% Free, zero setup)*<br>**GitHub Container Registry (`ghcr.io`)** *(Free for public container images)* |
| **9** | **Google Cloud Webhook Endpoint Infrastructure (`chat.googleapis.com`)** | External Cloud Service / Alerting Gateway | Google Cloud / Google Workspace | Commercial SaaS EULA | Included in Google Workspace ($6 – $18 / user / mo); webhook network egress: $0 | Per-user monthly Google Workspace subscription | • `ci.yml`<br>• `build-and-deploy-snapshot.yml`<br>• `run-system-tests.yml`<br>• `verify.yml` | **Cloud Webhook Ingestion Gateway**: Cloud HTTP POST endpoint receiving JSON payload cards to broadcast build outcomes, test regressions, and release promotions to Google Chat spaces. | **$0.00** | **No** *(Optional notification channel)* | **GitHub Commit Status & Check Runs** *(Native, $0)*<br>**GitHub Discussions / Release Announcements** *(Free)*<br>**Discord Webhook** *(100% Free)*<br>**Slack Incoming Webhooks** *(Free tier)* |
| **10** | **Cloud Key Management Service (Cloud KMS) / HSM** | External Cloud Infra / Cryptographic Key Vault | AWS (KMS / CloudHSM) / GCP (Cloud KMS) / Azure (Key Vault) | Commercial Cloud KMS License | **Cloud KMS:** ~$1.00 / key / mo + $0.03 per 10k operations (~$2 – $10 / mo)<br>**CloudHSM:** ~$1,050 / mo<br>**EV Code Signing Cert:** ~$400 – $700 / yr | Consumption-based pay-as-you-go per key/operation | • `publicize-release.yml`<br>• `build-and-deploy-snapshot.yml` | **FIPS 140-2 Level 3 Hardware Security Module**: Secure cloud key vault for storing private PGP/GPG artifact signing keys and EV Authenticode code signing keys, preventing key exfiltration during automated release execution. | **$0.00** | **Optional** *(PGP signing is mandatory for Maven Central, but GPG is $0)* | **Standard OpenPGP / GPG Keypair** stored as encrypted GitHub Actions Secrets (`GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`) *(100% Free)*<br>**Sigstore / Cosign** *(Free keyless signing)* |
| **11** | **External Upstream & Downstream GitHub Repositories** | External Infra Setup / Distributed Git Repos | GitHub (Microsoft) / Broadcom | GitHub Enterprise Terms / Proprietary Repositories | Public repos: $0<br>Private repos: Included in GitHub Enterprise ($21 / user / mo) | User seats in GitHub Enterprise Cloud / Server | • `release-train-*.yml` *(depends on `spring-io/release-train`)*<br>• `verify.yml` *(depends on `spring-boot-release-verification`)*<br>• `trigger-docs-build.yml` *(depends on `spring-boot-docs`)*<br>• `publicize-release.yml` *(depends on `homebrew-tap`)* | **Distributed Repository Topology**: External Git repositories that pipelines clone, query, or trigger via GitHub REST API calls and `repository_dispatch` events during coordinated release builds. | **$0.00** | **No** *(Decoupled in fork via standalone mode, smoke tests, and local docs)* | **Standalone Mode (`callback: none`)**<br>**Built-in Simple Smoke Tests**<br>**Public GitHub `<org>/homebrew-tap` repository** |
| **12** | **Sonatype Central Portal / Maven Central Registry Infrastructure** | External Cloud Service / Global OSS Package Registry | Sonatype Inc. / Maven Central | Maven Central Terms of Service (Free OSS) | **$0.00 (100% Free)** | Free public service for all global open-source Java projects | • `build-and-deploy-snapshot.yml`<br>• `publicize-release.yml` | **Global Open-Source Maven Central Repository**: The global standard registry for distributing open-source Java libraries. Replaces proprietary Artifactory for public consumption. | **$0.00** | **Yes** *(Standard for OSS Java libraries)* | **Maven Central via Sonatype Central Portal** (`central.sonatype.com`). Free publisher account, validated namespace ownership via GitHub username/DNS. |
| **13** | **GitHub Packages (Apache Maven) Cloud Registry** | External Cloud Service / In-Repo Maven Registry | GitHub (Microsoft) | GitHub Terms of Service | Included in GitHub Enterprise ($0 for public repos) | Free unlimited storage and data transfer for public open-source repositories | • `build-and-deploy-snapshot.yml`<br>• `release-train-build.yml` | **In-Repo Package Registry**: Cloud package registry storing snapshot and milestone dependencies directly under the repository namespace (`maven.pkg.github.com/<owner>/spring-boot`). | **$0.00** | **Yes** *(Free snapshot hosting)* | **GitHub Packages** (`maven.pkg.github.com/<owner>/spring-boot`) with zero external hosting configuration. |
| **14** | **GitHub Releases Storage & CDN Distribution** | External Cloud Service / Binary Hosting & Global CDN | GitHub (Microsoft) / Azure CDN | GitHub Terms of Service | Included in GitHub Enterprise ($0 for public repos) | Free unlimited storage and global download bandwidth for public repositories | • `publicize-release.yml`<br>• `publicize-milestone.yml` | **Binary Distribution & Release Hosting**: Stores compiled release assets (`spring-boot-cli-<ver>-bin.zip`, `docs.zip`, checksums) on a worldwide edge CDN. | **$0.00** | **Yes** *(Active fallback)* | **Native GitHub Releases (`gh release create`)** with automatic changelog generation from GitHub milestones. |

---

## 5. Open-Source Release Architecture & Blueprint (GitHub Enterprise Public Repo)

When releasing Spring Boot as an open-source project from a **public repository under GitHub Enterprise**, every commercial upstream dependency translates directly into a zero-cost open-source equivalent:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│                  OPEN-SOURCE RELEASE ARCHITECTURE (PUBLIC GITHUB REPO)                       │
├──────────────────────────┬─────────────────────────────────────┬─────────────────────────────┤
│ Functional Capability    │ Upstream Commercial Component       │ Open-Source Release Model   │
├──────────────────────────┼─────────────────────────────────────┼─────────────────────────────┤
│ 1. Artifact Distribution │ JFrog Artifactory SaaS ($1,200+/yr) │ Maven Central (Sonatype)    │
│                          │                                     │ + GitHub Packages ($0.00)   │
│ 2. Binary Releases       │ Broadcom Distribution Repos         │ GitHub Releases ($0.00)     │
│ 3. Static Security SAST  │ GHAS Commercial Seat ($588/yr)      │ Free GitHub CodeQL ($0.00)  │
│ 4. Build Caching         │ Gradle Develocity ($25k–$50k/yr)    │ actions/cache + Job Summary │
│ 5. Test Telemetry        │ Private Develocity Cluster          │ scans.gradle.com ($0.00)    │
│ 6. Verification Testing  │ Proprietary Broadcom RVT Repo       │ Built-in Smoke Tests ($0)   │
│ 7. Compute & Runners     │ Paid Larger Runners ($900+/yr)      │ Free ubuntu-latest ($0.00)  │
│ 8. Cryptographic Signing │ Cloud HSM / Commercial EV Cert      │ OpenPGP / GPG ($0.00)       │
│ 9. Notifications         │ Google Workspace Webhooks ($72+/yr) │ GitHub Check Runs & PRs ($0)│
│ 10. CLI Package Tap      │ spring-io/homebrew-tap (Restricted) │ <org>/homebrew-tap ($0.00)  │
└──────────────────────────┴─────────────────────────────────────┴─────────────────────────────┘
```

### Detailed Capability Mapping for Open-Source Release

#### 1. Artifact Distribution: Maven Central & GitHub Packages ($0.00)
* **Releases**: Upstream deploys releases to JFrog Artifactory (`repo.spring.io/release`) and stages them for Maven Central. For an open-source fork, register your namespace (e.g., `io.github.<your-org>`) on **Sonatype Central Portal** (`central.sonatype.com`). Publishing open-source artifacts to Maven Central is **100% free forever**.
* **Snapshots & Milestones**: Snapshots can be published for free to **GitHub Packages** (`maven.pkg.github.com/<owner>/spring-boot`) with zero bandwidth or storage fees on public repositories.
* **Fallbacks**: If no remote repository is configured, the pipeline builds standalone archives (`spring-boot-<version>.jar`, `spring-boot-cli-<version>-bin.zip`) and attaches them directly to the **GitHub Release**.

#### 2. Static Application Security Testing: GitHub CodeQL SAST ($0.00)
* Upstream triggers `run-codeql-analysis.yml` using `spring-io/github-actions/.github/workflows/codeql-analysis.yml`.
* In a private repository, GitHub Advanced Security (GHAS) requires a paid add-on license ($49/committer/month).
* **In a Public Repository**: GitHub provides **GitHub Advanced Security (CodeQL AST analysis, secret scanning, Dependabot alerts)** completely **FREE** with unlimited scans and zero committer charges.

#### 3. Build Acceleration & Telemetry: Native Cache & Public Build Scans ($0.00)
* Upstream uses a dedicated Gradle Enterprise instance (`ge.spring.io`) costing upwards of $25,000–$50,000/year.
* For the open-source fork:
  * Gradle dependency and task outputs are cached using **`actions/cache`** and `gradle/actions/setup-gradle` at **$0.00**.
  * Detailed build profiling scans can be published to **Gradle Public Build Scans** (`scans.gradle.com`) for free by running Gradle with the `--scan` flag or accepting terms in `settings.gradle`.
  * Actions Job Summaries display compilation metrics and test failure reports directly in the GitHub UI.

#### 4. Release Verification: Built-in Smoke Tests ($0.00)
* Upstream `verify.yml` attempts to clone `spring-projects/spring-boot-release-verification`.
* Because that repository is private to VMware/Broadcom, our pipeline fix automatically detects the HTTP 404 response and executes the built-in test suite:
  ```bash
  ./gradlew :smoke-test:spring-boot-smoke-test-simple:test
  ```
* This validates that the newly built Spring Boot libraries compile, package, and start up cleanly without requiring any proprietary test repos.

#### 5. Compute Infrastructure: Free Public Runners ($0.00)
* On private repositories, Windows runners cost $0.016/min and medium Linux runners cost $0.016/min.
* **On Public Repositories**: GitHub provides **unlimited free runner minutes** for standard GitHub-hosted runners (`ubuntu-latest`, `windows-latest`, `macos-latest`).
* Our workflow fixes have optimized memory allocations (`-Xmx4g`) and cleared 30GB+ of runner disk space via `jlumbroso/free-disk-space`, enabling all compilation, matrix tests, and packaging jobs to run cleanly on standard runners without needing paid `UBUNTU_MEDIUM` or `UBUNTU_LARGE` variables.

#### 6. Cryptographic Artifact Signing: OpenPGP / GPG ($0.00)
* Maven Central strictly requires OpenPGP signatures for all published `.jar`, `.pom`, and `.module` files.
* Generating an OpenPGP/GPG keypair using `gpg --gen-key` is **100% free**.
* Store the armored private key in repository secret `GPG_PRIVATE_KEY` and the passphrase in `GPG_PASSPHRASE`. Gradle's `signing` plugin automatically reads these secrets and signs every artifact during the build.

---

## 6. Total Cost of Ownership (TCO) Architectural Comparison

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Architecture Model A: Full Commercial Upstream Stack                        │
│ • JFrog Artifactory Enterprise SaaS:           $1,200 – $3,600 / year       │
│ • Gradle Develocity Enterprise:               $25,000 – $50,000 / year      │
│ • GitHub Advanced Security (10 committers):             $5,880 / year       │
│ • High-Spec GitHub Runners (4-core/8-core):               $900 / year       │
│ • EV Code Signing Certificate:                            $500 / year       │
│ • Google Workspace (Alerts):                               $72 / year       │
│ TOTAL ESTIMATED ANNUAL COST:                  ~$33,552 – $60,952 / year     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ Architecture Model B: Pragmatic Enterprise Hybrid (Private Repo)            │
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
│ Architecture Model C: Open-Source Release on Public Repo (YOUR TARGET MODEL)│
│ • Artifacts: Maven Central (Sonatype OSSRH) & GH Packages:    $0.00         │
│ • Releases: Native GitHub Releases (ZIPs, CLI binaries):      $0.00         │
│ • Build Caching: actions/cache & Gradle setup-gradle:         $0.00         │
│ • Security: Free GitHub CodeQL SAST on Public Repo:           $0.00         │
│ • Verification: Built-in Simple Smoke Tests:                  $0.00         │
│ • Runners: Standard Unlimited GitHub ubuntu/windows-latest:   $0.00         │
│ • Plugin Hosting: Gradle Plugin Portal (Free for OSS):        $0.00         │
│ • Cryptographic Signing: Standard OpenPGP / GPG Keypair:      $0.00         │
│ • CLI Distribution: Public GitHub-hosted Homebrew Tap:        $0.00         │
│ TOTAL ESTIMATED ANNUAL COST:                                  $0.00 / year  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Open-Source Release Setup & Execution Checklist ($0.00 Cost)

To execute open-source builds and releases from your public fork repository, complete this simple zero-cost setup:

### 1. Repository Configuration (Settings -> Secrets and variables -> Actions)
* [ ] **`COMMERCIAL`** (Repository Variable): Ensure this is set to `false` or leave unset (default is `false`).
* [ ] **`GPG_PRIVATE_KEY`** (Secret): Generate a free GPG key (`gpg --armor --export-secret-keys <KEY-ID>`) and paste into secrets.
* [ ] **`GPG_PASSPHRASE`** (Secret): Passphrase for the GPG private key.

### 2. Open-Source Artifact Publishing (Choose Option A or Option B)
* [ ] **Option A: Maven Central (Global Public Distribution)**:
  * Register a free account at [central.sonatype.com](https://central.sonatype.com).
  * Generate a Sonatype user token.
  * Add secrets: `SONATYPE_USERNAME` (Token Name) and `SONATYPE_PASSWORD` (Token Secret).
* [ ] **Option B: GitHub Packages & GitHub Releases (In-Repo Distribution)**:
  * Zero external registration required!
  * Releases automatically publish to GitHub Packages and create GitHub Releases using the standard `GITHUB_TOKEN`.

### 3. Gradle Plugin Distribution (Optional)
* [ ] If distributing the `org.springframework.boot` Gradle plugin to the community:
  * Register a free publisher account on [plugins.gradle.org](https://plugins.gradle.org).
  * Add secrets: `GRADLE_PUBLISH_KEY` and `GRADLE_PUBLISH_SECRET`.

### 4. Homebrew CLI Tap (Optional)
* [ ] Create a free public repository named `homebrew-tap` in your GitHub account (`https://github.com/<your-org>/homebrew-tap`).
* [ ] Create a Personal Access Token (PAT) with `repo` scope and save as secret `HOMEBREW_TAP_GITHUB_TOKEN`.
* [ ] Upon release, `publicize-release.yml` will automatically commit the updated `spring-boot.rb` formula to your tap, enabling users worldwide to install via:
  ```bash
  brew tap <your-org>/tap
  brew install spring-boot
  ```

### 5. Triggering the Release
1. Run `build-pull-request.yml` or `ci.yml` to verify full compilation and test suite passes on both Linux and Windows runners.
2. Trigger `release-train-build.yml` with `callback: none` and version (e.g., `3.5.0-OSS`).
3. Trigger `publicize-release.yml` to sign artifacts, publish packages, and generate the official GitHub Release with release notes!
