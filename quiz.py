from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton,
    QMessageBox, QButtonGroup, QGridLayout
)
from PyQt5.QtCore import Qt
from database import connect_db
from datetime import date


class StyledWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #4e54c8,
                    stop: 1 #8f94fb
                );
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel#questionBox {
                font-size: 16px;
                font-weight: 500;
                color: #222;
                background: #f0f4ff;
                border-radius: 16px;
                padding: 20px 24px;
                margin: 10px 0 30px 0;
                border: 2px solid #a2b3f5;
                max-width: 800px;
                min-height: 120px;
                qproperty-alignment: 'AlignTop | AlignLeft';
            }
            QRadioButton {
                background: #f0f4ff;
                padding: 16px 20px;
                margin: 10px;
                border-radius: 16px;
                border: 2px solid #a2b3f5;
                font-size: 15px;
                font-weight: 500;
                color: #333;
                min-width: 300px;
            }
            QRadioButton:hover {
                background-color: #e0e9ff;
            }
            QPushButton {
                background-color: #ffffff;
                border: none;
                padding: 14px 28px;
                border-radius: 14px;
                font-weight: 700;
                color: #5D54A4;
                margin: 12px 18px;
                font-size: 16px;
                min-width: 120px;
                box-shadow: 0 3px 10px rgba(93, 84, 164, 0.2);
            }
            QPushButton:hover {
                background-color: #e3e0fa;
                box-shadow: 0 4px 12px rgba(93, 84, 164, 0.5);
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #888;
                box-shadow: none;
            }
        """)


class QuizWindow(StyledWidget):
    def __init__(self, username, user_id, id_value, title, is_chapter=False, on_finish=None):
        super().__init__()
        self.setWindowTitle(f"Kuis: {title}")
        self.setMinimumSize(720, 800)
        self.username = username
        self.user_id = user_id
        self.lesson_or_chapter_id = id_value
        self.is_chapter = is_chapter
        self.lesson_title = title
        self.on_finish = on_finish
        self.jawaban_benar = []

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setLayout(self.layout)

        self.current_question_index = 0
        self.score = 0
        self.questions = []

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

        self.init_ui()
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

    def init_ui(self):
        self.question_label = QLabel()
        self.question_label.setObjectName("questionBox")
        self.question_label.setWordWrap(True)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.question_label)

        self.answers_layout = QGridLayout()
        self.answers_layout.setHorizontalSpacing(40)
        self.answers_layout.setVerticalSpacing(25)
        self.button_group = QButtonGroup(self)
        self.radio_buttons = []

        for i in range(4):
            rb = QRadioButton()
            self.radio_buttons.append(rb)
            self.button_group.addButton(rb, i)
            row = i // 2
            col = i % 2
            self.answers_layout.addWidget(rb, row, col)

        self.layout.addLayout(self.answers_layout)

        self.nav_layout = QHBoxLayout()
        self.nav_layout.setAlignment(Qt.AlignCenter)

        self.prev_button = QPushButton("Sebelumnya")
        self.prev_button.clicked.connect(self.prev_question)
        self.prev_button.setEnabled(False)
        self.nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Lanjut")
        self.next_button.clicked.connect(self.next_question)
        self.nav_layout.addWidget(self.next_button)

        self.layout.addLayout(self.nav_layout)

    def display_question(self):
        question_data = self.questions[self.current_question_index]
        question_text, a, b, c, d, self.correct_option = question_data

        self.question_label.setText(question_text)

        for rb, text in zip(self.radio_buttons, [a, b, c, d]):
            rb.setText(text)
            rb.setChecked(False)

        self.prev_button.setEnabled(self.current_question_index > 0)
        if self.current_question_index == len(self.questions) - 1:
            self.next_button.setText("Selesai")
        else:
            self.next_button.setText("Lanjut")

    def save_answer(self):
        selected_id = self.button_group.checkedId()
        if selected_id == -1:
            return None, None

        selected_option = "ABCD"[selected_id]
        question_data = self.questions[self.current_question_index]
        correct_option = question_data[5]
        is_correct = (selected_option == correct_option)
        return selected_option, is_correct


    def next_question(self):
        selected_option, is_correct = self.save_answer()

        if selected_option is None:
            QMessageBox.warning(self, "Peringatan", "Pilih salah satu jawaban terlebih dahulu.")
            return

        # Simpan status jawaban benar/salah
        self.jawaban_benar.append(is_correct)

        if is_correct:
            self.score += 1

        # Simpan jawaban ke database
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO user_answers (user_id, chapter_id, question, answer, correct) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE answer = VALUES(answer), correct = VALUES(correct)
        """, (self.user_id, self.lesson_or_chapter_id, self.question_label.text(), selected_option, is_correct))
        db.commit()
        db.close()

        # Jika ini soal terakhir
        if self.current_question_index == len(self.questions) - 1:

            # Jika ada jawaban salah, kurangi nyawa 1x
            if False in self.jawaban_benar:
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

            total_questions = len(self.questions)

            if self.score == total_questions:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("""
                    INSERT INTO user_progress (user_id, chapter_id, completed)
                    VALUES (%s, %s, TRUE)
                    ON DUPLICATE KEY UPDATE completed = TRUE
                """, (self.user_id, self.lesson_or_chapter_id))
                db.commit()
                db.close()
                QMessageBox.information(self, "Selesai", f"Skor Anda sempurna!\nBAB dianggap selesai.")
            else:
                QMessageBox.warning(self, "Belum Lulus", f"Skor Anda: {self.score}/{total_questions}\nAnda harus menjawab semua soal dengan benar untuk menyelesaikan BAB.")

            self.close()
            if self.on_finish:
                self.on_finish()
            return

        # Jika belum soal terakhir, lanjutkan
        self.current_question_index += 1
        self.display_question()


    def prev_question(self):
        if self.current_question_index == 0:
            return

        selected_option, is_correct = self.save_answer()
        if selected_option is None:
            QMessageBox.warning(self, "Peringatan", "Pilih salah satu jawaban terlebih dahulu.")
            return

        self.current_question_index -= 1
        self.display_question()
