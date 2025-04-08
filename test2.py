from integrations.google_sheets.scoring import update_habits_and_ids


def main() -> None:


    user_id = 123456789
    cache_morning = {
        2: {'name': 'Иван', 'score': 42, "username": None},
        3: {'name': 'Мария', 'score': 88, "username": None},
        4: {'name': 'Алексей', 'score': 76, "username": None},
        5: {'name': 'Наталья', 'score': 95, "username": None},
        6: {'name': 'Игорь', 'score': 67, "username": None},
        7: {'name': 'Ольга', 'score': 82, "username": None},
        8: {'name': 'Сергей', 'score': 50, "username": None},
        9: {'name': 'Елена', 'score': 91, "username": None},
        10: {'name': 'Константин', 'score': 60, "username": None},
        11: {'name': 'Марина', 'score': 74, "username": None},
        12: {'name': 'Дмитрий', 'score': 80, "username": None}
    }

    cache_evening = {
        2: {'name': 'Иван', 'score': 42, "username": "@ivan"},  # Повтор с morning
        3: {'name': 'Мария', 'score': 88, "username": "@maria"},  # Повтор с morning
        13: {'name': 'Татьяна', 'score': 65, "username": None},
        15: {'name': 'Роман', 'score': 55, "username": None},
        5: {'name': 'Наталья', 'score': 95, "username": "@natasha"},  # Повтор с morning
        17: {'name': 'Юлия', 'score': 72, "username": None},
        18: {'name': 'Светлана', 'score': 77, "username": None},
        123456789: {'name': 'Александр', 'score': 90, "username": "@alexandr"},
        19: {'name': 'Владимир', 'score': 60, "username": None},
        20: {'name': 'Алексей', 'score': 76, "username": "@alexey"}  # Повтор с morning
    }

    
    try:
    
        all_user_ids = update_habits_and_ids(cache_morning, cache_evening)
        print(all_user_ids)

 
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}\n")

if __name__ == "__main__":
    main()
