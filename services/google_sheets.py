from datetime import datetime, timedelta
from typing import Optional, Dict
from gspread.utils import rowcol_to_a1
from gspread_formatting import format_cell_range, CellFormat


weekdays_translation = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье"
}


# Получение дня недели на русском по дате
def day_week_name(date: datetime) -> str:
    day_of_week_english = date.strftime("%A")
    day_of_week_russian = weekdays_translation.get(day_of_week_english, "Неизвестно")
    return day_of_week_russian


# Записываем шапочку
def write_header(worksheet, col_index: int) -> None:

    # Определяем дату и день недели
    current_time = datetime.now()
    one_day_ago = current_time - timedelta(days=1)
    day_week = day_week_name(one_day_ago).lower()

    # Записываем значения
    one_day_ago_str = one_day_ago.strftime("%d.%m.%Y")
    worksheet.update_cell(2, col_index, one_day_ago_str)
    worksheet.merge_cells(2, col_index, 2, col_index+1)

    worksheet.update_cell(3, col_index, day_week)
    worksheet.merge_cells(3, col_index, 3, col_index+1)

    # Записываем утро и вечер
    worksheet.update_cell(4, col_index, "Утро")
    worksheet.update_cell(4, col_index+1, "Вечер")


# Применяем стиль к диапазону (границы, фон, шрифт)
def apply_style(
        worksheet, 
        start_row: int, start_col: int, 
        end_row: int, end_col: int, 
        background_color: Optional[Dict[str, float]] = None,
        borders: Optional[Dict[str, Dict[str, int]]] = None,
        text_format: Optional[Dict[str, Optional[bool]]]=None
    ) -> None:
    start_cell = rowcol_to_a1(start_row, start_col)
    end_cell = rowcol_to_a1(end_row, end_col)

    cell_format = CellFormat(
        backgroundColor=background_color,
        borders=borders,
        textFormat=text_format
    )
    format_cell_range(worksheet, f'{start_cell}:{end_cell}', cell_format)


# Функция для создания шапочки с применением стилей
def create_header_and_apply_styles(worksheet) -> None:

    # Получаем индекс колонки для добавления
    row_values = worksheet.row_values(3)
    now_number_col = len(row_values) + 2

    # Создаем шапочку
    write_header(worksheet, now_number_col)

    # Применяем стиль: Границы
    borders = {
        'top': {'style': 'SOLID', 'width': 1},
        'right': {'style': 'SOLID', 'width': 1},
        'bottom': {'style': 'SOLID', 'width': 1},
        'left': {'style': 'SOLID', 'width': 1},
    }
    apply_style(worksheet, 4, now_number_col, 4, now_number_col+1, borders=borders)

    # Применяем стиль: Шрифт (без жирного и черный цвет)
    text_format = {'fontFamily': 'Calibri', 'bold': False, 'foregroundColor': {'red': 0, 'green': 0, 'blue': 0}}
    apply_style(worksheet, 2, now_number_col, 4, now_number_col+1, text_format=text_format)

    # Применяем стиль: Закрашивание фона
    background_color = {'red': 63/255, 'green': 171/255, 'blue': 60/255}
    apply_style(worksheet, 1, now_number_col, 1, now_number_col+1, background_color=background_color)

    print("Шапочка создана и стиль применен успешно.")
