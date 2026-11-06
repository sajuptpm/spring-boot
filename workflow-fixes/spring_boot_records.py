# -*- coding: utf-8 -*-
"""
Defines all 84 data rows for Spring Boot 4.1.2:
- 49 Upstream Original Tool rows (matching master_list entries 5 to 221)
- 35 Recommended Fork Alternate rows placed immediately after their respective upstream tool
Every row has exactly 44 columns matching data1.xlsx headers.
"""

COMPONENT = "Spring Boot 4.1.2"

# =========================================================================
# REUSABLE ROW GENERATORS
# =========================================================================

def make_hosted_runner(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "GitHub Actions Hosted Runner",
        "ubuntu-latest (Ubuntu 24.04 LTS)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Standard GitHub-hosted Linux compute environment provided by GitHub Actions.",
        "2 vCPU, 7 GB RAM, 14 GB SSD storage; 6-hour execution timeout per job.",
        "Free",
        "No",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only (Ephemeral Microsoft Azure VM)",
        "None",
        "Permissible",
        "Free for public open-source repositories; 2,000 free pooled minutes/mo for private repos ($0.008/min thereafter)",
        "GitHub Actions Standard Free Tier ($0.00)",
        "Free compute allocation included with public repository hosting.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited public repo concurrency (subject to GitHub standard 20 concurrent jobs account limit)",
        "20 concurrent jobs per user/org on free tier; 2 vCPU, 7 GB RAM limit per runner.",
        "None (Native GITHUB_TOKEN automatically provisioned)",
        "Yes; standard GitHub-hosted runner provides ample capacity for 5 developers on public fork.",
        "Yes; 100% free of charge on public repositories.",
        "No",
        "Provides reliable, zero-maintenance ephemeral cloud Linux compute for CI/CD automation.",
        "Accessible",
        "Yes",
        "Yes; standard hosted runners execute cleanly without any billing or configuration prerequisites.",
        "https://github.com/features/actions",
        "https://github.com/pricing",
        "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions",
        "Yes; 100% free on public repositories, highly available, and requires no external credentials.",
        "N/A (Fully suitable for open-source model)",
        "Self-hosted Linux runner, Docker container runner, GitHub Large Runners",
        "GitHub Actions Standard Hosted Runner (ubuntu-latest)",
        "$0 cost, zero maintenance overhead, native GitHub Actions integration, securely isolated ephemeral VMs.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_codeql(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "CodeQL",
        "github/codeql-action v3 (uses spring-io/github-actions/.github/workflows/codeql-analysis.yml@5caba18f0b41)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Automated semantic static analysis (SAST) security scanning for Java codebase vulnerabilities.",
        "Free for public open-source repositories; requires GitHub Advanced Security (GHAS) license for private enterprise repos.",
        "Free",
        "No",
        "GitHub Advanced Security Terms / MIT Action",
        "MIT / Terms of Service",
        "None / Permissive",
        "Permitted",
        "Cloud SaaS logs (SARIF results and vulnerability findings uploaded to GitHub Security tab)",
        "None",
        "Permissible",
        "Free on public open-source repos; GHAS enterprise add-on: ~$49/committer/month ($588/yr)",
        "GitHub Open Source Security Scanning (Free)",
        "Native security scanning integrated into GitHub repository at zero cost for public forks.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited runs on public repositories.",
        "Execution limited by hosted runner memory and job timeout (6 hours).",
        "GITHUB_TOKEN (security-events: write, actions: read, contents: read)",
        "Yes; free for public open-source repositories with full security tab integration.",
        "Yes; zero additional subscription cost on public repositories.",
        "No",
        "Automates vulnerability scanning, CVE detection, and security compliance on pull requests and commits.",
        "Accessible",
        "Yes",
        "Yes; free semantic security scanner protecting open-source release artifacts against vulnerabilities.",
        "https://codeql.github.com",
        "https://github.com/enterprise/advanced-security",
        "https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql",
        "Yes; native GitHub SAST security tool, completely free for public open-source projects.",
        "N/A (Fully suitable for open-source model)",
        "SonarQube Community Edition, Semgrep OSS, SpotBugs, Snyk Open Source",
        "GitHub CodeQL Action (github/codeql-action v3)",
        "Official GitHub security scanner, zero licensing cost for public OSS, automatic pull request alerts.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_larger_runner_4core(wf_name, wf_yml, category, purpose, evidence, ml_issue, runs_on_label):
    return [
        "GitHub Actions Larger Runner (4-core)",
        f"{runs_on_label} (4 vCPU, 16 GB RAM, 150 GB SSD)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Provides extra CPU cores and high RAM (16 GB) to avoid Gradle daemon OutOfMemoryError during heavy multi-module compilation.",
        "Requires paid GitHub Team or Enterprise organization with metered billing enabled.",
        "Paid",
        "Yes (Fails to allocate or queue on personal/unbilled forks without GitHub paid runner entitlement)",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only (Ephemeral Microsoft Azure VM)",
        "None",
        "Permissible (Commercial runner service)",
        "GitHub Actions Larger Runners: 4-core Linux is $0.016/min (~$0.96/hour); ~$324 - $432/year at expected build volume",
        "GitHub Actions Larger Runner 4-core (Pay-As-You-Go)",
        "Upstream hardcodes 4-core runner label or variable to prevent Gradle heap exhaustion.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Organization-level concurrency limits based on paid runner pool size.",
        "4 vCPU, 16 GB RAM; billable per minute at $0.016/min.",
        "None (Requires organization billing / credit card on GitHub)",
        "Conditional; requires paid organization account with billing attached ($324-$432/yr).",
        "Conditional; requires allocating dedicated cloud runner budget.",
        "Yes (If running upstream workflow with larger runner labels)",
        "Upstream Spring Boot compilation consumes >5 GB heap; 4-core runner ensures stable parallel Gradle worker threads.",
        "Blocked (Fails to allocate without paid billing)",
        "No (Can be replaced with standard runner + JVM memory bounds)",
        "No as authored; workflow crashes or hangs in queued state on standard personal forks lacking larger runner quota.",
        "https://docs.github.com/en/actions/using-github-hosted-runners/using-larger-runners/about-larger-runners",
        "https://github.com/pricing",
        "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#per-minute-rates-for-larger-runners",
        "No; requires commercial paid runner subscription which breaks out-of-the-box open-source fork builds.",
        "Hardcoded runner label fails on free GitHub forks without active payment method and runner group configuration.",
        "Standard hosted runner (ubuntu-latest) with tuned Gradle daemon heap (-Xmx4g), Linux swapfile, Self-hosted runner",
        "GitHub Actions Standard Runner (ubuntu-latest) with tuned JVM flags",
        "100% free ($0/yr), executes on all standard GitHub accounts without billing, 2 vCPU / 7 GB RAM is sufficient with proper heap bounds.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_larger_runner_4core_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "GitHub Actions Standard Runner (ubuntu-latest with Heap Bounds)",
        "ubuntu-latest (2 vCPU, 7 GB RAM, 14 GB SSD)",
        "Executes build and tests using free standard GitHub-hosted runner with tuned JVM heap limits (-Xmx4g) and swap.",
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces billable larger runner with free standard runner, configuring Gradle memory bounds to prevent OOM errors.",
        "2 vCPU, 7 GB RAM; free for public repositories.",
        "Free",
        "No",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only (Ephemeral Microsoft Azure VM)",
        "None",
        "Permissible",
        "Free ($0.00)",
        "GitHub Actions Standard Free Tier ($0.00)",
        "Eliminates $324-$432/year runner expenditure while guaranteeing 100% workflow execution on any fork.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Standard GitHub public repo concurrency (20 concurrent jobs).",
        "2 vCPU, 7 GB RAM limit per runner.",
        "None",
        "Yes; 100% free and accessible to all 5 team members on standard GitHub accounts.",
        "Yes; $0 cost for entire team.",
        "No",
        "Upstream used larger runners for speed, but standard runners handle compilation reliably when memory bounds are tuned.",
        "Accessible",
        "Yes",
        "Yes; executes cleanly on standard free GitHub infrastructure.",
        "https://github.com/features/actions",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; zero financial barrier to fork maintainers and community contributors.",
        "N/A (Fully suitable for open-source model)",
        "Self-hosted runner (VM / K8s), GitHub Larger Runner (Pay-as-you-go)",
        "GitHub Actions Standard Runner (ubuntu-latest)",
        "$0 annual cost, zero cloud VM management, universally accessible to all open-source developers.",
        orig_tool,
        "Replaces billable larger runner ($324-$432/yr) with zero-cost standard hosted runner.",
        evidence
    ]

def make_larger_runner_8core(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "GitHub Actions Larger Runner (8-core)",
        "ubuntu22-4-16 (8 vCPU, 32 GB RAM, 300 GB SSD)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Provides massive memory (32 GB RAM) and 8 vCPUs for parallel test execution across all Spring Boot modules.",
        "Requires paid GitHub Team or Enterprise organization with metered billing enabled.",
        "Paid",
        "Yes (Hardcoded label runs-on: 'ubuntu22-4-16' fails on standard forks without dedicated runner pool)",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only (Ephemeral Microsoft Azure VM)",
        "None",
        "Permissible (Commercial runner service)",
        "GitHub Actions Larger Runners: 8-core Linux is $0.032/min (~$1.92/hour); ~$346 - $800/year at test execution volume",
        "GitHub Actions Larger Runner 8-core (Pay-As-You-Go)",
        "Upstream hardcodes 8-core label to execute heavy test matrix without memory thrashing.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Organization-level pool concurrency limits.",
        "8 vCPU, 32 GB RAM; billable per minute at $0.032/min.",
        "None (Requires organization billing / credit card on GitHub)",
        "Conditional; requires paid organization account with billing attached ($346/yr).",
        "Conditional; requires dedicated cloud runner budget.",
        "Yes (If running upstream release-train-test.yml with 8-core runner)",
        "Prevents heap exhaustion during multi-project Gradle test tasks and Antora documentation rendering.",
        "Blocked (Fails to allocate without paid billing)",
        "No (Can be replaced with standard runner + test matrix sharding)",
        "No as authored; workflow immediately aborts or queues indefinitely on unpaid GitHub forks.",
        "https://docs.github.com/en/actions/using-github-hosted-runners/using-larger-runners/about-larger-runners",
        "https://github.com/pricing",
        "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#per-minute-rates-for-larger-runners",
        "No; proprietary hardcoded runner label requires paid enterprise subscription.",
        "Fails on free GitHub forks due to unresolvable runner label ubuntu22-4-16.",
        "Standard hosted runner (ubuntu-latest) with test sharding, Self-hosted 8-core VM, Test matrix pruning",
        "Standard Hosted Runner (ubuntu-latest) with Test Sharding & Matrix Pruning",
        "Eliminates $346/yr runner cost while executing tests in parallel across free standard runners.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_larger_runner_8core_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Standard Hosted Runner (ubuntu-latest) with Test Sharding",
        "ubuntu-latest (2 vCPU, 7 GB RAM, 14 GB SSD)",
        "Executes release integration tests on free standard runners using test sharding and pruned test matrix.",
        "Recommended Fork Alternate",
        orig_tool,
        "Splits heavy test suites into parallel standard runner jobs, eliminating $346/year billable runner cost.",
        "2 vCPU, 7 GB RAM; free for public repositories.",
        "Free",
        "No",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only (Ephemeral Microsoft Azure VM)",
        "None",
        "Permissible",
        "Free ($0.00)",
        "GitHub Actions Standard Free Tier ($0.00)",
        "Zero-cost compute execution using standard GitHub-hosted runners.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "20 concurrent jobs on free public repositories.",
        "2 vCPU, 7 GB RAM limit per runner.",
        "None",
        "Yes; free and accessible for all 5 team members.",
        "Yes; $0 cost for entire team.",
        "No",
        "Standard runners handle test execution cleanly when sharded or when testing core framework modules.",
        "Accessible",
        "Yes",
        "Yes; executes cleanly on free GitHub Actions infrastructure.",
        "https://github.com/features/actions",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; fully viable on open-source community forks.",
        "N/A (Fully suitable for open-source model)",
        "Self-hosted runner, Cloud VM, GitHub Larger Runner",
        "GitHub Actions Standard Runner (ubuntu-latest)",
        "$0 cost, zero runner maintenance, works on any standard fork out of the box.",
        orig_tool,
        "Replaces paid 8-core runner ($346/yr) with zero-cost sharded standard runners.",
        evidence
    ]

def make_gradle(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "Gradle",
        "Gradle Wrapper v8.12+ (OpenJDK 25)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Official build automation tool for Spring Boot multi-module project compilation, dependency resolution, and packaging.",
        "None (Local command-line tool executed within runner).",
        "Free",
        "No",
        "Apache-2.0",
        "Apache-2.0",
        "None / Permissive",
        "Permitted",
        "Local-only (Runs on runner; build scans disabled unless key provided)",
        "Standard Apache-2.0 notice",
        "Permissible",
        "Free Open Source ($0.00)",
        "Gradle Build Tool (Open Source)",
        "De facto standard build system for the Spring ecosystem.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited local executions.",
        "Local runner CPU and RAM constraints.",
        "None (Invoked via ./gradlew wrapper)",
        "Yes; 100% open-source Apache-2.0 license allows unrestricted commercial and internal development.",
        "Yes; $0 cost for entire team.",
        "No",
        "Primary build tool defining project dependencies, compilation tasks, test execution, and publication.",
        "Accessible",
        "Yes",
        "Yes; core build system of Spring Boot, fully open-source and functional without proprietary plugins.",
        "https://gradle.org",
        "https://gradle.org",
        "https://gradle.org",
        "Yes; standard open-source build tool used across the entire Java industry.",
        "N/A (Fully suitable for open-source model)",
        "Apache Maven (requires rewriting entire build logic)",
        "Gradle Build Tool (Gradle Wrapper v8.12+)",
        "Native project build system, zero migration cost, 100% open-source.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_develocity(wf_name, wf_yml, category, purpose, evidence, ml_issue, secret_var):
    return [
        "Develocity",
        "Develocity 2024.1+ / ge.spring.io",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Accelerates builds with remote distributed build cache, test distribution, flaky test detection, and cloud build scans.",
        "Requires active commercial subscription and valid server access key.",
        "Paid",
        "Yes (Access key DEVELOCITY_ACCESS_KEY is private to Spring team; build scan publishing fails without key)",
        "Commercial SaaS EULA",
        "Commercial SaaS EULA",
        "None (Cloud SaaS)",
        "Restricted (Commercial software license)",
        "High (Transmits build scans, dependency graphs, console logs, environment variables, and test results to ge.spring.io)",
        "None",
        "Restricted (Requires commercial license from Gradle Inc.)",
        "Commercial annual subscription based on active committer seats + dedicated server hosting (~$25,000 - $50,000+/year)",
        "Gradle Develocity Enterprise (Quote Required)",
        "Upstream Spring engineering uses ge.spring.io to optimize CI build times across the global contributor base.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Per-committer seat license model.",
        "Server-enforced concurrency and storage limits.",
        secret_var,
        "No; proprietary commercial software requiring expensive enterprise quote ($25K-$50K/yr).",
        "No; commercially unviable for 5-member team on an open-source fork.",
        "Yes (Vendor Quote Required if retaining Develocity server connectivity)",
        "Dramatically reduces rebuild times by sharing compilation caches across all CI jobs and maintainer machines.",
        "Inaccessible (Secret missing in fork)",
        "No (Can be discarded / replaced with free local cache)",
        "No; private secret is absent in forks, resulting in missing build scans and cache misses.",
        "https://gradle.com/develocity",
        "https://gradle.com/develocity/contact/",
        "https://gradle.com/pricing/",
        "No; proprietary commercial subscription creates vendor lock-in and transmits internal build telemetry to external SaaS.",
        "Requires expensive annual contract ($25K-$50K/yr) and private access key inaccessible to fork maintainers.",
        "Standard Gradle local build cache, GitHub Actions Cache (actions/cache / gradle/actions/setup-gradle), BuildBuddy OSS",
        "Gradle Local Build Cache & GitHub Actions Cache (gradle/actions/setup-gradle@v6.4.0)",
        "100% free ($0/yr), zero external telemetry exfiltration, caches dependencies and outputs reliably in GitHub Actions.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_develocity_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Gradle Local Cache & GitHub Actions Cache (setup-gradle)",
        "gradle/actions/setup-gradle@v6.4.0 (cache-provider: basic)",
        "Provides fast build caching using standard Gradle local build cache and native GitHub Actions cache storage.",
        "Recommended Fork Alternate",
        orig_tool,
        "Eliminates dependency on commercial Develocity server while preserving fast CI incremental builds and dependency caching.",
        "10 GB default GitHub Actions cache quota per repository.",
        "Free",
        "No",
        "Apache-2.0",
        "Apache-2.0",
        "None / Permissive",
        "Permitted",
        "Local-only (Cache archives stored securely within GitHub Actions storage; zero external telemetry)",
        "Standard Apache-2.0 notice",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Replaces $25,000-$50,000/year commercial SaaS with free, built-in GitHub Actions caching.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited within GitHub Actions repository quota.",
        "10 GB repository cache size limit.",
        "None (Zero secrets required)",
        "Yes; fully open-source Apache-2.0 action with unlimited team usage.",
        "Yes; $0 cost for entire team.",
        "No",
        "Standard Gradle build cache provides ~80% of Develocity speedup for single-repo forks without external server costs.",
        "Accessible",
        "Yes",
        "Yes; guarantees 100% reliable local caching on any fork.",
        "https://github.com/gradle/actions/tree/main/setup-gradle",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; completely open-source, vendor-neutral, and requires zero external credentials.",
        "N/A (Fully suitable for open-source model)",
        "actions/cache@v4, Local ~/.gradle directory caching",
        "gradle/actions/setup-gradle@v6.4.0",
        "Official Gradle GitHub Action, automated dependency and wrapper caching, zero configuration needed.",
        orig_tool,
        "Replaces paid Develocity ($25K-$50K/yr) with zero-cost GitHub Actions cache.",
        evidence
    ]

def make_spring_enterprise(wf_name, wf_yml, category, purpose, evidence, ml_issue, secret_var):
    return [
        "Spring Enterprise",
        "Broadcom VMware Tanzu Spring Enterprise Subscription",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Provides commercial enterprise support, extended maintenance releases, proprietary CVE backports, and enterprise repositories.",
        "Requires active enterprise contract with Broadcom VMware Tanzu.",
        "Paid",
        "Yes (Requires active Broadcom Tanzu commercial contract; commercial Maven repos require private credentials)",
        "Commercial SaaS EULA",
        "Commercial SaaS EULA",
        "Restricted (Proprietary Broadcom commercial distribution terms)",
        "Restricted (Proprietary enterprise binaries cannot be redistributed commercially without Broadcom agreement)",
        "High (Builds connect to proprietary Tanzu Maven repos; commercial telemetry enabled)",
        "None",
        "Restricted (Commercial enterprise assets cannot be redistributed in public fork releases)",
        "Annual enterprise core-based subscription (~$50,000 - $200,000+/year based on managed CPU cores)",
        "Broadcom Tanzu Spring Enterprise Subscription (Quote Required)",
        "Upstream toggles vars.COMMERCIAL to true to produce commercial binaries for paying VMware Tanzu customers.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Core-based enterprise licensing.",
        "Restricted to licensed organizations.",
        secret_var,
        "No; requires enterprise master services agreement with Broadcom Inc. ($50K-$200K/yr).",
        "No; commercially unviable for 5-member team maintaining an open-source fork.",
        "Yes (Vendor Quote Required if commercial Tanzu support and repositories are mandated)",
        "Enables dual-track release engineering: free OSS builds vs commercial Tanzu enterprise distribution.",
        "Inaccessible (Requires Broadcom Tanzu contract)",
        "No (Can be discarded; fork maintains standard open-source releases)",
        "No; commercial mode fails on forks lacking Broadcom repository credentials and commercial tokens.",
        "https://tanzu.vmware.com/spring-enterprise",
        "https://tanzu.vmware.com/spring-enterprise",
        "https://tanzu.vmware.com/pricing",
        "No; commercial proprietary distribution model conflicts with open-source fork permissible release requirements.",
        "Proprietary subscription ($50K-$200K/yr) with non-redistributable commercial binaries.",
        "Community Open Source Release Model, Customer-maintained patch stream, AlmaLinux/Rocky-style rebuilds",
        "Community Open Source Release Model (Standard Apache-2.0 Spring Boot)",
        "100% open-source Apache-2.0, $0 license cost, full freedom to patch, build, and distribute customer releases.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_spring_enterprise_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Community Open Source Release Model & Public Patch Stream",
        "Standard Apache-2.0 Spring Boot Framework",
        "Builds and publishes 100% open-source Spring Boot releases under standard Apache-2.0 terms without commercial lock-in.",
        "Recommended Fork Alternate",
        orig_tool,
        "Eliminates proprietary Broadcom enterprise dependency, maintaining a clean open-source fork with full redistribution rights.",
        "None (Standard open-source model).",
        "Free",
        "No",
        "Apache-2.0",
        "Apache-2.0",
        "None / Permissive",
        "Permitted (Full commercial redistribution rights under Apache-2.0)",
        "Local-only (Zero external commercial telemetry)",
        "Standard Apache-2.0 notice",
        "Permissible",
        "Free Open Source ($0.00)",
        "Free Open Source ($0.00)",
        "Saves $50,000-$200,000/year while granting legal certainty and full freedom to distribute fork binaries.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Unlimited.",
        "None (vars.COMMERCIAL set to false or omitted)",
        "Yes; standard Apache-2.0 license grants full rights to 5-member team and downstream customers.",
        "Yes; $0 cost for entire team.",
        "No",
        "Fork operates on standard open-source principles; customer receives tested, verified community patches.",
        "Accessible",
        "Yes",
        "Yes; guarantees 100% permissible distribution of fork release artifacts.",
        "https://github.com/spring-projects/spring-boot",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; the natural open-source model intended for community forks.",
        "N/A (Fully suitable for open-source model)",
        "Self-managed security backports, Open-source CVE patch stream",
        "Community Open Source Release Model",
        "$0 cost, 100% legal compliance under Apache-2.0, zero external vendor contract dependencies.",
        orig_tool,
        "Replaces proprietary Broadcom Tanzu ($50K-$200K/yr) with standard open-source Apache-2.0 release model.",
        evidence
    ]

def make_jfrog_artifactory(wf_name, wf_yml, category, purpose, evidence, ml_issue, secret_var):
    return [
        "JFrog Artifactory",
        "repo.spring.io (JFrog Artifactory Cloud Enterprise)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Central Maven repository server used by Spring team to host snapshots (libs-snapshot-local) and stage releases.",
        "Requires commercial SaaS subscription and repository write credentials.",
        "Paid",
        "Yes (Write credentials ARTIFACTORY_USERNAME / ARTIFACTORY_PASSWORD are private to Spring project)",
        "Commercial SaaS EULA",
        "Commercial SaaS EULA",
        "None (Distribution registry)",
        "Permitted (Registry service)",
        "Cloud SaaS logs (Artifact metadata, build info, and downloader IP logs stored in JFrog cloud)",
        "None",
        "Permissible (Commercial registry service)",
        "JFrog Cloud Pro: ~$98 - $150/month ($1,176 - $1,800/year); JFrog Enterprise X: ~$500 - $3,000/month ($6,000 - $36,000/year)",
        "JFrog Artifactory Cloud Pro ($1,800/yr)",
        "Upstream Spring infrastructure relies on repo.spring.io as its central artifact hub.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Per-account or usage tier based on storage and data transfer.",
        "Storage and transfer quotas based on paid tier.",
        secret_var,
        "Conditional; requires purchasing a commercial JFrog Cloud plan ($1,800/yr).",
        "Conditional; requires dedicated software tooling budget.",
        "Yes (Purchase Order Required if dedicated Artifactory SaaS is selected)",
        "Centralizes staging, snapshot hosting, and promotion workflows across the entire Spring ecosystem.",
        "Inaccessible (Secret missing in fork)",
        "No (Can be replaced with GitHub Packages or Maven Central)",
        "No; deploy steps fail immediately due to missing HTTP Basic authentication credentials for repo.spring.io.",
        "https://jfrog.com/artifactory",
        "https://jfrog.com/pricing/",
        "https://jfrog.com/pricing/",
        "No; proprietary commercial SaaS registry is unnecessary for a standalone fork.",
        "Costs $1,800+/year and requires managing external repository credentials.",
        "GitHub Packages (ghcr.io/maven), Sonatype Central Portal (Maven Central), Nexus OSS, Local Maven directory",
        "GitHub Packages & GitHub Releases",
        "$0 cost, native GitHub authentication via GITHUB_TOKEN, seamless release hosting for fork consumers.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_jfrog_artifactory_alt(orig_tool, wf_name, wf_yml, category, evidence, repo_target):
    return [
        "GitHub Packages / GitHub Releases / Maven Central",
        "GitHub Packages Maven Registry & GitHub Releases",
        f"Hosts {repo_target} using native GitHub Packages or GitHub Releases at $0 incremental cost.",
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces proprietary JFrog Artifactory SaaS with free native GitHub artifact hosting and Maven Central publication.",
        "Public repositories: unlimited storage and data transfer; Private repositories: 500 MB storage free.",
        "Free",
        "No",
        "GitHub Terms of Service / Apache-2.0",
        "Terms of Service / Apache-2.0",
        "None / Permissive",
        "Permitted",
        "Low (Standard GitHub registry metadata; zero third-party telemetry)",
        "None",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Eliminates $1,800/year JFrog subscription while maintaining fully automated artifact publishing.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited for public repositories.",
        "Unlimited bandwidth on public GitHub Packages.",
        "GITHUB_TOKEN (Built-in) or OSSRH credentials for Maven Central",
        "Yes; completely free and native for all 5 team members.",
        "Yes; $0 cost for entire team.",
        "No",
        "GitHub Packages is natively integrated with GitHub Actions and requires zero external credentials.",
        "Accessible",
        "Yes",
        "Yes; provides clean, accessible artifact distribution for downstream fork consumers.",
        "https://github.com/features/packages",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; standard modern artifact hosting for open-source GitHub projects.",
        "N/A (Fully suitable for open-source model)",
        "Sonatype Nexus OSS (self-hosted), Cloudsmith, GitLab Package Registry",
        "GitHub Packages & GitHub Releases",
        "$0 cost, zero maintenance overhead, built-in GITHUB_TOKEN authentication, highly available global CDN.",
        orig_tool,
        "Replaces paid JFrog Artifactory ($1,800/yr) with zero-cost GitHub Packages/Releases.",
        evidence
    ]

def make_spring_release_train(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "Spring Release Train",
        "spring-io/release-train (Multi-Repo Coordination System)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Orchestrates synchronized multi-project release train across all Spring ecosystem projects (Framework, Boot, Data, Security, etc.).",
        "Requires participant membership in Spring I/O release train and write access to spring-io/release-train repo.",
        "Free (Internal to Spring)",
        "Yes (External private/restricted repository spring-io/release-train; token requires org write permissions)",
        "Apache-2.0 / Proprietary Orchestrator",
        "Proprietary / Apache-2.0",
        "None / Permissive",
        "Permitted",
        "Cloud SaaS logs (Workflow dispatches and issue state updates logged on spring-io/release-train)",
        "None",
        "Restricted (Cross-repository orchestration requires Broadcom/Spring organization tokens)",
        "Included in Spring ecosystem maintainer infrastructure (Not sold commercially)",
        "Spring Release Train Infrastructure (Inaccessible)",
        "Upstream uses release train to ensure all 20+ Spring projects release compatible versions simultaneously.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Restricted to official Spring portfolio maintainers.",
        "Synchronous coordinated releases.",
        "secrets.RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN",
        "No; cannot be licensed or joined by external organizations.",
        "No; inaccessible outside official Spring team.",
        "No (Cannot be purchased)",
        "Coordinates version alignments, staging repo handoffs, and release readiness across multiple independent repositories.",
        "Inaccessible (Secret missing and external repo inaccessible)",
        "No (Can be discarded / replaced with independent release dispatch)",
        "No; cross-repo dispatch to spring-io/release-train fails immediately due to missing participant token.",
        "https://github.com/spring-io/release-train",
        "N/A (Internal Infrastructure)",
        "N/A (Internal Infrastructure)",
        "No; a customer fork releases Spring Boot independently and does not participate in upstream release train dispatches.",
        "Fails on fork without private token; external repo spring-io/release-train rejects external dispatches.",
        "Independent standalone release process, GitHub Actions workflow_dispatch trigger, Semantic-release",
        "Standalone Independent Fork Release Process (workflow_dispatch)",
        "$0 cost, decouples fork from external ecosystem releases, enables on-demand customer patch releases.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_spring_release_train_alt(orig_tool, wf_name, wf_yml, category, evidence, alt_name, alt_desc):
    return [
        alt_name,
        "Native GitHub Actions workflow_dispatch / Manual Release CLI",
        alt_desc,
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces external multi-repo orchestrator with a self-contained, independent release workflow for the fork.",
        "None (Local fork execution).",
        "Free",
        "No",
        "MIT / Apache-2.0",
        "MIT / Apache-2.0",
        "None / Permissive",
        "Permitted",
        "Local-only (Zero external cross-repo calls)",
        "None",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Enables full independence from upstream VMware/Broadcom release schedule at $0 cost.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Unlimited.",
        "None (Standard GITHUB_TOKEN)",
        "Yes; simple, autonomous release workflow for 5-member team.",
        "Yes; $0 cost for entire team.",
        "No",
        "Fork releases customer patches on demand without waiting for or coordinating with other Spring portfolio projects.",
        "Accessible",
        "Yes",
        "Yes; guarantees 100% reliable release execution within the fork.",
        "https://github.com/features/actions",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; clean, self-contained open-source release model.",
        "N/A (Fully suitable for open-source model)",
        "Automated GitHub Release script, JReleaser, Maven Release Plugin",
        alt_name,
        "$0 cost, eliminates external network dependencies, grants full autonomy to fork release engineers.",
        orig_tool,
        "Replaces inaccessible external release train with independent fork release process.",
        evidence
    ]

def make_github_api(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "GitHub API",
        "GitHub REST / GraphQL API via gh CLI v2.x",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Used by gh CLI steps to query release train state, trigger remote workflows, and watch job execution.",
        "GitHub API rate limits: 1,000 requests/hour for GITHUB_TOKEN; 5,000 requests/hour for PAT.",
        "Free",
        "Yes (Requires write permissions to external repository spring-io/release-train)",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Cloud SaaS logs (API calls logged by GitHub platform)",
        "None",
        "Permissible",
        "Free with GitHub account",
        "GitHub Standard API (Free)",
        "Standard CLI mechanism for interacting with GitHub Actions workflows remotely.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Subject to standard GitHub API hourly rate limits.",
        "1,000 requests/hr per repository GITHUB_TOKEN; 5,000 requests/hr for authenticated PAT.",
        "secrets.RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN",
        "Yes; standard GitHub API is available to all users.",
        "Yes; $0 cost for entire team.",
        "No",
        "Automates cross-repository dispatching and run watching via gh run watch.",
        "Inaccessible (Missing token with write scope to external repo)",
        "No (Can be discarded alongside release train workflows)",
        "No; API calls target spring-io/release-train which denies permission to fork tokens.",
        "https://cli.github.com",
        "https://github.com/cli/cli",
        "https://docs.github.com/en/rest",
        "No as configured; hardcoded external repository targets cause API 404/403 errors.",
        "Targets external spring-io/release-train repo which is read-only or inaccessible to forks.",
        "Fork-local gh CLI commands, Native GITHUB_TOKEN, Discarding release-train workflow",
        "Native GITHUB_TOKEN & Standard GitHub CLI",
        "Operates strictly within the local fork repository without cross-repo authorization hurdles.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_github_api_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Native GITHUB_TOKEN & Standard GitHub CLI",
        "gh CLI v2.x / GitHub Actions Environment",
        "Executes necessary GitHub API operations locally within the fork using built-in GITHUB_TOKEN.",
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces cross-repo API calls with safe, local repository automation.",
        "1,000 requests/hour default repository GITHUB_TOKEN quota.",
        "Free",
        "No",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only",
        "None",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Zero-cost native platform automation.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Standard GitHub API rate limits.",
        "GITHUB_TOKEN (Built-in)",
        "Yes; built-in token works automatically for all team members.",
        "Yes; $0 cost for entire team.",
        "No",
        "Local API interactions suffice for tagging, creating releases, and uploading assets.",
        "Accessible",
        "Yes",
        "Yes; fully functional within any fork.",
        "https://cli.github.com",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; standard platform mechanism for open-source repositories.",
        "N/A (Fully suitable for open-source model)",
        "Git CLI commands, GitHub REST API",
        "Native GITHUB_TOKEN & Standard GitHub CLI",
        "$0 cost, zero secrets setup, scoped strictly to the fork repository.",
        orig_tool,
        "Replaces external cross-repo API calls with native fork-local automation.",
        evidence
    ]

def make_broadcom_rvt(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "Broadcom RVT upstream",
        "spring-projects/spring-boot-release-verification (Private RVT Repo)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Clones proprietary release verification test suite to validate staged Maven artifacts against enterprise application servers.",
        "Requires access to private repository spring-projects/spring-boot-release-verification.",
        "Paid (Included in Tanzu)",
        "Yes (Private proprietary repository spring-projects/spring-boot-release-verification is inaccessible to public forks)",
        "Proprietary Closed Source",
        "Proprietary",
        "Restricted (Proprietary test code)",
        "Restricted (Broadcom proprietary assets cannot be copied or redistributed)",
        "Local-only (Runs on runner; validates against commercial and open-source repos)",
        "None",
        "Restricted (Proprietary Broadcom asset; inaccessible and non-distributable)",
        "Included in Broadcom Tanzu commercial agreements (Not sold standalone)",
        "Broadcom RVT Suite (Inaccessible)",
        "Upstream uses RVT as the final quality gate before publishing enterprise Spring Boot releases.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Restricted to Broadcom engineers.",
        "Private repository access restricted by GitHub organization IAM.",
        "secrets.GH_ACTIONS_REPO_TOKEN / secrets.token",
        "No; proprietary closed-source repository that cannot be licensed by outside teams.",
        "No; inaccessible outside Broadcom.",
        "No (Cannot be purchased standalone)",
        "Validates compatibility with commercial application servers (WebLogic, WebSphere, Tanzu) prior to GA release.",
        "Inaccessible (Private repo 404 on checkout)",
        "No (Can be replaced with open-source smoke tests)",
        "No; actions/checkout fails with HTTP 404/Authentication error when cloning spring-projects/spring-boot-release-verification.",
        "https://github.com/spring-projects/spring-boot-release-verification",
        "N/A (Proprietary Closed Source)",
        "N/A (Proprietary Closed Source)",
        "No; closed-source proprietary repository completely unavailable to community forks.",
        "Private repository cannot be cloned by public forks; blocks workflow with fatal checkout error.",
        "Customer-owned smoke and integration test suite, Spring Boot Sample Apps, Testcontainers integration suite",
        "Customer Acceptance & Smoke Test Suite",
        "100% open-source, tailored to customer's actual runtime environments, zero proprietary blockers.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_broadcom_rvt_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Customer Acceptance & Smoke Test Suite",
        "Spring Boot Starter Smoke Tests & Sample Applications",
        "Validates staged artifacts against realistic open-source sample applications and embedded containers.",
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces proprietary closed-source Broadcom test repository with a transparent, customer-owned smoke test suite.",
        "None (Local runner execution).",
        "Free",
        "No",
        "Apache-2.0",
        "Apache-2.0",
        "None / Permissive",
        "Permitted",
        "Local-only",
        "Standard Apache-2.0 notice",
        "Permissible",
        "Free Open Source ($0.00)",
        "Free Open Source ($0.00)",
        "Eliminates dependency on inaccessible private repository while providing comprehensive verification.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Unlimited.",
        "None",
        "Yes; fully open-source and maintainable by 5-member team.",
        "Yes; $0 cost for entire team.",
        "No",
        "Customer smoke tests verify the specific starters, databases, and features required for customer deployments.",
        "Accessible",
        "Yes",
        "Yes; executes reliably on any fork without external dependencies.",
        "https://github.com/spring-projects/spring-boot/tree/main/spring-boot-tests",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; fully transparent, open-source verification suite.",
        "N/A (Fully suitable for open-source model)",
        "In-repo spring-boot-smoke-tests, Testcontainers integration suite",
        "Customer Acceptance & Smoke Test Suite",
        "$0 cost, 100% open-source, directly validates actual customer use cases without external blockers.",
        orig_tool,
        "Replaces inaccessible proprietary Broadcom RVT repository with transparent customer smoke tests.",
        evidence
    ]

def make_google_chat(wf_name, wf_yml, category, purpose, evidence, ml_issue, secret_var):
    return [
        "Google Chat",
        "Google Chat Webhook API (Google Workspace)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Sends real-time build and deployment status notifications (success/failure) to Spring engineering Google Chat spaces.",
        "Requires Google Workspace subscription and configured webhook URL.",
        "Paid",
        "Yes (Webhook secret GOOGLE_CHAT_WEBHOOK_URL is private to Spring team)",
        "Google APIs Terms of Service",
        "Commercial SaaS EULA",
        "None (Communication SaaS)",
        "Permitted",
        "Cloud SaaS logs (Build metadata, branch names, and run links sent to Google servers)",
        "None",
        "Permissible (Commercial alerting service)",
        "Google Workspace Business Standard: ~$12/user/month (~$144 - $168/year per user)",
        "Google Workspace Business ($168/yr)",
        "Upstream Spring team uses Google Chat as their primary internal developer collaboration platform.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Per-seat Google Workspace license.",
        "Webhook rate limits enforced by Google Workspace API.",
        "secrets.GOOGLE_CHAT_WEBHOOK_URL",
        "Conditional; requires active Google Workspace subscription ($168/yr).",
        "Conditional; requires team chat tooling budget.",
        "No (Can be replaced with free GitHub native notifications)",
        "Provides immediate developer visibility when scheduled snapshot builds or CI pipelines fail.",
        "Inaccessible (Secret missing in fork)",
        "No (Can be discarded / replaced with native summaries)",
        "No; webhook notification step fails or is skipped when secret is missing.",
        "https://workspace.google.com/products/chat/",
        "https://workspace.google.com/pricing/",
        "https://workspace.google.com/pricing/",
        "No; proprietary team webhook creates unnecessary SaaS dependency and fails when secret is omitted.",
        "Requires paid Google Workspace subscription and private incoming webhook URL.",
        "GitHub Step Summary ($GITHUB_STEP_SUMMARY), Native GitHub email notifications, Slack free webhook, Microsoft Teams",
        "GitHub Actions Native Workflow Run Summaries & PR Annotations",
        "100% free ($0/yr), built directly into GitHub Actions UI, zero third-party data transmission.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_google_chat_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "GitHub Actions Native Workflow Run Summaries & Annotations",
        "GitHub Step Summary ($GITHUB_STEP_SUMMARY) & Annotations API",
        "Generates rich markdown run summaries and inline pull request annotations for build and test results.",
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces proprietary external chat webhook with free, native, out-of-the-box GitHub Actions summaries.",
        "None (Local runner execution).",
        "Free",
        "No",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only (Stored in GitHub Actions job logs)",
        "None",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Zero-cost native platform notification mechanism.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Unlimited.",
        "None (GITHUB_TOKEN built-in)",
        "Yes; accessible to all 5 team members directly in GitHub UI.",
        "Yes; $0 cost for entire team.",
        "No",
        "Developers view detailed build metrics, test failures, and artifact links directly on the GitHub Actions summary page.",
        "Accessible",
        "Yes",
        "Yes; works seamlessly on all GitHub repositories.",
        "https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; standard platform mechanism for open-source repositories.",
        "N/A (Fully suitable for open-source model)",
        "GitHub Discussions notifications, Free Discord webhook, Free Slack webhook",
        "GitHub Actions Native Workflow Run Summaries & Annotations",
        "$0 cost, zero secrets setup, native markdown reporting directly in the GitHub web interface.",
        orig_tool,
        "Replaces paid Google Chat webhook ($168/yr) with native GitHub Actions markdown summaries.",
        evidence
    ]

def make_docker_hub(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "Docker Hub upstream",
        "Docker Hub Registry (docker.io anonymous pulls)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Pulls 11+ container images for database and message broker integration tests via Testcontainers.",
        "Anonymous rate limit: 100 pulls per 6 hours per IP address; easily exhausted on shared CI runners.",
        "Paid / Rate-Limited",
        "Yes (Anonymous IP pull limits trigger HTTP 429 Too Many Requests failures during concurrent CI runs)",
        "Docker Terms of Service",
        "Commercial SaaS EULA",
        "None (Container registry)",
        "Permitted",
        "Cloud SaaS logs (IP addresses and pull counts logged by Docker Inc.)",
        "None",
        "Permissible (Public container registry)",
        "Docker Team: ~$9/user/month ($108 - $216/year for 1-2 automation seats); Docker Business: ~$24/user/month ($288/year)",
        "Docker Hub Team Tier ($288/yr)",
        "Upstream pulls public database images directly from docker.io without authentication in open-source builds.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Per-IP rate limit: 100 pulls / 6 hours on anonymous; 200 pulls / 6 hours on personal free auth; unlimited on Team.",
        "100 pulls per 6 hours without authentication.",
        "None in upstream (Anonymous IP throttle)",
        "Conditional; anonymous pulls fail intermittently on shared runners; requires Team subscription or auth ($288/yr).",
        "Conditional; requires container registry tooling budget.",
        "Yes (Purchase Order Required if Docker Hub Team tier is purchased for rate limit exemption)",
        "Provides official verified container images for PostgreSQL, MySQL, MariaDB, Oracle, MongoDB, Redis, Kafka, etc.",
        "Blocked (Intermittent HTTP 429 rate limit failures)",
        "No (Can be replaced with GHCR mirror or authenticated free service account)",
        "No; anonymous pull limits cause unpredictable CI test failures when multiple jobs run on shared runner IPs.",
        "https://hub.docker.com",
        "https://www.docker.com/pricing/",
        "https://www.docker.com/pricing/",
        "No as anonymous; rate limits introduce non-deterministic failures on community pull requests.",
        "Anonymous IP throttling breaks builds when Testcontainers pulls dozens of database images.",
        "GitHub Container Registry (ghcr.io) mirror, Free authenticated Docker Hub account, Harbor OSS registry mirror",
        "GitHub Container Registry (GHCR) Mirror / Docker Hub Free Auth",
        "Free authenticated Docker Hub account or GHCR mirror eliminates rate limit errors at $0 cost.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_docker_hub_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "GitHub Container Registry (GHCR) Mirror / Docker Hub Free Auth",
        "GHCR (ghcr.io) / Free Docker Hub Service Account",
        "Pulls test containers via authenticated Docker Hub credentials or GitHub Container Registry mirror to bypass rate limits.",
        "Recommended Fork Alternate",
        orig_tool,
        "Eliminates anonymous Docker Hub IP pull limits, preventing HTTP 429 errors during system integration tests.",
        "Free authenticated Docker account provides 200 pulls / 6 hours; GHCR provides unlimited pulls for public images.",
        "Free",
        "No",
        "GitHub Terms of Service / Docker Terms",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only",
        "None",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Bypasses Docker rate limits without purchasing commercial Docker Team licenses ($288/yr).",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited with GHCR mirror.",
        "200 pulls / 6 hrs on free Docker Hub; unlimited on GHCR.",
        "GITHUB_TOKEN or free DOCKER_USERNAME/DOCKER_PASSWORD",
        "Yes; free solution that guarantees reliable builds for all 5 team members.",
        "Yes; $0 cost for entire team.",
        "No",
        "Provides 100% reliable image pulling for all 11+ Testcontainers database fixtures.",
        "Accessible",
        "Yes",
        "Yes; prevents intermittent rate limit build failures.",
        "https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; robust, zero-cost architecture for open-source CI pipelines.",
        "N/A (Fully suitable for open-source model)",
        "Testcontainers Cloud, Harbor OSS, AWS ECR Public",
        "GitHub Container Registry (GHCR) Mirror / Docker Hub Free Auth",
        "$0 cost, eliminates build-flakiness caused by rate limits, fully integrated with GitHub Actions.",
        orig_tool,
        "Replaces rate-limited anonymous Docker Hub pulls ($288/yr paid tier) with free authenticated/GHCR pulls.",
        evidence
    ]

def make_docker_testcontainers(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "Docker/Testcontainers",
        "Testcontainers Java v1.20+ & Docker Engine 26+",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Spins up real, ephemeral Docker containers (PostgreSQL, Kafka, Redis, MongoDB, MySQL, etc.) for integration tests.",
        "Limited by runner disk space and memory.",
        "Free",
        "No",
        "MIT",
        "MIT",
        "None / Permissive",
        "Permitted",
        "Local-only (Executes containers entirely on local runner Docker daemon)",
        "Standard MIT notice",
        "Permissible",
        "Free Open Source ($0.00)",
        "Testcontainers Open Source (MIT)",
        "Industry standard for testing Java applications against real production database systems.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Local runner resource bounds.",
        "None (Communicates with local Docker socket /var/run/docker.sock)",
        "Yes; standard MIT open-source license allows full commercial and development use.",
        "Yes; $0 cost for entire team.",
        "No",
        "Ensures Spring Boot auto-configurations and starter modules work correctly against authentic services.",
        "Accessible",
        "Yes",
        "Yes; works out of the box on standard GitHub-hosted Linux runners where Docker Engine is pre-installed.",
        "https://testcontainers.com",
        "https://testcontainers.com",
        "https://testcontainers.com",
        "Yes; essential open-source integration testing technology.",
        "N/A (Fully suitable for open-source model)",
        "H2/Embedded databases (do not test authentic SQL dialect behaviors)",
        "Testcontainers Java (MIT)",
        "De facto standard, ensures 100% fidelity with production database engines, completely free.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_docs_repo(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "external spring-boot-docs repository",
        "spring-projects/spring-boot-docs (External GitHub Repository)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "External repository containing Antora site configuration and templates used to generate Spring Boot documentation.",
        "Requires cross-repository dispatch permissions.",
        "Free (External)",
        "Yes (Dispatches to external repo spring-projects/spring-boot-docs; fork cannot trigger upstream workflows)",
        "Apache-2.0",
        "Apache-2.0",
        "None / Permissive",
        "Permitted",
        "Cloud SaaS logs (Workflow dispatch events logged by GitHub platform)",
        "Standard Apache-2.0 notice",
        "Permissible",
        "Free Open Source ($0.00)",
        "External Repository Dispatch Model",
        "Upstream Spring decouples docs rendering infrastructure into a dedicated repository.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Restricted to Spring team committers.",
        "Cross-repo dispatch rate limits.",
        "secrets.SPRING_BUILDMASTER_GITHUB_TOKEN",
        "No; external repository belongs to Spring I/O and cannot be managed by external teams.",
        "No; inaccessible outside official maintainers.",
        "No (Cannot be purchased)",
        "Decouples documentation site generation and deployment from framework code repository.",
        "Inaccessible (Fails with 404/403 on fork)",
        "No (Can be replaced with in-repo docs build)",
        "No; gh workflow run fails because forks do not have write access to spring-projects/spring-boot-docs.",
        "https://github.com/spring-projects/spring-boot-docs",
        "N/A (External Open Source Repo)",
        "N/A (External Open Source Repo)",
        "No as authored; hardcoded external repository dispatch cannot be executed by downstream forks.",
        "Dispatches to spring-projects/spring-boot-docs which rejects cross-repo requests from fork tokens.",
        "In-repo Antora documentation build, GitHub Pages publication, MkDocs / Hugo static site generator",
        "In-Repo Antora Documentation Build & GitHub Pages",
        "Self-contained, builds docs directly within fork, publishes free documentation on GitHub Pages.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_docs_repo_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "In-Repo Antora Documentation Build & GitHub Pages",
        "Antora 3.x / GitHub Pages / actions/deploy-pages@v4",
        "Builds reference documentation and API guides directly in the fork and deploys to GitHub Pages.",
        "Recommended Fork Alternate",
        orig_tool,
        "Eliminates dependency on external spring-projects/spring-boot-docs repository, making docs builds 100% self-contained.",
        "1 GB site limit on GitHub Pages; 100 GB monthly bandwidth limit.",
        "Free",
        "No",
        "MPL-2.0 (Antora) / Terms of Service (GitHub Pages)",
        "MPL-2.0 / Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only",
        "Standard MPL-2.0 notice",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Zero-cost documentation generation and hosting natively on GitHub.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Standard GitHub Pages limits.",
        "GITHUB_TOKEN (pages: write, id-token: write)",
        "Yes; free, native documentation hosting for 5-member team.",
        "Yes; $0 cost for entire team.",
        "No",
        "Enables fork maintainers to publish updated documentation for customer patches without external repo dependencies.",
        "Accessible",
        "Yes",
        "Yes; fully functional within any GitHub repository.",
        "https://antora.org",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; ideal open-source architecture for documentation.",
        "N/A (Fully suitable for open-source model)",
        "Asciidoctor PDF generator, MkDocs, Docusaurus",
        "In-Repo Antora Documentation Build & GitHub Pages",
        "$0 cost, zero cross-repo dependencies, automatically publishes customer documentation on GitHub Pages.",
        orig_tool,
        "Replaces external spring-boot-docs repo with self-contained in-repo docs build and GitHub Pages.",
        evidence
    ]

def make_automation_identity(wf_name, wf_yml, category, purpose, evidence, ml_issue, secret_var):
    return [
        "automation identity",
        "Human bot account seat (SPRING_BUILDMASTER_GITHUB_TOKEN)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Dedicated GitHub user account PAT used for automated cross-repository dispatches and release operations.",
        "Requires dedicated GitHub user seat license.",
        "Paid",
        "Yes (Token SPRING_BUILDMASTER_GITHUB_TOKEN is private to Spring buildmaster account)",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Cloud SaaS logs",
        "None",
        "Permissible (Commercial platform user seat)",
        "GitHub Enterprise Cloud / Server: ~$21/user/month (~$252/year per bot seat)",
        "GitHub Enterprise User Seat ($252/yr)",
        "Upstream provisions a dedicated buildmaster bot seat to manage automated multi-repo tasks.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Single seat license.",
        "Personal access token rate limits.",
        "secrets.SPRING_BUILDMASTER_GITHUB_TOKEN",
        "Conditional; requires paying for a dedicated GitHub user seat license ($252/yr).",
        "Conditional; requires allocating a user seat for automation.",
        "Yes (Purchase Order Required if purchasing dedicated GitHub automation seat)",
        "Allows automation scripts to perform actions with elevated, centralized permissions across multiple Spring repos.",
        "Inaccessible (Secret missing in fork)",
        "No (Can be replaced with standard GITHUB_TOKEN or GitHub App)",
        "No; workflow aborts when private bot token is missing from repository secrets.",
        "https://github.com",
        "https://github.com/pricing",
        "https://github.com/pricing",
        "No; paying for a separate bot user seat is unnecessary for fork operations.",
        "Requires paying $252/yr for a GitHub user license and managing static, long-lived personal access tokens.",
        "Native repository GITHUB_TOKEN, GitHub App short-lived tokens, Deploy keys",
        "Standard GITHUB_TOKEN & GitHub App Short-Lived Tokens",
        "$0 cost, eliminates human user seat fee, provides superior security with automated secret rotation.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_automation_identity_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Standard GITHUB_TOKEN & GitHub App Short-Lived Tokens",
        "GitHub Built-in GITHUB_TOKEN / GitHub App Installation Token",
        "Authenticates repository automation tasks using free built-in tokens or short-lived GitHub App tokens.",
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces paid human bot user seat with free native repository tokens, improving security and eliminating costs.",
        "None (Standard repository token).",
        "Free",
        "No",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only",
        "None",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Saves $252/year by replacing dedicated bot seat with native GitHub Actions tokens.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Standard repository token permissions.",
        "secrets.GITHUB_TOKEN",
        "Yes; automatically available to all 5 team members at zero cost.",
        "Yes; $0 cost for entire team.",
        "No",
        "Built-in GITHUB_TOKEN has all necessary permissions to create releases, tags, and run workflows inside the fork.",
        "Accessible",
        "Yes",
        "Yes; executes automatically without manual secret provisioning.",
        "https://docs.github.com/en/actions/security-guides/automatic-token-authentication",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; the standard recommended security practice on GitHub.",
        "N/A (Fully suitable for open-source model)",
        "GitHub App with private key, Deploy keys",
        "Standard GITHUB_TOKEN",
        "$0 cost, zero maintenance, automatically provisioned and expired with each workflow job.",
        orig_tool,
        "Replaces paid bot user seat ($252/yr) with free native GITHUB_TOKEN.",
        evidence
    ]

def make_github_packages(wf_name, wf_yml, category, purpose, evidence, ml_issue):
    return [
        "GitHub Packages",
        "GitHub Packages Maven Registry",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Hosts milestone and prerelease Maven packages directly within the GitHub repository.",
        "Free storage and data transfer for public repositories.",
        "Free",
        "No",
        "GitHub Terms of Service",
        "Terms of Service",
        "None / Permissive",
        "Permitted",
        "Low (Standard package registry metadata)",
        "None",
        "Permissible",
        "Free for public open-source repositories",
        "GitHub Packages Free Tier ($0.00)",
        "Native package repository integrated directly into the GitHub organization.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited for public repositories.",
        "Standard storage limits on private repos.",
        "GITHUB_TOKEN",
        "Yes; native and free for 5-member team.",
        "Yes; $0 cost for entire team.",
        "No",
        "Publishes milestone and release candidate builds for early adopter testing.",
        "Accessible",
        "Yes",
        "Yes; fully functional on any public GitHub fork.",
        "https://github.com/features/packages",
        "https://github.com/pricing",
        "https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-packages",
        "Yes; ideal, zero-cost registry for open-source prereleases.",
        "N/A (Fully suitable for open-source model)",
        "Sonatype Central Portal, Nexus OSS, GitHub Releases",
        "GitHub Packages Maven Registry",
        "Native GitHub integration, $0 cost, zero third-party account requirements.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_code_signing(wf_name, wf_yml, category, purpose, evidence, ml_issue, secret_var):
    return [
        "code-signing service",
        "DigiCert KeyLocker / Cloud HSM EV Code Signing Service",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Cryptographically signs Java JARs, POMs, and CLI native executables to establish authentic publisher identity and meet OS security gates.",
        "Requires active commercial EV certificate subscription and cloud HSM keystore operations.",
        "Paid",
        "Yes (Requires corporate EV signing certificate and cloud hardware security module credentials)",
        "Commercial SaaS EULA",
        "Commercial SaaS EULA",
        "None (Cryptographic infrastructure)",
        "Permitted",
        "Cloud SaaS logs (Signing events and timestamps logged in certificate authority audit log)",
        "None",
        "Permissible (Commercial cryptographic service)",
        "DigiCert KeyLocker / Sectigo EV Code Signing: ~$50 - $83/month (~$600 - $996/year)",
        "DigiCert KeyLocker EV Code Signing ($996/yr)",
        "Upstream uses hardware-backed code signing to satisfy Microsoft SmartScreen and enterprise repository trust requirements.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Per-organization certificate.",
        "Annual certificate validity with cloud signing operations.",
        "secrets.KEYLOCKER_TOKEN / secrets.GPG_PRIVATE_KEY",
        "Conditional; requires purchasing commercial EV code signing certificate ($996/yr).",
        "Conditional; requires dedicated security/PKI budget.",
        "Yes (Purchase Order Required if hardware-backed EV code signing is mandated)",
        "Guarantees that distributed binaries have not been tampered with and satisfies corporate security verification.",
        "Inaccessible (Secret missing in fork)",
        "No (Can be replaced with standard GPG signing / Sigstore)",
        "No; signing step fails when commercial KeyLocker token is absent.",
        "https://www.digicert.com/signing/keylocker",
        "https://www.digicert.com/signing/keylocker",
        "https://www.digicert.com/pricing",
        "No; expensive annual commercial certificate is unnecessary for open-source fork publishing.",
        "Costs $996/yr and requires enterprise identity verification and cloud HSM setup.",
        "Standard GPG key signing, Sigstore Cosign (keyless signing), Corporate existing PKI, GitHub Releases checksums",
        "Standard GPG Key Signing & Sigstore Cosign",
        "$0 cost, standard for Maven Central and Apache releases, verifiable by all standard Java tooling.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_code_signing_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Standard GPG Key Signing & Sigstore Cosign",
        "GnuPG v2.4+ / Sigstore Cosign v2.x",
        "Signs release artifacts (JARs, POMs, checksums) using standard open-source GPG keys and Sigstore signatures.",
        "Recommended Fork Alternate",
        orig_tool,
        "Replaces commercial EV certificate subscription with industry-standard GPG signing mandated by Maven Central.",
        "None (Unlimited local signing operations).",
        "Free",
        "No",
        "GPL-3.0-or-later (GnuPG CLI) / Apache-2.0 (Sigstore)",
        "GPL-3.0-or-later / Apache-2.0",
        "None / Permissive (Tools-only; zero copyleft impact on signed Java code)",
        "Permitted",
        "Local-only (Private key stored securely in GitHub Secrets; zero third-party telemetry)",
        "None",
        "Permissible",
        "Free Open Source ($0.00)",
        "Free Open Source ($0.00)",
        "Eliminates $996/year commercial certificate fee while achieving 100% compliance with Maven Central release standards.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Unlimited.",
        "secrets.GPG_PRIVATE_KEY, secrets.GPG_PASSPHRASE",
        "Yes; free standard cryptographic tooling accessible to 5-member team.",
        "Yes; $0 cost for entire team.",
        "No",
        "GPG signatures (.asc) are the universal standard for verifying Java releases on Maven Central.",
        "Accessible",
        "Yes",
        "Yes; fully functional on any repository with standard GitHub secrets.",
        "https://gnupg.org",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; de facto standard for open-source Java package verification.",
        "N/A (Fully suitable for open-source model)",
        "Sigstore Cosign, OpenSSL, Reusing corporate code signing service",
        "Standard GPG Key Signing (GnuPG v2.4+)",
        "$0 cost, universal support across Maven Central, Gradle, and SDKMAN, 100% compliant with open-source norms.",
        orig_tool,
        "Replaces commercial DigiCert KeyLocker ($996/yr) with zero-cost standard GPG signing.",
        evidence
    ]

def make_jfrog_staged_repo(wf_name, wf_yml, category, purpose, evidence, ml_issue, secret_var):
    return [
        "JFrog staged repository",
        "repo.spring.io/libs-staging-local (Staged Repository)",
        purpose,
        "Upstream Original Tool",
        "N/A (Upstream Original)",
        "Holds staged release candidate artifacts in an isolated Artifactory repository during verification before public promotion.",
        "Requires active JFrog Artifactory subscription and staged repo credentials.",
        "Paid",
        "Yes (Requires staging repository credentials RVT_COMMERCIAL_REPOSITORY_USERNAME / RVT_OSS_REPOSITORY_USERNAME)",
        "Commercial SaaS EULA",
        "Commercial SaaS EULA",
        "None (Distribution registry)",
        "Permitted",
        "Cloud SaaS logs",
        "None",
        "Permissible (Commercial registry service)",
        "Included with JFrog Artifactory Cloud subscription (~$1,800/yr)",
        "JFrog Artifactory Staged Repo ($1,800/yr)",
        "Upstream isolates staged builds from general consumption until verification tests pass.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Tier based.",
        "Storage limits based on paid Artifactory account.",
        "secrets.commercial-repository-password, secrets.commercial-repository-username, secrets.opensource-repository-password, secrets.opensource-repository-username",
        "Conditional; requires active JFrog Artifactory subscription ($1,800/yr).",
        "Conditional; requires software tooling budget.",
        "Yes (Included in Artifactory PO if Artifactory is purchased)",
        "Prevents unverified artifacts from leaking into public production repositories.",
        "Inaccessible (Secret missing in fork)",
        "No (Can be replaced with local workspace staging directory)",
        "No; verification step fails when attempting to download staged artifacts from repo.spring.io.",
        "https://jfrog.com/artifactory",
        "https://jfrog.com/pricing/",
        "https://jfrog.com/pricing/",
        "No; proprietary staged repository requires paid JFrog SaaS.",
        "Requires paid subscription and credentials inaccessible to fork maintainers.",
        "Local deployment repository ($GITHUB_WORKSPACE/deployment-repository), GitHub Packages staging, Nexus OSS",
        "Local Staged Maven Repository / GitHub Packages",
        "$0 cost, zero network round-trip overhead, validates artifacts directly within the CI pipeline run.",
        "N/A (Original Tool)",
        ml_issue,
        evidence
    ]

def make_jfrog_staged_repo_alt(orig_tool, wf_name, wf_yml, category, evidence):
    return [
        "Local Staged Maven Repository / GitHub Packages",
        "Local Maven Staged Directory / GitHub Packages",
        "Stages release artifacts in a local runner workspace directory or GitHub Packages repository for immediate smoke testing.",
        "Recommended Fork Alternate",
        orig_tool,
        "Eliminates remote JFrog staging repository, verifying artifacts locally at $0 cost with superior speed.",
        "None (Local runner storage).",
        "Free",
        "No",
        "Apache-2.0 / Terms of Service",
        "Apache-2.0 / Terms of Service",
        "None / Permissive",
        "Permitted",
        "Local-only",
        "None",
        "Permissible",
        "Free ($0.00)",
        "Free Open Source ($0.00)",
        "Saves $1,800/year Artifactory cost while speeding up release qualification.",
        category,
        COMPONENT,
        wf_name,
        wf_yml,
        "Unlimited.",
        "Unlimited.",
        "None (Local filesystem) or GITHUB_TOKEN",
        "Yes; completely accessible for all 5 team members.",
        "Yes; $0 cost for entire team.",
        "No",
        "Smoke tests validate staged JARs directly from local disk before tagging and publishing.",
        "Accessible",
        "Yes",
        "Yes; eliminates external network dependencies and credentials.",
        "https://github.com/features/actions",
        "N/A (Free Open Source)",
        "N/A (Free Open Source)",
        "Yes; simple, robust staging model for open-source repositories.",
        "N/A (Fully suitable for open-source model)",
        "Sonatype Central Staging API, Nexus OSS staging",
        "Local Staged Maven Repository",
        "$0 cost, zero secrets setup, 100% reproducible validation within the same GitHub Actions run.",
        orig_tool,
        "Replaces remote JFrog staged repository ($1,800/yr) with zero-cost local runner staging directory.",
        evidence
    ]

def get_all_records():
    records = []
    def add(row):
        assert len(row) == 44, f"Row must have 44 elements, got {len(row)}: {row[0]} ({row[3]})"
        records.append(row)

    # 1. ML Row 5: run-codeql-analysis.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Run CodeQL Analysis", "run-codeql-analysis.yml", "Test",
        "Executes CodeQL static security analysis workflow on push, PR, and schedule.",
        ".github/workflows/run-codeql-analysis.yml:8-13; commit 2904c4c0c49",
        "Standard GitHub-hosted runner is sufficient for public fork; no issues identified."
    ))

    # 2. ML Row 9: run-codeql-analysis.yml / CodeQL
    add(make_codeql(
        "Run CodeQL Analysis", "run-codeql-analysis.yml", "Test",
        "Performs automated semantic SAST security scanning for Java vulnerabilities across all Spring Boot modules.",
        ".github/workflows/run-codeql-analysis.yml:13; uses spring-io/github-actions/.github/workflows/codeql-analysis.yml@5caba18f0b41",
        "Native GitHub security scanning is free for public open-source repos; fully retained."
    ))

    # 3. ML Row 13: release-train-join.yml / Spring Release Train
    add(make_spring_release_train(
        "Release Train - Join", "release-train-join.yml", "Internal",
        "Notifies external spring-io/release-train repository that Spring Boot is joining a release train.",
        ".github/workflows/release-train-join.yml:21-22, 36, 40-50",
        "External release train orchestrator is private/inaccessible to fork; requires independent release lifecycle."
    ))
    add(make_spring_release_train_alt(
        "Spring Release Train", "Release Train - Join", "release-train-join.yml", "Internal",
        ".github/workflows/release-train-join.yml:21-50",
        "Standalone Fork Release Process / Workflow Discarded",
        "Releases Spring Boot independently without joining upstream release train."
    ))

    # 4. ML Row 16: release-train-join.yml / GitHub API
    add(make_github_api(
        "Release Train - Join", "release-train-join.yml", "Internal",
        "Triggers workflow and watches execution status on external spring-io/release-train repository via gh CLI.",
        ".github/workflows/release-train-join.yml:36, 40-50",
        "gh CLI calls fail on fork because external repo spring-io/release-train rejects fork participant token."
    ))
    add(make_github_api_alt(
        "GitHub API", "Release Train - Join", "release-train-join.yml", "Internal",
        ".github/workflows/release-train-join.yml:36-50"
    ))

    # 5. ML Row 20: release-train-build.yml / GitHub Actions Larger Runner (4-core)
    add(make_larger_runner_4core(
        "Release Train - Build", "release-train-build.yml", "Build",
        "Executes multi-module Gradle build and repeat build for release train artifacts.",
        ".github/workflows/release-train-build.yml:28 (runs-on: 'ubuntu22-2-8')",
        "Upstream hardcodes ubuntu22-2-8; personal/unbilled forks fail immediately with runner allocation error.",
        "ubuntu22-2-8"
    ))
    add(make_larger_runner_4core_alt(
        "GitHub Actions Larger Runner (4-core)", "Release Train - Build", "release-train-build.yml", "Build",
        ".github/workflows/release-train-build.yml:28"
    ))

    # 6. ML Row 23: release-train-build.yml / Gradle
    add(make_gradle(
        "Release Train - Build", "release-train-build.yml", "Build",
        "Compiles, packages, and verifies Spring Boot JARs and distributions during release train build.",
        ".github/workflows/release-train-build.yml:48, 94; .github/actions/release-train-build/action.yml",
        "Standard open-source build tool; fully retained without changes."
    ))

    # 7. ML Row 27: release-train-build.yml / Develocity
    add(make_develocity(
        "Release Train - Build", "release-train-build.yml", "Build",
        "Speeds up release build with remote build caching and publishes build scan telemetry to ge.spring.io.",
        ".github/workflows/release-train-build.yml:48; .github/actions/prepare-gradle-build/action.yml:40-47",
        "Upstream relies on private DEVELOCITY_ACCESS_KEY; missing key results in lost remote cache and no build scans.",
        "secrets.DEVELOCITY_ACCESS_KEY"
    ))
    add(make_develocity_alt(
        "Develocity", "Release Train - Build", "release-train-build.yml", "Build",
        ".github/actions/prepare-gradle-build/action.yml:36-47"
    ))

    # 8. ML Row 45: release-train-build.yml / Spring Enterprise
    add(make_spring_enterprise(
        "Release Train - Build", "release-train-build.yml", "Build",
        "Enables commercial release repository access and enterprise patch generation when vars.COMMERCIAL=true.",
        ".github/workflows/release-train-build.yml:50-52, 96-98",
        "Upstream uses commercial mode for paying Broadcom customers; proprietary binaries cannot be redistributed in public fork.",
        "vars.COMMERCIAL_RELEASE_REPO_URL, secrets.COMMERCIAL_ARTIFACTORY_PASSWORD"
    ))
    add(make_spring_enterprise_alt(
        "Spring Enterprise", "Release Train - Build", "release-train-build.yml", "Build",
        ".github/workflows/release-train-build.yml:50-52"
    ))

    # 9. ML Row 60: release-train-build.yml / JFrog Artifactory
    add(make_jfrog_artifactory(
        "Release Train - Build", "release-train-build.yml", "Build",
        "Stages and publishes release train artifacts to repo.spring.io using deployment-spec.yml.",
        ".github/workflows/release-train-build.yml:53-55, 99-101",
        "Upstream uses repo.spring.io; fork lacks write credentials and cannot publish to official Spring Artifactory.",
        "secrets.RELEASE_TRAIN_PARTICIPANT_MAVEN_REPOSITORY_PASSWORD"
    ))
    add(make_jfrog_artifactory_alt(
        "JFrog Artifactory", "Release Train - Build", "release-train-build.yml", "Build",
        ".github/workflows/release-train-build.yml:53-55",
        "release train artifacts"
    ))

    # 10. ML Row 65: release-train-build.yml / Spring Release Train
    add(make_spring_release_train(
        "Release Train - Build", "release-train-build.yml", "Build",
        "Reports release train build completion status and artifact metadata back to spring-io/release-train.",
        ".github/workflows/release-train-build.yml:112, 120",
        "Orchestrator callback fails on fork due to lack of write permissions on spring-io/release-train."
    ))
    add(make_spring_release_train_alt(
        "Spring Release Train", "Release Train - Build", "release-train-build.yml", "Build",
        ".github/workflows/release-train-build.yml:112-120",
        "Standalone Workflow Dispatch Release Trigger",
        "Triggers release build directly in the fork via workflow_dispatch."
    ))

    # 11. ML Row 68: build-and-deploy-snapshot.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        "Executes snapshot build, verification, and deployment jobs on hosted runner.",
        ".github/workflows/build-and-deploy-snapshot.yml:15, 58",
        "Standard runner executes cleanly on public fork."
    ))

    # 12. ML Row 71: build-and-deploy-snapshot.yml / Spring Enterprise
    add(make_spring_enterprise(
        "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        "Toggles commercial snapshot repository deployment (spring-enterprise-maven-dev-local) and branding.",
        ".github/workflows/build-and-deploy-snapshot.yml:23-26, 33-37",
        "Commercial snapshot mode requires proprietary Broadcom Tanzu credentials; fails on open-source fork.",
        "vars.COMMERCIAL, vars.COMMERCIAL_SNAPSHOT_REPO_URL"
    ))
    add(make_spring_enterprise_alt(
        "Spring Enterprise", "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        ".github/workflows/build-and-deploy-snapshot.yml:23-37"
    ))

    # 13. ML Row 74: build-and-deploy-snapshot.yml / JFrog Artifactory
    add(make_jfrog_artifactory(
        "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        "Deploys daily snapshots to repo.spring.io/libs-snapshot-local via spring-io/artifactory-deploy-action.",
        ".github/workflows/build-and-deploy-snapshot.yml:31-42",
        "Fork cannot deploy to repo.spring.io without official Spring project credentials; causes HTTP 401 deploy failure.",
        "secrets.ARTIFACTORY_USERNAME, secrets.ARTIFACTORY_PASSWORD"
    ))
    add(make_jfrog_artifactory_alt(
        "JFrog Artifactory", "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        ".github/workflows/build-and-deploy-snapshot.yml:31-42",
        "snapshot builds"
    ))

    # 14. ML Row 79: build-and-deploy-snapshot.yml / Broadcom RVT upstream
    add(make_broadcom_rvt(
        "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        "Clones private RVT repo spring-projects/spring-boot-release-verification to verify staged snapshots.",
        ".github/workflows/build-and-deploy-snapshot.yml:68-74",
        "Private repository cannot be cloned by external forks; results in fatal checkout error."
    ))
    add(make_broadcom_rvt_alt(
        "Broadcom RVT upstream", "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        ".github/workflows/build-and-deploy-snapshot.yml:68-74"
    ))

    # 15. ML Row 82: build-and-deploy-snapshot.yml / Google Chat
    add(make_google_chat(
        "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        "Sends Google Chat webhook alerts on snapshot build failure or verification completion.",
        ".github/workflows/build-and-deploy-snapshot.yml:50, 71",
        "Webhook secret is absent on forks; step fails or is skipped without alerting maintainers.",
        "secrets.GOOGLE_CHAT_WEBHOOK_URL"
    ))
    add(make_google_chat_alt(
        "Google Chat", "Build and Deploy Snapshot", "build-and-deploy-snapshot.yml", "Package",
        ".github/workflows/build-and-deploy-snapshot.yml:50, 71"
    ))

    # 16. ML Row 87: build-pull-request.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Build Pull Request", "build-pull-request.yml", "Build",
        "Compiles code, runs tests, and uploads failure reports for incoming pull requests.",
        ".github/workflows/build-pull-request.yml:9; commit 2904c4c0c49",
        "Standard hosted runner handles PR builds cleanly."
    ))

    # 17. ML Row 91: build-pull-request.yml / Gradle
    add(make_gradle(
        "Build Pull Request", "build-pull-request.yml", "Build",
        "Executes ./gradlew build for pull request qualification.",
        ".github/workflows/build-pull-request.yml:14; .github/actions/build/action.yml:64",
        "Core open-source build tool; fully retained."
    ))

    # 18. ML Row 95: build-pull-request.yml / Develocity upstream
    add(make_develocity(
        "Build Pull Request", "build-pull-request.yml", "Build",
        "Provides build scans and remote caching during pull request validation.",
        ".github/workflows/build-pull-request.yml:14; .github/actions/prepare-gradle-build/action.yml:42",
        "DEVELOCITY_ACCESS_KEY is withheld on fork PRs for security; PRs run without build scan telemetry.",
        "secrets.DEVELOCITY_ACCESS_KEY"
    ))
    add(make_develocity_alt(
        "Develocity upstream", "Build Pull Request", "build-pull-request.yml", "Build",
        ".github/actions/prepare-gradle-build/action.yml:36-47"
    ))

    # 19. ML Row 100: ci.yml / GitHub Actions Larger Runner (4-core)
    add(make_larger_runner_4core(
        "CI", "ci.yml", "Test",
        "Runs CI multi-module build and test matrix across supported OS environments.",
        ".github/workflows/ci.yml:17 (vars.UBUNTU_MEDIUM)",
        "UBUNTU_MEDIUM runner label requires billing; falls back to standard runner or fails if unset.",
        "UBUNTU_MEDIUM"
    ))
    add(make_larger_runner_4core_alt(
        "GitHub Actions Larger Runner (4-core)", "CI", "ci.yml", "Test",
        ".github/workflows/ci.yml:17"
    ))

    # 20. ML Row 103: ci.yml / Gradle
    add(make_gradle(
        "CI", "ci.yml", "Test",
        "Executes full CI build and unit test matrix across Gradle subprojects.",
        ".github/workflows/ci.yml:46; .github/actions/build/action.yml:64",
        "Standard open-source build tool; fully retained."
    ))

    # 21. ML Row 107: ci.yml / Develocity upstream
    add(make_develocity(
        "CI", "ci.yml", "Test",
        "Publishes build scans and shares remote build cache during CI matrix runs.",
        ".github/workflows/ci.yml:54",
        "Missing DEVELOCITY_ACCESS_KEY prevents build scan publishing to ge.spring.io.",
        "secrets.DEVELOCITY_ACCESS_KEY"
    ))
    add(make_develocity_alt(
        "Develocity upstream", "CI", "ci.yml", "Test",
        ".github/workflows/ci.yml:54"
    ))

    # 22. ML Row 112: ci.yml / Spring Enterprise
    add(make_spring_enterprise(
        "CI", "ci.yml", "Test",
        "Validates commercial repository compatibility and enterprise builds in CI matrix.",
        ".github/workflows/ci.yml:50-53",
        "Commercial mode requires proprietary repository credentials that are unavailable on public forks.",
        "vars.COMMERCIAL_RELEASE_REPO_URL, secrets.COMMERCIAL_ARTIFACTORY_PASSWORD"
    ))
    add(make_spring_enterprise_alt(
        "Spring Enterprise", "CI", "ci.yml", "Test",
        ".github/workflows/ci.yml:50-53"
    ))

    # 23. ML Row 115: ci.yml / Google Chat
    add(make_google_chat(
        "CI", "ci.yml", "Test",
        "Dispatches failure alert to Spring developer Google Chat space when CI jobs fail.",
        ".github/workflows/ci.yml:67",
        "Private webhook secret GOOGLE_CHAT_WEBHOOK_URL is missing in forks.",
        "secrets.GOOGLE_CHAT_WEBHOOK_URL"
    ))
    add(make_google_chat_alt(
        "Google Chat", "CI", "ci.yml", "Test",
        ".github/workflows/ci.yml:67"
    ))

    # 24. ML Row 120: run-system-tests.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Run System Tests", "run-system-tests.yml", "Test",
        "Executes heavy system integration tests against live containerized database services.",
        ".github/workflows/run-system-tests.yml:10",
        "Standard runner executes system tests; requires sufficient disk space for container images."
    ))

    # 25. ML Row 123: run-system-tests.yml / Docker/Testcontainers
    add(make_docker_testcontainers(
        "Run System Tests", "run-system-tests.yml", "Test",
        "Manages ephemeral database containers (Postgres, Kafka, Redis, Oracle, etc.) for system tests.",
        ".github/workflows/run-system-tests.yml:25; spring-boot-project/spring-boot-testcontainers",
        "Open-source test framework; fully retained."
    ))

    # 26. ML Row 128: run-system-tests.yml / Develocity
    add(make_develocity(
        "Run System Tests", "run-system-tests.yml", "Test",
        "Caches system test fixtures and publishes test distribution telemetry to ge.spring.io.",
        ".github/workflows/run-system-tests.yml:26",
        "Missing DEVELOCITY_ACCESS_KEY disables remote caching and build scan publication.",
        "secrets.DEVELOCITY_ACCESS_KEY"
    ))
    add(make_develocity_alt(
        "Develocity", "Run System Tests", "run-system-tests.yml", "Test",
        ".github/workflows/run-system-tests.yml:26"
    ))

    # 27. ML Row 133: run-system-tests.yml / Docker Hub upstream
    add(make_docker_hub(
        "Run System Tests", "run-system-tests.yml", "Test",
        "Pulls 11+ container images from Docker Hub during integration test execution.",
        ".github/workflows/run-system-tests.yml:25-26",
        "Anonymous pulls exceed 100 pulls/6hr rate limit on shared runner IPs, causing HTTP 429 test failures."
    ))
    add(make_docker_hub_alt(
        "Docker Hub upstream", "Run System Tests", "run-system-tests.yml", "Test",
        ".github/workflows/run-system-tests.yml:25-26"
    ))

    # 28. ML Row 139: trigger-docs-build.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Trigger Docs Build", "trigger-docs-build.yml", "Release Doc",
        "Runs dispatch CLI to trigger docs build workflow on documentation repository.",
        ".github/workflows/trigger-docs-build.yml:14",
        "Standard runner executes cleanly on public fork."
    ))

    # 29. ML Row 143: trigger-docs-build.yml / external spring-boot-docs repository
    add(make_docs_repo(
        "Trigger Docs Build", "trigger-docs-build.yml", "Release Doc",
        "External repository spring-projects/spring-boot-docs that compiles and hosts Antora documentation.",
        ".github/workflows/trigger-docs-build.yml:23",
        "Forks cannot trigger workflows on external repo spring-projects/spring-boot-docs; fails with 403 Forbidden."
    ))
    add(make_docs_repo_alt(
        "external spring-boot-docs repository", "Trigger Docs Build", "trigger-docs-build.yml", "Release Doc",
        ".github/workflows/trigger-docs-build.yml:23"
    ))

    # 30. ML Row 147: trigger-docs-build.yml / automation identity
    add(make_automation_identity(
        "Trigger Docs Build", "trigger-docs-build.yml", "Release Doc",
        "Bot account PAT used by gh CLI to authenticate cross-repo dispatch to docs repository.",
        ".github/workflows/trigger-docs-build.yml:21",
        "Secret SPRING_BUILDMASTER_GITHUB_TOKEN is private to Spring team; missing in fork.",
        "secrets.SPRING_BUILDMASTER_GITHUB_TOKEN"
    ))
    add(make_automation_identity_alt(
        "automation identity", "Trigger Docs Build", "trigger-docs-build.yml", "Release Doc",
        ".github/workflows/trigger-docs-build.yml:21"
    ))

    # 31. ML Row 152: publicize-milestone.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Publicize Prerelease", "publicize-milestone.yml", "Release",
        "Publishes milestone release notes, tags, and packages across registries.",
        ".github/workflows/publicize-milestone.yml:14, 32, 50, 62",
        "Standard runner handles prerelease steps cleanly."
    ))

    # 32. ML Row 156: publicize-milestone.yml / GitHub Packages
    add(make_github_packages(
        "Publicize Prerelease", "publicize-milestone.yml", "Release",
        "Publishes milestone artifacts to GitHub Packages Maven repository.",
        ".github/workflows/publicize-milestone.yml:54",
        "Standard native package registry; fully retained."
    ))

    # 33. ML Row 160: publicize-release.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Publicize Release", "publicize-release.yml", "Release",
        "Executes multi-step GA release publication across GitHub, Artifactory, SDKMAN, and Maven Central.",
        ".github/workflows/publicize-release.yml:13, 31, 47, 62, 77, 91",
        "Standard runner handles release steps cleanly."
    ))

    # 34. ML Row 164: publicize-release.yml / Spring Enterprise
    add(make_spring_enterprise(
        "Publicize Release", "publicize-release.yml", "Release",
        "Promotes and publicizes commercial enterprise releases when vars.COMMERCIAL=true.",
        ".github/workflows/publicize-release.yml:28, 98",
        "Commercial publication branch requires Broadcom commercial rights and commercial registry tokens.",
        "vars.COMMERCIAL"
    ))
    add(make_spring_enterprise_alt(
        "Spring Enterprise", "Publicize Release", "publicize-release.yml", "Release",
        ".github/workflows/publicize-release.yml:28, 98"
    ))

    # 35. ML Row 167: publicize-release.yml / JFrog Artifactory
    add(make_jfrog_artifactory(
        "Publicize Release", "publicize-release.yml", "Release",
        "Promotes staged release artifacts to production repository repo.spring.io/release using JFrog CLI.",
        ".github/workflows/publicize-release.yml:41",
        "Token JF_ARTIFACTORY_SPRING is private to Spring release engineers; missing in fork.",
        "secrets.JF_ARTIFACTORY_SPRING"
    ))
    add(make_jfrog_artifactory_alt(
        "JFrog Artifactory", "Publicize Release", "publicize-release.yml", "Release",
        ".github/workflows/publicize-release.yml:41",
        "GA release promotion"
    ))

    # 36. ML Row 172: publicize-release.yml / code-signing service
    add(make_code_signing(
        "Publicize Release", "publicize-release.yml", "Release",
        "Signs release artifacts and binaries using hardware-backed code signing service.",
        ".github/workflows/publicize-release.yml:40",
        "Commercial signing service requires expensive annual certificate; missing in fork.",
        "secrets.KEYLOCKER_TOKEN / secrets.GPG_PRIVATE_KEY"
    ))
    add(make_code_signing_alt(
        "code-signing service", "Publicize Release", "publicize-release.yml", "Release",
        ".github/workflows/publicize-release.yml:40"
    ))

    # 37. ML Row 177: release-train-leave.yml / Spring Release Train
    add(make_spring_release_train(
        "Release Train - Leave", "release-train-leave.yml", "Internal",
        "Notifies spring-io/release-train that Spring Boot is exiting the release train.",
        ".github/workflows/release-train-leave.yml:13-14, 28-40",
        "External release train is inaccessible to fork; workflow can be discarded."
    ))
    add(make_spring_release_train_alt(
        "Spring Release Train", "Release Train - Leave", "release-train-leave.yml", "Internal",
        ".github/workflows/release-train-leave.yml:13-40",
        "Independent Fork Lifecycle / Workflow Discarded",
        "Fork manages independent release cadence without participating in release train."
    ))

    # 38. ML Row 180: release-train-leave.yml / GitHub API
    add(make_github_api(
        "Release Train - Leave", "release-train-leave.yml", "Internal",
        "Calls GitHub API to update state on external spring-io/release-train repo via gh CLI.",
        ".github/workflows/release-train-leave.yml:28, 32-40",
        "Cross-repo API call fails on fork without participant token."
    ))
    add(make_github_api_alt(
        "GitHub API", "Release Train - Leave", "release-train-leave.yml", "Internal",
        ".github/workflows/release-train-leave.yml:28-40"
    ))

    # 39. ML Row 184: release-train-ready.yml / Spring Release Train
    add(make_spring_release_train(
        "Release Train - Ready", "release-train-ready.yml", "Internal",
        "Notifies spring-io/release-train that Spring Boot is ready for release train synchronization.",
        ".github/workflows/release-train-ready.yml:13-14, 28-41",
        "External release train is inaccessible to fork; workflow can be discarded."
    ))
    add(make_spring_release_train_alt(
        "Spring Release Train", "Release Train - Ready", "release-train-ready.yml", "Internal",
        ".github/workflows/release-train-ready.yml:13-41",
        "Independent Fork Lifecycle / Workflow Discarded",
        "Fork manages independent release cadence without participating in release train."
    ))

    # 40. ML Row 187: release-train-ready.yml / GitHub API
    add(make_github_api(
        "Release Train - Ready", "release-train-ready.yml", "Internal",
        "Calls GitHub API to update readiness state on external spring-io/release-train repo via gh CLI.",
        ".github/workflows/release-train-ready.yml:28, 32-41",
        "Cross-repo API call fails on fork without participant token."
    ))
    add(make_github_api_alt(
        "GitHub API", "Release Train - Ready", "release-train-ready.yml", "Internal",
        ".github/workflows/release-train-ready.yml:28-41"
    ))

    # 41. ML Row 191: release-train-retry.yml / Spring Release Train
    add(make_spring_release_train(
        "Release Train - Retry", "release-train-retry.yml", "Internal",
        "Triggers retry mechanism on external spring-io/release-train repository.",
        ".github/workflows/release-train-retry.yml:13-14, 28-34",
        "External release train is inaccessible to fork; workflow can be discarded."
    ))
    add(make_spring_release_train_alt(
        "Spring Release Train", "Release Train - Retry", "release-train-retry.yml", "Internal",
        ".github/workflows/release-train-retry.yml:13-34",
        "Independent Fork Lifecycle / Workflow Discarded",
        "Fork manages independent release cadence without participating in release train."
    ))

    # 42. ML Row 194: release-train-retry.yml / GitHub API
    add(make_github_api(
        "Release Train - Retry", "release-train-retry.yml", "Internal",
        "Calls GitHub API to request retry on external spring-io/release-train repo via gh CLI.",
        ".github/workflows/release-train-retry.yml:28, 31-34",
        "Cross-repo API call fails on fork without participant token."
    ))
    add(make_github_api_alt(
        "GitHub API", "Release Train - Retry", "release-train-retry.yml", "Internal",
        ".github/workflows/release-train-retry.yml:28-34"
    ))

    # 43. ML Row 198: release-train-test.yml / GitHub Actions Larger Runner (8-core)
    add(make_larger_runner_8core(
        "Release Train - Test", "release-train-test.yml", "Test",
        "Executes full multi-project integration test matrix for release train verification.",
        ".github/workflows/release-train-test.yml:28 (runs-on: 'ubuntu22-4-16')",
        "Hardcoded label ubuntu22-4-16 fails immediately on forks lacking paid larger runner entitlement."
    ))
    add(make_larger_runner_8core_alt(
        "GitHub Actions Larger Runner (8-core)", "Release Train - Test", "release-train-test.yml", "Test",
        ".github/workflows/release-train-test.yml:28"
    ))

    # 44. ML Row 201: release-train-test.yml / Develocity
    add(make_develocity(
        "Release Train - Test", "release-train-test.yml", "Test",
        "Distributes test execution and publishes test analytics to ge.spring.io.",
        ".github/workflows/release-train-test.yml:63; .github/actions/release-train-test/action.yml",
        "Missing DEVELOCITY_ACCESS_KEY disables test distribution and build scan publishing.",
        "secrets.DEVELOCITY_ACCESS_KEY"
    ))
    add(make_develocity_alt(
        "Develocity", "Release Train - Test", "release-train-test.yml", "Test",
        ".github/workflows/release-train-test.yml:63"
    ))

    # 45. ML Row 206: release-train-test.yml / JFrog Artifactory
    add(make_jfrog_artifactory(
        "Release Train - Test", "release-train-test.yml", "Test",
        "Resolves staged artifacts from repo.spring.io during release train test execution.",
        ".github/workflows/release-train-test.yml:68-70",
        "Fork lacks credentials to download staged artifacts from private repository on repo.spring.io.",
        "secrets.RELEASE_TRAIN_PARTICIPANT_MAVEN_REPOSITORY_PASSWORD"
    ))
    add(make_jfrog_artifactory_alt(
        "JFrog Artifactory", "Release Train - Test", "release-train-test.yml", "Test",
        ".github/workflows/release-train-test.yml:68-70",
        "staged test artifacts"
    ))

    # 46. ML Row 211: release-train-test.yml / Spring Release Train
    add(make_spring_release_train(
        "Release Train - Test", "release-train-test.yml", "Test",
        "Reports test execution status and test pass/fail results back to spring-io/release-train.",
        ".github/workflows/release-train-test.yml:57, 75",
        "Orchestrator callback fails on fork due to lack of write permissions on spring-io/release-train."
    ))
    add(make_spring_release_train_alt(
        "Spring Release Train", "Release Train - Test", "release-train-test.yml", "Test",
        ".github/workflows/release-train-test.yml:57, 75",
        "Independent Fork Test Execution Trigger",
        "Executes release tests independently and reports results natively in GitHub Actions."
    ))

    # 47. ML Row 214: verify.yml / GitHub Actions Hosted Runner
    add(make_hosted_runner(
        "Verify", "verify.yml", "Test",
        "Runs verification workflow on standard hosted runner.",
        ".github/workflows/verify.yml:38 (vars.UBUNTU_SMALL || 'ubuntu-latest')",
        "Standard hosted runner executes cleanly on public fork."
    ))

    # 48. ML Row 218: verify.yml / Broadcom RVT upstream
    add(make_broadcom_rvt(
        "Verify", "verify.yml", "Test",
        "Clones spring-projects/spring-boot-release-verification to validate staged release artifacts.",
        ".github/workflows/verify.yml:41-45",
        "Private repository cannot be cloned by external forks; results in fatal checkout error."
    ))
    add(make_broadcom_rvt_alt(
        "Broadcom RVT upstream", "Verify", "verify.yml", "Test",
        ".github/workflows/verify.yml:41-45"
    ))

    # 49. ML Row 221: verify.yml / JFrog staged repository
    add(make_jfrog_staged_repo(
        "Verify", "verify.yml", "Test",
        "Validates staged release candidate artifacts hosted on repo.spring.io/libs-staging-local.",
        ".github/workflows/verify.yml:73-79",
        "Staged repository requires private credentials; inaccessible to forks.",
        "secrets.commercial-repository-password, secrets.opensource-repository-password"
    ))
    add(make_jfrog_staged_repo_alt(
        "JFrog staged repository", "Verify", "verify.yml", "Test",
        ".github/workflows/verify.yml:73-79"
    ))

    return records
