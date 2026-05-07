from flask import Flask, jsonify, request # request를 추가로 가져와야 해!

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>3장: 데이터 통신 입문</h1>"

# [핵심] 데이터를 받아서 처리하는 통로 (POST 방식)
@app.route('/api/greet', methods=['POST'])
def greet_user():
    # 사용자가 보낸 JSON 데이터를 읽어와
    user_data = request.get_json()
    
    # [보안 포인트] 데이터가 비어있으면 거절한다! (Validation)
    if not user_data or 'name' not in user_data:
        return jsonify({"error": "이름이 없으면 입장을 거부합니다."}), 400
    
    name = user_data['name']
    return jsonify({
        "message": f"안녕하세요, {name}님! 당신은 백엔드 마스터 후보입니다.",
        "status": "success"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)