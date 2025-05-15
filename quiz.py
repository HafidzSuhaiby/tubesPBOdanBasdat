from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QRadioButton, QPushButton, QMessageBox, QButtonGroup
)
from database import connect_db
from datetime import date

class QuizWindow(QWidget):
    def __init__(self, username, user_id, id_value, title, is_chapter=False):
        super().__init__()
        self.setWindowTitle(f"Kuis: {title}")
        self.setMinimumSize(400, 300)
        self.username = username
        self.user_id = user_id
        self.lesson_or_chapter_id = id_value
        self.is_chapter = is_chapter
        self.lesson_title = title

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.current_question_index = 0
        self.score = 0
        self.questions = []
        self.selected_option = None

        self.lives = self.check_and_reset_lives()
        if self.lives <= 0:
            QMessageBox.warning(self, "Nyawa Habis", "Nyawa Anda habis untuk hari ini. Silakan coba besok.")
            self.close()
            return

        self.load_questions()
        if not self.questions:
            QMessageBox.warning(self, "Kosong", "Bab ini belum memiliki soal.")
            self.close()
            return

        self.display_question()

    def check_and_reset_lives(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT lives, last_life_reset FROM users WHERE id = %s", (self.user_id,))
        row = cursor.fetchone()
        if not row:
            db.close()
            return 0

        lives, last_reset = row
        today = date.today()
        if last_reset is None or str(last_reset) != str(today):
            cursor.execute("UPDATE users SET lives = 5, last_life_reset = %s WHERE id = %s", (today, self.user_id))
            db.commit()
            lives = 5

        db.close()
        return lives

    def load_questions(self):
        db = connect_db()
        cursor = db.cursor()
        if self.is_chapter:
            cursor.execute("""
                SELECT question, option_a, option_b, option_c, option_d, correct_option 
                FROM questions WHERE chapter_id = %s
            """, (self.lesson_or_chapter_id,))
        else:
            cursor.execute("""
                SELECT question, option_a, option_b, option_c, option_d, correct_option 
                FROM questions WHERE lesson_id = %s
            """, (self.lesson_or_chapter_id,))
        self.questions = cursor.fetchall()
        db.close()

    def display_question(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

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
        is_correct = (selected_option == self.correct_option)

        if is_correct:
            self.score += 1
        else:
            self.lives -= 1
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("UPDATE users SET lives = %s WHERE id = %s", (self.lives, self.user_id))
            db.commit()
            db.close()
            if self.lives == 0:
                QMessageBox.warning(self, "Game Over", "Nyawa Anda habis. Coba lagi besok.")
                self.close()
                return

        # Simpan jawaban ke tabel user_answers
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""INSERT INTO user_answers (user_id, chapter_id, question, answer, correct) VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE answer = VALUES(answer), correct = VALUES(correct)""", 
        (
        self.user_id,
        self.lesson_or_chapter_id,
        self.question_label.text(),
        selected_option,
        is_correct ))

        db.commit()
        db.close()
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO user_progress (user_id, chapter_id, completed)
                VALUES (%s, %s, TRUE)
                ON DUPLICATE KEY UPDATE completed = TRUE
            """, (self.user_id, self.lesson_or_chapter_id))
            db.commit()
            db.close()

            QMessageBox.information(self, "Selesai", f"Kuis selesai!\nSkor Anda: {self.score}/{len(self.questions)}")
            self.close()
        else:
            self.display_question()
