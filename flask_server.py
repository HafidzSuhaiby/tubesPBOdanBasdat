from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from datetime import datetime, date

app = Flask(__name__)
CORS(app)  # agar bisa diakses dari luar (PyQt5 client)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # sesuaikan
        database="duolingo_sederhana"
    )

@app.route("/")
def index():
    return "API BahasaKu aktif!"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    identifier = data.get("identifier")
    password = data.get("password")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, role FROM users WHERE (username = %s OR email = %s) AND password = %s", 
                   (identifier, identifier, password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return jsonify({"status": "success", "id": result[0], "role": result[1]})
    else:
        return jsonify({"status": "fail", "message": "Username/email atau password salah"}), 401

# ================== ENDPOINT PELAJARAN ================== #

# Ambil semua pelajaran
@app.route("/lessons", methods=["GET"])
def get_lessons():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM lessons")
        results = cursor.fetchall()
        conn.close()
        return jsonify([{"id": r[0], "title": r[1]} for r in results])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Tambah pelajaran baru
@app.route("/lessons", methods=["POST"])
def add_lesson():
    try:
        data = request.json
        title = data.get("title")
        desc = data.get("description", "")
        if not title:
            return jsonify({"status": "fail", "message": "Judul tidak boleh kosong"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lessons (title, description) VALUES (%s, %s)", (title, desc))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Pelajaran '{title}' ditambahkan."})
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500

# ================== ENDPOINT BAB ================== #

@app.route("/chapters", methods=["GET"])
def get_chapters():
    lesson_id = request.args.get("lesson_id")
    if not lesson_id:
        return jsonify({"status": "fail", "message": "lesson_id wajib"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM chapters WHERE lesson_id = %s", (lesson_id,))
        results = cursor.fetchall()
        conn.close()
        return jsonify([{"id": r[0], "title": r[1]} for r in results])
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500

@app.route("/chapters", methods=["POST"])
def add_chapter():
    data = request.json
    title = data.get("title")
    lesson_id = data.get("lesson_id")

    if not title or not lesson_id:
        return jsonify({"status": "fail", "message": "title dan lesson_id wajib"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chapters (title, lesson_id) VALUES (%s, %s)", (title, lesson_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"BAB '{title}' ditambahkan."})
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500

# ================== ENDPOINT SOAL ================== #

@app.route("/questions", methods=["GET"])
def get_questions():
    chapter_id = request.args.get("chapter_id")
    if not chapter_id:
        return jsonify({"status": "fail", "message": "chapter_id wajib"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, question, option_a, option_b, option_c, option_d, correct_option
            FROM questions
            WHERE chapter_id = %s
        """, (chapter_id,))
        results = cursor.fetchall()
        conn.close()

        return jsonify([
            {
                "id": r[0],
                "question": r[1],
                "a": r[2],
                "b": r[3],
                "c": r[4],
                "d": r[5],
                "correct": r[6]
            }
            for r in results
        ])
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500


@app.route("/questions", methods=["POST"])
def add_question():
    data = request.json
    fields = ["question", "a", "b", "c", "d", "correct", "chapter_id"]
    if not all(k in data and data[k] for k in fields):
        return jsonify({"status": "fail", "message": "Semua field harus diisi"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions 
            (question, option_a, option_b, option_c, option_d, correct_option, chapter_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["question"], data["a"], data["b"], data["c"],
            data["d"], data["correct"], data["chapter_id"]
        ))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Soal berhasil ditambahkan"})
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500
    
@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    user_id = data.get("user_id")
    chapter_id = data.get("chapter_id")
    question = data.get("question")
    answer = data.get("answer")
    correct = data.get("correct")

    if None in (user_id, chapter_id, question, answer, correct):
        return jsonify({"status": "fail", "message": "Data tidak lengkap"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Simpan jawaban
        cursor.execute("""
            INSERT INTO user_answers (user_id, chapter_id, question, answer, correct)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE answer=%s, correct=%s
        """, (user_id, chapter_id, question, answer, correct, answer, correct))

        # Cek dan kurangi nyawa jika salah
        if not correct:
            cursor.execute("SELECT lives, last_life_reset FROM users WHERE id = %s", (user_id,))
            lives_row = cursor.fetchone()
            today = date.today()

            if lives_row:
                lives, last_reset = lives_row
                # reset harian
                if last_reset is None or str(last_reset) != str(today):
                    lives = 5
                if lives > 0:
                    lives -= 1
                    cursor.execute("UPDATE users SET lives = %s, last_life_reset = %s WHERE id = %s",
                                   (lives, today, user_id))

        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Jawaban disimpan", "lives": lives})
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500

@app.route("/lives", methods=["GET"])
def get_lives():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id wajib"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT lives, last_life_reset FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        today = date.today()

        if not row:
            conn.close()
            return jsonify({"lives": 0})

        lives, last_reset = row
        if last_reset is None or str(last_reset) != str(today):
            lives = 5
            cursor.execute("UPDATE users SET lives = 5, last_life_reset = %s WHERE id = %s", (today, user_id))
            conn.commit()

        conn.close()
        return jsonify({"lives": lives})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/progress", methods=["POST"])
def update_progress():
    data = request.json
    user_id = data.get("user_id")
    chapter_id = data.get("chapter_id")

    if not user_id or not chapter_id:
        return jsonify({"status": "fail", "message": "user_id dan chapter_id wajib"}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_progress (user_id, chapter_id, completed)
            VALUES (%s, %s, TRUE)
            ON DUPLICATE KEY UPDATE completed = TRUE
        """, (user_id, chapter_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Progress berhasil disimpan"})
    except Exception as e:
        return jsonify({"status": "fail", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
