from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame, QLabel,QLineEdit,QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import add_lesson, add_chapter, add_question
from PyQt5.QtWidgets import QMessageBox
from lessons import LessonManager, QuestionManager, ChapterManager
from database import  connect_db, get_lessons, get_chapters_by_lesson
class AdminMenuWindow(QWidget):
    def __init__(self, username, user_id):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setFixedSize(600, 650)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #4e54c8,
                    stop: 1 #8f94fb
                );
            }
        """)

        # Card putih di tengah
        self.card = QFrame()
        self.card.setFixedSize(300, 400)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(self.card)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        # Judul
        title = QLabel("Admin Panel")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

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

        # Gaya tombol
        for btn in [btn1, btn2, btn3]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4e54c8, stop:1 #8f94fb
                    );
                    color: white;
                    padding: 10px;
                    font-size: 14px;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #5d63d8;
                }
            """)

        # Layout luar card di tengah
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.card)

    def open_lesson_manager(self):
        self.lesson_window = LessonManager()
        self.lesson_window.show()

    def open_question_manager(self):
        self.question_window = QuestionManager()
        self.question_window.show()

    def open_chapter_manager(self):
        self.chapter_window = ChapterManager()
        self.chapter_window.show()



# ------------------ Lesson Manager ------------------ #
class LessonManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Pelajaran")
        self.setFixedSize(600, 650)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #4e54c8,
                    stop: 1 #8f94fb
                );
            }
        """)

        self.card = QFrame(self)
        self.card.setFixedSize(300, 350)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        self.card.move((self.width() - self.card.width()) // 2, (self.height() - self.card.height()) // 2)

        layout = QVBoxLayout(self.card)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Tambah Pelajaran", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.lesson_input = QLineEdit()
        self.lesson_input.setPlaceholderText("Nama Pelajaran")
        self.lesson_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.lesson_input)

        save_btn = QPushButton("Simpan")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4e54c8, stop:1 #8f94fb
                );
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5d63d8;
            }
        """)
        save_btn.clicked.connect(self.save_lesson)
        layout.addWidget(save_btn)
        
        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.card)
        
    def save_lesson(self):
        lesson_name = self.lesson_input.text().strip()
        if not lesson_name:
            QMessageBox.warning(self, "Peringatan", "Nama pelajaran tidak boleh kosong!")
            return
        if add_lesson(lesson_name, ""):
            QMessageBox.information(self, "Sukses", f"Pelajaran '{lesson_name}' berhasil disimpan.")
            self.close() 
        else:QMessageBox.warning(self, "Gagal", "Terjadi kesalahan saat menyimpan pelajaran.")



# ------------------ TAMBAH BAB ------------------ #

class ChapterManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah BAB")
        self.setFixedSize(600, 650)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #4e54c8,
                    stop: 1 #8f94fb
                );
            }
        """)

        self.card = QFrame(self)
        self.card.setFixedSize(300, 400)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        self.card.move((self.width() - self.card.width()) // 2, (self.height() - self.card.height()) // 2)

        layout = QVBoxLayout(self.card)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        # Judul
        title = QLabel("Tambah BAB", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Label
        label = QLabel("Pilih Pelajaran:")
        label.setFont(QFont("Arial", 10))
        layout.addWidget(label)
        
        # Dropdown Pilih Pelajaran dengan tampilan seperti input BAB
        self.lesson_combo = QComboBox()
        self.lesson_combo.setStyleSheet(""" QComboBox {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        font-size: 14px;
        border: 1px solid #ccc;
            }
        QComboBox QAbstractItemView {
        background-color: white;
        selection-background-color: #4e54c8;
        border-radius: 5px;
        padding: 5px;    }""")
        self.lesson_map = {}  # title -> id
        self.load_lessons()
        layout.addWidget(self.lesson_combo)

        # Input BAB
        self.chapter_input = QLineEdit()
        self.chapter_input.setPlaceholderText("Nama BAB")
        self.chapter_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.chapter_input)

        # Tombol Simpan
        save_btn = QPushButton("Simpan")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4e54c8, stop:1 #8f94fb
                );
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5d63d8;
            }
        """)
        save_btn.clicked.connect(self.save_chapter)
        layout.addWidget(save_btn)

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.card)

    def load_lessons(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title FROM lessons")
            lessons = cursor.fetchall()
            conn.close()

            for lesson_id, title in lessons:
                self.lesson_combo.addItem(title)
                self.lesson_map[title] = lesson_id
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal memuat pelajaran: {e}")

    def save_chapter(self):
        chapter_title = self.chapter_input.text().strip()
        selected_lesson_title = self.lesson_combo.currentText()
        lesson_id = self.lesson_map.get(selected_lesson_title)

        if not chapter_title:
            QMessageBox.warning(self, "Peringatan", "Nama BAB tidak boleh kosong!")
            return

        if not lesson_id:
            QMessageBox.warning(self, "Peringatan", "Pilih pelajaran terlebih dahulu.")
            return

        if add_chapter(chapter_title, lesson_id):
            QMessageBox.information(self, "Berhasil", f"BAB '{chapter_title}' berhasil ditambahkan.")
            self.close()  # Kembali ke admin panel (karena jendela ini ditutup)
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan BAB.")



# ------------------ TAMBAH SOAL   ------------------ #


class QuestionManager(QWidget):
    def __init__(self, parent_admin_window=None):
        super().__init__()
        self.setWindowTitle("Tambah Soal")
        self.setFixedSize(600, 650)  # Lebar & tinggi lebih besar

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #4e54c8,
                    stop: 1 #8f94fb
                );
            }
        """)

        self.parent_admin_window = parent_admin_window

        self.card = QFrame()
        self.card.setFixedSize(600, 650)  # Ukuran cukup besar agar isi tidak terpotong
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 30px;
            }
        """)

        layout = QVBoxLayout(self.card)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Tambah Soal", self.card)
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        layout.addWidget(title)

        # Label + Dropdown Pelajaran
        label_pelajaran = QLabel("Pilih Pelajaran:")
        label_pelajaran.setFont(QFont("Arial", 12))
        label_pelajaran.setWordWrap(True)
        layout.addWidget(label_pelajaran)

        self.lesson_combo = QComboBox()
        self.lesson_combo.setMinimumHeight(40)
        self.lesson_combo.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #4e54c8;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.lesson_combo)

        # Label + Dropdown BAB
        label_bab = QLabel("Pilih BAB:")
        label_bab.setFont(QFont("Arial", 12))
        label_bab.setWordWrap(True)
        layout.addWidget(label_bab)

        self.chapter_combo = QComboBox()
        self.chapter_combo.setMinimumHeight(40)
        self.chapter_combo.setStyleSheet(self.lesson_combo.styleSheet())
        layout.addWidget(self.chapter_combo)

        self.lesson_map = {}
        self.chapter_map = {}
        self.lesson_combo.currentIndexChanged.connect(self.update_chapters)

        # Input soal dan pilihan
        layout.addWidget(self._make_input("Tulis pertanyaan soal di sini...", attr="question_input"))
        layout.addWidget(self._make_input("Pilihan A", attr="option_a_input"))
        layout.addWidget(self._make_input("Pilihan B", attr="option_b_input"))
        layout.addWidget(self._make_input("Pilihan C", attr="option_c_input"))
        layout.addWidget(self._make_input("Pilihan D", attr="option_d_input"))

        # Jawaban Benar
        label_jawaban = QLabel("Jawaban Benar:")
        label_jawaban.setFont(QFont("Arial", 12))
        label_jawaban.setWordWrap(True)
        layout.addWidget(label_jawaban)

        self.correct_option_combo = QComboBox()
        self.correct_option_combo.addItems(['A', 'B', 'C', 'D'])
        self.correct_option_combo.setMinimumHeight(40)
        self.correct_option_combo.setStyleSheet(self.lesson_combo.styleSheet())
        layout.addWidget(self.correct_option_combo)

        # Tombol Simpan
        save_btn = QPushButton("Simpan Soal")
        save_btn.setMinimumHeight(45)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4e54c8, stop:1 #8f94fb
                );
                color: white;
                padding: 12px;
                font-size: 16px;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #5d63d8;
            }
        """)
        save_btn.clicked.connect(self.save_question)
        layout.addWidget(save_btn)

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.card)

        self.load_lessons()

    def _make_input(self, placeholder, attr):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumHeight(40)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 12px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        setattr(self, attr, input_field)
        return input_field

    def load_lessons(self):
        lessons = get_lessons()
        self.lesson_combo.clear()
        self.lesson_map.clear()
        for lesson_id, title in lessons:
            self.lesson_combo.addItem(title)
            self.lesson_map[title] = lesson_id
        self.update_chapters()

    def update_chapters(self):
        lesson_title = self.lesson_combo.currentText()
        lesson_id = self.lesson_map.get(lesson_title)
        if lesson_id:
            chapters = get_chapters_by_lesson(lesson_id)
            self.chapter_combo.clear()
            self.chapter_map.clear()
            for chapter_id, title in chapters:
                self.chapter_combo.addItem(title)
                self.chapter_map[title] = chapter_id
        else:
            self.chapter_combo.clear()
            self.chapter_map.clear()

    def save_question(self):
        question = self.question_input.text().strip()
        option_a = self.option_a_input.text().strip()
        option_b = self.option_b_input.text().strip()
        option_c = self.option_c_input.text().strip()
        option_d = self.option_d_input.text().strip()
        correct_option = self.correct_option_combo.currentText()

        chapter_title = self.chapter_combo.currentText()
        chapter_id = self.chapter_map.get(chapter_title)

        if not question or not option_a or not option_b or not option_c or not option_d:
            QMessageBox.warning(self, "Peringatan", "Semua field pilihan harus diisi.")
            return
        if chapter_id is None:
            QMessageBox.warning(self, "Peringatan", "Pilih BAB terlebih dahulu.")
            return

        if add_question(question, option_a, option_b, option_c, option_d, correct_option, chapter_id):
            QMessageBox.information(self, "Sukses", "Soal berhasil disimpan.")
            self.close()
            if self.parent_admin_window:
                self.parent_admin_window.show()
        else:
            QMessageBox.warning(self, "Gagal", "Terjadi kesalahan saat menyimpan soal.")
