from utils.message_tracking import filling_table

def main() -> None:

    import time
    start = time.time()

    cache_morning = {
        2: {'name': 'Иван', "username": "@ivan"},  # 1 1
        3: {'name': 'Максим', "username": "@maria"}, # 1 0
    }

    cache_evening = {
        2: {'name': 'Иван', "username": "@ivan"}, # 1 1
        4: {'name': 'Петя', "username": None}, # 0 1
    }

    # Гусько Гусько ID: 5; 0 0
    
    try:
        
        filling_table(cache_morning, cache_evening)

    except Exception as e:
        print(f"\nПроизошла ошибка: {e}\n")

    end = time.time()
    print(f"код работал: {(end - start):.2f}")

if __name__ == "__main__":
    main()
