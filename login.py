from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush
import sys
from database import register_user, login_user, reset_password
from menu import MenuWindow  # Nanti kamu buat
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register - Duolingo Sederhana")
        self.setFixedSize(1200, 600)
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
        self.card = QFrame(self)
        self.card.setFixedSize(300, 300)
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
        title = QLabel("Register", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Input username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.username_input)

        # Input password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.password_input)

        # Tombol Register
        register_btn = QPushButton("Register")
        register_btn.setStyleSheet("""
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
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if register_user(username, password):
            QMessageBox.information(self, "Berhasil", "Registrasi berhasil!")
            self.close()
        else:
            QMessageBox.warning(self, "Gagal", "Username sudah digunakan.")


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Duolingo Sederhana")
        self.setFixedSize(1200, 600)
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
        self.card = QFrame(self)
        self.card.setFixedSize(300, 450)
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
        title = QLabel("Login", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Input username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Email")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.username_input)

        # Input password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.password_input)

        # Tombol login
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("""
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
        self.login_btn.clicked.connect(self.handle_login)
        layout.addWidget(self.login_btn)

        # Forgot Password link
        forgot = QLabel('<a href="#">Forgot Password?</a>', self.card)
        forgot.setAlignment(Qt.AlignCenter)
        forgot.setOpenExternalLinks(False)
        forgot.linkActivated.connect(self.open_forgot_password)  # <-- ini panggil method baru
        layout.addWidget(forgot)

        # Sign up link
        signup = QLabel("Don\'t have an account? <a href=\"#\">Sign up</a>", self.card)
        signup.setAlignment(Qt.AlignCenter)
        signup.setOpenExternalLinks(False)
        signup.linkActivated.connect(self.open_register)  # <-- ini juga
        layout.addWidget(signup)
    
    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def open_forgot_password(self):
        self.forgot_window = ForgotPasswordWindow()
        self.forgot_window.show()


    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = login_user(username, password)
        if user:
            QMessageBox.information(self, "Sukses", f"Selamat datang, {username}!")
            self.menu_window = MenuWindow(username, user[0])
            self.menu_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Gagal", "Username atau password salah.")

class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reset Password")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Password Baru")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.new_password_input)

        reset_btn = QPushButton("Reset Password")
        reset_btn.clicked.connect(self.reset_password)
        layout.addWidget(reset_btn)

        self.setLayout(layout)

    def reset_password(self):
        username = self.username_input.text()
        new_password = self.new_password_input.text()

        if reset_password(username, new_password):
            QMessageBox.information(self, "Berhasil", "Password berhasil direset.")
            self.close()
        else:
            QMessageBox.warning(self, "Gagal", "Username tidak ditemukan.")

# Jalankan aplikasi
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
