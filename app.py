import sqlite3
from flask import Flask, jsonify, request
# [보안 무기 장착] 비밀번호 해싱 도구 가져오기
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # 장부에 password 칸을 추가해서 새로 만든다
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL, 
                  password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/register', methods=['POST'])
def register():
    user_data = request.get_json()
    if not user_data or 'name' not in user_data or 'password' not in user_data:
        return jsonify({"error": "이름과 비밀번호가 모두 필요합니다."}), 400
    
    name = user_data['name']
    raw_password = user_data['password']

    # [보안의 핵심] 비밀번호를 알아볼 수 없는 '해시'로 변신시킨다!
    hashed_password = generate_password_hash(raw_password)

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # 장부에는 진짜 비밀번호(raw_password)가 아닌 해시(hashed_password)를 저장한다
    c.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({
        "message": f"{name}님 가입 완료!",
        "security_log": f"비밀번호가 안전하게 {hashed_password[:15]}... 로 암호화되었습니다."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)