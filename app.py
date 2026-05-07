import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

# [DB 설정] 데이터베이스 초기화 함수
def init_db():
    # 'database.db'라는 파일 이름의 장부를 만든다
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # users라는 이름의 표가 없으면 새로 만든다 (id와 name 칸 생성)
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# 서버 시작 전 장부부터 확인!
init_db()

@app.route('/')
def home():
    return "<h1>4장: 데이터베이스 마스터</h1>"

# [저장] 이름을 장부에 기록하는 통로
@app.route('/api/greet', methods=['POST'])
def greet_user():
    user_data = request.get_json()
    if not user_data or 'name' not in user_data:
        return jsonify({"error": "이름이 필요함"}), 400
    
    name = user_data['name']

    # [보안 핵심] 데이터베이스에 저장
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # [1000만원짜리 팁] 물음표(?)를 써서 데이터를 넣어야 해. (SQL 인젝션 방어)
    c.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"{name}님, 장부에 기록 완료!"})

# [조회] 장부에 누가 있는지 다 보여주는 통로
@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    
    # 데이터를 보기 좋게 정리
    user_list = [{"id": row[0], "name": row[1]} for row in rows]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)