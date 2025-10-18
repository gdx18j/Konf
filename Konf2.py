import shlex
import tkinter as tk
from tkinter import scrolledtext
import argparse # библиотека для чтения аргументов командной строки
import os # проверка, существует ли файл скрипта (os.path.exists)

# === Парсим аргументы командной строки ===
parser = argparse.ArgumentParser(description="VFS REPL Этап 2 — Конфигурация")
parser.add_argument("--vfs", type=str, default="default_vfs", help="Путь к физическому расположению VFS")
parser.add_argument("--prompt", type=str, default="vfs> ", help="Пользовательское приглашение к вводу")
parser.add_argument("--script", type=str, default=None, help="Путь к стартовому скрипту")

args = parser.parse_args()

# === Настройки ===
APP_TITLE = f"VFS REPL (вариант 17) — {args.vfs}"
PROMPT = args.prompt
SCRIPT_PATH = args.script

# === GUI функции ===
def append(text):
    """Добавляет строку в область вывода"""
    out.configure(state='normal')
    out.insert(tk.END, text + "\n")
    out.see(tk.END)
    out.configure(state='disabled')

def execute_command(line):
    """Обрабатывает одну команду"""
    line = line.strip()
    if not line:
        return

    append(f"{PROMPT}{line}")  # показываем ввод пользователя

    try:
        parts = shlex.split(line)
    except ValueError as e:
        append(f"Ошибка парсинга: {e}")
        return

    cmd = parts[0] if parts else ""
    args = parts[1:]

    # --- команды-заглушки ---
    if cmd == "ls":
        append(f"ls: вызвана заглушка. Аргументы: {args}")
    elif cmd == "cd":
        if args:
            append(f"cd: вызвана заглушка. Перейти в: {args[0]}")
        else:
            append("cd: вызвана заглушка. Аргумент (путь) не задан")
    elif cmd == "exit":
        append("exit: завершение работы.")
        root.after(300, root.destroy)
    else:
        append(f"Неизвестная команда: '{cmd}'. Поддерживаемые: ls, cd, exit")

def handle_command(event=None):
    """Вызывается при нажатии Enter или кнопки"""
    line = entry.get()
    entry.delete(0, tk.END)
    execute_command(line)

# === Создаём GUI ===
root = tk.Tk()
root.title(APP_TITLE)
root.geometry("700x400")

out = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20)
out.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

frame = tk.Frame(root)
frame.pack(fill=tk.X, padx=8, pady=(0, 8))

entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", handle_command)

btn = tk.Button(frame, text="Enter", command=handle_command)
btn.pack(side=tk.RIGHT)

# === При старте ===
append("=== VFS Эмулятор (Этап 2: Конфигурация) ===")
append(f"Параметры запуска:")
append(f"  VFS путь: {APP_TITLE}")
append(f"  Пользовательское приглашение: {PROMPT}")
append(f"  Стартовый скрипт: {SCRIPT_PATH or 'не указан'}")
append("")

# === Выполняем стартовый скрипт, если есть ===
if SCRIPT_PATH and os.path.exists(SCRIPT_PATH):
    append(f"Выполняется стартовый скрипт: {SCRIPT_PATH}")
    try:
        with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    execute_command(line)
                except Exception as e:
                    append(f"[строка {line_num}] Ошибка выполнения: {e}")
    except Exception as e:
        append(f"Ошибка чтения скрипта: {e}")
else:
    if SCRIPT_PATH:
        append(f"Файл скрипта не найден: {SCRIPT_PATH}")
append("")

append("Введите команду (ls, cd, exit):")

entry.focus_set()
root.mainloop()
