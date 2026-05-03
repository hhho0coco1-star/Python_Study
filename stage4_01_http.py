# ============================================================
# Stage 4 - 01. HTTP 기초 & requests 라이브러리
# ============================================================
# HTTP(HyperText Transfer Protocol): 클라이언트와 서버가 데이터를 주고받는 규약
# requests: 파이썬에서 HTTP 요청을 한 줄로 보낼 수 있는 외부 라이브러리
#
# 실습 API: https://jsonplaceholder.typicode.com (무료 테스트 API)
#   - 실제 DB 없이 HTTP 메서드 실습 가능 (응답은 가짜 데이터)
#
# [사전 설치]
#   pip install requests
#
# 학습 순서
#   1. HTTP 메서드 & 상태 코드 개념
#   2. GET 요청 — 데이터 조회
#   3. POST 요청 — 데이터 생성
#   4. PUT / PATCH / DELETE — 수정 & 삭제
#   5. 에러 처리 & 실전 패턴

import requests  # HTTP 요청 전송 라이브러리
import json      # JSON 직렬화/역직렬화 표준 라이브러리


# ============================================================
# [이론 1] HTTP 메서드 & 상태 코드
# ============================================================
#
# HTTP 메서드 (CRUD 와 1:1 대응)
#   GET    → 데이터 조회  (Read)   — URL에 데이터 포함, Body 없음
#   POST   → 데이터 생성  (Create) — Body에 데이터 포함
#   PUT    → 데이터 전체 수정 (Update) — 리소스 전체를 교체
#   PATCH  → 데이터 부분 수정 (Update) — 일부 필드만 변경
#   DELETE → 데이터 삭제  (Delete) — Body 없음
#
# REST API URL 패턴 예시
#   GET    /posts       → 모든 게시글 조회
#   GET    /posts/1     → ID=1인 게시글 조회
#   POST   /posts       → 새 게시글 생성
#   PUT    /posts/1     → ID=1 게시글 전체 수정
#   PATCH  /posts/1     → ID=1 게시글 일부 수정
#   DELETE /posts/1     → ID=1 게시글 삭제
#
# HTTP 상태 코드 (응답 코드)
#   200 OK              : 요청 성공 (조회, 수정, 삭제)
#   201 Created         : 리소스 생성 성공 (POST 요청 후)
#   400 Bad Request     : 잘못된 요청 (파라미터 오류 등)
#   401 Unauthorized    : 인증 필요 (로그인 안 됨)
#   403 Forbidden       : 권한 없음 (로그인은 됐지만 접근 불가)
#   404 Not Found       : 리소스 없음 (URL 오류)
#   422 Unprocessable   : 입력값 유효성 검사 실패
#   500 Internal Error  : 서버 내부 오류

print("=== [이론 1] 상태 코드 분류 ===")
status_codes = {
    "2xx 성공": ["200 OK", "201 Created", "204 No Content"],
    "4xx 클라이언트 오류": ["400 Bad Request", "401 Unauthorized", "403 Forbidden", "404 Not Found"],
    "5xx 서버 오류": ["500 Internal Server Error", "502 Bad Gateway"],
}
# 딕셔너리로 상태 코드 그룹 정의 — key: 분류명, value: 코드 목록

for category, codes in status_codes.items():
    # .items() → (key, value) 쌍으로 순회
    print(f"[{category}]")
    for code in codes:
        print(f"  - {code}")


# ============================================================
# [실습 1] HTTP 메서드 & 상태 코드
# ============================================================
# 1) 아래 URL 패턴을 딕셔너리로 정의하세요.
#    - "게시글 목록 조회"  : GET /posts
#    - "게시글 단건 조회"  : GET /posts/{id}
#    - "게시글 생성"       : POST /posts
#    - "게시글 삭제"       : DELETE /posts/{id}
# 2) 딕셔너리를 순회하며 "동작명 → 메서드 경로" 형식으로 출력하세요.
# 코드 작성 ↓

# [정답 코드]
api_map = {
    "게시글 목록 조회": "GET /posts",
    "게시글 단건 조회": "GET /posts/{id}",
    "게시글 생성":     "POST /posts",
    "게시글 삭제":     "DELETE /posts/{id}",
}
api_map2 = {
    "게시글 목록 조회" : "GET /posts",
    "게시글 단건 조회" : "GET /posts/{id}",
    "게시글 생성" : "POST /posts",
    "게시글 삭제" : "DELETE /posts/{id}",
}
# 딕셔너리로 API 설계 명세 정의 — key: 동작명, value: "메서드 경로" 문자열

print("\n=== [실습 1] API 설계 명세 ===")
for action, endpoint in api_map.items():
    print(f"{action} → {endpoint}")
    # f-string으로 "동작명 → 메서드 경로" 형식 출력
for action, endpoint in api_map2.items():
    print(f"{action} → {endpoint}")


# ============================================================
# [이론 2] GET 요청 — 데이터 조회
# ============================================================
#
# GET 요청: 서버에서 데이터를 읽어오는 요청 (데이터 변경 없음)
#
# 기본 패턴:
#   response = requests.get(url)
#   response = requests.get(url, params={"key": "value"})  # 쿼리 파라미터
#
# 응답 객체 주요 속성/메서드:
#   response.status_code   : HTTP 상태 코드 (int) — 예: 200
#   response.ok            : 상태 코드가 200~299이면 True
#   response.text          : 응답 본문을 문자열로 반환
#   response.json()        : 응답 본문을 딕셔너리(또는 리스트)로 파싱
#   response.headers       : 응답 헤더 딕셔너리
# 파싱(Parsing) : 일련의 문자열(데이터)을 설정된 문법 규칙에 따라 분석하여, 
# 컴퓨터가 이해할 수 있는 의미 있는 구조로 변환하는 과정을 말합니다
# 쿼리 파라미터: URL 뒤에 ?key=value 형태로 붙는 필터/검색 조건
#   예) /posts?userId=1 → userId가 1인 게시글만 조회

BASE_URL = "https://jsonplaceholder.typicode.com"
# 실습에 사용할 기본 URL 상수로 정의 — 이후 엔드포인트를 더해서 사용

print("\n=== [이론 2] GET 요청 — 게시글 목록 조회 ===")

response = requests.get(f"{BASE_URL}/posts")
# requests.get(url): 해당 URL로 GET 요청 전송 → response 객체 반환
# f-string으로 BASE_URL + "/posts" 를 합쳐 "https://jsonplaceholder.typicode.com/posts" 생성

print(f"상태 코드: {response.status_code}")
# 서버가 반환한 HTTP 상태 코드 출력 — 200이면 성공

print(f"응답 성공 여부: {response.ok}")
# response.ok: status_code가 200~299 사이이면 True, 그 외 False

posts = response.json()
# 응답 본문(JSON 문자열)을 파이썬 리스트로 변환
# jsonplaceholder /posts는 100개의 게시글 딕셔너리를 담은 리스트 반환

print(f"게시글 수: {len(posts)}개")
# len(posts): 리스트 길이 = 게시글 총 수 (100개)

print(f"첫 번째 게시글: {posts[0]}")
# posts[0]: 리스트 첫 번째 딕셔너리 출력 — id, userId, title, body 키 포함

print("\n=== [이론 2] GET 요청 — 단건 조회 ===")

post_id = 1
response_single = requests.get(f"{BASE_URL}/posts/{post_id}")
# URL에 post_id를 포함해 특정 게시글 1개만 조회
# /posts/1 → id=1인 게시글 반환

post = response_single.json()
# 단건 조회는 딕셔너리 1개 반환 (리스트가 아님)

print(f"제목: {post['title']}")
# post['title']: 딕셔너리에서 'title' 키의 값 접근

print(f"본문: {post['body'][:50]}...")
# post['body'][:50]: 본문 문자열의 앞 50글자만 슬라이싱해서 출력

print("\n=== [이론 2] GET 요청 — 쿼리 파라미터 ===")

response_filtered = requests.get(
    f"{BASE_URL}/posts",
    params={"userId": 1} # ?userId=1(parameter)
    # params 딕셔너리: {"userId": 1} → URL에 ?userId=1 을 자동으로 붙여줌
    # 실제 요청 URL: https://jsonplaceholder.typicode.com/posts?userId=1
)
filtered_posts = response_filtered.json()
print(f"userId=1의 게시글 수: {len(filtered_posts)}개")
# userId가 1인 게시글만 필터링되어 10개 반환


# ============================================================
# [실습 2] GET 요청
# ============================================================
# jsonplaceholder API를 사용하여:
# 1) /users 엔드포인트로 GET 요청을 보내고 사용자 수를 출력하세요.
# response_users = requests.get(f"{BASE_URL}/users")
# 2) 첫 번째 사용자의 name과 email을 출력하세요.
# 3) /users/3 으로 단건 조회 후 company의 name을 출력하세요.
#    (힌트: user['company']['name'] 형태로 접근)
# 코드 작성 ↓

# [정답 코드]
# 1) /users 전체 조회
resp_users = requests.get(f"{BASE_URL}/users")
# /users 엔드포인트로 GET 요청 전송

# users = resp_users.json()
users = resp_users.json() # json 파싱 -> 구조 변환
print(f"사용자 수 : {len(users)}명")
# 응답 JSON → 파이썬 리스트(사용자 10명)로 변환

print("\n=== [실습 2] 사용자 조회 ===")
print(f"사용자 수: {len(users)}명")

# 2) 첫 번째 사용자 정보
# first_user = users[0]
# 리스트 인덱스 0 = 첫 번째 사용자 딕셔너리
first_user = users[0]
print(f"이름 : {first_user['name']}, 이메일 : {first_user['email']}")

print(f"이름: {first_user['name']}")
print(f"이메일: {first_user['email']}")

# 3) id=3 단건 조회 → 중첩 딕셔너리 접근
# resp_user3 = requests.get(f"{BASE_URL}/users/3")
# user3 = resp_user3.json()

resp_user3 = requests.get(f"{BASE_URL}/users/3")
user3 = resp_user3.json()
print(f"id=3 회사명 : {user3['company']['name']}")

# 단건 조회 → 딕셔너리 1개 반환

print(f"id=3 회사명: {user3['company']['name']}")
# user3['company'] → 중첩 딕셔너리(회사 정보) 접근
# ['name'] → 회사명 문자열 접근


# ============================================================
# [이론 3] POST 요청 — 데이터 생성
# ============================================================
#
# POST 요청: 서버에 새 데이터를 생성하는 요청
#   - 요청 Body에 생성할 데이터를 JSON 형태로 담아 전송
#   - 성공 시 서버가 생성된 리소스 + 201 Created 반환
#
# 기본 패턴:
#   response = requests.post(url, json={"key": "value"})
#
# json= 파라미터:
#   - 딕셔너리를 자동으로 JSON 문자열로 직렬화
#   - Content-Type: application/json 헤더 자동 설정
#   - 직접 json.dumps()를 쓸 필요 없음

print("\n=== [이론 3] POST 요청 — 게시글 생성 ===")

new_post = {
    "title": "파이썬으로 보내는 첫 POST 요청",
    "body": "requests 라이브러리로 HTTP POST를 배웠습니다.",
    "userId": 1
}
# 생성할 게시글 데이터를 딕셔너리로 정의
# jsonplaceholder는 title, body, userId 3개 필드를 받음

response_post = requests.post(
    f"{BASE_URL}/posts",
    json=new_post
    # json= 파라미터: new_post 딕셔너리를 JSON으로 변환 후 Body에 포함
)
# /posts 엔드포인트로 POST 요청 전송

print(f"상태 코드: {response_post.status_code}")
# POST 성공 시 201 Created 반환 (200이 아님!)

created = response_post.json()
# 서버가 반환한 생성된 게시글 데이터 (id가 자동 부여됨)

print(f"생성된 게시글 ID: {created['id']}")
# jsonplaceholder는 101 이상의 가짜 ID 부여 (실제로 DB에 저장되지 않음)

print(f"생성된 제목: {created['title']}")


# ============================================================
# [실습 3] POST 요청
# ============================================================
# /todos 엔드포인트에 새 할 일을 생성하세요.
#   - userId: 1
#   - title: "파이썬 HTTP 챕터 완료하기"
#   - completed: False
# 생성 후 상태 코드와 반환된 데이터 전체를 출력하세요.
# 코드 작성 ↓

# [정답 코드]
new_todo = {
    "userId": 1,
    "title": "파이썬 HTTP 챕터 완료하기",
    "completed": False
}

new_todo2 = {
    "userId" : 1,
    "title" : "파이썬 HTTP 챕터 완료하기",
    "completed" : False
}
# 생성할 할 일 데이터 딕셔너리 정의

resp_todo = requests.post(
    f"{BASE_URL}/todos",
    json=new_todo
    # json= 파라미터로 딕셔너리 → JSON 자동 변환 후 Body 전송
)

resp_todo2 = requests.post(
    f"{BASE_URL}/todos",
    josn = new_todo2 
)

print("\n=== [실습 3] 할 일 생성 ===")
print(f"상태 코드: {resp_todo.status_code}")
# 201이면 생성 성공

created_todo = resp_todo.json()
print(f"생성된 데이터: {created_todo}")
# 반환된 딕셔너리 전체 출력 — id가 자동 부여되어 포함됨


# ============================================================
# [이론 4] PUT / PATCH / DELETE — 수정 & 삭제
# ============================================================
#
# PUT   : 리소스 전체를 교체 — 보내지 않은 필드는 초기화됨
# PATCH : 리소스 일부만 수정 — 보낸 필드만 변경, 나머지 유지
# DELETE: 리소스 삭제 — Body 없음, 성공 시 200 또는 204 반환
#
# PUT vs PATCH 차이:
#   PUT   → {"title": "새 제목"}만 보내면 body, userId 등이 null로 초기화
#   PATCH → {"title": "새 제목"}만 보내면 title만 변경, 나머지 필드 유지

print("\n=== [이론 4] PUT 요청 — 게시글 전체 수정 ===")

updated_post = {
    "id": 1,
    "title": "수정된 제목",
    "body": "수정된 본문 내용",
    "userId": 1
}
# PUT은 전체 교체이므로 모든 필드를 포함해야 함

resp_put = requests.put(
    f"{BASE_URL}/posts/1",
    json=updated_post
    # /posts/1: id=1인 게시글을 updated_post로 전체 교체
)
print(f"PUT 상태 코드: {resp_put.status_code}")
# 200 OK 반환
print(f"수정된 게시글: {resp_put.json()}")

print("\n=== [이론 4] PATCH 요청 — 제목만 수정 ===")

resp_patch = requests.patch(
    f"{BASE_URL}/posts/1",
    json={"title": "PATCH로 제목만 변경"}
    # PATCH는 변경할 필드만 전송 → 나머지 필드는 서버에서 유지
)
print(f"PATCH 상태 코드: {resp_patch.status_code}")
print(f"수정 결과: {resp_patch.json()}")

print("\n=== [이론 4] DELETE 요청 — 게시글 삭제 ===")

resp_delete = requests.delete(f"{BASE_URL}/posts/1")
# DELETE 요청: Body 없이 URL만으로 삭제 대상 지정

print(f"DELETE 상태 코드: {resp_delete.status_code}")
# 200 OK 반환 (서버에 따라 204 No Content를 반환하기도 함)

print(f"삭제 후 응답 본문: '{resp_delete.text}'")
# jsonplaceholder는 삭제 성공 시 빈 JSON {} 반환


# ============================================================
# [실습 4] PUT / PATCH / DELETE
# ============================================================
# 1) /posts/5 를 PUT으로 전체 수정하세요.
#    (title="수정 완료", body="PUT 실습", userId=1, id=5)
# 2) /posts/5 를 PATCH로 title만 "PATCH 실습"으로 수정하세요.
# 3) /posts/5 를 DELETE로 삭제하고 상태 코드를 출력하세요.
# 코드 작성 ↓

# [정답 코드]
# 1) PUT — 전체 수정
resp_put4 = requests.put(
    f"{BASE_URL}/posts/5",
    json={"id": 5, "title": "수정 완료", "body": "PUT 실습", "userId": 1}
    # PUT은 전체 교체이므로 모든 필드 포함 (id도 함께)
)
print(f"\n=== [실습 4] PUT 결과 ===")
print(f"상태 코드: {resp_put4.status_code}")
print(f"응답: {resp_put4.json()}")

resp_put44 = requests.put(
    # put : 전체 수정
    f"{BASE_URL}/posts/5",
    json = {"id" : 5, "title" : "수정 완료", "body" : "PUT 실습", "userId" : 1}
)

# 2) PATCH — 제목만 수정
resp_patch4 = requests.patch(
    f"{BASE_URL}/posts/5",
    json={"title": "PATCH 실습"}
    # 변경할 필드만 전송 — title 외 나머지는 서버에서 유지
)
print(f"\nPATCH 상태 코드: {resp_patch4.status_code}")
print(f"응답: {resp_patch4.json()}")

resp_patch44 = requests.patch(
    f"{BASE_URL}/posts/5",
    json = {"title" : "PATCH 실습(title 변경)"}
)

# 3) DELETE — 삭제
resp_del4 = requests.delete(f"{BASE_URL}/posts/5")
print(f"\nDELETE 상태 코드: {resp_del4.status_code}")
# 200이면 삭제 성공

resp_del44 = requests.delete(f"{BASE_URL}/post/5")


# ============================================================
# [이론 5] 에러 처리 & 실전 패턴
# ============================================================
#
# HTTP 요청은 네트워크 오류, 타임아웃, 서버 오류 등 다양한 실패 상황이 있다.
# → 예외 처리와 상태 코드 확인이 필수
#
# raise_for_status()
#   - 상태 코드가 4xx, 5xx이면 자동으로 예외(HTTPError) 발생
#   - 200~299이면 아무 일도 일어나지 않음
#   - 매번 if response.status_code != 200: 을 쓰는 것보다 간결
#
# timeout 파라미터
#   - 지정한 초(seconds)를 초과하면 Timeout 예외 발생
#   - 무한 대기를 방지하는 필수 안전장치
#
# requests.exceptions
#   - ConnectionError : 네트워크 연결 실패
#   - Timeout        : 요청 시간 초과
#   - HTTPError      : 4xx / 5xx 상태 코드 (raise_for_status 사용 시)

def safe_get(url, timeout=5):
    # url: 요청할 URL 문자열
    # timeout=5: 기본 타임아웃 5초 — 5초 내에 응답 없으면 예외 발생
    try:
        response = requests.get(url, timeout=timeout)
        # timeout=timeout: 지정한 초 이내에 응답 없으면 Timeout 예외 자동 발생

        response.raise_for_status()
        # 상태 코드 4xx/5xx → HTTPError 예외 자동 발생
        # 200~299이면 아무 일 없이 통과

        return response.json()
        # 정상 응답이면 딕셔너리/리스트로 변환 후 반환

    except requests.exceptions.Timeout:
        # Timeout: 지정 시간(5초) 초과 시 발생
        print(f"[오류] 요청 시간 초과: {url}")
        return None

    except requests.exceptions.ConnectionError:
        # ConnectionError: DNS 실패, 인터넷 연결 없음 등
        print(f"[오류] 네트워크 연결 실패: {url}")
        return None

    except requests.exceptions.HTTPError as e:
        # HTTPError: raise_for_status()가 발생시킨 예외
        # e에는 상태 코드와 메시지가 포함됨
        print(f"[오류] HTTP 오류 발생: {e}")
        return None

print("\n=== [이론 5] 에러 처리 — 정상 요청 ===")
result = safe_get(f"{BASE_URL}/posts/1")
# 정상 URL → 200 OK → 딕셔너리 반환
if result:
    print(f"제목: {result['title']}")
    # result가 None이 아닐 때만 접근 (에러 시 None 반환했으므로)

print("\n=== [이론 5] 에러 처리 — 존재하지 않는 리소스 ===")
result_404 = safe_get(f"{BASE_URL}/posts/99999")
# 99999번 게시글은 없음 → 404 Not Found → raise_for_status → HTTPError
print(f"결과: {result_404}")
# None 출력 (오류 메시지 출력 후 None 반환됨)


# ============================================================
# [실습 5] 에러 처리 & 실전 패턴
# ============================================================
# safe_get 함수를 참고하여 safe_post 함수를 만드세요.
#   - url, data(딕셔너리), timeout=5 파라미터
#   - POST 요청 후 raise_for_status() 호출
#   - 성공: 응답 JSON 반환
#   - 실패(Timeout, ConnectionError, HTTPError): 오류 메시지 출력 후 None 반환
# 만든 함수로 /posts에 {"title": "테스트", "body": "내용", "userId": 1} 를 전송하세요.
# 코드 작성 ↓

# [정답 코드]
def safe_post(url, data, timeout=5):
    try:
        response = requests.post(url, json = data, timeout = timeout)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.Timeout:
        print(f"[오류] POST 요청 시간 초과 : {url}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[오류] 네트워크 연결 실패 : {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[오류] HTTP POST 오류 : {e}")
        return None
"""
def safe_post(url, data, timeout=5):
    # url: 요청할 URL, data: Body에 담을 딕셔너리, timeout: 최대 대기 초
    try:
        response = requests.post(url, json=data, timeout=timeout)
        # json=data: 딕셔너리를 JSON으로 자동 변환 후 Body 전송
        # timeout=timeout: 지정 초 초과 시 Timeout 예외 발생

        response.raise_for_status()
        # 4xx/5xx 상태 코드면 HTTPError 예외 발생

        return response.json()
        # 성공 시 생성된 리소스 딕셔너리 반환

    except requests.exceptions.Timeout:
        print(f"[오류] POST 요청 시간 초과: {url}")
        return None

    except requests.exceptions.ConnectionError:
        print(f"[오류] 네트워크 연결 실패: {url}")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"[오류] POST HTTP 오류: {e}")
        return None
"""
print("\n=== [실습 5] safe_post 테스트 ===")
new_data = {"title": "테스트", "body": "내용", "userId": 1}
# 전송할 데이터 딕셔너리 정의

# result5 = safe_post(f"{BASE_URL}/posts", new_data)
# safe_post 호출 — POST 성공 시 생성된 게시글 딕셔너리 반환
result5 = safe_post(f"{BASE_URL}/posts", new_data)

if result5:
    print(f"성공(ID : {result5['id']}, 제목 : {result5['title']})")

if result5:
    print(f"생성 성공! ID: {result5['id']}, 제목: {result5['title']}")
    # result5가 None이 아닌 경우에만 출력 (에러 시 None)
