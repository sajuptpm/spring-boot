"""
Writes the 84 rows into the spring_boot sheet of workflow-fixes/data1.xlsx.
Applies exact formatting, fills, fonts, alignments, borders, and column widths matching angular.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.path.append('workflow-fixes')
import spring_boot_records

wb_path = 'workflow-fixes/data1.xlsx'
wb = openpyxl.load_workbook(wb_path)

if 'spring_boot' not in wb.sheetnames:
    ws = wb.create_sheet('spring_boot')
else:
    ws = wb['spring_boot']

# Clear entire worksheet
ws.delete_rows(1, ws.max_row + 10)

HEADERS = [
    "Name of Tool/Infra",
    "Version",
    "Purpose",
    "Record Type (Upstream Original Tool / Recommended Fork Alternate)",
    "Alternate of which too/infra (Mapping to Upstream Original Tool /infra)",
    "Reason of selecting this tool",
    "Any usage Limit",
    "Free/Paid",
    "Access-restricted, blocked, not publicly accessible, or unavailable for purchase",
    "License",
    "SPDX License Identifier (e.g., MIT, Apache-2.0, Commercial SaaS EULA)",
    "Copyleft / Viral Source Disclosure Risk (None / Permissive vs Weak Copyleft vs Strong Copyleft)",
    "Commercial Redistribution Rights (Permitted / Restricted / Non-commercial only)",
    "Telemetry & Code Exfiltration Risk (Local-only / Cloud SaaS logs / High)",
    "Attribution / Notice Requirements (Standard notice / None)",
    "Permissible for Company Fork Release? (Legal Verdict)",
    "Subscription Models Vailable",
    "Selected Subscription Model",
    "Reason of selecting this subscription model",
    "Category",
    "Conponent Name",
    "workflow name",
    "workflow yml",
    "User Limit",
    "User / Concurrency / Usage Limits",
    "Token/Key/Secret Based access",
    "Lincese Suitable for 5 member team and reason",
    "Subscription Suitable for 5 member team and reason",
    "Required to Purchase ?",
    "Why Upstream Uses It",
    "Access Status in Fork",
    "Is It Mandatory in Fork? (Yes / No - Can be discarded)",
    "Suitable for Release from Fork? (Yes/No + Reason)",
    "Official site",
    "Purchase Link",
    "Price Link",
    "Is it suitable for release from Forked Opensource Model ? Reason",
    "why it not suitable for release from Forked Opensource Model",
    "Alternate Options for release from Forked Opensource Model",
    "Best One alternate Option for release from Forked Opensource Model (with name and version)",
    "Reson of seleting that Best One alternate Option for release from Forked Opensource Model",
    "Replaces Upstream Tool (Name of original tool if this is an alternate)",
    "issues identified in master_list",
    "List of all evidence  verified"
]

FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="00FFFFFF")
FILL_HEADER = PatternFill(start_color="001F4E79", end_color="001F4E79", fill_type="solid")
ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)

FONT_DATA = Font(name="Calibri", size=10, bold=False, color="00000000")
FILL_UPSTREAM = PatternFill(start_color="00F2F4F7", end_color="00F2F4F7", fill_type="solid")
FILL_ALTERNATE = PatternFill(start_color="00E8F5E9", end_color="00E8F5E9", fill_type="solid")

ALIGN_DATA = Alignment(horizontal="left", vertical="top", wrap_text=True)

BORDER_THIN = Border(
    left=Side(style="thin", color="00D9D9D9"),
    right=Side(style="thin", color="00D9D9D9"),
    top=Side(style="thin", color="00D9D9D9"),
    bottom=Side(style="thin", color="00D9D9D9")
)

# 1. Write Header Row
ws.row_dimensions[1].height = 28.0
for col_idx, header in enumerate(HEADERS, 1):
    cell = ws.cell(row=1, column=col_idx, value=header)
    cell.font = FONT_HEADER
    cell.fill = FILL_HEADER
    cell.alignment = ALIGN_HEADER
    cell.border = BORDER_THIN

# 2. Get Records
records = spring_boot_records.get_all_records()
print(f"Retrieved {len(records)} records to write.")

# 3. Write Data Rows
for row_idx, record in enumerate(records, 2):
    ws.row_dimensions[row_idx].height = 24.0
    rec_type = record[3] # Record Type
    fill = FILL_ALTERNATE if rec_type == "Recommended Fork Alternate" else FILL_UPSTREAM
    
    for col_idx, val in enumerate(record, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = FONT_DATA
        cell.fill = fill
        cell.alignment = ALIGN_DATA
        cell.border = BORDER_THIN

# 4. Copy Column Widths from angular
ws_ang = wb['angular']
for col_idx in range(1, 45):
    letter = get_column_letter(col_idx)
    dim_ang = ws_ang.column_dimensions[letter]
    width = dim_ang.width if dim_ang.width is not None else 50.0
    ws.column_dimensions[letter].width = width

wb.save(wb_path)
print(f"Successfully wrote {len(records)} rows to {wb_path} sheet 'spring_boot'. Max row: {ws.max_row}, Max col: {ws.max_column}")
