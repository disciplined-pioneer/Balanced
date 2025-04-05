import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Настраиваем доступ
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Печатаем все доступные таблицы
try:
    spreadsheets = client.openall()
    print("Список доступных таблиц:")
    for spreadsheet in spreadsheets:
        print(f"- {spreadsheet.title}")
except Exception as e:
    print(f"Ошибка подключения: {e}")


# Открываем таблицу по имени и работаем с таблицей "Ученики"
spreadsheet = client.open("Копия 04 Таблица Кураторства")
worksheet = spreadsheet.worksheet("Ученики")

# Записываем значение в ячейку
worksheet.update_cell(1, 1, "Привет мир!")
cell_value = worksheet.cell(1, 1).value
print("Значение в ячейке A1:", cell_value)