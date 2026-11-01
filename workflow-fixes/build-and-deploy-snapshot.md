# Workflow Documentation & Fix: `build-and-deploy-snapshot.yml`

## 1. Overview
- **Workflow File**: [`.github/workflows/build-and-deploy-snapshot.yml`](file:///c:/projects/spring-boot/.github/workflows/build-and-deploy-snapshot.yml)
- **Target Repository**: [`https://github.com/sajuptpm/spring-boot`](https://github.com/sajuptpm/spring-boot)
- **Purpose**: Compiles Spring Boot snapshots on Linux with Java 25, runs tests, publishes artifacts locally, and deploys them.

---

## 2. Problems in the Fork & Changes Made

### A. Problems Identified
1. **Hardcoded Upstream Repository Check**: Upstream restricted execution to `spring-projects/spring-boot` and `spring-projects/spring-boot-commercial`. In a fork, this caused GitHub Actions to immediately skip the entire job.
2. **Inaccessible Private Artifactory (`https://repo.spring.io`)**: Upstream deploys directly to Spring's internal JFrog Artifactory (`repo.spring.io`). Forks do not have credentials for this server, which resulted in HTTP 401 Unauthorized errors.
3. **Private Verification Repository**: Upstream's `verify` job references `spring-projects/spring-boot-release-verification`, which is a private Broadcom/Spring repository inaccessible to public forks.
4. **Unconditional Notification Failures**: Sent a `curl` request to `${{ secrets.GOOGLE_CHAT_WEBHOOK_URL }}` even when empty.

### B. Summary of Changes Made

| Component | Upstream State | Fork State (Updated) |
| :--- | :--- | :--- |
| **Job Guard** | `if: ${{ github.repository == 'spring-projects/spring-boot' \|\| ... }}` | `if: ${{ github.repository == 'sajuptpm/spring-boot' \|\| github.repository == 'spring-projects/spring-boot' \|\| vars.ENABLE_SNAPSHOT_BUILD == 'true' }}` |
| **Job Permissions** | None at job level (`contents: read` at top level). | Added `permissions: contents: write` to allow creating GitHub Pre-Releases and uploading snapshot assets. |
| **Artifactory Deploy** | Executed unconditionally against `https://repo.spring.io`. | Only executes if `secrets.ARTIFACTORY_USERNAME` (or commercial username) is provided. Supports custom Artifactory URLs via `vars.ARTIFACTORY_DEPLOY_REPO_URL`. |
| **GitHub Release Deploy (ACTIVE)** | Did not exist. | **Added**: When Artifactory credentials are not configured, automatically packages `deployment-repository/` into `spring-boot-<version>-snapshot.zip` and publishes a GitHub Pre-Release with the ZIP attached. |
| **Workflow Artifact Upload** | Did not exist. | **Added**: Also uploads `spring-boot-<version>-snapshot.zip` as a downloadable GitHub Actions artifact (14-day retention). |
| **Google Chat Notification** | Executed unconditionally on completion. | Guarded with `steps.deploy-config.outputs.has_notification == 'true'`. |
| **Trigger Docs Build** | Executed unconditionally after build. | Guarded with `if: ${{ vars.TRIGGER_DOCS_BUILD == 'true' \|\| github.repository == 'spring-projects/spring-boot' }}`. |
| **Verify Job** | Executed unconditionally after build. | Guarded with `if: ${{ vars.ENABLE_VERIFY == 'true' \|\| github.repository == 'spring-projects/spring-boot' }}`. |

---

## 3. Existing Solutions & Free Alternatives Analysis

### A. Artifact / Snapshot Deployment (Artifactory vs. Alternatives)

| Feature | Option 1: GitHub Releases *(Active)* | Option 2: GitHub Actions Artifacts | Option 3: Free JFrog Artifactory Cloud | Option 4: GitHub Packages (Maven) |
| :--- | :--- | :--- | :--- | :--- |
| **Cost** | 100% Free | 100% Free | 100% Free Tier (up to 2GB storage, 10GB transfer/mo) | 100% Free for public repositories |
| **External Setup** | None (uses built-in `GITHUB_TOKEN`) | None (uses built-in `GITHUB_TOKEN`) | Sign up at [jfrog.com](https://jfrog.com/community/start-free/) | None (uses built-in `GITHUB_TOKEN` or PAT) |
| **Target Storage** | GitHub Repository Releases tab | GitHub Actions Run Summary | Custom `*.jfrog.io/artifactory` instance | `maven.pkg.github.com/sajuptpm/spring-boot` |
| **Direct Maven/Gradle Dependency** | No (download ZIP with all jars/poms) | No (download ZIP with all jars/poms) | **Yes** (standard Maven repository URL) | **Yes** (standard Maven repository URL with token) |
| **Retention / Expiry** | Permanent until deleted | 14 to 90 days (default 14 days) | Permanent within 2GB storage quota | Permanent within storage quota |
| **Pros** | - Zero external dependencies<br>- Permanent versioned downloads<br>- Release notes linked to commit | - Zero external dependencies<br>- Clean and automatic<br>- No git tags created | - 100% identical to upstream Spring Boot setup<br>- Direct `mvn` and Gradle dependency resolution | - Hosted natively on GitHub<br>- Supports `mvn` and Gradle dependency resolution |
| **Cons** | - Creates a git tag/release per build run<br>- Other projects cannot consume via `dependencies { ... }` block without unzipping | - Artifacts expire after 14 days<br>- Not visible on repository homepage | - Requires creating and managing an external JFrog account | - Consumer projects need a GitHub token with `read:packages` permission |

---

### B. Build Observability & Caching (Gradle Develocity vs. Alternatives)

| Solution | Provider | Cost | Tokens / Accounts Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Solution (`ge.spring.io`)** | Gradle Inc. (Hosted for Broadcom) | Paid / Private | Broadcom internal key | Private Develocity instance restricted to `spring-projects/*`. |
| **Alternative 1: GitHub-Native Job Summary & Artifacts** *(Active)* | **GitHub** | **100% Free** | **None** (Built into GitHub) | `gradle/actions/setup-gradle` automatically generates a **Job Summary** on the Actions run page with build duration, cache hits, and Gradle version. Test reports are uploaded on failure. |
| **Alternative 2: Public Gradle Build Scans (`scans.gradle.com`)** | **Gradle Inc.** | **100% Free** | **None** | Generates a free, shareable web link (e.g., `https://gradle.com/s/xyz123`) in the build log with complete task execution times and dependency trees. |
| **Alternative 3: Develocity Free Cloud / Trial** | **Gradle Inc.** | Free for eligible OSS | Requires registration at [gradle.com/develocity](https://gradle.com/develocity/) | Dedicated cloud instance (`https://<your-org>.develocity.com`) with team dashboards and private build scans. |

---

## 4. How to Use the Current Option & How to Switch

### A. Current Active Mode: GitHub Releases (Option 1)
- **Status**: **Enabled by default** in this workflow.
- **How it works**:
  1. The workflow builds all modules with Java 25.
  2. Because `ARTIFACTORY_USERNAME` is omitted, the workflow automatically packages all snapshot JARs, sources, and POMs into `spring-boot-<version>-snapshot.zip`.
  3. Uses `gh release create` to publish a **Pre-release** under `https://github.com/sajuptpm/spring-boot/releases` tagged `v<version>-build.<run_number>`.
  4. Also uploads the ZIP as a GitHub Actions run artifact for 14 days.
- **Required settings**:
  - In GitHub, go to **Settings > Actions > General > Workflow permissions**.
  - Select **Read and write permissions**.

---

### B. How to Switch to Option 3: Free JFrog Artifactory Cloud (`*.jfrog.io`)
If you want other Maven or Gradle projects to consume your Spring Boot snapshot builds directly via `repositories { maven { url '...' } }`:

1. **Sign up**: Go to [jfrog.com/community/start-free](https://jfrog.com/community/start-free/) and create a free cloud account. Your server will be `https://<your-org>.jfrog.io/artifactory`.
2. **Create Repository**:
   - In the JFrog console, navigate to **Administration > Repositories > Repositories > Add Repository > Local Repository**.
   - Select **Maven** as package type.
   - Set Repository Key to `libs-snapshot-local` (or your preferred name).
3. **Generate Identity Token**:
   - Go to your user profile in JFrog -> **Generate an Identity Token** or API Key.
4. **Configure GitHub Repository Secrets & Variables**:
   - **Secrets** (**Settings > Secrets and variables > Actions > Secrets**):
     - `ARTIFACTORY_USERNAME`: Your JFrog username / email.
     - `ARTIFACTORY_PASSWORD`: Your JFrog Identity Token or password.
   - **Variables** (**Settings > Secrets and variables > Actions > Variables**):
     - `ARTIFACTORY_DEPLOY_REPO_URL`: `https://<your-org>.jfrog.io/artifactory`
     - `ARTIFACTORY_REPOSITORY`: `libs-snapshot-local`
5. **Run Workflow**: The workflow will automatically detect `ARTIFACTORY_USERNAME` and deploy to your JFrog Artifactory using `spring-io/artifactory-deploy-action`.

---

### C. How to Switch to Option 4: GitHub Packages (Maven Registry)
GitHub Packages hosts Maven packages at `https://maven.pkg.github.com/sajuptpm/spring-boot`:

1. Configure GitHub Packages deployment credentials in Gradle `publish` block or deployment repository.
2. Pass `GITHUB_TOKEN` to authenticate uploads to `maven.pkg.github.com`.
3. Consumers add:
   ```groovy
   repositories {
       maven {
           url = uri("https://maven.pkg.github.com/sajuptpm/spring-boot")
           credentials {
               username = project.findProperty("gpr.user") ?: System.getenv("GITHUB_ACTOR")
               password = project.findProperty("gpr.key") ?: System.getenv("GITHUB_TOKEN")
           }
       }
   }
   ```

---

## 5. Complete Data Requirements (Secrets, Variables & Permissions)

### A. Repository Secrets (`secrets`)

| Secret Name | Required for Option 1 (Releases)? | Required for Option 3 (JFrog)? | Description |
| :--- | :--- | :--- | :--- |
| `ARTIFACTORY_USERNAME` | **No** (leave blank) | **Yes** | Username for your JFrog / Maven repository. |
| `ARTIFACTORY_PASSWORD` | **No** (leave blank) | **Yes** | Identity Token or password for JFrog / Maven repository. |
| `GPG_PRIVATE_KEY` | Optional | Optional | PGP private key for artifact signing. |
| `GPG_PASSPHRASE` | Optional | Optional | Passphrase for PGP private key. |
| `DEVELOCITY_ACCESS_KEY` | Optional | Optional | Access key for Gradle Develocity (`ge.spring.io` or your custom Develocity instance). |
| `GOOGLE_CHAT_WEBHOOK_URL` | Optional | Optional | Google Chat incoming webhook URL for notifications. |
| `GH_ACTIONS_REPO_TOKEN` | Optional | Optional | PAT for release verification (only if `ENABLE_VERIFY=true`). |

---

### B. Repository Variables (`vars`)

| Variable Name | Default Value | Description |
| :--- | :--- | :--- |
| `ARTIFACTORY_DEPLOY_REPO_URL` | `https://repo.spring.io` | Custom Artifactory URL (e.g. `https://<org>.jfrog.io/artifactory`). |
| `ARTIFACTORY_REPOSITORY` | `libs-snapshot-local` | Target repository name in Artifactory. |
| `ARTIFACTORY_PROJECT` | *(empty)* | Optional Artifactory project key. |
| `TRIGGER_DOCS_BUILD` | `false` | Set to `true` to trigger Antora docs build. |
| `ENABLE_VERIFY` | `false` | Set to `true` to run verification tests. |
| `UBUNTU_MEDIUM` | `ubuntu-latest` | Custom runner label for the main build job. |
| `UBUNTU_SMALL` | `ubuntu-latest` | Custom runner label for docs and verify jobs. |
| `COMMERCIAL` | `false` | Set to `true` only for commercial distribution. |

---

### C. GitHub Repository Settings
1. Go to **Settings > Actions > General > Workflow permissions**.
2. Select **Read and write permissions**.
3. Check the box **Allow GitHub Actions to create and approve pull requests**.
4. Click **Save**.

---

## 6. How to Run the Workflow

1. Trigger it manually using the provided Python utility:
   ```bash
   python workflow-fixes/trigger-workflow.py build-and-deploy-snapshot.yml main
   ```
2. Or trigger it via GitHub Web UI:
   - Go to `https://github.com/sajuptpm/spring-boot/actions/workflows/build-and-deploy-snapshot.yml`.
   - Click **Run workflow** -> Select `main` -> Click **Run workflow**.
3. Once completed, your snapshot artifacts will appear under **Releases** at `https://github.com/sajuptpm/spring-boot/releases` and under the run's **Artifacts** section.


---

## 7. How to Manually Verify via the GitHub UI

### Step 1: Verify the Actions Run Summary
1. Navigate to: `https://github.com/sajuptpm/spring-boot/actions`
2. Click **Build and Deploy Snapshot** in the left sidebar.
3. Click the most recent run (e.g., `Build and Deploy Snapshot #6`).
4. Look at the status header: confirms **Status: Success** with a green checkmark.
5. In the run summary page, scroll to the **Artifacts** section at the bottom.
6. Confirm that the `snapshot-artifacts-v4.2.0-SNAPSHOT` zip archive is listed with its file size (e.g. ~105 MB).

### Step 2: Verify the GitHub Release & Assets
1. Navigate to `https://github.com/sajuptpm/spring-boot/releases`.
2. Look for the release named `Spring Boot 4.2.0-SNAPSHOT (Build #X)` (e.g., `v4.2.0-SNAPSHOT-build.6`).
3. Confirm that it has a **`Pre-release`** badge.
4. Click to expand **Assets**:
   - Verify the published `.jar`, `.pom`, and checksum files (`.module`, `.jar.sha512`, etc.) are attached as downloadable release assets.
