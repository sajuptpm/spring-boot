import openpyxl
from openpyxl.styles import Font, Alignment

# Load workbook
wb = openpyxl.load_workbook('workflow-fixes/pipeline_result.xlsx')
ws = wb['spring boot']

data_ab_ae = {
    2: {
        'end_row': 4,
        'AB': '0.1 days',
        'AC': 'Configuring GITHUB_TOKEN permissions (security-events: write, actions: read); adding workflow_dispatch trigger for on-demand execution; verifying GitHub Advanced Security (GHAS) is enabled if running in a private fork.',
        'AD': 'Repository is public (free GHAS/CodeQL) or organization has GitHub Advanced Security licenses allocated; Java 25 compiles under standard GitHub runners without custom runner config.',
        'AE': 'Private repository lacking GHAS license causing the CodeQL action to abort immediately with license entitlement error.'
    },
    5: {
        'end_row': 5,
        'AB': '0.25 days',
        'AC': 'Configuring secret RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN with write permissions to spring-io/release-train; setting repository variable UBUNTU_MEDIUM; updating upstream repo reference if using an enterprise orchestrator repo.',
        'AD': 'An enterprise release train orchestrator repository exists and the provided PAT has write access to create/update train participant branches and state issues.',
        'AE': 'PAT lacking sufficient repository scopes (repo, workflow) or orchestrator API rate limits / branch protection rules preventing state updates.'
    },
    6: {
        'end_row': 7,
        'AB': '0.5 days',
        'AC': 'Configuring secrets RELEASE_TRAIN_PARTICIPANT_MAVEN_REPOSITORY_USERNAME, RELEASE_TRAIN_PARTICIPANT_MAVEN_REPOSITORY_PASSWORD, DEVELOCITY_ACCESS_KEY, RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN; setting UBUNTU_MEDIUM runner variable and COMMERCIAL_RELEASE_REPO_URL; running staging deploy test.',
        'AD': 'Staging Maven repository is deployed, active, and accessible from runner; Develocity server (ge.spring.io or corporate) accepts incoming build scans; runner has 25GB+ disk space.',
        'AE': 'Network firewall blocking egress to staging repository; invalid Maven repository credentials causing HTTP 401 deploy failures; runner disk exhaustion during repeat builds.'
    },
    8: {
        'end_row': 9,
        'AB': '0.5 days',
        'AC': 'Configuring secrets ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD, GPG_PRIVATE_KEY, GPG_PASSPHRASE, GOOGLE_CHAT_WEBHOOK_URL, DEVELOCITY_ACCESS_KEY, GH_ACTIONS_REPO_TOKEN; setting variables ARTIFACTORY_DEPLOY_REPO_URL, ARTIFACTORY_REPOSITORY, ARTIFACTORY_PROJECT, UBUNTU_MEDIUM; relaxing upstream repo if: guard check.',
        'AD': 'Enterprise Artifactory instance (e.g. JFrog) has snapshot repository initialized; GPG key is valid and unexpired; private verification repo token has read access; Google Chat webhook URL is valid.',
        'AE': 'Artifactory repository permissions rejecting POM/JAR uploads; PGP/GPG passphrase mismatches; verification repository token expired or lacking read access.'
    },
    10: {
        'end_row': 10,
        'AB': '0.1 days',
        'AC': 'Configuring optional secret DEVELOCITY_ACCESS_KEY; configuring repository variable UBUNTU_MEDIUM (or aliasing to ubuntu-latest); testing PR trigger on open/synchronize.',
        'AD': 'Standard GitHub-hosted runner quota is available; Develocity key is valid (or omitted if public scans are accepted).',
        'AE': 'Runner concurrency limits delaying PR checks when multiple PRs are submitted simultaneously.'
    },
    11: {
        'end_row': 11,
        'AB': '0.25 days',
        'AC': 'Configuring secrets DEVELOCITY_ACCESS_KEY, GOOGLE_CHAT_WEBHOOK_URL; setting variable UBUNTU_MEDIUM; configuring commercial Artifactory credentials if COMMERCIAL=true; validating Linux and Windows runner matrix execution.',
        'AD': 'Organization has Windows and Linux runner capacity; Google Chat webhook endpoint is active; Develocity server is online.',
        'AE': 'Windows runner I/O timeouts; webhook endpoint throttling or rejecting payload format.'
    },
    12: {
        'end_row': 12,
        'AB': '0.25 days',
        'AC': 'Configuring secrets DEVELOCITY_ACCESS_KEY, GOOGLE_CHAT_WEBHOOK_URL, DOCKERHUB_USERNAME/PASSWORD; setting variable UBUNTU_MEDIUM; verifying Docker daemon availability on runner.',
        'AD': 'Runner environment has Docker enabled with min 8GB RAM and 30GB disk space; Docker Hub credentials bypass anonymous pull rate limits.',
        'AE': 'Docker daemon failure or container image pull timeouts on large database images (Oracle, MS SQL, Neo4j).'
    },
    13: {
        'end_row': 14,
        'AB': '0.1 days',
        'AC': 'Configuring secret GH_ACTIONS_REPO_TOKEN with repo scope for dispatching downstream docs repository; setting variable UBUNTU_SMALL; pointing downstream repository name to organization docs repo.',
        'AD': 'Downstream documentation repository is set up with a workflow listening for repository_dispatch event type docs-build.',
        'AE': 'PAT lacking permissions to dispatch events to the target documentation repository.'
    },
    15: {
        'end_row': 15,
        'AB': '0.25 days',
        'AC': 'Configuring secrets JF_ARTIFACTORY_SPRING, GRADLE_PLUGIN_PUBLISH_KEY, GRADLE_PLUGIN_PUBLISH_SECRET, GH_ACTIONS_REPO_TOKEN; verifying Artifactory milestone promotion endpoint; validating Git tag protection.',
        'AD': 'Artifactory staging-to-milestone promotion permissions are granted; Gradle Plugin Portal API key has publisher rights for Spring Boot plugins.',
        'AE': 'Gradle Plugin Portal rejecting version if plugin ID is not owned by the publishing account; Artifactory promotion API failure.'
    },
    16: {
        'end_row': 16,
        'AB': '0.5 days',
        'AC': 'Configuring secrets JF_ARTIFACTORY_SPRING, GRADLE_PLUGIN_PUBLISH_KEY, GRADLE_PLUGIN_PUBLISH_SECRET, SDKMAN_CONSUMER_KEY, SDKMAN_CONSUMER_TOKEN, GH_ACTIONS_REPO_TOKEN; configuring Homebrew tap repo variable/token; relaxing repo guard; testing dry-run publication.',
        'AD': 'Corporate accounts for Artifactory Release repo, SDKMAN vendor portal, Homebrew tap repo, and Gradle Plugin Portal are fully active and pre-authenticated.',
        'AE': 'Accidental production release broadcast to public registries (SDKMAN/Gradle Portal) during testing; failure of third-party consumer APIs.'
    },
    17: {
        'end_row': 17,
        'AB': '0.1 days',
        'AC': 'Configuring secret RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN; setting variable UBUNTU_MEDIUM; verifying orchestrator dispatch.',
        'AD': 'Upstream/internal release train orchestrator is reachable and participant token has write access.',
        'AE': 'Token expired or orchestrator repo missing.'
    },
    18: {
        'end_row': 18,
        'AB': '0.1 days',
        'AC': 'Configuring secret RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN; setting variable UBUNTU_MEDIUM; verifying ready signal dispatch.',
        'AD': 'Orchestrator repo is waiting for ready signal on active train release branch.',
        'AE': 'Token expired or orchestrator repo missing.'
    },
    19: {
        'end_row': 19,
        'AB': '0.1 days',
        'AC': 'Configuring secret RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN; setting variable UBUNTU_MEDIUM; verifying retry signal dispatch.',
        'AD': 'Orchestrator has an in-flight failed stage ready to receive retry dispatch.',
        'AE': 'Token expired or orchestrator repo missing.'
    },
    20: {
        'end_row': 20,
        'AB': '0.5 days',
        'AC': 'Configuring secrets RELEASE_TRAIN_PARTICIPANT_MAVEN_REPOSITORY_USERNAME, RELEASE_TRAIN_PARTICIPANT_MAVEN_REPOSITORY_PASSWORD, DEVELOCITY_ACCESS_KEY, RELEASE_TRAIN_PARTICIPANT_GITHUB_TOKEN; setting variable UBUNTU_LARGE / UBUNTU_MEDIUM; verifying staging repository resolution.',
        'AD': 'Staging Maven repository contains staged artifacts from release-train-build; compute runner has 16GB RAM for full test suite.',
        'AE': 'Staging Maven repo unreachable from runner; missing staged upstream dependency artifacts causing test failure.'
    },
    21: {
        'end_row': 21,
        'AB': '0.25 days',
        'AC': 'Configuring secret GH_ACTIONS_REPO_TOKEN with access to private verification repository spring-projects/spring-boot-release-verification (or an enterprise clone); configuring GOOGLE_CHAT_WEBHOOK_URL; testing reusable workflow invocation.',
        'AD': 'The private verification repository is accessible via the provided PAT; staging Maven repository is populated and reachable.',
        'AE': 'Token lacking read permissions to private verification repo resulting in git clone failure; incompatibility between verification test suite version and Spring Boot version.'
    }
}

cols = ['AB', 'AC', 'AD', 'AE']

font_regular = Font(name='Calibri', size=11, bold=False)
font_estimate = Font(name='Calibri', size=11, bold=True)

for start_r, row_info in data_ab_ae.items():
    end_r = row_info['end_row']
    for col in cols:
        val = row_info[col]
        top_cell = ws[f'{col}{start_r}']
        top_cell.value = val
        
        is_centered = (col == 'AB')
        is_bold = (col == 'AB')
        
        top_cell.font = font_estimate if is_bold else font_regular
        top_cell.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center' if is_centered else None)
        
        # If multi-row block, clear child cells and merge
        if end_r > start_r:
            for r in range(start_r + 1, end_r + 1):
                ws[f'{col}{r}'].value = None
            ws.merge_cells(f'{col}{start_r}:{col}{end_r}')

wb.save('workflow-fixes/pipeline_result.xlsx')
print('Successfully populated columns AB through AE for all 15 workflows!')
