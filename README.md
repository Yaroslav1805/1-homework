https://github.com/Yaroslav1805/1-homework

Shell Emulator

Эмулятор командной оболочки с графическим интерфейсом (GUI), поддерживающий работу с виртуальной файловой системой. Подходит для выполнения базовых команд UNIX, таких как ls, cd, find, whoami, date, и exit. Логирование действий осуществляется в формате CSV.

Проект — это эмулятор командной оболочки, предназначенный для выполнения базовых файловых операций внутри виртуальной файловой системы. Основные особенности:

![Снимок экрана (259)](https://github.com/user-attachments/assets/12f53e7a-bb9e-47ed-b5b2-eb029bee44b5)

Загрузка виртуальной файловой системы из TAR-архива.
Поддержка команд UNIX.
Логирование всех действий в CSV-файл с указанием времени и даты.
Удобный GUI для взаимодействия.
Автоматическая сборка и тестирование через скрипты.

ls - Отображает содержимое текущей директории.
cd - Меняет текущую директорию на указанную.
find - Осуществляет поиск файла или директории по названию.
whoami - Возвращает имя текущего пользователя.
date - Показывает текущую дату и время.
exit- Завершает работу эмулятора.

Файлы конфигурации
config.ini:

Путь к архиву виртуальной файловой системы.
Путь к лог-файлу.

[Settings]
filesystem_path = C:\Users\Haier\PycharmProjects\pythonProject5\virtual_fs.tar
log_path = C:\Users\Haier\PycharmProjects\pythonProject5\session_log.csv

requirements.txt - список зависимостей, необходимых для работы проекта.
Установите зависимости, указанные в requirements.txt: pip install -r requirements.txt
Сборка проекта
Автоматическая сборка выполняется через build.py. Запустите скрипт и выберите действие: python build.py

Доступные опции:
Установка зависимостей.
Запуск программы.
Прогон тестов.
Очистка логов.
Ручной запуск программы, если требуется запустить программу напрямую: python shell_emulator.py

Для проверки корректности работы были написаны автоматические тесты. Результаты:

python build.py
Выберите "3" для запуска тестов

test_cd_command (tests.test_shell_emulator.TestShellEmulator) ... OK
test_ls_command (tests.test_shell_emulator.TestShellEmulator) ... OK
test_find_command (tests.test_shell_emulator.TestShellEmulator) ... OK
test_date_command (tests.test_shell_emulator.TestShellEmulator) ... OK

----------------------------------------------------------------------
Ran 4 tests in 0.002s

Все тесты успешно пройдены. Логика работы проекта проверена.

