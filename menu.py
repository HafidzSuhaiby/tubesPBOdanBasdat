from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QListWidget, QApplication, QMessageBox
)
import sys
from database import connect_db
from quiz import QuizWindow  # kita akan buat selanjutnya

class MenuWindow(QWidget):
    def __init__(self, username, user_id):
        super().__init__()
        self.setWindowTitle("Pilih Pelajaran")
        self.username = username
        self.user_id = user_id

        layout = QVBoxLayout()

        self.label = QLabel(f"Halo, {username}! Silakan pilih pelajaran:")
        layout.addWidget(self.label)

        self.lesson_list = QListWidget()
        self.lesson_list.itemClicked.connect(self.start_quiz)
        layout.addWidget(self.lesson_list)

        self.setLayout(layout)
        self.load_lessons()

    def load_lessons(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, title FROM lessons")
        lessons = cursor.fetchall()
        db.close()

        self.lesson_map = {}  # simpan id pelajaran
        self.lesson_list.clear()
        for lesson in lessons:
            self.lesson_map[lesson[1]] = lesson[0]
            self.lesson_list.addItem(lesson[1])

    def start_quiz(self, item):
        title = item.text()
        lesson_id = self.lesson_map[title]
        self.quiz_window = QuizWindow(self.username, self.user_id, lesson_id, title)
        self.quiz_window.show()

# Untuk pengujian langsung
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuWindow("testuser", 1)
    window.show()
    sys.exit(app.exec_())
