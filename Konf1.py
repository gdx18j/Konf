import tkinter as tk
from tkinter import scrolledtext
import shlex
import sys


class VFSEmulator:
    def __init__(self, root):
        self.root = root  # наше главное окно приложения
        self.root.title("VFS - Virtual File System")
        self.root.configure(bg='#2d2d2d')  # Темно-серый фон окна
        self.current_dir = "/home/user"

        # интерфейс
        self.create_interface()

        # Регистрация команд
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit
        }

        # Начальные сообщения
        self.output_area.insert(tk.END, "Добро пожаловать в VFS эмулятор!\n")
        self.output_area.insert(tk.END, f"Текущая директория: {self.current_dir}\n")
        self.output_area.insert(tk.END, "Введите 'exit' для выхода\n\n")
        self.output_area.see(tk.END)

    def create_interface(self):
        # Область вывода - темная тема с приятными цветами
        self.output_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            width=80,
            height=20,
            bg='#1e1e1e',  # Темный фон
            fg='#d4d4d4',  # Светло-серый текст
            insertbackground='#569cd6',  # Голубой курсор
            selectbackground='#264f78',  # Темно-синий выделенный текст
            font=('Consolas', 10)  # Красивый моноширинный шрифт
        )
        self.output_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_area.config(state=tk.DISABLED)

        # Поле ввода
        input_frame = tk.Frame(self.root, bg='#2d2d2d')
        input_frame.pack(padx=10, pady=5, fill=tk.X)

        self.input_entry = tk.Entry(
            input_frame,
            bg='#252526',  # Темный фон
            fg='#cccccc',  # Светлый текст
            insertbackground='#569cd6',  # Голубой курсор
            selectbackground='#264f78',  # Темно-синий выделенный текст
            font=('Consolas', 12),
            width=70,
            relief='flat',  # Плоский стиль
            highlightthickness=1,
            highlightcolor='#569cd6',
            highlightbackground='#3e3e42'
        )
        self.input_entry.pack(fill=tk.X, expand=True)
        self.input_entry.bind('<Return>', self.execute_command)
        self.input_entry.focus()

    def execute_command(self, event):
        command_line = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not command_line:
            return

        # Показ введенной команды
        self.display_command(command_line)

        try:
            # Парсинг аргументов с учетом кавычек
            parts = shlex.split(command_line)  # парсинг элемент, обрабатывает кавычки
            cmd = parts[0].lower()  # первое слово - команда в нижнем регистре!!!
            args = parts[1:] if len(parts) > 1 else []  # все остальное аргументы

            # Выполнение команды, проверка на ошибки
            if cmd in self.commands:
                self.commands[cmd](args)
            else:
                self.display_error(f"Команда '{cmd}' не найдена")

        except ValueError as e:
            self.display_error(f"Ошибка парсинга: непарные кавычки")
        except Exception as e:
            self.display_error(f"Неожиданная ошибка: {str(e)}")

        self.output_area.see(tk.END)

    def display_command(self, command):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, f"$ {command}\n", "command")
        self.output_area.config(state=tk.DISABLED)

    def display_output(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, f"{text}\n")
        self.output_area.config(state=tk.DISABLED)

    def display_error(self, text):
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.END, f"Ошибка: {text}\n", "error")
        self.output_area.config(state=tk.DISABLED)

    # ls
    def cmd_ls(self, args):
        """Команда ls - заглушка"""
        self.display_output(f"ls: аргументы {args}")
        self.display_output("file1.txt  file2.txt  directory/")

    # cd
    def cmd_cd(self, args):
        """Команда cd - заглушка"""
        if len(args) == 0:
            new_dir = "/home/user"
        elif len(args) == 1:
            new_dir = args[0]
        else:
            self.display_error("cd: слишком много аргументов")
            return

        self.display_output(f"cd: изменение директории на {new_dir}")
        self.current_dir = new_dir
        self.display_output(f"Текущая директория: {self.current_dir}")

    # exit
    def cmd_exit(self, args):
        """Команда exit - завершение работы"""
        self.display_output("Завершение работы эмулятора...")
        self.root.after(1000, self.root.destroy)


def main():
    root = tk.Tk()
    root.geometry("700x500")

    # Устанавливаем тему, похожую на современные IDE
    root.configure(bg='#2d2d2d')

    app = VFSEmulator(root)

    app.output_area.tag_config("command", foreground="#4ec9b0")  # Бирюзовый для команд
    app.output_area.tag_config("error", foreground="#f44747")  # Красный для ошибок

    root.mainloop()


if __name__ == "__main__":
    main()
