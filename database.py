import mysql.connector

# Fungsi untuk membuat koneksi ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # ganti jika ada password
        database="test_server"
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

def get_chapters_by_lesson(lesson_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM chapters WHERE lesson_id = %s", (lesson_id,))
    chapters = cursor.fetchall()
    conn.close()
    return chapters

def add_chapter(title, lesson_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chapters (title, lesson_id) VALUES (%s, %s)", (title, lesson_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error tambah bab:", e)
        return False
    finally:
        conn.close()

def add_question(question, option_a, option_b, option_c, option_d, correct_option, chapter_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions 
            (question, option_a, option_b, option_c, option_d, correct_option, chapter_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (question, option_a, option_b, option_c, option_d, correct_option, chapter_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error tambah soal:", e)
        return False
    finally:
        conn.close()




def get_lessons():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM lessons")
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        print("Error get_lessons:", e)
        return []

def get_all_users():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_info_view")
        users = cursor.fetchall()
        return users
    except Exception as e:
        print("Error get_all_users:", e)
        return []
    finally:
        conn.close()

def update_user_role(user_id, new_role):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error update_user_role:", e)
        return False
    finally:
        conn.close()

def delete_user(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print("Error delete_user:", e)
        return False
    finally:
        conn.close()

def edit_user(user_id, new_username, new_email):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (new_username, new_email, user_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error edit_user:", e)
        return False
    finally:
        conn.close()

def get_user_id_by_username(username):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print("Error get_user_id_by_username:", e)
        return None
    finally:
        conn.close()

def get_user_lives(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT lives FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print("Error get_user_lives:", e)
        return 0
    finally:
        conn.close()

def get_all_questions(view_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT question_id, question, option_a, option_b, option_c, option_d, correct_option, chapter_title, lesson_title FROM {view_name}")
        questions = cursor.fetchall()
        return questions
    except Exception as e:
        print("Error get_all_questions:", e)
        return []
    finally:
        conn.close()

def update_question(question_id, question, a, b, c, d, correct):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE questions
            SET question = %s, option_a = %s, option_b = %s, option_c = %s, option_d = %s, correct_option = %s
            WHERE id = %s
        """, (question, a, b, c, d, correct, question_id))
        conn.commit()
        return True
    except Exception as e:
        print("Error update_question:", e)
        return False
    finally:
        conn.close()

def get_all_user_scores():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.callproc('get_all_user_scores')
        for result in cursor.stored_results():
            return result.fetchall()
    except Exception as e:
        print("Error get_all_user_scores (proc):", e)
        return []
    finally:
        conn.close()

