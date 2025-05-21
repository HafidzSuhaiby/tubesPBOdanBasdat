from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout,
    QComboBox, QApplication, QMessageBox
)
from database import connect_db
from PyQt5.QtWidgets import QComboBox, QListWidget, QListWidgetItem
from database import get_chapters_by_lesson, add_chapter
from quiz import QuizWindow
from PyQt5.QtCore import Qt

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

        # Pilih pelajaran
        self.lesson_combo = QComboBox()
        layout.addWidget(QLabel("Pilih Pelajaran"))
        layout.addWidget(self.lesson_combo)
        self.lesson_combo.currentIndexChanged.connect(self.load_chapters)

        # Pilih bab
        self.chapter_combo = QComboBox()
        layout.addWidget(QLabel("Pilih Bab"))
        layout.addWidget(self.chapter_combo)

        # Pertanyaan dan opsi
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

        self.load_chapters()

    def load_chapters(self):
        lesson_title = self.lesson_combo.currentText()
        lesson_id = self.lesson_map.get(lesson_title)
        if not lesson_id:
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, title FROM chapters WHERE lesson_id = %s", (lesson_id,))
        chapters = cursor.fetchall()
        db.close()

        self.chapter_map = {}
        self.chapter_combo.clear()
        for id_, title in chapters:
            self.chapter_map[title] = id_
            self.chapter_combo.addItem(title)

    def add_question(self):
        chapter_title = self.chapter_combo.currentText()
        chapter_id = self.chapter_map.get(chapter_title)
        
        question = self.question_input.toPlainText()
        a = self.option_a.text()
        b = self.option_b.text()
        c = self.option_c.text()
        d = self.option_d.text()
        correct = self.correct_option.currentText()
        
        if not all([question, a, b, c, d]):
            QMessageBox.warning(self, "Gagal", "Semua isian harus diisi.")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("""
                        INSERT INTO questions 
                        (chapter_id, question, option_a, option_b, option_c, option_d, correct_option)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)""", (chapter_id, question, a, b, c, d, correct))
            db.commit()
            QMessageBox.information(self, "Berhasil", "Soal berhasil ditambahkan.")
            self.question_input.clear()
            self.option_a.clear()
            self.option_b.clear()
            self.option_c.clear()
            self.option_d.clear()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menambahkan soal:\n{e}")
        finally:
            db.close()

class ChapterManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Bab")
        layout = QVBoxLayout()

        self.lesson_combo = QComboBox()
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, title FROM lessons")
        for id_, title in cursor.fetchall():
            self.lesson_combo.addItem(title, id_)
        db.close()

        layout.addWidget(QLabel("Pilih Pelajaran"))
        layout.addWidget(self.lesson_combo)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul Bab")
        layout.addWidget(QLabel("Judul Bab"))
        layout.addWidget(self.title_input)

        add_btn = QPushButton("Tambah Bab")
        add_btn.clicked.connect(self.save)
        layout.addWidget(add_btn)

        self.setLayout(layout)

    def save(self):
        title = self.title_input.text()
        lesson_id = self.lesson_combo.currentData()
        if title:
            if add_chapter(title, lesson_id):
                QMessageBox.information(self, "Berhasil", "Bab berhasil ditambahkan.")
                self.title_input.clear()
            else:
                QMessageBox.warning(self, "Gagal", "Gagal menambahkan bab.")



from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QMessageBox, QFrame
from PyQt5.QtCore import Qt
from database import connect_db, get_chapters_by_lesson

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

                cursor.execute("SELECT COUNT(*) FROM user_answers WHERE user_id = %s AND chapter_id = %s", (self.user_id, chap_id))
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
            self.quiz_window = QuizWindow(self.username, self.user_id, chapter_id, chapter_title, is_chapter=True)
            self.quiz_window.show()
            self.close()
