from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QComboBox, QApplication, QMessageBox
)
import sys
from database import connect_db

class QuestionManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Soal")

        layout = QVBoxLayout()

        # Pilih pelajaran
        self.lesson_combo = QComboBox()
        layout.addWidget(QLabel("Pilih Pelajaran"))
        layout.addWidget(self.lesson_combo)

        # Pertanyaan
        self.question_input = QTextEdit()
        layout.addWidget(QLabel("Pertanyaan"))
        layout.addWidget(self.question_input)

        # Opsi jawaban
        self.option_a = QLineEdit()
        self.option_b = QLineEdit()
        self.option_c = QLineEdit()
        self.option_d = QLineEdit()

        layout.addWidget(QLabel("Opsi A"))
        layout.addWidget(self.option_a)
        layout.addWidget(QLabel("Opsi B"))
        layout.addWidget(self.option_b)
        layout.addWidget(QLabel("Opsi C"))
        layout.addWidget(self.option_c)
        layout.addWidget(QLabel("Opsi D"))
        layout.addWidget(self.option_d)

        # Jawaban benar
        self.correct_option = QComboBox()
        self.correct_option.addItems(["A", "B", "C", "D"])
        layout.addWidget(QLabel("Jawaban Benar"))
        layout.addWidget(self.correct_option)

        # Tombol tambah soal
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
        for id_, title in lessons:
            self.lesson_map[title] = id_
            self.lesson_combo.addItem(title)

    def add_question(self):
        lesson_title = self.lesson_combo.currentText()
        lesson_id = self.lesson_map[lesson_title]

        question = self.question_input.toPlainText()
        a = self.option_a.text()
        b = self.option_b.text()
        c = self.option_c.text()
        d = self.option_d.text()
        correct = self.correct_option.currentText()

        if not question or not a or not b or not c or not d:
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

# Untuk menjalankan langsung
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionManager()
    window.show()
    sys.exit(app.exec_())
