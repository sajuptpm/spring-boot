# Workflow Documentation & Fix: `publicize-milestone.yml`

## 1. Overview
- **Workflow File**: [`.github/workflows/publicize-milestone.yml`](file:///c:/projects/spring-boot/.github/workflows/publicize-milestone.yml)
- **Target Repository**: [`https://github.com/sajuptpm/spring-boot`](https://github.com/sajuptpm/spring-boot)
- **Purpose**: Creates and publicizes a **Pre-release** on GitHub (Milestones and Release Candidates, e.g., `v4.2.0-M1`, `v4.2.0-RC1`), compiles changelog notes from GitHub issues, builds documentation, compiles and publishes the Spring Boot Gradle plugin, and attaches all assets directly to the GitHub Release.

---

## 2. Architecture: Original Solution vs. GitHub-Native Active Alternative

Rather than skipping stages when external proprietary credentials are not present, this workflow implements a **Dual-Mode Architecture**:

| Stage | Mode 1: Original Upstream Solution | Mode 2: GitHub-Native Best Alternative (Active Default) | Configuration / Switch |
| :--- | :--- | :--- | :--- |
| **Publish Gradle Plugin** | Uses JFrog CLI to download artifacts from Broadcom's private Artifactory and publishes to `plugins.gradle.org` using `gradle.publish.key` and `gradle.publish.secret`. | Uses Java 25 & Gradle to build `:build-plugin:spring-boot-gradle-plugin`, publishes Maven publication to **GitHub Packages** (`maven.pkg.github.com/sajuptpm/spring-boot`), uploads an Actions Artifact, and attaches plugin JARs to the GitHub Release. | Automatically runs Mode 2. Set `vars.PLUGIN_PUBLISH_TARGET = 'gradle-portal'` to force Mode 1. |
| **Trigger Docs Build** | Runs `gh workflow run deploy-docs.yml -r docs-build` which rsyncs via SSH to Broadcom servers and busts Cloudflare cache. | Packages documentation sources and reference modules into `spring-boot-docs-v<version>.zip`, uploads Actions Artifact, and attaches docs zip directly to the GitHub Release. | Automatically runs Mode 2. Set `vars.DOCS_BUILD_TARGET = 'upstream'` to force Mode 1. |
| **Create GitHub Release** | Creates release with changelog from GitHub issues using `GH_ACTIONS_REPO_TOKEN` PAT. | Uses built-in `GITHUB_TOKEN` (`contents: write`, `issues: write`), auto-generates git tag and milestone, compiles changelog, and attaches all built plugin & doc assets. | Active by default with zero token configuration required. |

---

## 3. Issues in the Fork & Changes Made

### A. Problems Identified & Resolved
1. **Skipped Stages Without Alternatives**: Upstream jobs crashed on missing private tokens. Skipping them completely left the user without built plugins or documentation. We replaced unconditional skips with functional GitHub-native alternatives.
2. **Missing Manual Dispatch Trigger**: Added `workflow_dispatch` with an optional `milestone` input.
3. **Hardcoded Tag Version**: The tag filter was extended to generic patterns (`v*-M*`, `v*-RC*`).
4. **Java 25 Baseline**: Spring Boot 4.x requires Java 25. Configured `prepare-gradle-build` with `java-version: '25'`.
5. **Composite Action Evaluation Bug in `create-github-release`**: In composite actions, string `'false'` evaluated to truthy in `if: ${{ !inputs.edit }}`. Updated action to inspect `gh release view "$TAG"` dynamically.
6. **Token Fallback & Permissions**: Configured `contents: write`, `packages: write`, `issues: write` with fallback to `GITHUB_TOKEN`.

### B. Summary of Changes Made

| Component | Upstream State | Fork State (Updated) | Reason |
| :--- | :--- | :--- | :--- |
| **Triggers (`on`)** | Only `push: tags: [v4.2.0-M*, v4.2.0-RC*]` | Added `workflow_dispatch` (with optional `milestone` input) and generic tag patterns (`v*-M*`, `v*-RC*`). | Allows testing on-demand and supports any version milestone tag. |
| **Version Reading** | Only parsed `gradle.properties`. | Accepts input `milestone` if provided, else falls back to `gradle.properties`. | Allows specifying exact milestone on manual dispatch. |
| **`publish-gradle-plugin`** | Failed on missing Artifactory & Portal keys. | **Dual Mode**: Builds plugin via Java 25, publishes to GitHub Packages, uploads artifact, attaches to Release. | Generates real, functional plugin assets with zero external setup. |
| **`trigger-docs-build`** | Dispatched to `docs-build` SSH rsync. | **Dual Mode**: Packages documentation into archive, uploads artifact, attaches to Release. | Provides downloadable reference documentation without external SSH servers. |
| **`create-github-release`** | Required pre-existing tag and milestone. | Auto-provisions git tag and milestone; downloads and attaches built plugin and docs assets. | Produces a fully populated pre-release page. |

---

## 4. Existing Solutions & Free Alternatives Analysis

### Feature 1: Gradle Plugin Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (Gradle Plugin Portal + JFrog)** | Gradle Inc. & Broadcom | Paid / Restricted | `GRADLE_PLUGIN_PUBLISH_KEY`, `GRADLE_PLUGIN_PUBLISH_SECRET`, `JF_ARTIFACTORY_SPRING` | Publishes plugin to `plugins.gradle.org`. Restricted to official Spring Boot maintainers. |
| **Alternative 1: GitHub Packages (Maven)** *(Active)* | **GitHub** | **100% Free** | **Built-in `GITHUB_TOKEN`** | Publishes plugin to `https://maven.pkg.github.com/sajuptpm/spring-boot`. Add repo to `pluginManagement { repositories { ... } }`. |
| **Alternative 2: GitHub Releases Attachment** *(Active)* | **GitHub** | **100% Free** | **Zero Setup** | Bundles plugin `.jar`, `.pom`, `-sources.jar`, `-javadoc.jar` directly on the GitHub Pre-release page. |
| **Alternative 3: Sonatype / Maven Central (OSSRH)** | Sonatype | 100% Free for OSS | Free account under verified namespace (e.g. `io.github.sajuptpm`) | Publishes plugins to Maven Central for global consumption without extra repository declarations. |

---

### Feature 2: Documentation Publishing

| Solution | Provider | Cost | Description |
| :--- | :--- | :--- | :--- |
| **Upstream Solution (`deploy-docs.yml`)** | Broadcom Infrastructure | Restricted | Rsyncs via SSH to Broadcom docs server (`DOCS_HOST`, `DOCS_SSH_KEY`). |
| **Alternative 1: Release Archive & Actions Artifact** *(Active)* | **GitHub** | **100% Free** | Packages documentation sources and reference modules into `spring-boot-docs-v<version>.zip` attached to the release. |
| **Alternative 2: GitHub Pages** | **GitHub** | **100% Free** | Deploys static HTML documentation to `https://sajuptpm.github.io/spring-boot/`. |

---

## 5. Live Test Verification

We tested and verified this workflow end-to-end via `workflow_dispatch`.

- **Run ID**: [41314805758](https://github.com/sajuptpm/spring-boot/actions/runs/41314805758)
- **Workflow Name**: Publicize Prerelease (#5)
- **Conclusion**: **SUCCESS (100% Passed — All 4 Jobs Succeeded)**
- **GitHub Release Created**: [v4.2.0-SNAPSHOT (Pre-release)](https://github.com/sajuptpm/spring-boot/releases/tag/v4.2.0-SNAPSHOT)

### Verified Job Execution:
1. `Read Version`: Parsed `4.2.0-SNAPSHOT` from `gradle.properties` (Status: **Success**).
2. `Trigger Docs Build`: Packaged documentation and uploaded artifact `spring-boot-docs-v4.2.0-SNAPSHOT` (Status: **Success**).
3. `Publish Gradle Plugin`: Built plugin with Java 25, deployed Maven artifacts to GitHub Packages, uploaded artifact `spring-boot-gradle-plugin-v4.2.0-SNAPSHOT` (Status: **Success**).
4. `Create GitHub Release`: Created pre-release and attached all built plugin JARs, POMs, and docs zip archive (Status: **Success**).

### Verified Release Assets Attached:
- `spring-boot-docs-v4.2.0-SNAPSHOT.zip` (539 KB)
- `spring-boot-gradle-plugin-4.2.0-*-javadoc.jar` (360 KB)
- `spring-boot-gradle-plugin-4.2.0-*-sources.jar` (73 KB)
- `spring-boot-gradle-plugin-4.2.0-*.jar` (159 KB)
- `spring-boot-gradle-plugin-4.2.0-*.pom` (2.8 KB)

---

## 6. How You Can Test It Later (Scripts & Instructions)

### Tool 1: `trigger-workflow.py`
Use this script to trigger a prerelease publication on-demand:

```bash
# Publicize current version from gradle.properties
python workflow-fixes/trigger-workflow.py publicize-milestone.yml main

# Or specify a custom milestone version
python workflow-fixes/trigger-workflow.py publicize-milestone.yml main milestone=4.2.0-M1
```

---

### Tool 2: `check-runs.py`
Use this script to monitor progress:

```bash
python workflow-fixes/check-runs.py 5
```

---

### Method 3: GitHub Web UI
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions/workflows/publicize-milestone.yml`
2. Click **Run workflow** -> (Optionally enter a milestone like `4.2.0-M1`) -> Click **Run workflow**.

---

## 7. How to Manually Verify via the GitHub UI

### Step 1: Verify the Actions Run Summary
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions`
2. In the left navigation bar, click **Publicize Prerelease**.
3. Click the most recent run at the top (e.g. `Publicize Prerelease #5`).
4. **Header Verification**: Confirms **Status: Success** with a green checkmark.
5. **Job Graph Verification**:
   - `Read Version`: **Green checkmark**.
   - `Trigger Docs Build`: **Green checkmark**.
   - `Publish Gradle Plugin`: **Green checkmark**.
   - `Create GitHub Release`: **Green checkmark**.
   *(No skipped jobs!)*

### Step 2: Verify Artifacts in Actions
Scroll to the **Artifacts** section at the bottom of the run page:
- `spring-boot-gradle-plugin-v4.2.0-SNAPSHOT`
- `spring-boot-docs-v4.2.0-SNAPSHOT`

### Step 3: Verify the Generated Pre-release Page
1. Navigate to: `https://github.com/sajuptpm/spring-boot/releases`
2. Click on the pre-release `v4.2.0-SNAPSHOT`.
3. Confirm the yellow/orange **`Pre-release`** badge.
4. Expand **Assets**: verify that the documentation zip and all Gradle plugin JARs and POMs are listed.

### Step 4: Verify GitHub Packages
1. Navigate to: `https://github.com/sajuptpm?tab=packages&repo_name=spring-boot`
2. Confirm the `org.springframework.boot:spring-boot-gradle-plugin` package is published.
