import gspread
from config.config import FORMS
# Connect the google spread sheet
gc = gspread.service_account(filename='service_account.json')

def get_worksheet(excel_name, sheet_name):
    sh = gc.open(excel_name)
    worksheet = sh.worksheet(sheet_name)

    return worksheet