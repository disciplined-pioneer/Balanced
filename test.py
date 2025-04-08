from services.google_sheets.google_sheets import create_header_and_apply_styles
from integrations.google_sheets.google_sheets import authorize_spreadsheet


from services.google_sheets.google_sheets import *
def main() -> None:

    

    user_id = 123456789
    cache_morning = {
        user_id: {'name': 'Иван', 'score': 42, "username": None},
        356730193: {'name': 'Алексей', 'score': 73, "username": "@киса"},
        user_id-1: {'name': 'Мария', 'score': 88, "username": None},
        380601733: {'name': 'Мария', 'score': 88, "username": "@собака"}
    }


    # Создаем шапочку и применяем стили
    habits = authorize_spreadsheet("habits")
    students = authorize_spreadsheet("Ученики")
    col_date_index = create_header_and_apply_styles(habits)
    

    try:

        # Проходим по всем элементам кэша
        count = 0
        all_col = habits.col_values(7)
        for key in cache_morning:
            if str(key) in all_col:
                num_row_id = all_col.index(str(key)) + 1  # Если пользователь есть
            else:
                count += 1
                num_row_id = len(all_col) + count  # Если пользователя нет
                habits.update_cell(num_row_id, 7, str(key))  # Добавляем id

            # Получаем строку из students по ключу (если существует)
            num_row_students = find_row_by_value(students, 13, str(key))

            # Получаем имя и фамилию
            if num_row_students is not None:
                
                name = students.cell(num_row_students, 8).value
                surname = students.cell(num_row_students, 9).value
                telegram = cache_morning[key]["username"]

                habits.update_cell(num_row_id, 4, name)   # Обновляем имя
                habits.update_cell(num_row_id, 5, surname)  # Обновляем фамилию
                habits.update_cell(num_row_id, 6, telegram)   # Обновляем телеграм

            # Обновляем ячейку по найденному индексу (для даты)
            habits.update_cell(num_row_id, col_date_index, 1)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
