"""
Generate sample contacts.xlsx for testing
Run: python make_sample.py
"""
import openpyxl
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Contacts"

headers = ["Name", "Email", "Company", "Role"]
ws.append(headers)

rows = [
    ["Manoj Rajendran", "manoj_rajendran@credang.com", "Credang", "Head of Partnerships"],
    ["Your Name",       "your@email.com",               "Your Company", "Manager"],
    ["Another Contact", "another@email.com",             "Another Co",  "Director"],
]
for row in rows:
    ws.append(row)

wb.save("contacts.xlsx")
print("contacts.xlsx created!")

