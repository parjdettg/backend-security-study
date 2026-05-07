import json

# 서버가 요청을 처리하는 함수
def handle_request(request_type):
    if request_type == "GET_INFO":
        return {"status": "success", "message": "보안 점검 완료", "level": "Master Candidate"}
    else:
        return {"status": "error", "message": "잘못된 요청"}

# 가상의 요청 실행
user_request = "GET_INFO"
response = handle_request(user_request)

# 결과를 사람이 보기 좋게 출력
print(f"서버 응답 데이터: {json.dumps(response, ensure_ascii=False, indent=4)}")