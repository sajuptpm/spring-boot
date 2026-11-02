import openpyxl
from openpyxl.styles import Font, Alignment
import os
import shutil

src_file = 'workflow-fixes/spring_pipeline_result.xlsx'
dest_file = 'workflow-fixes/spring_pipeline_result.xlsx'
updated_file = 'workflow-fixes/spring_pipeline_result_updated.xlsx'

wb = openpyxl.load_workbook(src_file)
ws = wb['spring boot']

data_ag = {
    2: {
        'end_row': 4,
        'AG': 'Yes (Mandatory). SAST semantic vulnerability scanning is a non-negotiable compliance requirement for commercial/enterprise releases (SLSA, SOC2, NIST SSDF). It detects critical CWE security flaws, injection vectors, and cryptographic issues in Java 25 code before binaries are signed and distributed to enterprise customers.'
    },
    5: {
        'end_row': 5,
        'AG': 'No (Not Needed). Upstream "Release Train" is a multi-project release coordination protocol specifically designed for Broadcom to synchronize Spring Framework, Spring Data, Spring Security, and Spring Boot releases together. A standalone enterprise fork of Spring Boot manages its own release schedule independently and lacks write access to the external spring-io/release-train orchestrator.'
    },
    6: {
        'end_row': 7,
        'AG': 'Conditional / Optional. Needed only if your enterprise orchestrates multiple internal Spring libraries together in a synchronized multi-project train. For a standalone Spring Boot release, this pipeline is redundant because publicize-release.yml and build-and-deploy-snapshot.yml already compile, package, test, and publish official enterprise GA and snapshot artifacts.'
    },
    8: {
        'end_row': 9,
        'AG': 'Yes (Mandatory). Essential for the continuous development lifecycle, integration testing, and pre-release staging. It compiles, tests, and publishes nightly snapshot artifacts (*-SNAPSHOT) to corporate Maven/Artifactory registries so internal enterprise consumers, QA teams, and downstream applications can test against pre-release builds.'
    },
    10: {
        'end_row': 10,
        'AG': 'Yes (Mandatory). Core pull-request verification gate. Validates every internal PR, bugfix, and security patch against the full compile and test suite prior to merging into main, preventing regressions from contaminating enterprise release branches.'
    },
    11: {
        'end_row': 11,
        'AG': 'Yes (Mandatory). Primary continuous integration pipeline that validates code across both Linux and Windows environments on every push. Cross-platform testing is vital for enterprise software to ensure compatibility across heterogeneous corporate developer workstations and server environments.'
    },
    12: {
        'end_row': 12,
        'AG': 'Yes (Mandatory). Comprehensive end-to-end integration and compatibility gate. Executes live tests against real containerized enterprise infrastructure (PostgreSQL, Oracle, MySQL, MS SQL, MongoDB, Neo4j, Cassandra, Redis, RabbitMQ, Kafka) via Testcontainers to ensure auto-configurations and database drivers work properly before release.'
    },
    13: {
        'end_row': 14,
        'AG': 'Optional / Conditional. Only needed if your organization hosts an independent, decoupled documentation portal repository (built with Antora). If reference documentation is packaged directly as release archive assets (ZIP) or published via internal Wiki/Confluence/Pages, this trigger is not required.'
    },
    15: {
        'end_row': 15,
        'AG': 'Optional / Recommended. Needed if your enterprise adheres to phased milestone and release candidate cycles (e.g. 4.2.0-M1, 4.2.0-RC1) for beta testing and customer preview programs. If the enterprise cuts direct General Availability (GA) releases without milestone staging, this pipeline can be omitted.'
    },
    16: {
        'end_row': 16,
        'AG': 'Yes (Mandatory). The cornerstone enterprise production release pipeline. Creates the official immutable Git release tag (e.g. v4.2.0), packages GA distribution binaries, generates release notes, publishes to corporate Artifactory/Nexus repositories, and publishes distributable CLI packages for end users.'
    },
    17: {
        'end_row': 17,
        'AG': 'No (Not Needed). Proprietary Broadcom train deregistration utility used to remove a project from an active synchronized train. Redundant for a standalone enterprise fork that operates its own lifecycle.'
    },
    18: {
        'end_row': 18,
        'AG': 'No (Not Needed). Upstream status notification utility signaling to spring-io/release-train that artifacts are ready for promotion. Irrelevant for internal enterprise releases where promotion is handled internally.'
    },
    19: {
        'end_row': 19,
        'AG': 'No (Not Needed). Dispatches retry requests to upstream release train orchestrator. In a GitHub Actions environment, retrying failed release stages is natively handled using GitHub\'s built-in "Re-run failed jobs" button or CLI.'
    },
    20: {
        'end_row': 20,
        'AG': 'Conditional / Optional. Needed only if verifying artifacts against an external multi-project release train staging repository. For standalone enterprise distributions, post-build sanity testing is already handled by verify.yml and pre-release testing by ci.yml and run-system-tests.yml.'
    },
    21: {
        'end_row': 21,
        'AG': 'Yes (Mandatory). Automated sanity and pre-promotion gate called before promoting staging artifacts to production GA. Executes smoke tests (application bootstrap, actuator health endpoints, auto-configuration checks) to guarantee that built JARs are functional and free of corrupt packaging before release publication.'
    }
}

font_regular = Font(name='Calibri', size=11, bold=False)

for start_r, row_info in data_ag.items():
    end_r = row_info['end_row']
    val = row_info['AG']
    
    top_cell = ws[f'AG{start_r}']
    top_cell.value = val
    top_cell.font = font_regular
    top_cell.alignment = Alignment(wrap_text=True, vertical='center')
    
    if end_r > start_r:
        for r in range(start_r + 1, end_r + 1):
            ws[f'AG{r}'].value = None
        ws.merge_cells(f'AG{start_r}:AG{end_r}')

ws.column_dimensions['AG'].width = 45.0

# Always save to updated_file first
wb.save(updated_file)
print(f'Successfully saved populated workbook to {updated_file}')

# Now attempt to overwrite dest_file
try:
    wb.save(dest_file)
    print(f'Successfully overwritten {dest_file} directly!')
    if os.path.exists(updated_file):
        os.remove(updated_file)
except PermissionError:
    print(f'File {dest_file} is currently locked by Excel. The updated file is preserved at {updated_file}.')
