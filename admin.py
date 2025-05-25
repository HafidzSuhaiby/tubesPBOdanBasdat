from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame, QLabel, QLineEdit, QComboBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from lessons import LessonManager, QuestionManager, ChapterManager
from menu import MenuWindow
from login import LoginWindow
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel, QFrame, QMessageBox, QDialog, QHBoxLayout, QInputDialog
from database import connect_db, get_lessons, get_chapters_by_lesson, get_all_users, add_lesson, add_chapter, add_question, get_all_users, update_user_role, delete_user, edit_user, get_user_id_by_username, get_all_user_scores


class AdminMenuWindow(QWidget):
    def __init__(self, username, user_id):
        super().__init__()
        self.username = username
        self.user_id = user_id
        self.setWindowTitle("Admin Panel")
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

        self.card = QFrame()
        self.card.setFixedSize(300, 650)
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

        title = QLabel("Admin Panel")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        btn1 = QPushButton("Tambah Pelajaran")
        btn1.clicked.connect(self.open_lesson_manager)
        layout.addWidget(btn1)

        btn3 = QPushButton("Tambah BAB")
        btn3.clicked.connect(self.open_chapter_manager)
        layout.addWidget(btn3)

        btn2 = QPushButton("Tambah Soal")
        btn2.clicked.connect(self.open_question_manager)
        layout.addWidget(btn2)

        btn_users = QPushButton("Lihat Daftar Pengguna")
        btn_users.clicked.connect(self.open_user_list)
        layout.addWidget(btn_users)

        btn_user_menu = QPushButton("Lihat Tampilan Menu User")
        btn_user_menu.clicked.connect(self.open_user_menu)
        layout.addWidget(btn_user_menu)

        btn_questions = QPushButton("Lihat & Edit Soal")
        btn_questions.clicked.connect(self.open_question_list)
        layout.addWidget(btn_questions)

        btn_score = QPushButton("Daftar Skor User")
        btn_score.clicked.connect(self.open_score_list)
        layout.addWidget(btn_score)

        btn_logout = QPushButton("Keluar")
        btn_logout.clicked.connect(self.logout)
        layout.addWidget(btn_logout)


        for btn in [btn1, btn2, btn3, btn_user_menu, btn_users, btn_questions, btn_score, btn_logout]:
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
    
    def open_user_list(self):
        self.user_window = UserListWindow()
        self.user_window.show()

    def open_user_menu(self):
        self.menu_window = MenuWindow(self.username, self.user_id, email="admin@example.com")
        self.menu_window.show()

    def open_question_list(self):
        self.question_list_window = QuestionListWindow()
        self.question_list_window.show()

    def open_score_list(self):
        self.score_list_window = ScoreListWindow()
        self.score_list_window.show()
    
    def logout(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class UserListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kelola Pengguna")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(720, 800)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #4e54c8, stop: 1 #8f94fb);
            }
        """)

        self.card = QFrame()
        self.card.setFixedSize(600, 700)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(self.card)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Kelola Pengguna")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

        self.load_users()

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.card)

    def load_users(self):
        self.clear_scroll()
        users = get_all_users()
        for user in users:
            id_, username, email, role = user
            frame = QFrame()
            frame.setStyleSheet("background-color: #f5f5f5; padding: 10px; border-radius: 8px;")
            f_layout = QVBoxLayout(frame)

            info = QLabel(f"ID: {id_} | Username: {username} | Email: {email} | Role: {role}")
            info.setStyleSheet("font-size: 13px;")
            f_layout.addWidget(info)

            btn_layout = QHBoxLayout()

            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, uid=id_, uname=username, em=email, rl=role: self.open_edit(uid, uname, em, rl))
            btn_layout.addWidget(edit_btn)

            role_btn = QPushButton("Ganti Role")
            role_btn.clicked.connect(lambda _, uid=id_, current_role=role: self.change_role(uid, current_role))
            btn_layout.addWidget(role_btn)

            del_btn = QPushButton("Hapus")
            del_btn.clicked.connect(lambda _, uid=id_: self.delete_user(uid))
            btn_layout.addWidget(del_btn)

            for btn in [edit_btn, role_btn, del_btn]:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4e54c8;
                        color: white;
                        border: none;
                        padding: 6px 12px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #5d63d8;
                    }
                """)

            f_layout.addLayout(btn_layout)
            self.scroll_layout.addWidget(frame)

    def clear_scroll(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def open_edit(self, user_id, username, email, role):
        dialog = EditUserDialog(user_id, username, email, role)
        if dialog.exec_():
            self.load_users()


    def change_role(self, user_id, current_role):
        dialog = RoleChangeDialog(user_id, current_role)
        if dialog.exec_():
            self.load_users()


    def delete_user(self, user_id):
        confirm = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus user ini?")
        if confirm == QMessageBox.Yes:
            if delete_user(user_id):
                QMessageBox.information(self, "Sukses", "User dihapus.")
                self.load_users()
            else:
                QMessageBox.warning(self, "Gagal", "Gagal menghapus user.")

class EditUserDialog(QDialog):
    def __init__(self, user_id, username, email, role):
        super().__init__()
        self.setWindowTitle("Edit User")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(300, 250)
        self.user_id = user_id

        layout = QVBoxLayout(self)

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit(username)
        layout.addWidget(self.username_input)

        # Email
        layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit(email)
        layout.addWidget(self.email_input)


        # Tombol Simpan
        save_btn = QPushButton("Simpan")
        save_btn.clicked.connect(self.save_changes)
        layout.addWidget(save_btn)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #ccc;
                font-size: 13px;
            }
            QPushButton {
                background-color: #4e54c8;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5d63d8;
            }
        """)

    def save_changes(self):
        uname = self.username_input.text().strip()
        email = self.email_input.text().strip()
        new_role = self.role_combo.currentText()

        if not uname or not email:
            QMessageBox.warning(self, "Peringatan", "Semua field wajib diisi.")
            return

        success_user = edit_user(self.user_id, uname, email)
        success_role = update_user_role(self.user_id, new_role)

        if success_user and success_role:
            QMessageBox.information(self, "Berhasil", "Data berhasil diperbarui.")
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan perubahan.")

class RoleChangeDialog(QDialog):
    def __init__(self, user_id, current_role):
        super().__init__()
        self.setWindowTitle("Ganti Role Pengguna")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(300, 150)
        self.user_id = user_id

        layout = QVBoxLayout(self)

        label = QLabel("Pilih role baru:")
        layout.addWidget(label)

        self.role_combo = QComboBox()
        self.role_combo.addItems(["siswa_biasa", "siswa_super", "admin"])
        self.role_combo.setCurrentText(current_role)
        layout.addWidget(self.role_combo)

        save_btn = QPushButton("Simpan")
        save_btn.clicked.connect(self.save_role)
        layout.addWidget(save_btn)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 13px;
            }
            QComboBox {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #ccc;
            }
            QPushButton {
                background-color: #4e54c8;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5d63d8;
            }
        """)

    def save_role(self):
        new_role = self.role_combo.currentText()

        # Validasi role yang diperbolehkan
        allowed_roles = ["admin", "siswa_biasa", "siswa_super"]
        if new_role not in allowed_roles:
            QMessageBox.warning(self, "Error", "Role tidak valid.")
            return

        if update_user_role(self.user_id, new_role):
            QMessageBox.information(self, "Sukses", f"Role berhasil diubah menjadi {new_role}")
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", "Gagal mengubah role.")


class QuestionListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kelola Soal")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(750, 800)
        self.card = QFrame()
        self.card.setFixedSize(700, 750)
        self.card.setStyleSheet("background-color: white; border-radius: 10px; padding: 20px;")

        layout = QVBoxLayout(self.card)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Daftar Soal")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.view_selector = QComboBox()
        self.view_selector.addItems([
            "view_soal_bahasa_indonesia",
            "view_soal_bahasa_inggris",
            "view_soal_bahasa_jepang"
        ])
        self.view_selector.currentTextChanged.connect(self.load_questions)
        layout.addWidget(self.view_selector)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

        self.load_questions()

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.card)

    def load_questions(self):
        from database import get_all_questions
        self.clear_scroll()

        view = self.view_selector.currentText()
        questions = get_all_questions(view)

        for q in questions:
            qid, text, a, b, c, d, correct, chapter, lesson = q
            frame = QFrame()
            frame.setStyleSheet("background-color: #f2f2f2; padding: 10px; border-radius: 8px;")
            f_layout = QVBoxLayout(frame)

            info = QLabel(f"[{lesson} - {chapter}]\nID: {qid} | {text}\nA: {a} | B: {b} | C: {c} | D: {d} | Jawaban Benar: {correct}")
            info.setWordWrap(True)
            f_layout.addWidget(info)

            btn_edit = QPushButton("Edit")
            btn_edit.clicked.connect(lambda _, qid=qid, t=text, a=a, b=b, c=c, d=d, correct=correct: self.open_edit(qid, t, a, b, c, d, correct))
            f_layout.addWidget(btn_edit)

            self.scroll_layout.addWidget(frame)

    def open_edit(self, qid, question, a, b, c, d, correct):
        dialog = EditQuestionDialog(qid, question, a, b, c, d, correct)
        if dialog.exec_():
            self.load_questions()

    def clear_scroll(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class EditQuestionDialog(QDialog):
    def __init__(self, qid, question, a, b, c, d, correct):
        super().__init__()
        self.setWindowTitle("Edit Soal")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(400, 400)
        self.qid = qid

        layout = QVBoxLayout(self)

        self.q_input = QLineEdit(question)
        layout.addWidget(QLabel("Pertanyaan:"))
        layout.addWidget(self.q_input)

        self.a_input = QLineEdit(a)
        layout.addWidget(QLabel("Pilihan A:"))
        layout.addWidget(self.a_input)

        self.b_input = QLineEdit(b)
        layout.addWidget(QLabel("Pilihan B:"))
        layout.addWidget(self.b_input)

        self.c_input = QLineEdit(c)
        layout.addWidget(QLabel("Pilihan C:"))
        layout.addWidget(self.c_input)

        self.d_input = QLineEdit(d)
        layout.addWidget(QLabel("Pilihan D:"))
        layout.addWidget(self.d_input)

        self.correct_input = QComboBox()
        self.correct_input.addItems(['A', 'B', 'C', 'D'])
        self.correct_input.setCurrentText(correct)
        layout.addWidget(QLabel("Jawaban Benar:"))
        layout.addWidget(self.correct_input)

        save_btn = QPushButton("Simpan Perubahan")
        save_btn.clicked.connect(self.save)
        layout.addWidget(save_btn)

    def save(self):
        from database import update_question
        q = self.q_input.text().strip()
        a = self.a_input.text().strip()
        b = self.b_input.text().strip()
        c = self.c_input.text().strip()
        d = self.d_input.text().strip()
        correct = self.correct_input.currentText()

        if not q or not a or not b or not c or not d:
            QMessageBox.warning(self, "Error", "Semua field wajib diisi.")
            return

        if update_question(self.qid, q, a, b, c, d, correct):
            QMessageBox.information(self, "Berhasil", "Soal berhasil diperbarui.")
            self.accept()
        else:
            QMessageBox.warning(self, "Gagal", "Gagal menyimpan soal.")

class ScoreListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daftar Skor Pengguna")
        self.setWindowIcon(QtGui.QIcon('logo.ico'))
        self.setFixedSize(700, 800)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #4e54c8, stop: 1 #8f94fb);
            }
        """)

        self.card = QFrame()
        self.card.setFixedSize(650, 750)
        self.card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        layout = QVBoxLayout(self.card)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("Skor Pengguna")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)

        self.load_scores()

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.addWidget(self.card)

    def load_scores(self):
        from database import get_all_user_scores
        self.clear_scroll()

        scores = get_all_user_scores()
        if not scores:
            msg = QLabel("Belum ada data jawaban pengguna.")
            self.scroll_layout.addWidget(msg)
            return

        for uid, username, total, benar, salah in scores:
            frame = QFrame()
            frame.setStyleSheet("background-color: #f5f5f5; padding: 10px; border-radius: 8px;")
            f_layout = QVBoxLayout(frame)

            info = QLabel(f"ID: {uid} | Username: {username}\nJawaban: {total} | Benar: {benar} | Salah: {salah}")
            info.setStyleSheet("font-size: 13px;")
            info.setWordWrap(True)

            f_layout.addWidget(info)
            self.scroll_layout.addWidget(frame)

    def clear_scroll(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
