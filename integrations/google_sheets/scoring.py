from itertools import zip_longest

from integrations.google_sheets.google_sheets import authorize_spreadsheet
from integrations.google_sheets.creating_header import create_header_and_apply_styles

# Добавляет в all_id недостающие user_id из cache.
def merge_ids_from_cache(cache: dict, all_id: dict) -> dict:
    existing_ids = set(all_id.values())
    added_ids = []  # Список для хранения добавленных ID

    for user_id in cache.keys():
        if user_id not in existing_ids:
            new_index = max(all_id.keys()) + 1 if all_id else 0
            all_id[new_index] = user_id
            added_ids.append(user_id)  # Добавляем новый ID в список

    return all_id, added_ids


# Обновляет историю присутствия ID на основе cache.
def update_presence_history(all_user_ids: dict, cache: dict) -> dict:

    for user_id in all_user_ids:
        if user_id in cache:
            all_user_ids[user_id].append(1)
        else:
            all_user_ids[user_id].append(0)
    return all_user_ids


# Преобразует число в букву
def number_to_excel_column(n):
    column = ""
    while n > 0:
        n -= 1
        column = chr(n % 26 + 65) + column
        n //= 26
    return column


# Получение списка всех участников
def list_all_participants() -> list:

    # Получаем колонки
    worksheet = authorize_spreadsheet("Ученики")
    h_col = worksheet.col_values(8)[3:]   # Имя
    i_col = worksheet.col_values(9)[3:]   # Фамилия
    l_col = worksheet.col_values(12)[3:]   # @username
    m_col = worksheet.col_values(13)[3:]  # TG_ID

    # Объединяем и преобразуем к спискам + фильтруем пустые строки
    combined = [
        [h, i, l, m]
        for h, i, l, m in zip_longest(h_col, i_col, l_col, m_col, fillvalue="")
        if any(cell.strip() for cell in (h, i, l, m))
    ]

    return combined


# Функция для получения информации о новых учениках по индексу.
def get_new_students(total_added_ids: list) -> list:

    # Все ученики в листе "Ученики"
    info_users = list_all_participants()
    id_students = [row[3] for row in info_users]

    # Получаем индексы новых учеников
    indices = [i for i, student_id in enumerate(id_students) if int(student_id) in total_added_ids]

    # Извлекаем информацию о новых учениках по индексам
    elements = [info_users[i] for i in indices]

    return elements


# Функция для начисления баллов
def update_habits_and_ids(cache_morning, cache_evening):

    # Создаем шапочку и применяем стили
    habits = authorize_spreadsheet("habits")
    col_date_index = create_header_and_apply_styles(habits)

    # Получаем все id в таблице
    all_col_G = habits.col_values(7)
    all_id = {i + 1: int(value) for i, value in enumerate(all_col_G) if value.isdigit()}

    # Мержим ids из кэша
    updated_all_id, added_ids_morning = merge_ids_from_cache(cache_morning, all_id)
    updated_all_id, added_ids_evening = merge_ids_from_cache(cache_evening, all_id)

    # Перезаписываем все id (добавляем новые)
    all_user_ids_values = [[str(user_id)] for user_id in list(updated_all_id.values())]
    habits.update(range_name='G5', values=all_user_ids_values)  # обновляем все id

    # Обновляем историю для утреннего и вечернего кэша (добавление 1 и 0)
    all_user_ids = {key: [] for key in updated_all_id.values()}  # user_id: []
    all_user_ids = update_presence_history(all_user_ids, cache_morning)
    all_user_ids = update_presence_history(all_user_ids, cache_evening)

    # Многомерный список и вставка данных в диапазон
    multi_dimensional_list = list(all_user_ids.values())
    habits.update(range_name=f'{number_to_excel_column(col_date_index)}5', values=multi_dimensional_list)

    # Список всех id, которые являются новыми
    total_added_ids = []
    total_added_ids.extend(added_ids_morning)
    total_added_ids.extend(added_ids_evening)

    # Получаем информацию о новых участниках и добавляем в таблицу
    info_new_users = get_new_students(total_added_ids)
    if info_new_users:
        sorted_info_new_users = sorted(info_new_users, key=lambda user: [str(i[0]) for i in all_user_ids_values].index(user[3]))
        habits.update(range_name=f'D{len(all_col_G)+1}', values=sorted_info_new_users)

    return all_user_ids
