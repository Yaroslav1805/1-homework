import os
import subprocess


# Функция для установки зависимостей
def install_dependencies():
    print("Installing dependencies...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)


# Функция для запуска проекта
def run_project():
    print("Running project...")
    subprocess.run(["python", "shell_emulator.py"], check=True)


# Функция для запуска тестов
def run_tests():
    print("Running tests...")
    subprocess.run(["python", "-m", "unittest", "discover", "-s", "tests"], check=True)


# Основное меню скрипта
if __name__ == "__main__":
    print("Build Script Options:")
    print("1. Install dependencies")
    print("2. Run project")
    print("3. Run tests")
    print("4. Clean logs")

    choice = input("Select an option: ")

    if choice == "1":
        install_dependencies()
    elif choice == "2":
        run_project()
    elif choice == "3":
        run_tests()
    elif choice == "4":
        if os.path.exists("session_log.csv"):
            os.remove("session_log.csv")
            print("Logs cleaned.")
        else:
            print("No logs to clean.")
    else:
        print("Invalid option.")
