import sys
import os
import subprocess
import threading
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QTextEdit, QWidget, QMessageBox
import shutil

class BotManagerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.bot_process = None

    def init_ui(self):
        self.setWindowTitle("Управление ботом")
        self.setGeometry(300, 300, 600, 400)
        layout = QVBoxLayout()
        self.start_button = QPushButton("Запуск")
        self.start_button.setFixedSize(150, 40)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #36732a;
            }
        """)
        self.restart_button = QPushButton("Перезапуск")
        self.restart_button.setFixedSize(150, 40)
        self.stop_button = QPushButton("Стоп")
        self.stop_button.setStyleSheet("""
                    QPushButton {
                        background-color: #F44336;
                        color: white;
                    }
                """)
        self.stop_button.setFixedSize(150, 40)
        self.start_button.clicked.connect(self.start_bot)
        self.restart_button.clicked.connect(self.restart_bot)
        self.stop_button.clicked.connect(self.stop_bot)

        layout.addWidget(self.start_button)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.stop_button)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        self.setLayout(layout)

        self.extract_files()

    def log_message(self, message):
        """Добавить сообщение в консоль и в лог файл."""
        self.console.append(message)

    def extract_files(self):
        """Распаковываем необходимые файлы из .exe в рабочую директорию."""
        if getattr(sys, 'frozen', False):
            resource_dir = sys._MEIPASS
        else:
            resource_dir = os.path.dirname(__file__)

        app_data_dir = self.get_resource_path
        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)

        files_to_copy = ["bot_manager.log"]
        for file in files_to_copy:
            src = os.path.join(resource_dir, file)
            dst = os.path.join(app_data_dir, file)
            if not os.path.exists(dst):
                shutil.copy(src, dst)

    @property
    def get_resource_path(self):
        """Путь к рабочей директории для работы программы."""
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, "data")
        else:
            return os.path.dirname(__file__)

    def start_bot(self):
        """Запуск бота."""
        if self.bot_process is not None and self.bot_process.poll() is None:
            QMessageBox.warning(self, "Ошибка", "Бот уже запущен!")
            return

        self.log_message("Запуск бота...")
        self.bot_process = subprocess.Popen(
            [sys.executable, "C:\\Users\\slend\\OneDrive\\OneDrive\\bot\\bot2.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        threading.Thread(target=self.read_output, daemon=True).start()

    def stop_bot(self):
        """Остановка бота."""
        if self.bot_process is None or self.bot_process.poll() is not None:
            QMessageBox.warning(self, "Ошибка", "Бот не запущен.")
            return

        self.log_message("Остановка бота...")
        self.bot_process.terminate()
        self.bot_process = None

    def restart_bot(self):
        """Перезапуск бота."""
        if self.bot_process is None or self.bot_process.poll() is not None:
            QMessageBox.warning(self, "Ошибка", "Бот не запущен")
            return

        self.log_message("Перезапуск бота...")
        self.bot_process.terminate()
        self.bot_process = None
        self.start_bot()

    def read_output(self):
        """Чтение вывода из консоли запускаемого процесса."""
        if self.bot_process is None:
            return

        def read_stream(stream, prefix=""):
            while True:
                if self.bot_process is None:
                    break
                line = stream.readline()
                if not line:
                    break
                self.log_message(f"{prefix}{line.strip()}")

        threading.Thread(target=read_stream, args=(self.bot_process.stdout,), daemon=True).start()
        threading.Thread(target=read_stream, args=(self.bot_process.stderr, "[Ошибка] "), daemon=True).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotManagerApp()
    window.show()
    sys.exit(app.exec())
