
import json  # импорт модуля для работы с JSON
import mysql.connector  # импорт модуля для работы с базой данных MySQL


with open('true.json') as json_file:  # открытие JSON-файла и чтение его содержимого
    data = json.load(json_file)  # загрузка содержимого файла в переменную data в формате JSON


columns = []  # создание пустого списка для хранения данных из JSON-файла
for item in data:  # перебор элементов в переменной data
    ip_address = item.split(' - - ')[0]  # получение IP-адреса из строки лога
    request_time = item.split('[')[1].split(']')[0]  # получение времени запроса из строки лога
    status_code = item.split('" ')[1].split(' ')[0]  # получение кода статуса HTTP-ответа из строки лога
    user_agent = item.split('"')[len(item.split('"'))-2]  # получение информации о браузере из строки лога
    columns.append((ip_address, request_time, status_code, user_agent))  # добавление данных в список


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Savser2004",
    database="test"
)  # подключение к базе данных MySQL с именем test


c = conn.cursor()  # создание курсора для работы с базой данных


c.execute('''CREATE TABLE IF NOT EXISTS my_table
             (ip_address TEXT, request_time TEXT, status_code TEXT, user_agent TEXT)''')  # создание таблицы my_table, если она не существует


c.executemany('INSERT INTO my_table VALUES (%s, %s, %s, %s)', columns)  # добавление данных из списка в таблицу


# Сохранение изменений и закрытие соединения с базой данных
conn.commit()  # сохранение изменений
conn.close()  # закрытие соединения с базой данных












# Импортируем необходимые библиотеки
import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import font

# Функция для фильтрации данных
def filter_data():
    # Получаем ключевое слово из поля ввода и удаляем лишние пробелы
    keyword = entry_filter.get().strip()
    
    # Очищаем таблицу перед отображением новых результатов
    tree.delete(*tree.get_children())
    
    # Устанавливаем соединение с базой данных
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Savser2004",
        database="test"
    )
    cursor = connection.cursor()
    
    # Выполняем запрос на выборку данных с учетом ключевого слова
    cursor.execute("SELECT * FROM my_table WHERE ip_address LIKE %s OR request_time LIKE %s OR status_code LIKE %s OR user_agent LIKE %s",
                   ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    
    # Отображаем результаты выборки в таблице
    for row in rows:
        tree.insert("", tk.END, text="", values=row)
    
    # Закрываем соединение с базой данных
    connection.close()

# Создаем главное окно приложения
root = tk.Tk()
root.title("my_table Data")
root.geometry("800x400")

# Создаем фрейм для фильтрации данных
frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

# Добавляем метку и поле ввода для фильтрации данных
label_filter = tk.Label(frame_filter, text="фильтрация по любому из столбцов:", font=("Arial", 14))
label_filter.pack(side=tk.LEFT)

entry_filter = tk.Entry(frame_filter, font=("Arial", 14))
entry_filter.pack(side=tk.LEFT, padx=5)

# Добавляем кнопку для применения фильтра
button_filter = tk.Button(frame_filter, text="применить фильтр", font=("Arial", 14), command=filter_data)
button_filter.pack(side=tk.LEFT)

# Создаем таблицу для отображения данных
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12), background="#D3D3D3", foreground="black")
style.configure("Treeview.Heading", font=("Arial", 14), background="#A9A9A9", foreground="white")

tree = ttk.Treeview(root)
tree["columns"] = ("ip_address", "request_time", "status_code", "user_agent")
tree.column("#0", width=0, stretch=tk.NO)
tree.column("ip_address", anchor=tk.CENTER, width=120)
tree.column("request_time", anchor=tk.CENTER, width=120)
tree.column("status_code", anchor=tk.CENTER, width=80)
tree.column("user_agent", anchor=tk.CENTER, width=180)

tree.heading("#0", text="")
tree.heading("ip_address", text="IP Address")
tree.heading("request_time", text="Request Time")
tree.heading("status_code", text="Status Code")
tree.heading("user_agent", text="User Agent")

tree.pack(fill=tk.BOTH, expand=True)

# Устанавливаем соединение с базой данных
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Savser2004",
    database="test"
)
cursor = connection.cursor()

# Выполняем запрос на выборку всех данных из таблицы и отображаем их в таблице
cursor.execute("SELECT * FROM my_table")
rows = cursor.fetchall()

for row in rows:
    tree.insert("", tk.END, text="", values=row)

# Закрываем соединение с базой данных
connection.close()

# Запускаем главный цикл приложения
root.mainloop()