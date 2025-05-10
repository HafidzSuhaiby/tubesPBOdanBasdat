import mysql.connector
import sqlite3

# Fungsi untuk membuat koneksi ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # ganti jika ada password
        database="duolingo_sederhana"
    )

# Fungsi untuk registrasi user baru
def register_user(username, email, password):
    db = connect_db()
    cursor = db.cursor()

    # Cek apakah username atau email sudah dipakai
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    if cursor.fetchone():
        db.close()
        return False  # Username atau email sudah dipakai

    # Insert user baru
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
    db.commit()
    db.close()
    return True

def login_user(identifier, password):
    conn = connect_db()
    cursor = conn.cursor()
    # Cek apakah identifier cocok dengan username atau email
    cursor.execute("SELECT id, role FROM users WHERE (username = %s OR email = %s) AND password = %s",(identifier, identifier, password))
    user = cursor.fetchone()
    conn.close()
    return user  # (id, role)


def reset_password(username, new_password):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, username))
        db.commit()
        db.close()
        return True

    db.close()
    return False

def add_lesson(title, desc):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lessons (title, description) VALUES (%s, %s)", (title, desc))
        conn.commit()
        return True
    except Exception as e:
        print("Error tambah pelajaran:", e)
        return False
    finally:
        conn.close()

def add_question(question, correct_answer, lesson_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO questions (question_text, correct_answer, lesson_id) VALUES (%s, %s, %s)",
            (question, correct_answer, lesson_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print("Error tambah soal:", e)
        return False
    finally:
        conn.close()
