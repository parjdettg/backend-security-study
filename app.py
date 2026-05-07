from flask import Flask, jsonify

app = Flask(__name__)

# 정문(Root) 경로
@app.route('/')
def home():
    return "<h1>Backend Master Server Online</h1><p>Security Check: Passed</p>"

# 데이터 통신 전용 통로 (API)
@app.route('/api/status')
def get_status():
    data = {
        "status": "running",
        "instructor": "Gemini",
        "message": "천만 원짜리 수업에 오신 걸 환영합니다."
    }
    return jsonify(data)

if __name__ == '__main__':
    # 5000번 포트로 서버 가동!
    app.run(debug=True, port=5000)