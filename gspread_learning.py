import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('IGUA_DRIVE_SECRET.json', scope)
gc = gspread.authorize(credentials)

# wks = gc.open("Where is the money Lebowski?").sheet1

sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1XzZeGav7xOc-Vvhuq6aCoox_dsWTQruLx04xkl_SBbg/edit?usp=drive_web&ouid=106328115973184488048')
worksheet = sheet.get_worksheet(0)
worksheet.update_acell('B2', "it's down there somewhere, let me take another look.")

# Fetch a cell range
cell_list = worksheet.range('A1:B7')
print(cell_list)

# Open a worksheet from spreadsheet with one shot
# wks = gc.open("Where is the money Lebowski?").sheet1
