from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QApplication, QMessageBox
)
import sys
from database import connect_db

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

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO lessons (title, description) VALUES (%s, %s)", (title, desc))
        db.commit()
        db.close()

        QMessageBox.information(self, "Berhasil", "Pelajaran berhasil ditambahkan.")
        self.title_input.clear()
        self.desc_input.clear()

# Untuk menjalankan langsung
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LessonManager()
    window.show()
    sys.exit(app.exec_())
