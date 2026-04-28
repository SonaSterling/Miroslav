import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

# Основное окно
root = tk.Tk()
root.title("Weather Diary")
root.geometry("700x600")  # чуть больше места, чтобы всё поместилось

# Поля ввода
tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Температура (°C):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
temp_entry = tk.Entry(root)
temp_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Описание погоды:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
weather_entry = tk.Entry(root)
weather_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Осадки (да/нет):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
precip_var = tk.StringVar(value='нет')
precip_choice = ttk.Combobox(root, textvariable=precip_var, values=['да', 'нет'], state='readonly')
precip_choice.grid(row=3, column=1, padx=5, pady=5)

# Таблица для отображения записей
columns = ('date', 'temp', 'weather', 'precip')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())
tree.grid(row=7, column=0, columnspan=4, padx=5, pady=10, sticky='nsew')

# Скроллер
scrollbar = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=7, column=4, sticky='ns')

# Кнопки
add_button = tk.Button(root, text="Добавить запись")
add_button.grid(row=4, column=0, padx=5, pady=5)

save_button = tk.Button(root, text="Сохранить в JSON")
save_button.grid(row=4, column=1, padx=5, pady=5)

load_button = tk.Button(root, text="Загрузить из JSON")
load_button.grid(row=4, column=2, padx=5, pady=5)

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.grid(row=8, column=0, columnspan=5, pady=10)

tk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5)
filter_date_entry = tk.Entry(filter_frame)
filter_date_entry.grid(row=0, column=1, padx=5)
filter_date_button = tk.Button(filter_frame, text="Фильтр по дате")
filter_date_button.grid(row=0, column=2, padx=5)

tk.Label(filter_frame, text="Фильтр по температуре (> °C):").grid(row=0, column=3, padx=5)
filter_temp_entry = tk.Entry(filter_frame)
filter_temp_entry.grid(row=0, column=4, padx=5)
filter_temp_button = tk.Button(filter_frame, text="Фильтр по температуре")
filter_temp_button.grid(row=0, column=5, padx=5)

reset_filter_button = tk.Button(filter_frame, text="Сброс фильтров")
reset_filter_button.grid(row=0, column=6, padx=5)

# Хранение данных
records = []

# Вспомогательные функции
def validate_date(d):
    try:
        datetime.strptime(d, '%Y-%m-%d')
        return True
    except:
        return False

def add_record():
    date = date_entry.get().strip()
    temp = temp_entry.get().strip()
    weather = weather_entry.get().strip()
    precip = precip_var.get()

    if not validate_date(date):
        messagebox.showerror("Ошибка", "Пожалуйста, введите правильную дату (ГГГГ-ММ-ДД).")
        return
    try:
        temp_num = float(temp)
    except:
        messagebox.showerror("Ошибка", "Температура должна быть числом.")
        return
    if not weather:
        messagebox.showerror("Ошибка", "Описание погоды не должно быть пустым.")
        return

    record = {
        'date': date,
        'temp': temp_num,
        'weather': weather,
        'precip': precip
    }
    records.append(record)
    tree.insert('', tk.END, values=(date, temp_num, weather, precip))
    # Очистить поля
    date_entry.delete(0, tk.END)
    temp_entry.delete(0, tk.END)
    weather_entry.delete(0, tk.END)
    precip_var.set('нет')

add_button.config(command=add_record)

def save_to_json():
    filename = filedialog.asksaveasfilename(defaultextension=".json",
                                             filetypes=[("JSON files", "*.json")])
    if filename:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=4)

def load_from_json():
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filename:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Очистка текущих данных
        for item in tree.get_children():
            tree.delete(item)
        records.clear()
        for rec in data:
            records.append(rec)
            tree.insert('', tk.END, values=(rec['date'], rec['temp'], rec['weather'], rec['precip']))

def filter_by_date():
    date_filter = filter_date_entry.get().strip()
    if not validate_date(date_filter):
        messagebox.showerror("Ошибка", "Некорректный формат даты.")
        return
    # Очистка и фильтрация
    for item in tree.get_children():
        tree.delete(item)
    for rec in records:
        if rec['date'] == date_filter:
            tree.insert('', tk.END, values=(rec['date'], rec['temp'], rec['weather'], rec['precip']))

def filter_by_temp():
    threshold = 0
    try:
        threshold = float(filter_temp_entry.get().strip())
    except:
        messagebox.showerror("Ошибка", "Введите число для фильтра по температуре.")
        return
    for item in tree.get_children():
        tree.delete(item)
    for rec in records:
        if rec['temp'] > threshold:
            tree.insert('', tk.END, values=(rec['date'], rec['temp'], rec['weather'], rec['precip']))

def reset_filters():
    for item in tree.get_children():
        tree.delete(item)
    for rec in records:
        tree.insert('', tk.END, values=(rec['date'], rec['temp'], rec['weather'], rec['precip']))

# Привязка кнопок к функциям
add_button.config(command=add_record)
save_button.config(command=save_to_json)
load_button.config(command=load_from_json)
filter_date_button.config(command=filter_by_date)
filter_temp_button.config(command=filter_by_temp)
reset_filter_button.config(command=reset_filters)

# Старт цикла
root.mainloop()
