from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QRadioButton, QPushButton, QMessageBox, QButtonGroup, QApplication
)
import sys
from database import connect_db

class QuizWindow(QWidget):
    def __init__(self, username, user_id, lesson_id, lesson_title):
        super().__init__()
        self.setWindowTitle(f"Kuis: {lesson_title}")
        self.setMinimumSize(400, 300)
        self.username = username
        self.user_id = user_id
        self.lesson_id = lesson_id
        self.lesson_title = lesson_title

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.current_question_index = 0
        self.score = 0
        self.questions = []
        self.selected_option = None

        self.load_questions()
        if not self.questions:
            QMessageBox.warning(self, "Kosong", "Pelajaran ini belum memiliki soal.")
            self.close()
            return

        self.display_question()

    def load_questions(self):
        print("Mulai load_questions")  # DEBUG
        print("lesson_id:", self.lesson_id)
        
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
                       SELECT question, option_a, option_b, option_c, option_d, correct_option 
                       FROM questions WHERE lesson_id = %s
                       """, (self.lesson_id,))
        self.questions = cursor.fetchall()
        db.close()
        print("Soal ditemukan:", len(self.questions))  # DEBUG
        
        if not self.questions:
            QMessageBox.information(self, "Info", "Belum ada soal untuk pelajaran ini.")
            self.close()
            return
        self.display_question()
        
    def display_question(self):
        # Bersihkan layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Tampilkan pertanyaan dan opsi
        question_data = self.questions[self.current_question_index]
        question_text, a, b, c, d, self.correct_option = question_data

        self.question_label = QLabel(question_text)
        self.layout.addWidget(self.question_label)

        self.button_group = QButtonGroup(self)
        self.radio_buttons = []

        for idx, option_text in enumerate([a, b, c, d]):
            rb = QRadioButton(option_text)
            self.radio_buttons.append(rb)
            self.button_group.addButton(rb, idx)
            self.layout.addWidget(rb)

        self.next_button = QPushButton("Lanjut")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

    def next_question(self):
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            QMessageBox.warning(self, "Peringatan", "Pilih salah satu jawaban terlebih dahulu.")
            return

        selected_option = "ABCD"[selected_id]
        if selected_option == self.correct_option:
            self.score += 1

        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            QMessageBox.information(
                self,
                "Selesai",
                f"Kuis selesai!\nSkor Anda: {self.score}/{len(self.questions)}"
            )
            self.close()
        else:
            self.display_question()
