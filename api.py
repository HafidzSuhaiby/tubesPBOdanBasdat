# api.py
import requests

API_BASE_URL = "http://192.168.1.5:5000"  # GANTI sesuai IP server Flask kamu

def api_login(identifier, password):
    try:
        response = requests.post(f"{API_BASE_URL}/login", json={
            "identifier": identifier,
            "password": password
        })
        response.raise_for_status()
        return response.json()  # {id, role}
    except requests.RequestException as e:
        return {"error": str(e)}

def api_get_lessons():
    try:
        response = requests.get(f"{API_BASE_URL}/lessons")
        response.raise_for_status()
        return response.json()  # List of lessons
    except requests.RequestException as e:
        return {"error": str(e)}
    
def api_add_lesson(title, description=""):
    try:
        response = requests.post(f"{API_BASE_URL}/lessons", json={
            "title": title,
            "description": description
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def api_get_chapters(lesson_id):
    try:
        response = requests.get(f"{API_BASE_URL}/chapters", params={"lesson_id": lesson_id})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def api_add_chapter(title, lesson_id):
    try:
        response = requests.post(f"{API_BASE_URL}/chapters", json={
            "title": title,
            "lesson_id": lesson_id
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def api_get_questions(chapter_id):
    try:
        response = requests.get(f"{API_BASE_URL}/questions", params={"chapter_id": chapter_id})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def api_add_question(data):
    try:
        response = requests.post(f"{API_BASE_URL}/questions", json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def api_submit_answer(user_id, chapter_id, question, answer, correct):
    try:
        response = requests.post(f"{API_BASE_URL}/submit_answer", json={
            "user_id": user_id,
            "chapter_id": chapter_id,
            "question": question,
            "answer": answer,
            "correct": correct
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def api_mark_chapter_complete(user_id, chapter_id):
    try:
        response = requests.post(f"{API_BASE_URL}/progress", json={
            "user_id": user_id,
            "chapter_id": chapter_id
        })
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

