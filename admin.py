from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from lessons import LessonManager, QuestionManager, ChapterManager

class AdminMenuWindow(QWidget):
    def __init__(self, username, user_id):
        super().__init__()
        self.setWindowTitle("Admin Panel")

        layout = QVBoxLayout()

        # Tombol Tambah Pelajaran
        btn1 = QPushButton("Tambah Pelajaran")
        btn1.clicked.connect(self.open_lesson_manager)
        layout.addWidget(btn1)

         # Tombol Tambah BAB
        btn3 = QPushButton("Tambah BAB")
        btn3.clicked.connect(self.open_chapter_manager)
        layout.addWidget(btn3)

        # Tombol Tambah Soal
        btn2 = QPushButton("Tambah Soal")
        btn2.clicked.connect(self.open_question_manager)
        layout.addWidget(btn2)

        self.setLayout(layout)

    def open_lesson_manager(self):
        self.lesson_window = LessonManager()
        self.lesson_window.show()

    def open_question_manager(self):
        self.question_window = QuestionManager()
        self.question_window.show()

    def open_chapter_manager(self):
        self.chapter_window = ChapterManager()
        self.chapter_window.show()
