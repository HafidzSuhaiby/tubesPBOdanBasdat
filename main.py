from login import login_user
from menu import show_menu
from lessons import tampilkan_lessons
from quiz import mulai_kuis
from users import Admin, SiswaBiasa, SiswaSuper

def main():
    user = login_user()
    if user:
        print(f"Selamat datang, {user.get_info()}")
        show_menu(user)

if __name__ == "__main__":
    main()
