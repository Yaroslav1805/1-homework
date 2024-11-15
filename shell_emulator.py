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
