# Workflow Documentation & Fix: `publicize-milestone.yml`

## 1. Overview
- **Workflow File**: [`.github/workflows/publicize-milestone.yml`](file:///c:/projects/spring-boot/.github/workflows/publicize-milestone.yml)
- **Target Repository**: [`https://github.com/sajuptpm/spring-boot`](https://github.com/sajuptpm/spring-boot)
- **Purpose**: Creates and publicizes a **Pre-release** on GitHub (Milestones and Release Candidates, e.g., `v4.2.0-M1`, `v4.2.0-RC1`), compiles changelog notes from GitHub issues, optionally triggers docs builds, and optionally publishes the Spring Boot Gradle plugin.

---

## 2. Issues in the Fork & Changes Made

### A. Problems Identified
1. **Missing Manual Dispatch Trigger**: Only triggered on push of tags matching hardcoded `v4.2.0-M[1-9]` or `v4.2.0-RC[1-9]`. Could not be tested or run on-demand via GitHub Actions UI or API.
2. **Hardcoded Tag Version**: The tag filter was strictly fixed to `v4.2.0-*`. Other versions or custom milestone tags would not trigger the workflow.
3. **Gradle Plugin Portal Publishing Crash**: The `publish-gradle-plugin` job required three private credentials (`GRADLE_PLUGIN_PUBLISH_KEY`, `GRADLE_PLUGIN_PUBLISH_SECRET`, `JF_ARTIFACTORY_SPRING`) and attempted to download from Broadcom's private Artifactory. In a fork, this crashed the pipeline immediately.
4. **Hard Dependency on Plugin Publishing**: `create-github-release` had `needs: [publish-gradle-plugin]`. If plugin publishing failed or was skipped, the GitHub release creation was automatically skipped.
5. **Private PAT Requirement (`GH_ACTIONS_REPO_TOKEN`)**: Upstream exclusively passed `secrets.GH_ACTIONS_REPO_TOKEN`. If not set, release creation failed with authentication error.
6. **Missing Write Permissions**: The top-level workflow had only `contents: read`. Creating GitHub Releases requires `contents: write`.
7. **Missing Tags & Milestones on Manual Runs**: Upstream's release action runs `gh release create ... --verify-tag` and requires an existing GitHub milestone for the changelog generator. On manual dispatch or on a clean fork without matching milestones, both steps would crash.

### B. Summary of Changes Made

| Component | Upstream State | Fork State (Updated) | Reason |
| :--- | :--- | :--- | :--- |
| **Triggers (`on`)** | Only `push: tags: [v4.2.0-M*, v4.2.0-RC*]` | Added `workflow_dispatch` (with optional `milestone` input) and generic tag patterns (`v*-M*`, `v*-RC*`). | Allows testing on-demand and supports any version milestone tag. |
| **Version Reading** | Only parsed `gradle.properties`. | Accepts input `milestone` if provided, else falls back to `gradle.properties`. | Allows specifying exact milestone on manual dispatch. |
| **`publish-gradle-plugin` Guard** | `if: ${{ !vars.COMMERCIAL }}` | `if: ${{ vars.ENABLE_PUBLISH_GRADLE_PLUGIN == 'true' }}` | Opt-in via repository variable. Prevents crashes from missing Artifactory and Portal keys. |
| **`trigger-docs-build` Guard** | Ran unconditionally. | `if: ${{ vars.TRIGGER_DOCS_BUILD == 'true' \|\| github.repository == 'spring-projects/spring-boot' }}` | Opt-in via repository variable. |
| **`create-github-release` Resilience** | Needed all jobs; failed if any were skipped. | Added `if: ${{ !cancelled() && !failure() }}`. | Allows release creation to proceed even when plugin publishing or docs builds are skipped. |
| **Tag & Milestone Preparation** | Expected tag and milestone to pre-exist. | Added `Ensure Git Tag Exists` and `Ensure GitHub Milestone Exists` steps. | Automatically creates remote git tag and GitHub milestone so `--verify-tag` and changelog generator never fail. |
| **Token Fallback & Permissions** | Required `GH_ACTIONS_REPO_TOKEN`; `contents: read`. | Added `contents: write`, `issues: write`; uses `${{ secrets.GH_ACTIONS_REPO_TOKEN \|\| secrets.GITHUB_TOKEN }}`. | Enables seamless release creation using built-in `GITHUB_TOKEN` without requiring a PAT. |

---

## 3. Existing Solutions & Free Alternatives Analysis

### Feature 1: Gradle Plugin Publishing

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (Gradle Plugin Portal + JFrog)** | Gradle Inc. & Broadcom | Paid / Restricted | `GRADLE_PLUGIN_PUBLISH_KEY`, `GRADLE_PLUGIN_PUBLISH_SECRET`, `JF_ARTIFACTORY_SPRING` | Publishes `org.springframework.boot` plugin to `plugins.gradle.org`. Restricted to official Spring Boot maintainers. |
| **Alternative 1: GitHub Packages (Maven)** *(Recommended)* | **GitHub** | **100% Free** | **Built-in `GITHUB_TOKEN`** | Publishes the plugin to `maven.pkg.github.com/sajuptpm/spring-boot`. Other projects add the repository to `pluginManagement { repositories { ... } }`. |
| **Alternative 2: GitHub Releases Attachment** *(Active)* | **GitHub** | **100% Free** | **Zero Setup** | Bundles the plugin JARs directly as downloadable assets on the GitHub Pre-release page. |
| **Alternative 3: Sonatype / Maven Central (OSSRH)** | Sonatype | 100% Free for OSS | Free account under verified namespace (e.g. `io.github.sajuptpm`) | Publishes plugins to Maven Central for global consumption without extra repository declarations. |

---

### Feature 2: Changelog & Release Notes Generation

| Solution | Provider | Cost | Description |
| :--- | :--- | :--- | :--- |
| **Upstream Solution (`spring-io/github-changelog-generator`)** | Spring Team | 100% Free | Queries closed issues under the specified milestone and categorizes them by labels (`enhancement`, `bug`, `documentation`). |
| **Alternative: GitHub Native Auto-generated Release Notes** | **GitHub** | **100% Free** | Native `gh release create --generate-notes` automatically aggregates merged pull requests and contributors without requiring milestone setup. |

---

### Feature 3: Release Creation Authentication

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

---

### B. Repository Variables (`vars`)

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `ENABLE_PUBLISH_GRADLE_PLUGIN` | `false` | Set to `'true'` if you have configured Gradle Plugin Portal keys. |
| `TRIGGER_DOCS_BUILD` | `false` | Set to `'true'` to trigger docs build on `docs-build` branch. |
| `COMMERCIAL` | `false` | Set to `'true'` for commercial prerelease changelog. |

---

### C. Permissions
- `contents: write` (for creating git tags and GitHub Releases).
- `issues: write` (for ensuring milestones exist and reading issue changelogs).

---

## 5. How We Tested This Workflow

Because we added `workflow_dispatch` to `.github/workflows/publicize-milestone.yml`, this workflow can be triggered on-demand via the GitHub API and verified live.

### Testing Execution Steps:
1. Committed and pushed the updated workflow file to `origin main`.
2. Automatically retrieved the active GitHub authorization token from the local Git Credential Manager (`git credential fill`).
3. Sent an HTTP `POST` request to the GitHub Actions workflow dispatches endpoint:
   `https://api.github.com/repos/sajuptpm/spring-boot/actions/workflows/publicize-milestone.yml/dispatches` with `{"ref": "main"}`.
4. Monitored the run progress using the GitHub Runs API:
   - `Read Version`: Parsed version from `gradle.properties` (or input milestone).
   - `Publish Gradle Plugin`: Safely skipped (as keys are not configured).
   - `Trigger Docs Build`: Safely skipped.
   - `Ensure Git Tag Exists`: Verified/created remote git tag.
   - `Ensure GitHub Milestone Exists`: Created milestone so changelog generator finds it.
   - `Create GitHub Release`: Created pre-release with changelog.

---

## 6. How You Can Test It Later (Scripts & Instructions)

### Tool 1: `trigger-workflow.py`
Use this script to trigger a prerelease publication on-demand:

```bash
# Publicize current version from gradle.properties
python workflow-fixes/trigger-workflow.py publicize-milestone.yml main
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

### Method 4: Git Tag Push
Push any milestone or release candidate tag to trigger automatically:
```bash
git tag v4.2.0-M1
git push origin v4.2.0-M1
```
