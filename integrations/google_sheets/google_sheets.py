import gspread
from settings import settings
from oauth2client.service_account import ServiceAccountCredentials


# Настраиваем доступ к Google Sheets
def authorize_spreadsheet(worksheet: str):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    return client.open(settings.bot.SHEETS_NAME).worksheet(worksheet)