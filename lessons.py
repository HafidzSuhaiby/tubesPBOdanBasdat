from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QComboBox, QApplication, QMessageBox
)
from database import connect_db

# ========== Lesson Manager ==========
class LessonManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Pelajaran")
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul pelajaran (misal: Bahasa Inggris - Dasar)")
        layout.addWidget(QLabel("Judul Pelajaran"))
        layout.addWidget(self.title_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Deskripsi (opsional)")
        layout.addWidget(QLabel("Deskripsi"))
        layout.addWidget(self.desc_input)

        self.add_btn = QPushButton("Tambah Pelajaran")
        self.add_btn.clicked.connect(self.add_lesson)
        layout.addWidget(self.add_btn)

        self.setLayout(layout)

    def add_lesson(self):
        title = self.title_input.text()
        desc = self.desc_input.text()

        if not title:
            QMessageBox.warning(self, "Gagal", "Judul pelajaran tidak boleh kosong.")
            return

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO lessons (title, description) VALUES (%s, %s)", (title, desc))
            db.commit()
            QMessageBox.information(self, "Berhasil", "Pelajaran berhasil ditambahkan.")
            self.title_input.clear()
            self.desc_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menambahkan pelajaran:\n{e}")
        finally:
            db.close()


# ========== Question Manager ==========
class QuestionManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Soal")

        layout = QVBoxLayout()
        self.lesson_combo = QComboBox()
        layout.addWidget(QLabel("Pilih Pelajaran"))
        layout.addWidget(self.lesson_combo)

        self.question_input = QTextEdit()
        layout.addWidget(QLabel("Pertanyaan"))
        layout.addWidget(self.question_input)

        self.option_a = QLineEdit()
        self.option_b = QLineEdit()
        self.option_c = QLineEdit()
        self.option_d = QLineEdit()

        layout.addWidget(QLabel("Opsi A")); layout.addWidget(self.option_a)
        layout.addWidget(QLabel("Opsi B")); layout.addWidget(self.option_b)
        layout.addWidget(QLabel("Opsi C")); layout.addWidget(self.option_c)
        layout.addWidget(QLabel("Opsi D")); layout.addWidget(self.option_d)

        self.correct_option = QComboBox()
        self.correct_option.addItems(["A", "B", "C", "D"])
        layout.addWidget(QLabel("Jawaban Benar"))
        layout.addWidget(self.correct_option)

        self.add_btn = QPushButton("Tambah Soal")
        self.add_btn.clicked.connect(self.add_question)
        layout.addWidget(self.add_btn)

        self.setLayout(layout)
        self.load_lessons()

    def load_lessons(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, title FROM lessons")
        lessons = cursor.fetchall()
        db.close()

        self.lesson_map = {}
        self.lesson_combo.clear()
        for id_, title in lessons:
            self.lesson_map[title] = id_
            self.lesson_combo.addItem(title)

    def add_question(self):
        lesson_title = self.lesson_combo.currentText()
        lesson_id = self.lesson_map.get(lesson_title)

        question = self.question_input.toPlainText()
        a, b, c, d = self.option_a.text(), self.option_b.text(), self.option_c.text(), self.option_d.text()
        correct = self.correct_option.currentText()

        if not all([question, a, b, c, d]):
            QMessageBox.warning(self, "Gagal", "Semua isian harus diisi.")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO questions 
            (lesson_id, question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (lesson_id, question, a, b, c, d, correct))
        db.commit()
        db.close()

        QMessageBox.information(self, "Berhasil", "Soal berhasil ditambahkan.")
        self.question_input.clear()
        self.option_a.clear()
        self.option_b.clear()
        self.option_c.clear()
        self.option_d.clear()
