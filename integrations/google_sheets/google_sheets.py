import gspread
from settings import settings
from oauth2client.service_account import ServiceAccountCredentials

from integrations.google_sheets.scoring import update_habits_and_ids
from integrations.google_sheets.accrual_fines_users import accrual_fines_users

# Настраиваем доступ к Google Sheets
def authorize_spreadsheet(worksheet: str):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    return client.open(settings.bot.SHEETS_NAME).worksheet(worksheet)


# Функция для заполнения всей таблицы
def filling_table(cache_morning: dict, cache_evening: dict):
    
    all_user_ids = update_habits_and_ids(cache_morning, cache_evening)
    accrual_fines_users(all_user_ids)