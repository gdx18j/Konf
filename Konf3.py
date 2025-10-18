import shlex
import tkinter as tk
from tkinter import scrolledtext
import argparse
import zipfile
import io
import os

# === Парсер аргументов командной строки ===
parser = argparse.ArgumentParser(description="VFS REPL Этап 3 — Виртуальная файловая система")
parser.add_argument("--vfs", type=str, required=True, help="Путь к ZIP-файлу виртуальной файловой системы")
parser.add_argument("--prompt", type=str, default="vfs> ", help="Пользовательское приглашение к вводу")
parser.add_argument("--script", type=str, default=None, help="Путь к стартовому скрипту")

args = parser.parse_args()

APP_TITLE = f"VFS REPL (вариант 17) — {args.vfs}"
PROMPT = args.prompt
SCRIPT_PATH = args.script
VFS_PATH = args.vfs

# === Хранилище виртуальной файловой системы ===
vfs = {}
current_dir = "/"


def append(text):
    """Добавляет текст в окно вывода"""
    out.configure(state="normal")
    out.insert(tk.END, text + "\n")
    out.see(tk.END)
    out.configure(state="disabled")


# === Загрузка VFS ===
def load_vfs(zip_path):
    """Загружает ZIP-файл в память"""
    global vfs
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                vfs[name] = zf.read(name)  # сохраняем содержимое файлов в память
        append(f"VFS успешно загружена: {zip_path}")
        return True
    except FileNotFoundError:
        append(f"Ошибка: файл VFS '{zip_path}' не найден.")
    except zipfile.BadZipFile:
        append(f"Ошибка: '{zip_path}' не является корректным ZIP-архивом.")
    except Exception as e:
        append(f"Ошибка загрузки VFS: {e}")
    return False


# === Выполнение одной команды ===
def execute_command(line):
    global current_dir  # ДОБАВЛЕНО: объявляем current_dir как глобальную переменную

    line = line.strip()
    if not line:
        return

    append(f"{PROMPT}{line}")

    try:
        parts = shlex.split(line)
    except ValueError as e:
        append(f"Ошибка парсинга: {e}")
        return

    cmd = parts[0] if parts else ""
    args = parts[1:]

    # === команды ===
    if cmd == "ls":
        prefix = current_dir.strip("/")
        if prefix:
            prefix += "/"

        seen = set()
        for path in vfs.keys():
            if path.startswith(prefix):
                rest = path[len(prefix):]
                part = rest.split("/")[0]
                if part:
                    seen.add(part)

        if seen:
            for name in sorted(seen):
                append(name)
        else:
            append("Папка пуста.")

    elif cmd == "cd":
        if not args:
            append("Ошибка: не указан путь.")
            return

        target = args[0].strip("/")
        if target == "":
            current_dir = "/"
            append("Текущая директория: /")
            return

        if current_dir.strip("/"):
            full_path = f"{current_dir.strip('/')}/{target}"
        else:
            full_path = target

        # проверяем, есть ли такой путь (папка)
        found = any(
            path.startswith(full_path + "/") or path == full_path
            for path in vfs.keys()
        )

        if found:
            current_dir = "/" + full_path.strip("/") + "/"
            append(f"Текущая директория: {current_dir}")
        else:
            append(f"Ошибка: путь '{current_dir}{target}' не найден.")

    elif cmd == "exit":
        append("exit: завершение работы.")
        root.after(300, root.destroy)

    else:
        append(f"Неизвестная команда: '{cmd}'. Доступные: ls, cd, exit")


# === Обработчик ввода ===
def handle_command(event=None):
    line = entry.get()
    entry.delete(0, tk.END)
    execute_command(line)


# === GUI ===
root = tk.Tk()
root.title(APP_TITLE)
root.geometry("750x450")

out = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20)
out.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

frame = tk.Frame(root)
frame.pack(fill=tk.X, padx=8, pady=(0, 8))

entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", handle_command)

btn = tk.Button(frame, text="Enter", command=handle_command)
btn.pack(side=tk.RIGHT)

# === Загрузка VFS ===
append("=== VFS Эмулятор (Этап 3: Виртуальная ФС) ===")
if not load_vfs(VFS_PATH):
    append("Ошибка: не удалось загрузить VFS. Работа невозможна.")
else:
    # --- motd ---
    if "motd" in vfs:
        append("--- motd ---")
        append(vfs["motd"].decode("utf-8", errors="ignore"))
        append("-------------")

    # --- выполняем стартовый скрипт ---
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
    elif SCRIPT_PATH:
        append(f"Файл скрипта не найден: {SCRIPT_PATH}")

append("")
append("Введите команду (ls, cd, exit):")

entry.focus_set()
root.mainloop()