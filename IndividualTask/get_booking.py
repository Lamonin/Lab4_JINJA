from jinja2 import Template
import sqlite3
from booking_model import *

# устанавливаем соединение с базой данных (базу данных взять из ЛР 1)
conn = sqlite3.connect("booking.sqlite")

# Получаем данные из базы данных
# t = get_guest_booking_status(conn, status_name="Проживал(а)")
guest_index = 0
status_index = 0

guests_list = get_guests(conn)
guests_list = pd.concat(
    [pd.DataFrame([["Все"]], columns=guests_list.columns), guests_list],
    ignore_index=True,
)

status_list = get_statuses(conn)
status_list = pd.concat(
    [pd.DataFrame([["Все"]], columns=status_list.columns), status_list],
    ignore_index=True,
)

booking_info = get_guest_booking_status(
    conn,
    guest_name=guests_list.iloc[(guest_index, 0)] if guest_index != 0 else None,
    status_name=status_list.iloc[(status_index, 0)] if status_index != 0 else None,
)

# закрываем соединение с базой
conn.close()

# открываем шаблон из файла booking_templ.html и читаем информацию
f_template = open("booking_templ.html", "r", encoding="utf-8-sig")
html = f_template.read()
f_template.close()

# создаем объект-шаблон
template = Template(html)

# генерируем результат на основе шаблона
result_html = template.render(
    booking_info=booking_info,
    guests_list=guests_list,
    status_list=status_list,
    guest_index=guest_index,
    status_index=status_index,
    len=len,
)

# создаем файл для HTML-страницы
f = open("booking.html", "w", encoding="utf-8-sig")

# выводим сгенерированную страницу в файл
f.write(result_html)
f.close()
