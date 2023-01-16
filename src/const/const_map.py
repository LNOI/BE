sheet_name_input = [
     "1. CUSTOMER",
    "2. SCRA",
    "3. NETTING",
    "4. COLLATERAL",
    "5. GUARANTEE",
    "OD",
    "CC",
    "6. EXPOSURE",
    "7. REG TABLE",
    "8. MAPPING TABLE",
    "9. REG TABLE CAL",
    "10. ASSET MAPPING"
]

sheet_name_output = [
    "1. CUSTOMER",
    "2. SCRA",
    "3. NETTING",
    "4. COLLATERAL",
    "5. GUARANTEE",
    "OD",
    "CC",
    "6. EXPOSURE",
    "7. REG TABLE",
    "8. MAPPING TABLE",
    "9. REG TABLE CAL",
    "10. ASSET MAPPING",
    "11. CREDIT RISK OUTPUT"
]

map_customer = {
    "CPTY_TYPE_1" :"CPTY_TYPE",
    "CPTY_SUB_TYPE_1":"CPTY_SUB_TYPE"
}
map_scra = {'Unnamed: 0': '',
 'Note: This is an example taken. The Bank needs to input the SCRA responses rowwise.': 'Note: This is an example taken. The Bank needs to input the SCRA responses rowwise.',
 'Unnamed: 2': '',
 'Unnamed: 3': '',
 'Unnamed: 4': '',
 'Unnamed: 5': '',
 'Unnamed: 6': '',
 'Unnamed: 7': '',
 'Unnamed: 8': '',
 'SCRA Group': ''}

# from openpyxl import load_workbook
# import time
# st = time.time
# wb = load_workbook("resource/data/format_output.xlsx")
# print(time.time())