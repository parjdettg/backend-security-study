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


# [검증] 로그인 시도 통로
@app.route('/api/login', methods=['POST'])
def login():
    user_data = request.get_json()
    if not user_data or 'name' not in user_data or 'password' not in user_data:
        return jsonify({"error": "이름과 비밀번호를 입력하세요."}), 400
    
    name = user_data['name']
    password_input = user_data['password']

    # 1. 장부에서 해당 이름을 가진 사람을 찾는다
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE name = ?", (name,))
    result = c.fetchone()
    conn.close()

    # 2. 사람이 없으면 거절
    if not result:
        return jsonify({"error": "등록되지 않은 사용자입니다."}), 401
    
    # 장부에 저장된 외계어(해시) 꺼내기
    stored_hashed_password = result[0]

    # 3. [보안의 정수] 입력한 비번과 장부의 외계어를 대조한다!
    if check_password_hash(stored_hashed_password, password_input):
        return jsonify({
            "status": "success",
            "message": f"환영합니다, {name}님! 보안 검증을 통과하셨습니다."
        })
    else:
        # 비번이 틀렸을 때
        return jsonify({"error": "비밀번호가 일치하지 않습니다."}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)    