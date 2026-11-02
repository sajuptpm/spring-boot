import openpyxl
from openpyxl.styles import Font, Alignment

# Load workbook
wb = openpyxl.load_workbook('workflow-fixes/pipeline_result.xlsx')
ws = wb['spring boot']

# Column AF: Changes required to make original version of pipeline working in the fork (based on column AB)
data_af = {
    2: {
        'end_row': 4,
        'AF': 'Add workflow_dispatch trigger for on-demand manual security scans in the fork without pushing commits; optionally add path filters (paths-ignore) on automated push: trigger to conserve runner minutes. Zero changes to CodeQL jobs, stages, or analysis rules.'
    },
    5: {
        'end_row': 5,
        'AF': 'Update target repository string in the github-script step from "spring-io/release-train" to point to your enterprise orchestrator repository (e.g. "<org>/release-train"); configure repository variable UBUNTU_MEDIUM in GitHub Settings. No changes to join protocol, payload, or job steps.'
    },
    6: {
        'end_row': 7,
        'AF': 'Configure repository variable UBUNTU_MEDIUM in GitHub Settings; set input callback to "none" (for standalone release) or point to your enterprise callback repository. Zero pipeline code changes needed: with staging Maven credentials and Develocity keys populated, full build, Gradle publish, and callbacks run as originally designed.'
    },
    8: {
        'end_row': 9,
        'AF': 'Relax the upstream repository guard check from if: ${{ github.repository == "spring-projects/spring-boot" ... }} to allow execution in the fork (or check vars.ENABLE_SNAPSHOT_BUILD == "true"); add workflow_dispatch trigger; update target Artifactory URL if internal repo differs from repo.spring.io. Zero changes to snapshot compilation, packaging, or Gradle deploy tasks.'
    },
    10: {
        'end_row': 10,
        'AF': 'Add workflow_dispatch trigger to allow manual validation of PR checks; ensure repository variable UBUNTU_MEDIUM is populated in GitHub Settings. Zero code changes needed for compilation, test suites, or Develocity build scan steps.'
    },
    11: {
        'end_row': 11,
        'AF': 'Add workflow_dispatch trigger for manual on-demand execution; optionally filter the automated push: trigger to control runner concurrency. With vars.UBUNTU_MEDIUM, DEVELOCITY_ACCESS_KEY, and GOOGLE_CHAT_WEBHOOK_URL populated in GitHub Settings, both Linux and Windows matrix jobs run unmodified.'
    },
    12: {
        'end_row': 12,
        'AF': 'Add workflow_dispatch trigger with target input parameters (java-version, system-test-target) to allow executing tests on-demand; ensure runner variable UBUNTU_MEDIUM points to a Docker-enabled runner. Zero changes to Docker container execution, testcontainer setup, or database test suites.'
    },
    13: {
        'end_row': 14,
        'AF': 'Update target documentation repository in the repository_dispatch step from "spring-projects/spring-boot-docs" to your organization docs repository (e.g. "<org>/spring-boot-docs"); add workflow_dispatch trigger. With GH_ACTIONS_REPO_TOKEN configured with repo scope, the dispatch event structure remains 100% original.'
    },
    15: {
        'end_row': 15,
        'AF': 'Add workflow_dispatch trigger with input milestone: (e.g. "4.2.0-M1") for controlled milestone triggers without pushing raw git tags; update downstream docs repo reference if maintaining internal docs. With Artifactory and Gradle Plugin Portal keys configured, all promotion and publication jobs execute as originally coded.'
    },
    16: {
        'end_row': 16,
        'AF': 'Add workflow_dispatch trigger with inputs milestone: and latest: for authorized release dispatch; update Homebrew tap repository reference from "spring-projects/homebrew-tap" to your organization tap if applicable. With SDKMAN, Gradle Plugin Portal, and Artifactory secrets populated, all GA distribution jobs execute without flow changes.'
    },
    17: {
        'end_row': 17,
        'AF': 'Update orchestrator repository target in the github-script step from "spring-io/release-train" to your enterprise orchestrator repository; configure variable UBUNTU_MEDIUM. No changes to deregistration script, API payload, or runner flow.'
    },
    18: {
        'end_row': 18,
        'AF': 'Update orchestrator repository target in the github-script step from "spring-io/release-train" to your enterprise orchestrator repository; configure variable UBUNTU_MEDIUM. No changes to ready-signal notification script or job steps.'
    },
    19: {
        'end_row': 19,
        'AF': 'Update orchestrator repository target in the github-script step from "spring-io/release-train" to your enterprise orchestrator repository; configure variable UBUNTU_MEDIUM. No changes to retry dispatch logic or job steps.'
    },
    20: {
        'end_row': 20,
        'AF': 'Exclude Antora documentation task during test stage (-x :spring-boot-project:spring-boot-docs:antora) to prevent doc build timeouts during test phase; configure variable UBUNTU_LARGE in GitHub Settings. With staging Maven credentials and Develocity keys configured, full integration test stages run as originally architected.'
    },
    21: {
        'end_row': 21,
        'AF': 'Ensure permissions are set to contents: read for reusable workflow compatibility; add workflow_dispatch trigger for standalone verification; update verification repository target from "spring-projects/spring-boot-release-verification" to your enterprise verification repository if hosted internally. No changes to RVT test execution commands or staging resolution.'
    }
}

font_regular = Font(name='Calibri', size=11, bold=False)

for start_r, row_info in data_af.items():
    end_r = row_info['end_row']
    val = row_info['AF']
    
    top_cell = ws[f'AF{start_r}']
    top_cell.value = val
    top_cell.font = font_regular
    top_cell.alignment = Alignment(wrap_text=True, vertical='center')
    
    if end_r > start_r:
        for r in range(start_r + 1, end_r + 1):
            ws[f'AF{r}'].value = None
        ws.merge_cells(f'AF{start_r}:AF{end_r}')

# Set comfortable column width for AF
ws.column_dimensions['AF'].width = 38.0

wb.save('workflow-fixes/pipeline_result.xlsx')
print('Successfully populated Column AF for all 15 workflows!')
