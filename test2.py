from integrations.google_sheets.scoring import update_habits_and_ids
from integrations.google_sheets.accrual_fines_users import accrual_fines_users


def main() -> None:

    import time
    start = time.time()

    cache_morning = {
        21: {'name': 'Иван', 'score': 42, "username": None},
        34: {'name': 'Мария', 'score': 88, "username": None},
        45: {'name': 'Алексей', 'score': 76, "username": None},
        21: {'name': 'Наталья', 'score': 95, "username": None},
        6: {'name': 'Игорь', 'score': 67, "username": None},
        24: {'name': 'Ольга', 'score': 82, "username": None},
        38: {'name': 'Сергей', 'score': 50, "username": None},
        18: {'name': 'Елена', 'score': 91, "username": None},
        21: {'name': 'Константин', 'score': 60, "username": None},
        47: {'name': 'Марина', 'score': 74, "username": None},
        35: {'name': 'Дмитрий', 'score': 80, "username": None}
    }

    cache_evening = {
        21: {'name': 'Иван', 'score': 42, "username": "@ivan"},  # Повтор с morning
        3: {'name': 'Мария', 'score': 88, "username": "@maria"},  # Повтор с morning
        13: {'name': 'Татьяна', 'score': 65, "username": None},
        24: {'name': 'Роман', 'score': 55, "username": None},
        5: {'name': 'Наталья', 'score': 95, "username": "@natasha"},  # Повтор с morning
        17: {'name': 'Юлия', 'score': 72, "username": None},
        18: {'name': 'Светлана', 'score': 77, "username": None},
        47: {'name': 'Александр', 'score': 90, "username": "@alexandr"},
        19: {'name': 'Владимир', 'score': 60, "username": None},
        20: {'name': 'Алексей', 'score': 76, "username": "@alexey"}  # Повтор с morning
    }

    
    try:
        
        # Заполняем все ячейки данными
       all_user_ids = update_habits_and_ids(cache_morning, cache_evening)
       for key, value in all_user_ids.items():
           print(key, value)
       accrual_fines_users(all_user_ids)

    except Exception as e:
        print(f"\nПроизошла ошибка: {e}\n")

    end = time.time()
    print(f"код работал: {end - start}")

if __name__ == "__main__":
    main()
