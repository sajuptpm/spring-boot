import openpyxl

wb = openpyxl.load_workbook('workflow-fixes/data1.xlsx', data_only=True)
ws = wb['spring_boot']

print(f"Sheet dimensions: max_row={ws.max_row}, max_column={ws.max_column}")

# 1. Header check
headers = [ws.cell(1, c).value for c in range(1, 45)]
print(f"Headers count: {len(headers)}")
for i, h in enumerate(headers, 1):
    if not h:
        print(f"ERROR: Header {i} is empty!")

# 2. Check empty cells in data rows
empty_cells = []
for r in range(2, ws.max_row + 1):
    for c in range(1, 45):
        val = ws.cell(r, c).value
        if val is None or val == "":
            empty_cells.append((r, c, headers[c-1]))

print(f"Total empty data cells across 84 rows x 44 columns: {len(empty_cells)}")
if empty_cells:
    for r, c, h in empty_cells[:10]:
        print(f"  Empty at Row {r}, Col {c} ({h})")

# 3. Check Record Type counts
upstream_count = 0
alternate_count = 0
for r in range(2, ws.max_row + 1):
    rec_type = ws.cell(r, 4).value
    if rec_type == 'Upstream Original Tool':
        upstream_count += 1
    elif rec_type == 'Recommended Fork Alternate':
        alternate_count += 1
    else:
        print(f"Unknown record type at row {r}: {rec_type}")

print(f"Record Types: Upstream={upstream_count}, Alternates={alternate_count}, Total={upstream_count + alternate_count}")

# 4. Check Workflows covered
wfs = set(ws.cell(r, 22).value for r in range(2, ws.max_row + 1))
print(f"Workflows covered ({len(wfs)}):")
for w in sorted(wfs):
    print(f"  - {w}")

# 5. Check PO / Quote requirement breakdown
po_col = 29 # Required to Purchase ?
po_counts = {}
for r in range(2, ws.max_row + 1):
    val = ws.cell(r, po_col).value
    po_counts[val] = po_counts.get(val, 0) + 1

print("\nRequired to Purchase Breakdown:")
for k, v in sorted(po_counts.items()):
    print(f"  {k}: {v}")

# 6. Check Legal Verdict breakdown
legal_col = 16 # Permissible for Company Fork Release?
legal_counts = {}
for r in range(2, ws.max_row + 1):
    val = ws.cell(r, legal_col).value
    legal_counts[val] = legal_counts.get(val, 0) + 1

print("\nLegal Verdict Breakdown:")
for k, v in sorted(legal_counts.items()):
    print(f"  {k}: {v}")
