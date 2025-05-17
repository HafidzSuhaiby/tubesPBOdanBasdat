from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QListWidget, QListWidgetItem,
    QApplication, QHBoxLayout, QDialog, QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap, QCursor, QFont
from PyQt5.QtCore import Qt
import sys
from database import connect_db
from lessons import ChapterWindow


# === Dialog Profil ===
class ProfileDialog(QDialog):
    def __init__(self, parent, username, email):
        super().__init__(parent)
        self.setWindowTitle("Profil Pengguna")
        self.setFixedSize(300, 200)
        self.username = username
        self.email = email
        self.parent = parent

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Username: {username}"))
        layout.addWidget(QLabel(f"Email: {email}"))

        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.handle_logout)
        layout.addWidget(btn_logout)

        self.setLayout(layout)

    def handle_logout(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.parent.close()
        self.close()


# === MenuWindow ===
class MenuWindow(QWidget):
    def __init__(self, username, user_id, email="user@example.com"):
        super().__init__()
        self.setWindowTitle("Pilih Pelajaran")
        self.username = username
        self.user_id = user_id
        self.email = email
        self.setFixedSize(350, 600)

        self.setStyleSheet("""
        QWidget {
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #4e54c8,
                stop: 1 #8f94fb
            );
            font-family: 'Segoe UI', Arial;
        }

        QLabel {
            color: #222;
        }

        QListWidget {
            font-size: 18px;
            padding: 10px;
            border: none;
            background: transparent;
        }

        QListWidget::item {
            background: #ffffff;
            margin: 4px;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #ddd;
            color: #222;
            transition: all 0.3s ease;
        }

        QListWidget::item:hover {
            background-color: #5d63d8;
            color: white;
            font-weight: bold;
        }

        QListWidget::item:selected {
            background: #5c63d8;
            color: white;
            font-weight: bold;
            border: none;
        }
        """)

        main_layout = QVBoxLayout()

        # Top bar
        top_bar = QHBoxLayout()
        self.profile_pic = QLabel()
        pixmap = QPixmap("profil.png").scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.profile_pic.setPixmap(pixmap)
        self.profile_pic.setCursor(QCursor(Qt.PointingHandCursor))
        self.profile_pic.setStyleSheet("background: transparent; border-radius: 15px;")
        self.profile_pic.mousePressEvent = self.show_user_info

        self.halo_label = QLabel(f"Halo, {username}")
        self.halo_label.setStyleSheet("font-size: 13px; margin-left: 5px; background: transparent;")
        self.halo_label.setFont(QFont("Segoe UI", 10))

        self.lives_label = QLabel()
        self.lives_label.setStyleSheet("font-size: 13px; color: white; background: transparent; margin-right: 10px;")
        self.lives_label.setFont(QFont("Segoe UI", 10))
        self.update_lives_display()

        top_bar.addWidget(self.profile_pic)
        top_bar.addWidget(self.halo_label)
        top_bar.addStretch()
        top_bar.addWidget(self.lives_label)

        main_layout.addLayout(top_bar)

        # Label judul
        self.pilih_label = QLabel("Silakan pilih pelajaran:")
        self.pilih_label.setAlignment(Qt.AlignCenter)
        self.pilih_label.setStyleSheet("font-size: 16px; margin-top: 30px; background: transparent; color: white;")
        self.pilih_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        main_layout.addWidget(self.pilih_label)

        # Daftar pelajaran
        self.lesson_list = QListWidget()
        self.lesson_list.setSpacing(10)
        self.lesson_list.setFocusPolicy(Qt.NoFocus)
        self.lesson_list.itemClicked.connect(self.start_quiz)
        self.lesson_list.setFixedWidth(260)

        lesson_container = QHBoxLayout()
        lesson_container.addStretch()
        lesson_container.addWidget(self.lesson_list)
        lesson_container.addStretch()
        main_layout.addLayout(lesson_container)

        self.setLayout(main_layout)
        self.load_lessons()

    def load_lessons(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, title FROM lessons")
        lessons = cursor.fetchall()
        db.close()

        self.lesson_map = {}
        self.lesson_list.clear()
        for lesson in lessons:
            title = lesson[1]
            self.lesson_map[title] = lesson[0]
            item = QListWidgetItem(title)
            item.setTextAlignment(Qt.AlignCenter)
            self.lesson_list.addItem(item)

    def update_lives_display(self):
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT lives FROM users WHERE id = %s", (self.user_id,))
            result = cursor.fetchone()
            db.close()
            if result:
                lives = result[0]
                self.lives_label.setText(f"❤️ {lives}")
        except Exception as e:
            self.lives_label.setText("❤️ ?")
            print("Gagal memuat nyawa:", e)

    def start_quiz(self, item):
        try:
            title = item.text()
            lesson_id = self.lesson_map[title]
            self.chapter_window = ChapterWindow(
                self.username, self.user_id, lesson_id, title
            )
            self.chapter_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "ERROR", f"Gagal buka ChapterWindow:\n{e}")

    def show_user_info(self, event):
        dialog = ProfileDialog(self, self.username, self.email)
        dialog.exec_()

    def logout_user(self):
        from login import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


# Jalankan aplikasi untuk testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuWindow("testuser", 1, "testuser@example.com")
    window.show()
    sys.exit(app.exec_())
