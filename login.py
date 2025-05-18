from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush
import sys
from database import register_user, login_user, reset_password, connect_db
from menu import MenuWindow  
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont
from users import Admin, SiswaBiasa, SiswaSuper


class SplashScreenWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bahasaku - Splash")
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

        # Tambahkan QLabel untuk gambar
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("logo.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(200, 200)
        self.image_label.setAttribute(Qt.WA_TranslucentBackground)
        self.image_label.setStyleSheet("background: transparent;")
        self.image_label.move((self.width() - 200) // 2, self.height())  # mulai dari bawah


        # Animasi slide dari bawah ke tengah
        self.animation = QPropertyAnimation(self.image_label, b"pos")
        self.animation.setDuration(1200)
        self.animation.setStartValue(QPoint((self.width() - 200) // 2, self.height()))
        self.animation.setEndValue(QPoint((self.width() - 200) // 2, (self.height() - 200) // 2))
        self.animation.finished.connect(self.finish_animation)
        self.animation.start()

    def finish_animation(self):
        QTimer.singleShot(1000, self.show_login)

    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()



class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register - Duolingo Sederhana")
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

        # Card putih di tengah
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
        title = QLabel("Register", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        #input Username
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Username")
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.name_input)

        # Input Email
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
        username = self.name_input.text()
        email = self.username_input.text()
        password = self.password_input.text()
        
        if register_user(username, email, password):
            QMessageBox.information(self, "Berhasil", "Registrasi berhasil!")
            self.close()
        else:
            QMessageBox.warning(self, "Gagal", "Username atau email sudah digunakan.")



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Duolingo Sederhana")
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
        self.username_input.setPlaceholderText("Username atau Email")
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

        result = login_user(username, password)  # Misal return (user_id, role)

        if not result:
            QMessageBox.warning(self, "Login Gagal", "Username atau password salah.")
            return

        user_id, role = result

        # Buat objek sesuai role
        try:
            if role == "admin":
                user_obj = Admin(user_id, username)
            elif role == "siswa_super":
                user_obj = SiswaSuper(user_id, username)
            else:
                user_obj = SiswaBiasa(user_id, username)
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid user data: {e}")
            return


        QMessageBox.information(self, "Sukses", f"Selamat datang, {user_obj.username}!")

        try:
            if isinstance(user_obj, Admin):
                from admin import AdminMenuWindow
                # Pastikan argumen sesuai constructor AdminMenuWindow
                self.menu_window = AdminMenuWindow(user_obj.username, user_obj.user_id)
            else:
                from menu import MenuWindow
                self.menu_window = MenuWindow(user_obj.username, user_obj.user_id)
        
            self.menu_window.show()
            self.close()

        except Exception as e:
            print("Gagal membuka menu:", e)
            QMessageBox.warning(self, "Error", f"Gagal membuka menu: {e}")


class ForgotPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reset Password - Duolingo Sederhana")
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

        # Card putih di tengah
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
        title = QLabel("Reset Password", self.card)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Input Username
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

        # Input Password Baru
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Password Baru")
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
            }
        """)
        layout.addWidget(self.new_password_input)

        # Tombol Reset Password
        reset_btn = QPushButton("Reset Password")
        reset_btn.setStyleSheet("""
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
        reset_btn.clicked.connect(self.reset_password)
        layout.addWidget(reset_btn)

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
    splash = SplashScreenWindow()
    splash.show()
    sys.exit(app.exec_())


