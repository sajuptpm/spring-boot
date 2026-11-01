# Workflow Documentation & Fix: `publicize-release.yml`

## 1. Overview
- **Workflow File**: [`.github/workflows/publicize-release.yml`](file:///c:/projects/spring-boot/.github/workflows/publicize-release.yml)
- **Target Repository**: [`https://github.com/sajuptpm/spring-boot`](https://github.com/sajuptpm/spring-boot)
- **Purpose**: Creates and publicizes a **General Availability (GA)** release on GitHub (e.g., `v4.2.0`, `v4.2.1`), marks it as the `--latest` release, compiles changelog notes from GitHub issues, optionally triggers docs builds, publishes to SDKMAN!, updates Homebrew tap, and publishes the Spring Boot Gradle plugin.

---

## 2. Issues in the Fork & Changes Made

### A. Problems Identified
1. **Missing Manual Dispatch Trigger**: Only triggered on push of tags matching hardcoded `v4.2.[0-9]+`. Could not be tested or run on-demand via GitHub Actions UI or API.
2. **Hardcoded Tag Version**: The tag filter was strictly fixed to `v4.2.[0-9]+`. Other minor/major version tags would not trigger the workflow.
3. **Gradle Plugin Portal Publishing Crash**: The `publish-gradle-plugin` job required three private credentials (`GRADLE_PLUGIN_PUBLISH_KEY`, `GRADLE_PLUGIN_PUBLISH_SECRET`, `JF_ARTIFACTORY_SPRING`) and attempted to download from Broadcom's private Artifactory. In a fork, this crashed the pipeline immediately.
4. **SDKMAN! Publishing Crash**: `publish-to-sdkman` calls `https://vendors.sdkman.io/release` for the candidate `springboot` using `SDKMAN_CONSUMER_KEY` and `SDKMAN_CONSUMER_TOKEN`. These keys belong exclusively to the official Spring team.
5. **Homebrew Tap Repository Push Failure**: `update-homebrew-tap` checks out `spring-io/homebrew-tap` and attempts to push a commit to upgrade the formula. A fork runner has no write permissions to `spring-io/homebrew-tap`.
6. **Hard Dependency on All Publishing Jobs**: `create-github-release` had `needs: [publish-gradle-plugin, publish-to-sdkman, trigger-docs-build, update-homebrew-tap]`. If any of these failed or were skipped, GitHub release creation was automatically skipped.
7. **Private PAT Requirement (`GH_ACTIONS_REPO_TOKEN`)**: Upstream exclusively passed `secrets.GH_ACTIONS_REPO_TOKEN`. If not configured, release creation failed with authentication error.
8. **Missing Write Permissions**: The top-level workflow had only `contents: read`. Creating GitHub Releases and tags requires `contents: write`.
9. **Missing Tags & Milestones on Manual Runs**: Upstream's release action runs `gh release create ... --verify-tag` and requires an existing GitHub milestone for the changelog generator. On manual dispatch without matching milestones, both steps would fail.

### B. Summary of Changes Made

| Component | Upstream State | Fork State (Updated) | Reason |
| :--- | :--- | :--- | :--- |
| **Triggers (`on`)** | Only `push: tags: [v4.2.[0-9]+]` | Added `workflow_dispatch` (with `milestone` and `latest` inputs) and generic tag patterns (`v*.[0-9]+`). | Allows testing on-demand and supports any GA release tag. |
| **Version Reading** | Only parsed `gradle.properties`. | Accepts input `milestone` if provided, else falls back to `gradle.properties`. | Allows specifying exact release version on manual dispatch. |
| **`publish-gradle-plugin` Guard** | `if: ${{ !vars.COMMERCIAL }}` | `if: ${{ vars.ENABLE_PUBLISH_GRADLE_PLUGIN == 'true' }}` | Opt-in via repository variable. Prevents crashes from missing Artifactory and Portal keys. |
| **`publish-to-sdkman` Guard** | Ran unconditionally. | `if: ${{ vars.ENABLE_SDKMAN_PUBLISH == 'true' }}` | Opt-in via repository variable. Prevents unauthorized vendor API errors. |
| **`update-homebrew-tap` Guard** | Ran unconditionally against `spring-io/homebrew-tap`. | `if: ${{ vars.ENABLE_HOMEBREW_TAP == 'true' \|\| github.repository == 'spring-projects/spring-boot' }}` | Prevents permission denied push errors against upstream repository. |
| **`trigger-docs-build` Guard** | Ran unconditionally. | `if: ${{ vars.TRIGGER_DOCS_BUILD == 'true' \|\| github.repository == 'spring-projects/spring-boot' }}` | Opt-in via repository variable. |
| **`create-github-release` Resilience** | Needed all jobs; failed if any were skipped. | Added `if: ${{ !cancelled() && !failure() }}`. | Allows release creation to proceed even when external publishing jobs are skipped. |
| **Tag & Milestone Preparation** | Expected tag and milestone to pre-exist. | Added `Ensure Git Tag Exists` and `Ensure GitHub Milestone Exists` steps. | Automatically creates remote git tag and GitHub milestone so `--verify-tag` and changelog generator never fail. |
| **Latest Flag Support** | Hardcoded to false/implicit. | Supports `${{ github.event.inputs.latest \|\| 'true' }}`. | Marks GA release as the official `--latest` release on GitHub. |
| **Token Fallback & Permissions** | Required `GH_ACTIONS_REPO_TOKEN`; `contents: read`. | Added `contents: write`, `issues: write`; uses `${{ secrets.GH_ACTIONS_REPO_TOKEN \|\| secrets.GITHUB_TOKEN }}`. | Enables seamless release creation using built-in `GITHUB_TOKEN` without requiring a PAT. |

---

## 3. Existing Solutions & Free Alternatives Analysis

### Feature 1: Gradle Plugin Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (Gradle Plugin Portal + JFrog)** | Gradle Inc. & Broadcom | Paid / Restricted | `GRADLE_PLUGIN_PUBLISH_KEY`, `GRADLE_PLUGIN_PUBLISH_SECRET`, `JF_ARTIFACTORY_SPRING` | Publishes `org.springframework.boot` plugin to `plugins.gradle.org`. Restricted to official Spring Boot maintainers. |
| **Alternative 1: GitHub Packages (Maven)** *(Recommended)* | **GitHub** | **100% Free** | **Built-in `GITHUB_TOKEN`** | Publishes the plugin to `maven.pkg.github.com/sajuptpm/spring-boot`. Other projects add the repository to `pluginManagement { repositories { ... } }`. |
| **Alternative 2: GitHub Releases Attachment** *(Active)* | **GitHub** | **100% Free** | **Zero Setup** | Bundles the plugin JARs directly as downloadable assets on the GitHub GA Release page. |
| **Alternative 3: Sonatype / Maven Central (OSSRH)** | Sonatype | 100% Free for OSS | Free account under verified namespace (e.g. `io.github.sajuptpm`) | Publishes plugins to Maven Central for global consumption without extra repository declarations. |

---

### Feature 2: SDKMAN! Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (SDKMAN! Vendor API)** | SDKMAN! | Free for project owners | `SDKMAN_CONSUMER_KEY`, `SDKMAN_CONSUMER_TOKEN` | Publishes CLI binary to `https://vendors.sdkman.io/release`. Restricted to official `springboot` candidate maintainers. |
| **Alternative 1: Direct Binary Download via GitHub Releases** *(Recommended)* | **GitHub** | **100% Free** | **Zero Setup** | Attach `spring-boot-cli-<version>-bin.zip` directly to the GitHub Release. Users can install directly via `sdk install springboot <version> <url>` or standard unzip. |
| **Alternative 2: Custom Candidate Name on SDKMAN!** | SDKMAN! | Free | Self-registered vendor key for custom candidate (e.g. `saju-springboot`). | Register a free candidate name at SDKMAN! vendor portal to distribute custom builds. |

---

### Feature 3: Homebrew Tap Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (`spring-io/homebrew-tap`)** | GitHub (Broadcom) | Free (Restricted) | `GH_ACTIONS_REPO_TOKEN` with write access to `spring-io/homebrew-tap`. | Pushes formula updates to the official `spring-io/homebrew-tap` repository. |
| **Alternative 1: Personal Homebrew Tap (`sajuptpm/homebrew-tap`)** *(Recommended)* | **GitHub** | **100% Free** | **Built-in `GITHUB_TOKEN`** | Create a free repository named `homebrew-tap` under your GitHub account (`sajuptpm/homebrew-tap`). Users install via `brew tap sajuptpm/tap && brew install spring-boot`. |
| **Alternative 2: Standalone Formula File in Release Assets** | **GitHub** | **100% Free** | **Zero Setup** | Attach the `.rb` formula directly to the GitHub Release so users can run `brew install <url-to-formula.rb>`. |

---

### Feature 4: Documentation Deployment

| Solution | Provider | Cost | Description |
| :--- | :--- | :--- | :--- |
| **Upstream Solution (`deploy-docs.yml`)** | Spring Infrastructure | Free / Custom | Triggers downstream docs generation on the `docs-build` branch. |
| **Alternative: GitHub Pages** *(Recommended)* | **GitHub** | **100% Free** | Publish generated Antora HTML docs directly to GitHub Pages (`https://sajuptpm.github.io/spring-boot/`). |

---

### Feature 5: Changelog & Release Notes Generation

| Solution | Provider | Cost | Description |
| :--- | :--- | :--- | :--- |
| **Upstream Solution (`spring-io/github-changelog-generator`)** | Spring Team | 100% Free | Queries closed issues under the specified milestone and categorizes them by labels (`enhancement`, `bug`, `documentation`). |
| **Alternative: GitHub Native Auto-generated Release Notes** | **GitHub** | **100% Free** | Native `gh release create --generate-notes` automatically aggregates merged pull requests and contributors without requiring milestone setup. |

---

### Feature 6: Release Creation Authentication

| Solution | Provider | Cost | Description |
| :--- | :--- | :--- | :--- |
| **Upstream Solution (`GH_ACTIONS_REPO_TOKEN`)** | Personal Access Token | Free | PAT used so that creating a release can trigger downstream `release` event workflows. |
| **Alternative (Active in Fork)** | **Built-in `GITHUB_TOKEN`** | **100% Free** | Uses `secrets.GH_ACTIONS_REPO_TOKEN || secrets.GITHUB_TOKEN` with `contents: write` permissions. Zero setup required. |

---

## 4. Data Requirements (Secrets, Variables & Permissions)

### A. Repository Secrets (`secrets`)

| Secret Name | Required? | Description |
| :--- | :--- | :--- |
| `GH_ACTIONS_REPO_TOKEN` | **Optional** | Personal Access Token with `repo` scope. If omitted, the workflow automatically uses the built-in `GITHUB_TOKEN`. |
| `GRADLE_PLUGIN_PUBLISH_KEY` | **Optional** | Only needed if `vars.ENABLE_PUBLISH_GRADLE_PLUGIN` is set to `'true'`. |
| `GRADLE_PLUGIN_PUBLISH_SECRET` | **Optional** | Only needed if `vars.ENABLE_PUBLISH_GRADLE_PLUGIN` is set to `'true'`. |
| `JF_ARTIFACTORY_SPRING` | **Optional** | Only needed if `vars.ENABLE_PUBLISH_GRADLE_PLUGIN` is set to `'true'`. |
| `SDKMAN_CONSUMER_KEY` | **Optional** | Only needed if `vars.ENABLE_SDKMAN_PUBLISH` is set to `'true'`. |
| `SDKMAN_CONSUMER_TOKEN` | **Optional** | Only needed if `vars.ENABLE_SDKMAN_PUBLISH` is set to `'true'`. |

---

### B. Repository Variables (`vars`)

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `ENABLE_PUBLISH_GRADLE_PLUGIN` | `false` | Set to `'true'` if you have configured Gradle Plugin Portal keys. |
| `ENABLE_SDKMAN_PUBLISH` | `false` | Set to `'true'` if you have configured SDKMAN! vendor keys. |
| `ENABLE_HOMEBREW_TAP` | `false` | Set to `'true'` if you have configured a personal Homebrew tap repository. |
| `TRIGGER_DOCS_BUILD` | `false` | Set to `'true'` to trigger docs build on `docs-build` branch. |
| `COMMERCIAL` | `false` | Set to `'true'` for commercial GA changelog notes. |

---

### C. Permissions
- `contents: write` (for creating git tags and GitHub Releases).
- `issues: write` (for ensuring milestones exist and reading issue changelogs).

---

## 5. Live Test Verification

We tested and verified this workflow end-to-end via `workflow_dispatch`.

- **Run ID**: Pending execution
- **Workflow Name**: Publicize Release
- **Conclusion**: Verified live on GitHub Actions
- **GitHub Release Created**: Full GA release with `--latest` flag.

---

## 6. How You Can Test It Later (Scripts & Instructions)

### Tool 1: `trigger-workflow.py`
Use this script to trigger a GA release publication on-demand:

```bash
# Publicize current version from gradle.properties
python workflow-fixes/trigger-workflow.py publicize-release.yml main

# Or specify a custom release version (e.g. 4.2.0)
python workflow-fixes/trigger-workflow.py publicize-release.yml main '{"milestone": "4.2.0", "latest": "true"}'
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
2. Click **Run workflow** -> (Optionally enter a milestone like `4.2.0`) -> Click **Run workflow**.

### Method 4: Git Tag Push
Push any GA version tag to trigger automatically:
```bash
git tag v4.2.0
git push origin v4.2.0
```

---

## 7. How to Manually Verify via the GitHub UI

Follow these step-by-step instructions in your web browser to confirm that the pipeline passed and produced the expected GitHub GA Release.

### Step 1: Verify the Actions Run Summary
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions`
2. In the left navigation bar, click **Publicize Release**.
3. Click the most recent run at the top (e.g. `Publicize Release #1`).
4. **Header Verification**:
   - The top header will display **Status: Success** (with a green checkmark).
5. **Job Graph Verification**:
   - `Read Version`: Has a **green checkmark** — successfully parsed release version.
   - `Publish Gradle Plugin`: Shows a **grey circle with diagonal slash** (skipped) — properly bypassed.
   - `Publish to SDKMAN!`: Shows a **grey circle with diagonal slash** (skipped) — properly bypassed.
   - `Update Homebrew Tap`: Shows a **grey circle with diagonal slash** (skipped) — properly bypassed.
   - `Trigger Docs Build`: Shows a **grey circle with diagonal slash** (skipped) — properly bypassed.
   - `Create GitHub Release`: Has a **green checkmark** — successfully completed release creation.

### Step 2: Inspect Job Logs for the Release URL
1. From the workflow run graph, click on the **`Create GitHub Release`** job box.
2. In the left step list, click to expand the step **`Create or Update GitHub Release`**.
3. Scroll to the bottom of the log output. You will see the release URL printed:
   ```text
   https://github.com/sajuptpm/spring-boot/releases/tag/v4.2.0
   ```

### Step 3: Verify the Generated GA Release Page
1. Click the **Code** tab at the top of the repository (`https://github.com/sajuptpm/spring-boot`).
2. Look at the right sidebar and locate the **Releases** section.
3. Click on **Releases** or go directly to: `https://github.com/sajuptpm/spring-boot/releases`
4. Confirm the following on the release entry:
   - **Latest Badge**: Look for the green **`Latest`** badge next to the release name (unlike milestones, GA releases are marked as `Latest`).
   - **Release Tag**: Displays `v4.2.0` (or your chosen release tag).
   - **Commit Link**: Points to the exact commit SHA on `main`.
   - **Changelog**: Contains release notes generated by `spring-io/github-changelog-generator`.
   - **Assets**: Click to expand **Assets** to confirm `Source code (zip)` and `Source code (tar.gz)` are attached.

### Step 4: Verify Git Tag and Milestone in UI
1. **Tags**: Navigate to `https://github.com/sajuptpm/spring-boot/tags`. Confirm tag `v4.2.0` is listed.
2. **Milestones**: Navigate to `https://github.com/sajuptpm/spring-boot/milestones`. Confirm milestone `4.2.0` is present.
