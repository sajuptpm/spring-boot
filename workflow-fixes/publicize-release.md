# Workflow Documentation & Fix: `publicize-release.yml`

## 1. Overview
- **Workflow File**: [`.github/workflows/publicize-release.yml`](file:///c:/projects/spring-boot/.github/workflows/publicize-release.yml)
- **Target Repository**: [`https://github.com/sajuptpm/spring-boot`](https://github.com/sajuptpm/spring-boot)
- **Purpose**: Creates and publicizes a **General Availability (GA)** release on GitHub (e.g., `v4.2.0`, `v4.2.1`), marks it as the official `--latest` release, compiles changelog notes from GitHub issues, builds documentation, compiles and publishes the Spring Boot Gradle plugin, packages CLI binary distributions for SDKMAN!, generates Homebrew formulas, and attaches all assets directly to the GitHub Release.

---

## 2. Architecture: Original Solution vs. GitHub-Native Active Alternative

Rather than skipping stages when external proprietary credentials are not present, this workflow implements a **Dual-Mode Architecture**:

| Stage | Mode 1: Original Upstream Solution | Mode 2: GitHub-Native Best Alternative (Active Default) | Configuration / Switch |
| :--- | :--- | :--- | :--- |
| **Publish Gradle Plugin** | Uses JFrog CLI to download artifacts from Broadcom's private Artifactory and publishes to `plugins.gradle.org` using `gradle.publish.key` and `gradle.publish.secret`. | Uses Java 25 & Gradle to build `:build-plugin:spring-boot-gradle-plugin`, publishes Maven publication to **GitHub Packages** (`maven.pkg.github.com/sajuptpm/spring-boot`), uploads an Actions Artifact, and attaches plugin JARs to the GA Release. | Automatically runs Mode 2. Set `vars.PLUGIN_PUBLISH_TARGET = 'gradle-portal'` to force Mode 1. |
| **Publish to SDKMAN!** | Calls `https://vendors.sdkman.io/release` for candidate `springboot` using `SDKMAN_CONSUMER_KEY` and `SDKMAN_CONSUMER_TOKEN`. | Packages `spring-boot-cli` binary into `spring-boot-cli-<version>-bin.zip`, uploads an Actions Artifact, and attaches it directly to the GA Release (enabling `sdk install springboot <version> <url>` or direct unzip). | Automatically runs Mode 2. Set `vars.ENABLE_SDKMAN_PUBLISH = 'true'` to force Mode 1. |
| **Update Homebrew Tap** | Pushes a formula update commit directly to `spring-io/homebrew-tap` using `GH_ACTIONS_REPO_TOKEN`. | Generates a valid Homebrew formula (`spring-boot.rb`) pointing to the GitHub Release binary, uploads it as an Actions Artifact, and attaches it to the GA Release. | Automatically runs Mode 2. Set `vars.ENABLE_HOMEBREW_TAP = 'true'` to push to upstream tap. |
| **Trigger Docs Build** | Runs `gh workflow run deploy-docs.yml -r docs-build` which rsyncs via SSH to Broadcom servers and busts Cloudflare cache. | Packages documentation sources and reference modules into `spring-boot-docs-v<version>.zip`, uploads Actions Artifact, and attaches docs zip directly to the GA Release. | Automatically runs Mode 2. Set `vars.DOCS_BUILD_TARGET = 'upstream'` to force Mode 1. |
| **Create GitHub Release** | Creates release with changelog from GitHub issues using `GH_ACTIONS_REPO_TOKEN` PAT. | Uses built-in `GITHUB_TOKEN` (`contents: write`, `issues: write`), auto-generates git tag and milestone, compiles changelog, unsets prerelease flag, sets `--latest=true`, and attaches all built plugin, CLI, formula, and doc assets. | Active by default with zero token configuration required. |

---

## 3. Issues in the Fork & Changes Made

### A. Problems Identified & Resolved
1. **Skipped Stages Without Alternatives**: Previously, external publishing stages were skipped when Broadcom credentials were not configured. We replaced unconditional skips with functional GitHub-native alternatives.
2. **Missing Manual Dispatch Trigger**: Added `workflow_dispatch` with `milestone` and `latest` inputs.
3. **Hardcoded Tag Version**: The tag filter was extended to generic patterns (`v*.[0-9]+`).
4. **Java 25 Baseline**: Spring Boot 4.x requires Java 25. Configured `prepare-gradle-build` with `java-version: '25'`.
5. **Prerelease to Latest Promotion Error**: Unsets `--prerelease=false` when marking a GA release as `--latest`, preventing GitHub API `HTTP 422: Latest release cannot be draft or prerelease` errors.
6. **Token Fallback & Permissions**: Configured `contents: write`, `packages: write`, `issues: write` with fallback to `GITHUB_TOKEN`.

---

## 4. Existing Solutions & Free Alternatives Analysis

### Feature 1: Gradle Plugin Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (Gradle Plugin Portal + JFrog)** | Gradle Inc. & Broadcom | Paid / Restricted | `GRADLE_PLUGIN_PUBLISH_KEY`, `GRADLE_PLUGIN_PUBLISH_SECRET`, `JF_ARTIFACTORY_SPRING` | Publishes plugin to `plugins.gradle.org`. Restricted to official Spring Boot maintainers. |
| **Alternative 1: GitHub Packages (Maven)** *(Active)* | **GitHub** | **100% Free** | **Built-in `GITHUB_TOKEN`** | Publishes plugin to `https://maven.pkg.github.com/sajuptpm/spring-boot`. Add repo to `pluginManagement { repositories { ... } }`. |
| **Alternative 2: GitHub Releases Attachment** *(Active)* | **GitHub** | **100% Free** | **Zero Setup** | Bundles plugin `.jar`, `.pom`, `-sources.jar`, `-javadoc.jar` directly on the GitHub GA Release page. |
| **Alternative 3: Sonatype / Maven Central (OSSRH)** | Sonatype | 100% Free for OSS | Free account under verified namespace (e.g. `io.github.sajuptpm`) | Publishes plugins to Maven Central for global consumption without extra repository declarations. |

---

### Feature 2: SDKMAN! Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (SDKMAN! Vendor API)** | SDKMAN! | Restricted | `SDKMAN_CONSUMER_KEY`, `SDKMAN_CONSUMER_TOKEN` | Publishes CLI binary to `https://vendors.sdkman.io/release`. Restricted to official `springboot` candidate maintainers. |
| **Alternative 1: Direct Release Attachment & SDKMAN Install** *(Active)* | **GitHub** | **100% Free** | **Zero Setup** | Attach `spring-boot-cli-<version>-bin.zip` directly to the GitHub Release. Users can install directly via `sdk install springboot <version> <url>` or standard unzip. |
| **Alternative 2: Custom Candidate Name on SDKMAN!** | SDKMAN! | Free | Self-registered vendor key for custom candidate (e.g. `saju-springboot`). | Register a free candidate name at SDKMAN! vendor portal to distribute custom builds. |

---

### Feature 3: Homebrew Tap Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (`spring-io/homebrew-tap`)** | GitHub (Broadcom) | Restricted | `GH_ACTIONS_REPO_TOKEN` with write access to `spring-io/homebrew-tap`. | Pushes formula updates to the official `spring-io/homebrew-tap` repository. |
| **Alternative 1: Personal Homebrew Tap (`sajuptpm/homebrew-tap`)** | **GitHub** | **100% Free** | **Built-in `GITHUB_TOKEN`** | Create a free repository named `homebrew-tap` under your GitHub account (`sajuptpm/homebrew-tap`). Users install via `brew tap sajuptpm/tap && brew install spring-boot`. |
| **Alternative 2: Standalone Formula File in Release Assets** *(Active)* | **GitHub** | **100% Free** | **Zero Setup** | Attach `spring-boot.rb` directly to the GitHub Release so users can run `brew install <url-to-formula.rb>`. |

---

### Feature 4: Documentation Publishing

| Solution | Provider | Cost | Description |
| :--- | :--- | :--- | :--- |
| **Upstream Solution (`deploy-docs.yml`)** | Broadcom Infrastructure | Restricted | Rsyncs via SSH to Broadcom docs server (`DOCS_HOST`, `DOCS_SSH_KEY`). |
| **Alternative 1: Release Archive & Actions Artifact** *(Active)* | **GitHub** | **100% Free** | Packages documentation sources and reference modules into `spring-boot-docs-v<version>.zip` attached to the release. |
| **Alternative 2: GitHub Pages** | **GitHub** | **100% Free** | Deploys static HTML documentation to `https://sajuptpm.github.io/spring-boot/`. |

---

## 5. Live Test Verification

We tested and verified this workflow end-to-end via `workflow_dispatch`.

- **Workflow Name**: Publicize Release
- **Conclusion**: **SUCCESS (100% Passed — All Jobs Succeeded)**
- **GitHub GA Release Created**: [v4.2.0 (Official Latest Release)](https://github.com/sajuptpm/spring-boot/releases/tag/v4.2.0)
- **Latest Flag Confirmed**: Verified via GitHub REST API (`https://api.github.com/repos/sajuptpm/spring-boot/releases/latest`) that `v4.2.0` is the active, official `--latest` GA release.

### Verified Step Execution:
1. `Read Version`: Parsed `4.2.0` from dispatch inputs (Status: **Success**).
2. `Trigger Docs Build`: Packaged documentation and uploaded artifact `spring-boot-docs-v4.2.0` (Status: **Success**).
3. `Update Homebrew Tap`: Generated `spring-boot.rb` formula and uploaded artifact `spring-boot-homebrew-formula-v4.2.0` (Status: **Success**).
4. `Publish to SDKMAN!`: Built CLI binary distribution and uploaded artifact `spring-boot-cli-dist-v4.2.0` (Status: **Success**).
5. `Publish Gradle Plugin`: Built plugin with Java 25, deployed Maven artifacts to GitHub Packages, uploaded artifact `spring-boot-gradle-plugin-v4.2.0` (Status: **Success**).
6. `Create GitHub Release`: Promoted `v4.2.0` to official `--latest` GA release and attached all built plugin, CLI, formula, and docs assets (Status: **Success**).

---

## 6. How You Can Test It Later (Scripts & Instructions)

### Tool 1: `trigger-workflow.py`
Use this script to trigger a GA release publication on-demand:

```bash
# Publicize current version from gradle.properties
python workflow-fixes/trigger-workflow.py publicize-release.yml main

# Or specify a custom release version (e.g. 4.2.0)
python workflow-fixes/trigger-workflow.py publicize-release.yml main milestone=4.2.0,latest=true
```

---

### Tool 2: `check-runs.py`
Use this script to monitor progress:

```bash
python workflow-fixes/check-runs.py 5
```

---

### Method 3: GitHub Web UI
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions/workflows/publicize-release.yml`
2. Click **Run workflow** -> Enter milestone (e.g. `4.2.0`) -> Click **Run workflow**.

---

## 7. How to Manually Verify via the GitHub UI

### Step 1: Verify the Actions Run Summary
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions`
2. In the left navigation bar, click **Publicize Release**.
3. Click the most recent run at the top.
4. **Header Verification**: Confirms **Status: Success** with a green checkmark.
5. **Job Graph Verification**:
   - `Read Version`: **Green checkmark**.
   - `Trigger Docs Build`: **Green checkmark**.
   - `Update Homebrew Tap`: **Green checkmark**.
   - `Publish to SDKMAN!`: **Green checkmark**.
   - `Publish Gradle Plugin`: **Green checkmark**.
   - `Create GitHub Release`: **Green checkmark**.
   *(No skipped jobs!)*

### Step 2: Verify Artifacts in Actions
Scroll to the **Artifacts** section at the bottom of the run page:
- `spring-boot-gradle-plugin-v4.2.0`
- `spring-boot-docs-v4.2.0`
- `spring-boot-cli-dist-v4.2.0`
- `spring-boot-homebrew-formula-v4.2.0`

### Step 3: Verify the Generated GA Release Page
1. Navigate to: `https://github.com/sajuptpm/spring-boot/releases`
2. Click on the release `v4.2.0`.
3. Confirm the green **`Latest`** badge.
4. Expand **Assets**: verify that documentation zip, CLI distribution zip, Homebrew formula, and all Gradle plugin JARs and POMs are attached.
