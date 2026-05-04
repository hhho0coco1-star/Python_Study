# ============================================================
# Stage 4 - 02. FastAPI 기초
# ============================================================
# FastAPI: 파이썬으로 REST API 서버를 빠르게 만드는 웹 프레임워크
#   - Spring의 @RestController 역할을 파이썬에서 담당
#   - Pydantic으로 요청/응답 데이터를 자동 검증
#   - /docs 접속 시 Swagger UI 자동 생성 (별도 설정 없음)
#
# 프레임워크 : 뼈대 or 틀 == 밀키트 
# 개발하기 위해 필요한 기본 구조와 도구들이 갖춰진 일종의 '반제품 패키지'
# 
# [사전 설치]
#   pip install fastapi uvicorn
#
#   uvicorn: FastAPI 앱을 실제로 실행하는 ASGI 서버
#            (Spring의 내장 Tomcat 역할)
#
# [실행 방법]
#   uvicorn stage4_02_fastapi:app --reload
#   → http://127.0.0.1:8000      (API 서버)
#   → http://127.0.0.1:8000/docs (Swagger UI — 자동 생성)
#
# 학습 순서
#   1. FastAPI 앱 생성 & 첫 번째 라우트
#   2. 경로 매개변수 (Path Parameter)
#   3. 쿼리 매개변수 (Query Parameter)
#   4. Pydantic 모델 — 요청 Body 검증
#   5. 의존성 주입 (Depends)

from fastapi import FastAPI, HTTPException, Depends, Query, Path
from pydantic import BaseModel, Field
from typing import Optional


# ============================================================
# [이론 1] FastAPI 앱 생성 & 첫 번째 라우트
# ============================================================
#
# FastAPI 앱은 Spring의 @SpringBootApplication 과 유사하게
# 하나의 app 객체를 중심으로 모든 라우트가 등록된다.
#
# 라우트 등록 방식:
#   @app.get("/경로")    → GET 요청 처리
#   @app.post("/경로")   → POST 요청 처리
#   @app.put("/경로")    → PUT 요청 처리
#   @app.delete("/경로") → DELETE 요청 처리
#
# 반환값:
#   - 딕셔너리를 반환하면 FastAPI가 자동으로 JSON 응답으로 변환
#   - Spring의 @ResponseBody + Jackson 자동 직렬화와 동일한 역할

app = FastAPI(
    title="파이썬 FastAPI 학습",
    description="Stage 4-02 실습 서버",
    version="1.0.0"
)
# FastAPI() : 앱 인스턴스 생성
# title, description, version → /docs 페이지 상단에 자동 표시


@app.get("/")
def read_root():
    # GET / 요청이 오면 이 함수가 실행됨
    # 딕셔너리 반환 → FastAPI가 {"message": "..."} JSON 응답으로 변환
    return {"message": "FastAPI 서버가 정상 실행 중입니다!"}


@app.get("/health")
def health_check():
    # 서버 상태 확인용 엔드포인트 — 모니터링 도구가 주기적으로 호출
    return {"status": "ok"}


# ============================================================
# [실습 1] 첫 번째 라우트 만들기
# ============================================================
# 1) GET /hello 요청 시 {"greeting": "안녕하세요, FastAPI!"} 를 반환하는
#    라우트 함수 say_hello()를 작성하세요.
@app.get("/hello")
def say_hello():
    return {"greeting" : "안녕하세요, FastAPI!"}
# 2) GET /info 요청 시 서버 이름("FastAPI 학습 서버")과
#    버전("1.0.0")을 담은 딕셔너리를 반환하세요.
@app.get("/info")
def get_info():
    return {"name" : "FastAPI 학습 서버", "version" : "1.0.0"}
# 코드 작성 ↓

# [정답 코드]
@app.get("/hello")
def say_hello():
    return {"greeting": "안녕하세요, FastAPI!"}

@app.get("/info")
def get_info():
    return {"name": "FastAPI 학습 서버", "version": "1.0.0"}


# ============================================================
# [이론 2] 경로 매개변수 (Path Parameter)
# ============================================================
#
# URL 경로의 일부를 변수로 받는 방식
#   /items/{item_id}  →  item_id 를 함수 파라미터로 전달
#
# Spring 비교:
#   @GetMapping("/items/{itemId}")
#   public Item getItem(@PathVariable Long itemId) { ... }
#
# 타입 힌트를 붙이면 FastAPI가 자동으로 타입 변환 + 검증
#   item_id: int → URL에서 "abc" 가 오면 422 에러 자동 반환
#
# Path() : 경로 매개변수에 추가 제약 조건 설정
#   ge=1  → 1 이상 (Greater than or Equal)
#   le=100 → 100 이하 (Less than or Equal)

# 예시용 데이터 (DB 대신 딕셔너리 사용)
fake_items_db = {
    1: {"id": 1, "name": "노트북", "price": 1500000},
    2: {"id": 2, "name": "마우스", "price": 35000},
    3: {"id": 3, "name": "키보드", "price": 85000},
}


@app.get("/items/{item_id}")
def get_item(item_id: int = Path(ge=1, description="조회할 아이템 ID (1 이상)")):
    # item_id: int  → URL의 {item_id} 를 int로 자동 변환
    # Path(ge=1)    → 1 미만이면 422 Unprocessable Entity 자동 반환
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail=f"ID {item_id} 아이템을 찾을 수 없습니다.")
        # HTTPException: Spring의 ResponseStatusException 과 동일한 역할
        # status_code=404 → HTTP 404 응답, detail → 오류 메시지 JSON 반환
    return fake_items_db[item_id]


@app.get("/users/{user_id}/posts/{post_id}")
def get_user_post(user_id: int, post_id: int):
    # 경로 매개변수를 2개 이상 사용하는 패턴
    # /users/1/posts/5 → user_id=1, post_id=5
    return {"user_id": user_id, "post_id": post_id, "message": "중첩 경로 매개변수"}


# ============================================================
# [실습 2] 경로 매개변수
# ============================================================
# fake_items_db를 활용하여:
# 1) GET /products/{product_id} 라우트를 만드세요.
#    - product_id가 fake_items_db에 없으면 404 + "상품 없음" 메시지
#    - 있으면 해당 아이템 반환
@app.get("/products/{product_id}")
def get_product(product_id : int):
    if product_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="상품 없음")
    return fake_items_db[product_id]
# 2) GET /categories/{category}/items/{item_id} 라우트를 만드세요.
#    - category(str)와 item_id(int)를 경로 매개변수로 받아
#    - {"category": ..., "item_id": ...} 형태로 반환
@app.get("/categories/{category}/items/{item_id}")
def get_category_item(category : str, item_id : int):
    return {"category" : category, "item_id" : item_id}
# 코드 작성 ↓


# [정답 코드]
@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="상품 없음")
    return fake_items_db[product_id]

@app.get("/categories/{category}/items/{item_id}")
def get_category_item(category: str, item_id: int):
    return {"category": category, "item_id": item_id}


# ============================================================
# [이론 3] 쿼리 매개변수 (Query Parameter)
# ============================================================
#
# URL 뒤에 ?key=value 형태로 전달되는 파라미터
#   /items?skip=0&limit=10&keyword=노트북
#
# Spring 비교:
#   @GetMapping("/items")
#   public List<Item> getItems(@RequestParam int skip,
#                               @RequestParam int limit) { ... }
#
# FastAPI에서는 경로에 포함되지 않은 파라미터가 자동으로 쿼리 매개변수로 처리됨
#
# Optional 처리:
#   keyword: Optional[str] = None  → 없어도 됨 (기본값 None)
#
# Query() : 쿼리 매개변수에 제약 조건 & 설명 추가
#   ge=0     → 0 이상
#   le=100   → 100 이하
#   min_length=1 → 최소 1글자 이상

@app.get("/items")
def list_items(
    skip: int = Query(default=0, ge=0, description="건너뛸 아이템 수"),
    limit: int = Query(default=10, ge=1, le=100, description="가져올 최대 개수"),
    keyword: Optional[str] = Query(default=None, description="검색 키워드 (선택)")
):
    # skip, limit: 페이지네이션 — /items?skip=0&limit=5
    # keyword: 검색 필터 — /items?keyword=노트북
    items = list(fake_items_db.values())
    # fake_items_db.values() → 딕셔너리의 값(아이템 딕셔너리)들을 리스트로 변환

    if keyword:
        items = [item for item in items if keyword in item["name"]]
        # 키워드가 name에 포함된 아이템만 필터링 (리스트 컴프리헨션)

    return {
        "total": len(items),
        "skip": skip,
        "limit": limit,
        "items": items[skip: skip + limit]
        # 슬라이싱으로 페이지네이션 구현
    }


# ============================================================
# [실습 3] 쿼리 매개변수
# ============================================================
# GET /search 라우트를 만드세요.
#   - q (str, 필수): 검색어
#   - max_price (int, 선택, 기본값=None): 이 금액 이하인 아이템만 반환
#   - fake_items_db에서 조건에 맞는 아이템 리스트를 반환
#   - 예) /search?q=키&max_price=100000 → 이름에 "키"가 포함되고 가격 ≤ 100000
# 코드 작성 ↓

@app.get("/search")
def search_items(
    q : str = Query(description="검색어(필수)"),
    max_price : Optional[int] = Query(default=None, ge=0, description="최대 가격")
    # Optional : 선택(있어도 되고, 없어도 된다.) /= Required : 필수
):
    results = [item for item in fake_items_db.values() if q in item["name"]]

    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    return {"query" : q, "max_price" : max_price, "results" : results}

# [정답 코드]
@app.get("/search")
def search_items(
    q: str = Query(description="검색어 (필수)"),
    max_price: Optional[int] = Query(default=None, ge=0, description="최대 가격")
):
    results = [item for item in fake_items_db.values() if q in item["name"]]
    # q가 name에 포함된 아이템 필터링

    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]
        # max_price가 있으면 가격 조건 추가 필터링

    return {"query": q, "max_price": max_price, "results": results}


# ============================================================
# [이론 4] Pydantic 모델 — 요청 Body 검증
# ============================================================
#
# Pydantic: 데이터 검증 라이브러리
#   - BaseModel을 상속하는 클래스로 요청/응답 스키마 정의
#   - 타입이 맞지 않으면 422 Unprocessable Entity 자동 반환
#   - Spring의 @RequestBody + @Valid + DTO 클래스 조합과 동일한 역할
#
# Field() : 필드에 제약 조건 & 설명 추가
#   min_length=1  → 최소 1글자
#   ge=0          → 0 이상
#   description   → /docs에 표시되는 설명
#
# 응답 모델:
#   response_model=ItemResponse → 반환 데이터를 이 모델로 직렬화
#   (불필요한 필드 자동 제거, Spring의 @JsonIgnore 없이 처리 가능)

class ItemCreate(BaseModel):
    # POST /items 요청 Body 스키마
    name: str = Field(min_length=1, max_length=50, description="아이템 이름")
    price: int = Field(ge=0, description="가격 (0 이상)")
    description: Optional[str] = Field(default=None, description="설명 (선택)")
    # Optional[str] = None → 없어도 되는 필드


class ItemResponse(BaseModel):
    # 응답 Body 스키마 — id 포함
    id: int
    name: str
    price: int
    description: Optional[str] = None


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    # item: ItemCreate → 요청 Body를 ItemCreate 모델로 자동 파싱 & 검증
    # response_model=ItemResponse → 반환값을 ItemResponse 스키마로 직렬화
    # status_code=201 → 생성 성공 시 201 Created 반환
    new_id = max(fake_items_db.keys()) + 1
    # 현재 최대 ID + 1로 새 ID 생성 (실제 서비스에서는 DB AUTO_INCREMENT 사용)

    new_item = {"id": new_id, "name": item.name, "price": item.price, "description": item.description}
    # Pydantic 모델의 필드는 .속성명 으로 접근
    fake_items_db[new_id] = new_item
    return new_item


class ItemUpdate(BaseModel):
    # PATCH /items/{item_id} 요청 Body — 모든 필드 선택 (부분 수정)
    name: Optional[str] = Field(default=None, min_length=1)
    price: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = None


@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")

    stored = fake_items_db[item_id]
    # 기존 데이터 가져오기

    update_data = item.model_dump(exclude_unset=True)
    # model_dump(exclude_unset=True): 클라이언트가 실제로 보낸 필드만 딕셔너리로 변환
    # → 보내지 않은 필드는 포함되지 않음 (PATCH의 핵심: 보낸 것만 수정)

    stored.update(update_data)
    # 기존 딕셔너리에 변경 내용만 덮어씀
    return stored


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    del fake_items_db[item_id]
    # 204 No Content → 응답 Body 없음 (return 생략)


# ============================================================
# [실습 4] Pydantic 모델
# ============================================================
# 간단한 메모 API를 만드세요.
#
# 데이터 저장소:
#   fake_memo_db = {}  (딕셔너리, 전역 변수)
#
fake_memo_db = {}
memo_counter = 1  # ID 카운터 (전역 변수)
# 1) MemoCreate 모델 정의
#    - title: str (필수, 최소 1글자)
#    - content: str (필수, 최소 1글자)
class MemoCreate(BaseModel):
    title: str = Field(min_length=1, description="메모 제목")
    content: str = Field(min_length=1, description="메모 내용")

class MemoCreate2(BaseModel):
    title : str = Field(min_length=1, description="메모 제목")
    content : str = Field(min_length=1, description="메모 내용")
#
# 2) MemoResponse 모델 정의
#    - id: int
#    - title: str
#    - content: str
class MemoResponse(BaseModel):
    id: int
    title: str
    content: str

class MemoResponse(BaseModel):
    id : int
    title : str
    content : str
#
# 3) POST /memos 라우트
#    - MemoCreate로 요청 받아 fake_memo_db에 저장
#    - MemoResponse로 응답, 상태 코드 201
@app.post("/memos", response_model=MemoResponse, status_code=201)
def create_memo(memo: MemoCreate):
    global memo_counter
    # global: 함수 밖에서 선언된 변수를 함수 안에서 수정할 때 필요
    new_memo = {"id": memo_counter, "title": memo.title, "content": memo.content}
    fake_memo_db[memo_counter] = new_memo
    memo_counter += 1
    return new_memo

@app.post("/memos", response_model=MemoResponse, status_code=201)
def create_memo(memo : MemoCreate):
    global memo_counter
    new_memo = {"id" : memo_counter, "title" : memo.title, "content" : memo.content}
    fake_memo_db[memo_counter] = new_memo
    memo_counter += 1
    return new_memo
#
# 4) GET /memos/{memo_id} 라우트
#    - 없으면 404, 있으면 MemoResponse로 반환
# 코드 작성 ↓
@app.get("/memos/{memo_id}", response_model=MemoResponse)
def get_memo(memo_id: int):
    if memo_id not in fake_memo_db:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    return fake_memo_db[memo_id]


@app.get("/memos/{memo_id}", response_model=MemoResponse)
def get_memo(memo_id : int):
    if memo_id not in fake_memo_db:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    return fake_memo_db[memo_id]

# [정답 코드]


# ============================================================
# [이론 5] 의존성 주입 (Depends)
# ============================================================
#
# Depends: 공통 로직(인증, DB 세션, 파라미터 검증 등)을 재사용하는 메커니즘
#   - Spring의 ArgumentResolver, @Component 주입과 유사한 역할
#   - 함수를 다른 함수의 파라미터로 주입 → 코드 중복 제거
#
# 대표 활용 패턴:
#   1) 공통 쿼리 파라미터 추출 (페이지네이션 등)
#   2) 간단한 API 키 인증
#   3) DB 세션 관리 (Stage 4-03에서 본격 활용)
#
# 사용법:
#   def common_params(skip: int = 0, limit: int = 10):
#       return {"skip": skip, "limit": limit}
#
#   @app.get("/items")
#   def list(params = Depends(common_params)):
#       # params = {"skip": 0, "limit": 10}

def common_pagination(
    skip: int = Query(default=0, ge=0, description="건너뛸 수"),
    limit: int = Query(default=10, ge=1, le=50, description="최대 개수")
):
    # 여러 라우트에서 공통으로 사용할 페이지네이션 파라미터
    return {"skip": skip, "limit": limit}


def verify_api_key(api_key: str = Query(description="API 키")):
    # 간단한 API 키 인증 의존성
    # 실제 서비스에서는 Header에서 받아 DB 조회로 검증
    if api_key != "secret-key-1234":
        raise HTTPException(status_code=401, detail="유효하지 않은 API 키입니다.")
    return api_key


@app.get("/v2/items")
def list_items_v2(pagination: dict = Depends(common_pagination)):
    # Depends(common_pagination): common_pagination 함수 실행 결과를 주입
    # → 요청의 skip, limit 쿼리 파라미터를 자동으로 파싱해 딕셔너리로 전달
    items = list(fake_items_db.values())
    skip = pagination["skip"]
    limit = pagination["limit"]
    return {"items": items[skip: skip + limit], "pagination": pagination}


@app.get("/secure/items")
def list_secure_items(
    pagination: dict = Depends(common_pagination),
    api_key: str = Depends(verify_api_key)
    # 두 의존성을 동시에 주입 — 둘 다 통과해야 라우트 함수 실행
):
    items = list(fake_items_db.values())
    return {"items": items, "authenticated": True}


# ============================================================
# [실습 5] 의존성 주입
# ============================================================
# 1) 공통 의존성 함수 check_positive_id(item_id: int) 를 만드세요.
#    - item_id가 1 미만이면 HTTPException(400, "ID는 1 이상이어야 합니다.")
#    - 아니면 item_id 반환
def check_positive_id(item_id: int = Path(description="아이템 ID")):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="ID는 1 이상이어야 합니다.")
    return item_id

def check_positive_id(item_id : int = Path(description="아이템 ID")):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="ID는 1 이상이어야 합니다.")
    return item_id
#
# 2) GET /v2/items/{item_id} 라우트를 Depends(check_positive_id) 를 사용해 만드세요.
#    - 검증 통과 후 fake_items_db에서 조회, 없으면 404
# 코드 작성 ↓
@app.get("/v2/items/{item_id}", response_model=ItemResponse)
def get_item_v2(item_id: int = Depends(check_positive_id)):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    return fake_items_db[item_id]

@app.get("/v2/items/{item_id}", response_model=ItemResponse)
def get_item_v2(item_id : int = Depends(check_positive_id)):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    return fake_items_db[item_id]






# ============================================================
# 실행 진입점
# ============================================================
# 이 파일을 직접 실행할 때: python stage4_02_fastapi.py
# uvicorn으로 실행할 때:    uvicorn stage4_02_fastapi:app --reload
#
# 권장: uvicorn 방식 (--reload 옵션으로 코드 변경 시 자동 재시작)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("stage4_02_fastapi:app", host="0.0.0.0", port=8000, reload=True)
