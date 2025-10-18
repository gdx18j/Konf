import shlex
import tkinter as tk
from tkinter import scrolledtext

APP_TITLE = "VFS REPL"

def append(text): # вывод в окно
    out.configure(state='normal')
    out.insert(tk.END, text + "\n")
    out.see(tk.END)
    out.configure(state='disabled')

def handle_command(event=None): # Enter комманда
    line = entry.get().strip() # берет текст из ввода и удаляет пробелы
    if not line:
        return
    append(f"> {line}")  # показать ввод как в терминале
    entry.delete(0, tk.END)

    # парсер аргументов (поддержка кавычек)
    try:
        parts = shlex.split(line)
    except ValueError as e:
        append(f"Ошибка парсинга: {e}")
        return

    cmd = parts[0] if parts else ""
    args = parts[1:]

    # команды-заглушки
    if cmd == "ls":
        append(f"ls: вызвана заглушка. Аргументы: {args}")
    elif cmd == "cd":
        if args:
            append(f"cd: вызвана заглушка. Перейти в: {args[0]}")
        else:
            append("cd: вызвана заглушка. Аргумент (путь) не задан")
    elif cmd == "exit":
        append("exit: завершение работы.")
        root.after(200, root.destroy)  # завершение работы через 200 тиков
    else:
        append(f"Неизвестная команда: '{cmd}'. Поддерживаемые: ls, cd, exit")

# --- GUI ---
root = tk.Tk() # создание окна
root.title(APP_TITLE)
root.geometry("700x400")

out = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20)
out.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

frame = tk.Frame(root)
frame.pack(fill=tk.X, padx=8, pady=(0,8))

entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", handle_command) # если нажать Enter вызов handle_command

btn = tk.Button(frame, text="Enter", command=handle_command) # то же самое
btn.pack(side=tk.RIGHT)

# приветственное сообщение / демонстрация motd-подобного вывода
append("Добро пожаловать в простейший VFS REPL (заглушка).")
append("Поддерживаемые команды: ls, cd, exit.")
append('Пример использования: ls "my folder"  или  cd /home/user')
append("Если в кавычках ошибка — увидите сообщение об ошибке парсинга.\n")

entry.focus_set() # курсор в поле ввода сразу
root.mainloop() # Главный цикл tkinter. Работа пока окно не закрыто
