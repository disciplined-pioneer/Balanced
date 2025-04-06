from services.google_sheets import create_header_and_apply_styles
from integrations.google_sheets import authorize_spreadsheet

def main() -> None:
    habits = authorize_spreadsheet("habits")

    # Создаем шапочку и применяем стили
    create_header_and_apply_styles(habits)

if __name__ == "__main__":
    main()
