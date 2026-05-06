# ============================================================
# Stage 4 - 03. 데이터베이스 (SQLite / MySQL + SQLAlchemy ORM)
# ============================================================
# SQLite  : 파일 하나가 곧 DB — 설치 없이 바로 사용 가능한 경량 데이터베이스
# SQLAlchemy : 파이썬 ORM 라이브러리
#              SQL을 직접 쓰지 않고 파이썬 클래스/객체로 DB를 조작
#              Spring의 JPA(Hibernate) 와 동일한 역할
#
# ORM(Object-Relational Mapping)
#   파이썬 클래스  ←→  DB 테이블
#   클래스 인스턴스 ←→  테이블 행(Row)
#   클래스 속성    ←→  컬럼(Column)
#
# [사전 설치]
#   pip install sqlalchemy fastapi uvicorn       ← 기본
#   pip install pymysql                          ← MySQL 사용 시 추가 설치
#
# [실행 방법]
#   uvicorn stage4_03_database:app --reload
#   → http://127.0.0.1:8000/docs 에서 직접 테스트
#
# 학습 순서
#   1. DB 연결 설정 (engine, SessionLocal)
#   2. 모델 정의 (Base 상속 클래스 → 테이블)
#   3. Pydantic 스키마 분리 (요청/응답 DTO)
#   4. 세션 의존성 주입 (get_db + Depends)
#   5. CRUD API 완성

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session


# ============================================================
# [이론 1] DB 연결 설정
# ============================================================
#
# SQLAlchemy 연결 흐름:
#   1. create_engine(DB_URL) → DB와 실제 연결을 담당하는 엔진 생성
#   2. sessionmaker(engine)  → 세션 팩토리 생성 (세션 = 하나의 트랜잭션 단위)
#   3. declarative_base()    → 모델 클래스들이 상속할 Base 클래스 생성
#
# DB URL 형식:
#   SQLite    : "sqlite:///파일명.db"
#   MySQL     : "mysql+pymysql://유저명:비밀번호@호스트:포트/DB명"
#   PostgreSQL: "postgresql://유저명:비밀번호@호스트/DB명"
#
# Spring 비교:
#   application.properties의 spring.datasource.url 설정과 동일한 역할
#
# autocommit=False : 명시적으로 commit() 호출 시에만 DB에 반영
# autoflush=False  : flush(SQL 전송)를 자동으로 하지 않음
# bind=engine      : 이 세션이 사용할 DB 엔진 지정

DATABASE_URL = "sqlite:///./stage4_items.db"
# "./stage4_items.db" : 현재 디렉토리에 stage4_items.db 파일로 생성

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    # SQLite 전용 옵션: 여러 스레드에서 동일 연결 허용
    # FastAPI는 비동기로 여러 요청을 동시에 처리하므로 필요
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 세션 팩토리: SessionLocal()을 호출할 때마다 새 세션(트랜잭션) 생성

Base = declarative_base()
# 모든 ORM 모델 클래스가 상속할 기반 클래스


# ============================================================
# [실습 1-1] DB URL 빈칸 채우기
# ============================================================
# 아래 빈칸(???)을 채워 올바른 DB URL을 완성하세요.
#
# 1) SQLite — 현재 디렉토리에 "test.db" 파일로 연결
#    DATABASE_URL = "???:///./test.db"4
#       "sqlite:///./test.db"
#
# 2) MySQL — localhost:3306, 계정 root/1234, DB명 shopdb
#    DATABASE_URL = "mysql+???://root:1234@???:3306/shopdb"
#       pymysql / localhost
#
# 3) create_engine 에서 MySQL 사용 시 제거해야 할 옵션은?
#    connect_args={"???": False}
#       connect_args={"check_same_thread" : Fasle} - 여러 개의 스레드 생성
#       SQLite -> MySQL 넘어갈 때 사용(SQLite 는 하나의 한 개의 스레드 사용 -> MySQL 여러 개 스레드 사용)
#
# [정답]
# 1) "sqlite:///./test.db"
# 2) "mysql+pymysql://root:1234@localhost:3306/shopdb"
# 3) connect_args={"check_same_thread": False}  ← 이 줄 전체 제거


# ============================================================
# [실습 1-2] MySQL로 직접 전환해보기
# ============================================================
# MySQL 서버가 설치되어 있어야 합니다.
#
# ▶ Step 1. pymysql 드라이버 설치 (터미널)
#    pip install pymysql
#
# ▶ Step 2. MySQL에서 DB 생성 (MySQL Workbench 또는 터미널)
#    CREATE DATABASE practice_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
#    (utf8mb4: 한글 + 이모지까지 저장 가능한 인코딩)
#
# ▶ Step 3. 이 파일의 DATABASE_URL을 아래처럼 교체하세요.
#    변경 전: DATABASE_URL = "sqlite:///./stage4_items.db"
#    변경 후: DATABASE_URL = "mysql+pymysql://root:본인비밀번호@localhost:3306/practice_db"
#
# ▶ Step 4. create_engine에서 connect_args 줄을 제거하세요.
#    변경 전: engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
#    변경 후: engine = create_engine(DATABASE_URL)
#
# ▶ Step 5. 서버 실행
#    uvicorn stage4_03_database:app --reload
#    → /docs에서 POST /items로 아이템 2~3개 생성 후 GET /items 로 확인
#
# ▶ Step 6. MySQL Workbench에서 직접 확인
#    SELECT * FROM practice_db.items;
#    → API로 저장한 데이터가 MySQL 테이블에 실제로 있는지 눈으로 확인
#
# ▶ Step 7. 실습 완료 후 SQLite로 되돌리기
#    Step 3, 4를 원래대로 되돌리면 SQLite 모드 복귀
#
# ┌─────────────────────────────────────────────────────────────┐
# │              SQLite vs MySQL 한눈에 비교                     │
# ├───────────────────┬──────────────────┬──────────────────────┤
# │ 항목              │ SQLite           │ MySQL                │
# ├───────────────────┼──────────────────┼──────────────────────┤
# │ 설치              │ 불필요 (내장)    │ 별도 서버 설치 필요  │
# │ 사용 목적         │ 개발/테스트/학습 │ 실서비스/운영 환경   │
# │ 저장 방식         │ .db 파일 하나    │ DB 서버 프로세스     │
# │ 동시 접속         │ 제한적           │ 다중 사용자 지원     │
# │ connect_args      │ 필요             │ 불필요 (제거)        │
# │ String 컬럼 길이  │ 생략 가능        │ 반드시 명시 필요     │
# │ DB 사전 생성      │ 불필요           │ CREATE DATABASE 필요 │
# └───────────────────┴──────────────────┴──────────────────────┘


# ============================================================
# [이론 2] 모델 정의 (파이썬 클래스 → DB 테이블)
# ============================================================
#
# Base를 상속한 클래스 하나 = DB 테이블 하나
#   __tablename__ : 실제 DB에 생성될 테이블 이름
#   Column(타입)  : 컬럼 정의
#
# 주요 컬럼 타입:
#   Integer  → INT
#   String   → VARCHAR (MySQL은 길이 필수: String(50))
#   Boolean  → BOOLEAN (SQLite에서는 0/1로 저장)
#
# Column 옵션:
#   primary_key=True  → PK 지정
#   index=True        → 인덱스 생성 (검색 성능 향상)
#   nullable=False    → NOT NULL 제약 조건
#   unique=True       → UNIQUE 제약 조건
#   default=값        → 기본값 설정
#
# Spring 비교:
#   @Entity, @Table(name="..."), @Id, @Column 어노테이션 조합과 동일

class Item(Base):
    __tablename__ = "items"
    # DB에 생성될 테이블 이름

    id = Column(Integer, primary_key=True, index=True)
    # PK + 인덱스 자동 생성 → Spring의 @Id @GeneratedValue 와 동일

    name = Column(String(50), nullable=False)
    # VARCHAR(50), NOT NULL → Spring의 @Column(nullable=false) 와 동일

    price = Column(Integer, nullable=False)
    # INT, NOT NULL

    description = Column(String(200), nullable=True, default=None)
    # 선택 컬럼 — NULL 허용

    is_available = Column(Boolean, default=True)
    # 판매 가능 여부 — 기본값 True


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False, unique=True)
    # unique=True → UNIQUE 제약 조건 (중복 username 불가)
    email = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)


# 정의된 모든 모델을 DB에 테이블로 생성 (이미 있으면 건너뜀)
Base.metadata.create_all(bind=engine)
# Spring의 spring.jpa.hibernate.ddl-auto=update 와 유사
# 앱 시작 시 모델에 정의된 테이블이 없으면 자동 생성


# ============================================================
# [실습 2] 모델 직접 작성하기
# ============================================================
# 아래 조건에 맞는 Order(주문) 모델을 작성하세요.
#
# 조건:
#   - 테이블명: "orders"
#   - id       : PK, 인덱스
#   - item_id  : INT, NOT NULL (어떤 아이템의 주문인지)
#   - quantity : INT, NOT NULL (수량)
#   - status   : VARCHAR(20), 기본값 "pending" (주문 상태)
#
# 작성 후 Base.metadata.create_all(bind=engine) 이 이미 호출되어 있으므로
# 서버 재시작 시 orders 테이블이 자동 생성됩니다.
# 코드 작성 ↓
class Order2(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    statud = Column(String(20), default="pending")

# [정답 코드]
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")


# ============================================================
# [이론 3] Pydantic 스키마 분리
# ============================================================
#
# ORM 모델(Item, User)과 API 스키마(Pydantic)를 분리하는 이유:
#   - ORM 모델 : DB 구조 정의 (테이블, 컬럼, 관계)
#   - Pydantic  : API 요청/응답 형식 정의 (유효성 검사, 직렬화)
#   - 비밀번호처럼 DB엔 저장되지만 응답에는 빠져야 하는 필드 처리 가능
#
# Spring 비교:
#   Entity(DB 모델) + DTO(요청/응답 객체) 분리 패턴과 동일
#
# model_config = {"from_attributes": True}
#   → ORM 모델 객체를 Pydantic 모델로 자동 변환 허용
#   → 없으면 딕셔너리만 변환 가능하고 ORM 객체는 변환 안 됨
#   → Pydantic v1이면: class Config: orm_mode = True

class ItemCreate(BaseModel): # 생성
    # POST 요청 Body 스키마 — id 없음 (DB가 자동 생성)
    name: str = Field(min_length=1, max_length=50)
    price: int = Field(ge=0)
    description: Optional[str] = None
    is_available: bool = True


class ItemUpdate(BaseModel): # 수정
    # PATCH 요청 Body 스키마 — 모든 필드 선택 (부분 수정)
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    price: Optional[int] = Field(default=None, ge=0)
    description: Optional[str] = None
    is_available: Optional[bool] = None


class ItemResponse(BaseModel):
    # 응답 스키마 — id 포함
    id: int
    name: str
    price: int
    description: Optional[str]
    is_available: bool

    model_config = {"from_attributes": True}
    # ORM 객체(Item 인스턴스) → ItemResponse 자동 변환 허용


class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    email: str = Field(min_length=5)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


# ============================================================
# [실습 3] Pydantic 스키마 직접 작성하기
# ============================================================
# 위에서 만든 Order 모델에 맞는 Pydantic 스키마 3개를 작성하세요.
#
# 1) OrderCreate — POST 요청용
#    - item_id : int, 1 이상
#    - quantity : int, 1 이상
#    - status는 포함하지 않음 (DB 기본값 "pending" 사용)
class OrderCreate(BaseModel): # BaseModel : 최상위 기본 클래스(검증용)
    item_id : int = Field(ge=1)
    quantity : int = Field(ge=1)

#
# 2) OrderUpdate — PATCH 요청용 (모든 필드 선택)
#    - quantity : Optional[int], 1 이상
#    - status   : Optional[str]
class OrderUpdate(BaseModel):
    quantity : Optional[int] = Field(default=None, ge=1) # Optional[int] : int 가 들어오거나, 값이 안 들어올 수도 있음
    status : Optional[str] = None
#
# 3) OrderResponse — 응답용
#    - id, item_id, quantity, status 모두 포함
#    - from_attributes = True 설정 필수
# 코드 작성 ↓
class OrderResponse(BaseModel):
    id : int
    item_id : int
    quantity : int
    status : str
    
    model_config = {"from_attributes" : True}

# [정답 코드]
class OrderCreate(BaseModel):
    item_id: int = Field(ge=1)
    quantity: int = Field(ge=1)

class OrderUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, ge=1)
    status: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    status: str

    model_config = {"from_attributes": True} 
    # 이 모델은 DB 객체(ORM 객체)로부터 데이터를 직접 읽어올 수 있도록 설정됨


# ============================================================
# [이론 4] 세션 의존성 주입 (get_db + Depends)
# ============================================================
#
# 세션(Session) = 하나의 DB 트랜잭션 단위
#   - 요청이 시작될 때 열고, 요청이 끝나면 반드시 닫아야 함
#   - 닫지 않으면 DB 연결 풀이 고갈됨 (연결 누수)
#
# yield를 사용한 의존성 함수:
#   - yield 앞  : 요청 처리 전 실행 (세션 열기)
#   - yield     : 세션을 라우트 함수에 전달
#   - yield 뒤  : 요청 처리 후 항상 실행 (세션 닫기) — finally 보장
#
# Spring 비교:
#   @Transactional 어노테이션 + EntityManager 주입과 유사한 역할

def get_db():
    db = SessionLocal()
    # 새 DB 세션(트랜잭션) 생성
    try:
        yield db
        # 라우트 함수에 db 세션을 전달 — 함수 실행 동안 이 세션 사용
    finally:
        db.close()
        # 요청이 성공하든 실패하든 반드시 세션 닫기 (연결 반환)


app = FastAPI(title="Stage 4-03 데이터베이스", version="1.0.0")


# ============================================================
# [실습 4] 세션 흐름 이해하기
# ============================================================
# 아래 빈칸을 채워 get_db 함수의 동작 순서를 완성하세요.
#
# def get_db():
#     db = ???()          # 1) 새 세션 생성
#           SessionLocal()
#     try:
#         ??? db           # 2) 라우트 함수에 세션 전달
#           yield db
#     finally:
#         db.???()         # 3) 요청 종료 후 세션 반드시 닫기
#           db.close()
#
# Q. finally 블록이 없으면 어떤 문제가 생길까요?
#    → 예외 발생 시 세션이 닫히지 않아 DB 연결이 계속 쌓임 (연결 누수)
#       연결 풀이 고갈되면 새 요청이 DB에 접근하지 못하고 멈춤
#
# [정답]
# db = SessionLocal()
# yield db
# db.close()


# ============================================================
# [이론 5] CRUD API 완성
# ============================================================
#
# db.add(객체)      → INSERT 준비 (아직 DB 반영 안 됨)
# db.commit()       → 트랜잭션 커밋 (DB에 실제 반영)
# db.refresh(객체)  → DB에서 최신 데이터를 다시 읽어옴 (id 등 자동 생성 값 갱신)
# db.query(모델)    → SELECT 쿼리 시작
#   .filter(조건)   → WHERE 절
#   .first()        → LIMIT 1, 없으면 None
#   .all()          → 결과 전체 리스트
#   .offset(n)      → OFFSET n (건너뛰기)
#   .limit(n)       → LIMIT n (최대 개수)
# db.delete(객체)   → DELETE 준비
#
# Spring 비교:
#   repository.save()     → db.add() + db.commit()
#   repository.findById() → db.query().filter().first()
#   repository.findAll()  → db.query().all()
#   repository.delete()   → db.delete() + db.commit()

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # db: Session = Depends(get_db) → 요청마다 새 세션 자동 주입
    db_item = Item(
        name=item.name,
        price=item.price,
        description=item.description,
        is_available=item.is_available
    )
    # Pydantic ItemCreate → ORM Item 인스턴스로 변환
    db.add(db_item)       # INSERT 준비
    db.commit()           # DB에 실제 저장, id 자동 생성
    db.refresh(db_item)   # 자동 생성된 id 값을 채움
    return db_item        # ORM 객체 → ItemResponse 자동 변환


@app.get("/items", response_model=list[ItemResponse])
def list_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Item).offset(skip).limit(limit).all()
    # SELECT * FROM items LIMIT limit OFFSET skip


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    # SELECT * FROM items WHERE id = item_id LIMIT 1
    if item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    return item


@app.patch("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_data: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")

    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
        # setattr(객체, "속성명", 값) → item.name = value 와 동일
        # 동적으로 속성 이름을 문자열로 지정할 때 사용

    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다.")
    db.delete(item)
    db.commit()
    # 204 No Content → return 없음


# ============================================================
# [실습 5-1] User CRUD API 작성하기
# ============================================================
# User 모델 / UserCreate / UserResponse 는 위에 이미 정의되어 있습니다.
# 아래 4개의 라우트를 완성하세요.
#
# 1) POST /users
#    - UserCreate로 요청 받아 DB에 저장
#    - username 또는 email이 이미 존재하면 400 + "이미 존재하는 사용자입니다."
#    - 성공 시 UserResponse 반환, 상태 코드 201
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    # | 연산자: OR 조건 — username 또는 email이 이미 있으면
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
#
# 2) GET /users
#    - 전체 사용자 목록 반환 (skip=0, limit=10 쿼리 파라미터)
@app.get("/users", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()

@app.get("/users", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()
#
# 3) GET /users/{user_id}
#    - 없으면 404, 있으면 UserResponse 반환
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user in None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user
#
# 4) DELETE /users/{user_id}
#    - 없으면 404, 있으면 삭제 후 204 반환
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    db.delete(user)
    db.commit()

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user in None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    db.delete(user)
    db.commit()

# ============================================================
# [실습 5-2] 검색 & 필터 쿼리 작성하기
# ============================================================
# GET /items/search 라우트를 만드세요.
#   - keyword (str, 선택): 아이템 이름에 포함된 문자열로 필터
#   - max_price (int, 선택): 이 금액 이하인 아이템만 반환
#   - available_only (bool, 기본값=False): True이면 is_available=True 인 것만
#   - 결과를 list[ItemResponse]로 반환
#
# 힌트:
#   .filter(Item.name.contains(keyword))  → LIKE '%keyword%'
#   .filter(Item.price <= max_price)
#   .filter(Item.is_available == True)
# 코드 작성 ↓

# [정답 코드]
@app.get("/items/search", response_model=list[ItemResponse])
def search_items(
    keyword: Optional[str] = None,
    max_price: Optional[int] = None,
    available_only: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Item)
    # db.query(Item) : SELECT * FROM items — 아직 실행되지 않은 쿼리 객체

    if keyword:
        query = query.filter(Item.name.contains(keyword))
        # .contains(keyword) → SQL: WHERE name LIKE '%keyword%'

    if max_price is not None:
        query = query.filter(Item.price <= max_price)
        # WHERE price <= max_price

    if available_only:
        query = query.filter(Item.is_available == True)
        # WHERE is_available = 1

    return query.all()


# ============================================================
# [실습 5-3] Order CRUD API 작성하기
# ============================================================
# Order 모델 / OrderCreate / OrderUpdate / OrderResponse 는
# 위 실습 2·3에서 이미 정의했습니다.
#
# 아래 4개의 라우트를 완성하세요.
#
# 1) POST /orders
#    - OrderCreate로 요청 받아 DB에 저장, OrderResponse 반환, 201
@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(item_id=order.item_id, quantity=order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
#
# 2) GET /orders
#    - 전체 주문 목록 반환 (skip=0, limit=10)
@app.get("/orders", response_model=list[OrderResponse])
def list_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Order).offset(skip).limit(limit).all()
#
# 3) PATCH /orders/{order_id}
#    - OrderUpdate로 부분 수정, 없으면 404
@app.patch("/orders/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_data: OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    for field, value in order_data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order

#
# 4) DELETE /orders/{order_id}
#    - 없으면 404, 삭제 후 204
@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    db.delete(order)
    db.commit()

# ============================================================
# 실행 진입점
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("stage4_03_database:app", host="0.0.0.0", port=8000, reload=True)
