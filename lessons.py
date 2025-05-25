from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QComboBox, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QFrame
from quiz import QuizWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from database import connect_db, get_chapters_by_lesson, get_lessons, add_chapter, add_lesson, add_question


# ===================== Lesson Manager =====================
class LessonManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Pelajaran")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(720, 800)
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
        else:
            QMessageBox.warning(self, "Gagal", "Terjadi kesalahan saat menyimpan pelajaran.")


# ===================== Chapter Manager =====================
class ChapterManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah BAB")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(720, 800)
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

        title = QLabel("Tambah BAB", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        label = QLabel("Pilih Pelajaran:")
        label.setFont(QFont("Arial", 10))
        layout.addWidget(label)

        self.lesson_combo = QComboBox()
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
        self.lesson_map = {}
        self.load_lessons()
        layout.addWidget(self.lesson_combo)

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
            self.close()
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan BAB.")


# ===================== Question Manager =====================
class QuestionManager(QWidget):
    def __init__(self, parent_admin_window=None):
        super().__init__()
        self.setWindowTitle("Tambah Soal")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(720, 800)
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

        self.card = QFrame(self)
        self.card.setFixedSize(400, 650)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
            }
        """)
        self.card.move((self.width() - self.card.width()) // 2, (self.height() - self.card.height()) // 2)

        layout = QVBoxLayout(self.card)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Tambah Soal", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Pelajaran
        layout.addWidget(self._label("Pilih Pelajaran:"))
        self.lesson_combo = QComboBox()
        self._style_combo(self.lesson_combo)
        layout.addWidget(self.lesson_combo)

        # BAB
        layout.addWidget(self._label("Pilih BAB:"))
        self.chapter_combo = QComboBox()
        self._style_combo(self.chapter_combo)
        layout.addWidget(self.chapter_combo)

        self.lesson_map = {}
        self.chapter_map = {}
        self.lesson_combo.currentIndexChanged.connect(self.update_chapters)

        # Input soal dan pilihan
        layout.addWidget(self._line_input("Pertanyaan", "question_input"))
        layout.addWidget(self._line_input("Pilihan A", "option_a_input"))
        layout.addWidget(self._line_input("Pilihan B", "option_b_input"))
        layout.addWidget(self._line_input("Pilihan C", "option_c_input"))
        layout.addWidget(self._line_input("Pilihan D", "option_d_input"))

        # Jawaban Benar
        layout.addWidget(self._label("Jawaban Benar:"))
        self.correct_option_combo = QComboBox()
        self.correct_option_combo.addItems(["A", "B", "C", "D"])
        self._style_combo(self.correct_option_combo)
        layout.addWidget(self.correct_option_combo)

        # Tombol simpan
        save_btn = QPushButton("Simpan Soal")
        save_btn.setMinimumHeight(40)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #4e54c8, stop: 1 #8f94fb
                );
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5d63d8;
            }
        """)
        save_btn.clicked.connect(self.save_question)
        layout.addWidget(save_btn)

        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)
        outer.addWidget(self.card)

        self.load_lessons()

    def _label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Arial", 11))
        return label

    def _style_combo(self, combo):
        combo.setMinimumHeight(35)
        combo.setStyleSheet("""
            QComboBox {
                background-color: #f0f0f0;
                padding: 8px;
                border-radius: 5px;
                font-size: 13px;
                border: 1px solid #ccc;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #4e54c8;
                border-radius: 5px;
            }
        """)

    def _line_input(self, placeholder, attr_name):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumHeight(35)
        input_field.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 8px;
                border-radius: 5px;
                font-size: 13px;
                border: 1px solid #ccc;
            }
        """)
        setattr(self, attr_name, input_field)
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
        self.chapter_combo.clear()
        self.chapter_map.clear()
        if lesson_id:
            chapters = get_chapters_by_lesson(lesson_id)
            for chapter_id, title in chapters:
                self.chapter_combo.addItem(title)
                self.chapter_map[title] = chapter_id

    def save_question(self):
        question = self.question_input.text().strip()
        option_a = self.option_a_input.text().strip()
        option_b = self.option_b_input.text().strip()
        option_c = self.option_c_input.text().strip()
        option_d = self.option_d_input.text().strip()
        correct_option = self.correct_option_combo.currentText()

        chapter_title = self.chapter_combo.currentText()
        chapter_id = self.chapter_map.get(chapter_title)

        if not all([question, option_a, option_b, option_c, option_d]):
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi.")
            return

        if chapter_id is None:
            QMessageBox.warning(self, "Peringatan", "BAB belum dipilih.")
            return

        if add_question(question, option_a, option_b, option_c, option_d, correct_option, chapter_id):
            QMessageBox.information(self, "Sukses", "Soal berhasil disimpan.")
            self.close()
            if self.parent_admin_window:
                self.parent_admin_window.show()
        else:
            QMessageBox.warning(self, "Gagal", "Terjadi kesalahan saat menyimpan soal.")


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

            QLabel#titleLabel {
                font-size: 22px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }

            QLabel#subtitleLabel {
                font-size: 16px;
                color: #555;
                margin-bottom: 20px;
            }

            QListWidget#chapterList {
                border: none;
                background: transparent;
            }

            QListWidget::item {
                background: #ffffff;
                border: 2px solid #a2b3f5;
                border-radius: 12px;
                padding: 12px 16px;
                margin: 8px;
                font-size: 15px;
                color: #333;
            }

            QListWidget::item:hover {
                background: #e3e8fd;
            }

            QListWidget::item:disabled {
                background: #f0f0f0;
                color: #999;
                border: 2px dashed #ccc;
            }

            QFrame#card {
                background: white;
                border-radius: 20px;
                padding: 30px;
                max-width: 320px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
            }
        """)

class ChapterWindow(StyledWidget):
    def __init__(self, username, user_id, lesson_id, lesson_title):
        super().__init__()
        self.username = username
        self.user_id = user_id
        self.lesson_id = lesson_id
        self.lesson_title = lesson_title

        self.setWindowTitle(f"{lesson_title} - Pilih BAB")
        self.setFixedSize(400, 550)  # Lebih besar sedikit supaya judul muat

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)  # Margin lebih luas
        layout.setSpacing(24)

        title = QLabel(f"Pelajaran: {lesson_title}\nPilih Bab:")
        title.setWordWrap(True)
        title.setStyleSheet("""
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: #FFFFFF; /* ungu gelap */
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
            margin-bottom: 16px;
        """)
        layout.addWidget(title)

        self.list = QListWidget()
        self.list.setStyleSheet("""
    QListWidget {
        background: transparent;
        border: none;
    }
    QListWidget::item {
        background: #f0f4ff;
        border: 2px solid #a2b3f5;
        border-radius: 16px;
        padding: 18px 24px;
        margin: 10px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 19px;
        font-weight: 700;
        color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                              stop:0 #5d54a4, stop:1 #8e7cc3);
        text-shadow: 1px 1px 2px rgba(93, 84, 164, 0.7);
        transition: background-color 0.25s ease, border-color 0.25s ease, color 0.3s ease;
    }
    QListWidget::item:hover:!disabled {
        background: #d7defa;
        border-color: #5d54a4;
        color: #3c2e8e;
        cursor: pointer;
        text-shadow: 2px 2px 4px rgba(60, 46, 142, 0.9);
    }
    QListWidget::item:selected {
        background: #5d54a4;
        color: white;
        border-color: #4b3b7a;
        text-shadow: none;
    }
    QListWidget::item:disabled {
        color: #aaa;
        border-style: dashed;
        background: #f7f8fc;
        cursor: not-allowed;
        text-shadow: none;
    }
""")

        self.list.itemClicked.connect(self.start_quiz)
        layout.addWidget(self.list)

        self.setLayout(layout)

        self.load_chapters()

    def load_chapters(self):
        chapters = get_chapters_by_lesson(self.lesson_id)
        self.list.clear()

        try:
            db = connect_db()
            cursor = db.cursor()

            for i, (chap_id, chap_title) in enumerate(chapters):
                cursor.execute("SELECT COUNT(*) FROM questions WHERE chapter_id = %s", (chap_id,))
                total = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM user_answers WHERE user_id = %s AND chapter_id = %s AND correct = TRUE", (self.user_id, chap_id))
                answered = cursor.fetchone()[0]


                locked = False

                if i > 0:
                    prev_chap_id = chapters[i - 1][0]
                    cursor.execute("SELECT completed FROM user_progress WHERE user_id = %s AND chapter_id = %s", (self.user_id, prev_chap_id))
                    progress = cursor.fetchone()
                    if not progress or not progress[0]:
                        locked = True

                item_text = f"{chap_title} - {answered}/{total}" + (" 🔒" if locked else "")
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, chap_id)
                if locked:
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                self.list.addItem(item)

        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "ERROR", f"Gagal load bab:\n{e}")
        finally:
            db.close()

    def start_quiz(self, item):
        if not item.flags() & Qt.ItemIsEnabled:
            return

        chapter_id = item.data(Qt.UserRole)
        chapter_title = item.text().split(" - ")[0]
        if chapter_id:
            from quiz import QuizWindow
            self.quiz_window = QuizWindow(
                self.username, self.user_id, chapter_id, chapter_title,
                is_chapter=True,
                on_finish=self.return_to_menu
            )
            self.quiz_window.show()
            self.close()

    def return_to_menu(self):
        from menu import MenuWindow
        self.menu_window = MenuWindow(self.username, self.user_id)
        self.menu_window.show()

