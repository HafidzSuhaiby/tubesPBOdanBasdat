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
def register_user(username, password):
    db = connect_db()
    cursor = db.cursor()

    # Cek apakah username sudah ada
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        db.close()
        return False  # Username sudah ada

    # Insert user baru
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    db.close()
    return True

# Fungsi untuk login
def login_user(username, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    db.close()
    return user  # Akan None jika tidak ditemukan

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

