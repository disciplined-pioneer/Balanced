from integrations.google_sheets.scoring import get_students
from integrations.google_sheets.google_sheets import authorize_spreadsheet


# Функция для начисления штрафов
def accrual_fines_users(all_user_ids: dict) -> None:
    fine = authorize_spreadsheet("fine")

    # Получаем всех текущих должников
    all_id_fine = fine.col_values(4)
    all_id_fine = [int(item) for item in all_id_fine if item.isdigit()]

    # Штрафы по логике: user_id -> количество штрафов
    user_fines = {}
    for user_id, statuses in all_user_ids.items():
        # Отладочный вывод
        print(f"Пользователь {user_id} с состоянием {statuses}")

        if statuses == [0, 0]:  # два нуля → 2 штрафа
            user_fines[user_id] = 2
            print(f"Пользователю {user_id} начислено 2 штрафа")
        elif statuses == [0, 1] or statuses == [1, 0]:  # один ноль → 1 штраф
            user_fines[user_id] = 1
            print(f"Пользователю {user_id} начислен 1 штраф")
        elif statuses == [1, 1]:  # два единичных значения → без штрафов
            print(f"Пользователю {user_id} штраф не начисляется (статус [1, 1])")
        else:
            print(f"Неопределённый статус для пользователя {user_id}: {statuses}")

    # Новые должники, которых ещё нет в таблице
    new_debtors = list(set(user_fines.keys()) - set(all_id_fine))
    new_debtors_info = get_students(new_debtors)

    # Добавляем их с долгом 0
    new_debtors_info = [row + [0] for row in new_debtors_info]
    if new_debtors_info:
        fine.update(range_name=f'A{len(all_id_fine) + 2}', values=new_debtors_info)
        all_id_fine += new_debtors  # чтобы индексы были корректны

    # Считываем долги
    amount_fine = fine.col_values(5)
    int_all_fines = [int(item) if item.isdigit() else 0 for item in amount_fine]

    # Начисляем штрафы
    for user_id, count in user_fines.items():
        if user_id in all_id_fine:
            index = all_id_fine.index(user_id)
            int_all_fines[index] += count * 100  # штрафы

    # Обновляем таблицу
    formatted = [[val] for val in int_all_fines]
    fine.update(range_name='E2', values=formatted)
    fine.update(range_name='G2', values=formatted)

