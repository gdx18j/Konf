VFS REPL (вариант №17)

Эмулятор командной строки UNIX-подобной ОС с виртуальной файловой системой (VFS).
Работает через графический интерфейс.

Команды:
ls       - показать содержимое папки
cd <dir> - перейти в папку
tree     - показать дерево файлов
history  - история введённых команд
rev <текст> - перевернуть текст
rmdir <папка> - удалить пустую папку
exit     - выход из программы

Запуск:
python vfs_repl_v5.py --vfs vfs.zip --script test5.txt

test5.txt - пример скрипта с командами для тестирования.
vfs.zip   - архив виртуальной файловой системы.


=== VFS Эмулятор (Этап 4: Основные команды) == VFS успешно загружена: myvfs.zip
Выполняется стартовый скрипт: test3.txt
user@vfs> 1s
testvfs
user@vfs> cd testvfs
Текущая директория: /testvfs/
user@vfs> cd non_folder
Ошибка: путь '/testvfs/non_folder' не найден.
user@vfs> cd /
Текущая директория: /
user@vfs> cd testvfs
Текущая директория: /testvfs/
user@vfs> cd home
Текущая директория: /testvfs/home/
user@vfs> 1s
guest
user
user@vfs> tree
Дерево папки /testvfs/home/:
guest
- guest.txt
user
- readme.md
user@vfs> rev "hello world"
dirow olleh
exit
