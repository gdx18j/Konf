import shlex
import tkinter as tk
from tkinter import scrolledtext
import argparse
import zipfile
import io
import os

# === Парсер аргументов командной строки ===
parser = argparse.ArgumentParser(description="VFS REPL Этап 4 — Основные команды")
parser.add_argument("--vfs", type=str, required=True, help="Путь к ZIP-файлу виртуальной файловой системы")
parser.add_argument("--prompt", type=str, default="vfs> ", help="Пользовательское приглашение к вводу")
parser.add_argument("--script", type=str, default=None, help="Путь к стартовому скрипту")

args = parser.parse_args()

APP_TITLE = f"VFS REPL — {args.vfs}"
PROMPT = args.prompt
SCRIPT_PATH = args.script
VFS_PATH = args.vfs

# === Хранилище виртуальной файловой системы ===
vfs = {}
current_dir = "/"
history = []  # для команды history

def append(text):
    """Добавляет текст в окно вывода"""
    out.configure(state="normal")
    out.insert(tk.END, text + "\n")
    out.see(tk.END)
    out.configure(state="disabled")


# === Загрузка VFS ===
def load_vfs(zip_path):
    global vfs
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                vfs[name] = zf.read(name)
        append(f"VFS успешно загружена: {zip_path}")
        return True
    except FileNotFoundError:
        append(f"Ошибка: файл VFS '{zip_path}' не найден.")
    except zipfile.BadZipFile:
        append(f"Ошибка: '{zip_path}' не является корректным ZIP-архивом.")
    except Exception as e:
        append(f"Ошибка загрузки VFS: {e}")
    return False


# === Вспомогательные функции ===
def list_dir(path):
    """Возвращает список элементов текущей папки"""
    prefix = path.strip("/")
    if prefix:
        prefix += "/"
    seen = set()
    for p in vfs.keys():
        if p.startswith(prefix):
            rest = p[len(prefix):]
            part = rest.split("/")[0]
            if part:
                seen.add(part)
    return sorted(seen)

def tree_dir(path, prefix=""):
    """Рекурсивный вывод дерева каталогов"""
    items = list_dir(path)
    for i, item in enumerate(items):
        connector = "└── " if i == len(items)-1 else "├── "
        append(prefix + connector + item)
        full_path = f"{path.strip('/')}/{item}" if path != "/" else item
        # если есть вложенные файлы/папки
        if any(p.startswith(full_path + "/") for p in vfs.keys()):
            new_prefix = prefix + ("    " if i == len(items)-1 else "│   ")
            tree_dir("/" + full_path, new_prefix)


# === Выполнение одной команды ===
def execute_command(line):
    global current_dir
    line = line.strip()
    if not line:
        return

    append(f"{PROMPT}{line}")
    history.append(line)

    try:
        parts = shlex.split(line)
    except ValueError as e:
        append(f"Ошибка парсинга: {e}")
        return

    cmd = parts[0] if parts else ""
    args = parts[1:]

    # === команды ===
    if cmd == "ls":
        items = list_dir(current_dir)
        if items:
            for name in items:
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
        full_path = f"{current_dir.strip('/')}/{target}" if current_dir.strip("/") else target
        found = any(path.startswith(full_path + "/") or path == full_path for path in vfs.keys())
        if found:
            current_dir = "/" + full_path.strip("/") + "/"
            append(f"Текущая директория: {current_dir}")
        else:
            append(f"Ошибка: путь '{current_dir}{target}' не найден.")

    elif cmd == "tree":
        append(f"Дерево папки {current_dir}:")
        tree_dir(current_dir)

    elif cmd == "history":
        for idx, h in enumerate(history, 1):
            append(f"{idx}: {h}")

    elif cmd == "rev":
        if not args:
            append("Ошибка: не указан текст для реверса.")
        else:
            reversed_text = " ".join(args)[::-1]
            append(reversed_text)

    elif cmd == "exit":
        append("exit: завершение работы.")
        root.after(300, root.destroy)

    else:
        append(f"Неизвестная команда: '{cmd}'. Доступные: ls, cd, tree, history, rev, exit")


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
append("=== VFS Эмулятор (Этап 4: Основные команды) ===")
if not load_vfs(VFS_PATH):
    append("Ошибка: не удалось загрузить VFS. Работа невозможна.")
else:
    if "motd" in vfs:
        append("--- motd ---")
        append(vfs["motd"].decode("utf-8", errors="ignore"))
        append("-------------")

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
append("Введите команду (ls, cd, tree, history, rev, exit):")

entry.focus_set()
root.mainloop()
