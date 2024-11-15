# import os
# import tarfile
# import configparser
# import csv
# from datetime import datetime
# import tkinter as tk
# from tkinter import scrolledtext
#
# class ShellEmulator:
#     def __init__(self, config_file):
#         self.load_config(config_file)
#         self.setup_logging()
#         self.load_virtual_fs()
#         self.current_path = "/"
#         self.username = os.getlogin()
#
#     def load_config(self, config_file):
#         config = configparser.ConfigParser()
#         config.read(config_file)
#         self.fs_archive_path = config['Paths']['virtual_fs_archive']
#         self.log_file_path = config['Paths']['log_file']
#
#     def setup_logging(self):
#         with open(self.log_file_path, 'w', newline='') as csvfile:
#             log_writer = csv.writer(csvfile)
#             log_writer.writerow(['Datetime', 'Command', 'Output'])
#
#     def log_action(self, command, output):
#         with open(self.log_file_path, 'a', newline='') as csvfile:
#             log_writer = csv.writer(csvfile)
#             log_writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), command, output])
#
#     def load_virtual_fs(self):
#         self.virtual_fs = {}
#         with tarfile.open(self.fs_archive_path, 'r') as tar:
#             for member in tar.getmembers():
#                 self.virtual_fs[member.name] = member
#
#     def list_dir(self, path):
#         result = "\n".join([name for name in self.virtual_fs if name.startswith(path) and '/' not in name[len(path)+1:]])
#         self.log_action("ls " + path, result)
#         return result
#
#     def change_dir(self, path):
#         if path in self.virtual_fs:
#             self.current_path = path
#             result = f"Changed directory to {path}"
#         else:
#             result = f"No such directory: {path}"
#         self.log_action("cd " + path, result)
#         return result
#
#     def find(self, filename):
#         result = "\n".join([name for name in self.virtual_fs if filename in name])
#         self.log_action("find " + filename, result)
#         return result
#
#     def whoami(self):
#         result = self.username
#         self.log_action("whoami", result)
#         return result
#
#     def get_date(self):
#         result = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         self.log_action("date", result)
#         return result
#
#     def cd_command(self, path):
#         if path == "/":
#             self.current_directory = "/"  # Установите текущую директорию в корень
#         elif path in self.file_system[self.current_directory]:  # Проверка наличия директории
#             self.current_directory = path
#         else:
#             print(f"No such directory: {path}")
#
#     def exit_shell(self):
#         self.log_action("exit", "Shell exited")
#         self.root.destroy()
#
#     def execute_command(self, command):
#         parts = command.split()
#         if not parts:
#             return ""
#
#         cmd = parts[0]
#         args = parts[1:]
#
#         if cmd == "ls":
#             return self.list_dir(self.current_path)
#         elif cmd == "cd":
#             return self.cd_command(self.current_path)
#             #return self.change_dir(args[0] if args else "/")
#         elif cmd == "find":
#             return self.find(args[0] if args else "")
#         elif cmd == "whoami":
#             return self.whoami()
#         elif cmd == "date":
#             return self.get_date()
#         elif cmd == "exit":
#             self.exit_shell()
#             return "Exiting shell..."
#         else:
#             return f"Command not found: {cmd}"
#
#     def start_gui(self):
#         self.root = tk.Tk()
#         self.root.title("Shell Emulator")
#
#         # Create input field for commands
#         self.input_entry = tk.Entry(self.root, width=80)
#         self.input_entry.bind("<Return>", self.on_enter_command)
#         self.input_entry.pack()
#
#         # Create scrolled text area for output
#         self.output_area = scrolledtext.ScrolledText(self.root, width=80, height=20)
#         self.output_area.pack()
#
#         # Run GUI
#         self.root.mainloop()
#
#     def on_enter_command(self, event):
#         command = self.input_entry.get()
#         output = self.execute_command(command)
#         self.output_area.insert(tk.END, f"{self.current_path}$ {command}\n{output}\n\n")
#         self.input_entry.delete(0, tk.END)
#
# if __name__ == "__main__":
#     emulator = ShellEmulator("config.ini")
#     emulator.start_gui()

import sys
import os
import tarfile
import csv
import configparser
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget


class ShellEmulator(QMainWindow):
    def __init__(self, config_path):
        super().__init__()
        self.setWindowTitle("Shell Emulator")
        self.setGeometry(300, 300, 600, 400)

        # Настройки из конфигурационного файла
        config = configparser.ConfigParser()
        config.read(config_path)
        self.fs_path = config.get("Settings", "filesystem_path")
        self.log_path = config.get("Settings", "log_path")

        # Инициализация виртуальной файловой системы
        self.current_dir = '/'
        self.filesystem = {}
        self.load_filesystem()

        # Лог-файл
        self.log_file = open(self.log_path, mode='w', newline='')
        self.log_writer = csv.writer(self.log_file)
        self.log_writer.writerow(["Timestamp", "Command"])

        # GUI-компоненты
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.process_command)

        layout = QVBoxLayout()
        layout.addWidget(self.output_display)
        layout.addWidget(self.input_line)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_filesystem(self):
        with tarfile.open(self.fs_path, 'r') as tar:
            for member in tar.getmembers():
                self.filesystem[member.name] = member

    def log_command(self, command):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_writer.writerow([timestamp, command])
        self.log_file.flush()

    def process_command(self):
        command = self.input_line.text()
        self.log_command(command)

        parts = command.split()
        if not parts:
            return

        cmd = parts[0]

        if cmd == "ls":
            self.ls_command()
        elif cmd == "cd":
            self.cd_command(parts[1] if len(parts) > 1 else "/")
        elif cmd == "find":
            self.find_command(parts[1] if len(parts) > 1 else "")
        elif cmd == "whoami":
            self.output_display.append(os.getlogin())
        elif cmd == "date":
            self.output_display.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif cmd == "exit":
            self.close()
        else:
            self.output_display.append(f"Unknown command: {cmd}")

        self.input_line.clear()

    def ls_command(self):
        entries = [name for name in self.filesystem if name.startswith(self.current_dir) and name != self.current_dir]
        output = "\n".join(entries)
        self.output_display.append(output)

    def cd_command(self, path):
        if path == "/":
            self.current_dir = "/"
        else:
            new_path = os.path.join(self.current_dir, path).rstrip("/")
            if new_path in self.filesystem and self.filesystem[new_path].isdir():
                self.current_dir = new_path
            else:
                self.output_display.append(f"No such directory: {path}")

    def find_command(self, name):
        matches = [name for name in self.filesystem if name.endswith(name)]
        output = "\n".join(matches)
        self.output_display.append(output)

    def closeEvent(self, event):
        self.log_file.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    config_path = "config.ini"  # Путь к конфигурационному файлу
    emulator = ShellEmulator(config_path)
    emulator.show()

    sys.exit(app.exec_())
