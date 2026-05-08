# ============================================================
# Stage 4 - 04. JWT 인증 (Authentication & Authorization)
# ============================================================
# JWT(JSON Web Token) : 로그인 상태를 토큰으로 증명하는 방식
#   - 서버가 세션을 저장하지 않아도 됨 (Stateless)
#   - 토큰 자체에 사용자 정보가 인코딩되어 있음
#
# 인증(Authentication) vs 인가(Authorization)
#   인증 : "너 누구야?" → 로그인 (신원 확인)
#   인가 : "너 이거 할 수 있어?" → 권한 확인
#
# [사전 설치]
#   pip install python-jose[cryptography]   ← JWT 생성/검증
#   pip install passlib[bcrypt]             ← 비밀번호 해싱
#   pip install fastapi uvicorn sqlalchemy
#
# [실행 방법]
#   uvicorn stage4_04_auth:app --reload
#   → http://127.0.0.1:8000/docs 에서 테스트
#
# 학습 순서
#   1. JWT 구조 이해
#   2. 비밀번호 해싱 (평문 저장 금지!)
#   3. JWT 토큰 생성
#   4. OAuth2 Bearer 토큰 검증
#   5. 보호된 엔드포인트 작성

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session


# ============================================================
# [이론 1] JWT 구조
# ============================================================
#
# JWT는 점(.)으로 구분된 3개 파트로 구성됩니다:
#
#   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9   ← Header  (Base64)
#   .eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcwMH0   ← Payload (Base64)
#   .SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw   ← Signature (HMAC)
#
# Header   : 알고리즘 정보 (예: HS256)
# Payload  : 실제 데이터 (sub=사용자 ID, exp=만료시간 등)
# Signature: Header + Payload를 SECRET_KEY로 서명한 값
#             → 위조 방지: 서버만 SECRET_KEY를 알고 있음
#
# 인증 흐름:
#   1. 클라이언트 → POST /login (username, password)
#   2. 서버 → 비밀번호 검증 후 JWT 발급
#   3. 클라이언트 → 이후 모든 요청 헤더에 포함
#        Authorization: Bearer <JWT 토큰>
#   4. 서버 → 토큰 서명 검증 + 사용자 식별
#
# Spring 비교:
#   Spring Security + JWT Filter 조합과 동일한 역할
#   OncePerRequestFilter 에서 토큰 파싱하는 로직과 유사

# JWT 설정값 — 실제 서비스에서는 환경변수로 관리
SECRET_KEY = "my-super-secret-key-change-in-production"
# 서명에 사용하는 비밀 키 — 절대 외부에 노출 금지
ALGORITHM = "HS256"
# HMAC-SHA256 알고리즘으로 서명
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# 토큰 유효 시간: 30분


# ============================================================
# [실습 1] JWT 구조 이해하기
# ============================================================
# 아래 빈칸을 채워 JWT 동작 원리를 완성하세요.
#
# Q1. JWT는 총 ??? 개의 파트로 구성되며, 구분자는 ???입니다.
#     → 3개, 점(.)
#
# Q2. 세 파트의 이름과 역할을 써보세요.
#     - Header : 알고리즘 정보 (Base64 인코딩)
#     - Payload : 사용자 데이터 (sub, exp 등)
#     - Signature : 위조 방지 서명 값
#
# Q3. JWT가 "위조"를 막을 수 있는 이유는?
#     → ???
#
# [정답]
# Q1. 3개, 점(.)
# Q2. Header / Payload / Signature
# Q3. Signature가 SECRET_KEY로 서명되어 있어, 내용을 변조하면
#     서명이 달라져 서버에서 invalid로 거부됨


# ============================================================
# DB 설정 (stage4_03에서 이어지는 users 테이블 재사용)
# ============================================================

DATABASE_URL = "sqlite:///./stage4_auth.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    # 평문 비밀번호는 절대 저장하지 않음 — 해싱된 값만 저장
    is_active = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# [이론 2] 비밀번호 해싱 (passlib + bcrypt)
# ============================================================
#
# 왜 비밀번호를 해싱해야 하나?
#   - DB가 유출되어도 원래 비밀번호를 알 수 없음
#   - 단방향 해싱: 평문 → 해시값 (역방향 불가)
#   - bcrypt는 salt를 자동으로 추가해 레인보우 테이블 공격 방어
#
# CryptContext : passlib의 해싱 컨텍스트 (알고리즘 설정)
#   pwd_context.hash("비밀번호")           → 해시값 생성
#   pwd_context.verify("평문", "해시값")   → 비교 (True/False)
#
# Spring 비교:
#   BCryptPasswordEncoder.encode() / matches() 와 동일

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# schemes=["bcrypt"] : bcrypt 알고리즘 사용
# deprecated="auto" : 구버전 해시 자동 업그레이드


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)
    # "1234" → "$2b$12$随机salt+해시값"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    # 평문과 해시값을 비교 — 일치하면 True


# ============================================================
# [실습 2] 비밀번호 해싱 함수 이해하기
# ============================================================
# 아래 빈칸을 채우세요.
#
# 1) 비밀번호 "secret123"을 해싱하는 코드:
#    hashed = pwd_context.hash("secret123")
#       pwd_context.hash("secret123")
#
# 2) 로그인 시 입력한 비밀번호와 DB 해시값을 비교하는 코드:
#    is_valid = pwd_context.verify("입력값", db_user.hashed_password)
#       pwd_context.verify("입력값", db_user.hashed_password)
#
# 3) 왜 DB에 평문 비밀번호를 저장하면 안 되나요?
#    → ???
#
# [정답]
# 1) pwd_context.hash("secret123")
# 2) pwd_context.verify("입력값", db_user.hashed_password)
# 3) DB 유출 시 모든 사용자 비밀번호가 노출됨.
#    해싱하면 유출되어도 원래 비밀번호를 알 수 없음.


# ============================================================
# [이론 3] JWT 토큰 생성
# ============================================================
#
# jwt.encode(payload, key, algorithm)
#   payload : 토큰에 담을 데이터 (dict)
#     - "sub" : subject — 주로 username 또는 user_id
#     - "exp" : 만료 시간 (datetime 객체)
#   key       : SECRET_KEY
#   algorithm : "HS256"
#
# jwt.decode(token, key, algorithms)
#   - 서명 검증 + payload 반환
#   - 서명 오류나 만료 시 JWTError 예외 발생
#
# timedelta(minutes=30) : 현재 시각 + 30분 = 만료 시각

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    # 원본 data를 변경하지 않도록 복사

    expire = datetime.now(timezone.utc) + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    # 만료 시각 계산: 현재 UTC 시각 + 만료 시간

    to_encode["exp"] = expire
    # payload에 만료 시각 추가 — jose가 자동으로 검증에 사용

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # payload를 SECRET_KEY로 서명하여 JWT 문자열 반환


# ============================================================
# [실습 3] 토큰 생성 코드 이해하기
# ============================================================
# 아래 질문에 답하세요.
#
# Q1. 토큰 payload에서 "sub" 는 무엇의 약자이며, 보통 무슨 값을 담나요?
#     → ???
#
# Q2. "exp" 값이 없으면 어떻게 될까요?
#     → ???
#
# Q3. 아래 코드에서 사용자 "alice"에게 30분짜리 토큰을 발급하는 코드를 작성하세요.
#    token = create_access_token(
#        data={"sub", "alice"},
#        expires_delta=timedelta(minutes=30)
#    )
#
# [정답]
# Q1. subject(주체). 보통 username 또는 user_id를 담아 "누구의 토큰인지" 식별함.
# Q2. 토큰이 만료되지 않음 (영구 유효) → 보안 취약점.
#     jose는 exp 없이도 decode하지만 실서비스에서는 필수.
# Q3. token = create_access_token(
#         data={"sub": "alice"},
#         expires_delta=timedelta(minutes=30)
#     )


# ============================================================
# [이론 4] OAuth2 Bearer 토큰 검증
# ============================================================
#
# OAuth2PasswordBearer(tokenUrl="/login")
#   - 요청 헤더 "Authorization: Bearer <토큰>" 에서 토큰 추출
#   - /docs 에서 "Authorize" 버튼을 제공해 편리하게 테스트 가능
#   - tokenUrl : 토큰 발급 엔드포인트 (Swagger UI 로그인 창에 사용)
#
# get_current_user 함수:
#   - oauth2_scheme: str = Depends(oauth2_scheme) 으로 토큰 주입
#   - jwt.decode() 로 서명 검증 + payload 추출
#   - payload["sub"] 로 username 꺼내기
#   - DB에서 사용자 조회 → 없으면 401
#
# credentials_exception : 401 Unauthorized
#   WWW-Authenticate: Bearer 헤더 — 클라이언트에게 Bearer 토큰 요구 알림
#
# Spring 비교:
#   JwtAuthenticationFilter + SecurityContextHolder.setAuthentication()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# 보호된 엔드포인트에서 Depends(oauth2_scheme)으로 토큰 자동 추출
# 클라이언트(브라우저)에게 "앞으로 비밀번호가 필요한 문(API)에 들어오려면 
# /login에서 받아온 토큰을 제출해!"라고 선언하는 것입니다.


# Pydantic 스키마
# 회원가입 신청서 
class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    email: str = Field(min_length=5)
    password: str = Field(min_length=4)

# 회원 정보 응답서
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}

# 로그인 후 -> 발급증/출입증
class Token(BaseModel):
    access_token: str
    token_type: str
    # token_type은 항상 "bearer"

# 로그인 후 -> 발급증/출입증
class TokenData(BaseModel):
    username: Optional[str] = None
    # JWT payload에서 꺼낸 username 저장용


# 본격적인 신분증 검사
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증에 실패했습니다.",
        headers={"WWW-Authenticate": "Bearer"},
        # WWW-Authenticate: Bearer → "Bearer 토큰이 필요합니다" 알림
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 서명 검증 + payload 추출 — 실패 시 JWTError
        # token : 클라이언트(브라우저)가 보낸 암호화된 문자열
        # SECRET_KEY : 서버만 알고 있는 비밀번호
        # algorithms=[ALGORITHM] : "어떤 수학적 방법으로 암호화했니?"
        username: str = payload.get("sub")
        # sub : 토큰의 주인
        # payload : '주인의 이름(ID)'
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


app = FastAPI(title="Stage 4-04 JWT 인증", version="1.0.0")


# ============================================================
# [실습 4] 인증 흐름 빈칸 채우기
# ============================================================
# get_current_user 함수의 동작 순서를 완성하세요.
#
# def get_current_user(token: str = Depends(???), db = Depends(get_db)):
#                                    oauth2_scheme
#     try:
#         payload = jwt.???(token, SECRET_KEY, algorithms=[ALGORITHM])
#                       decode
#         username = payload.get("???")
#                               sub
#         if username is None:
#             raise ???
#                   credentials_exception
#     except ???:
#                JWTError
#         raise credentials_exception
#
#     user = db.query(User).filter(User.username == username).???()
#                                                              first
#     return user
#
# Q. Depends(oauth2_scheme) 은 어디서 토큰을 꺼내나요?
#    → HTTP 요청의 '헤더(Header)'
#
# [정답]
# Depends(oauth2_scheme) : 요청 헤더 "Authorization: Bearer <토큰>" 에서 추출
# jwt.decode : 서명 검증 후 payload dict 반환
# payload.get("sub") : JWT payload의 subject (username)
# first() : 단건 조회


# ============================================================
# [이론 5] 라우트 구현
# ============================================================
#
# POST /register : 회원가입
#   - 비밀번호를 해싱하여 DB 저장
#   - username/email 중복 시 400
#
# POST /login : 로그인 → JWT 발급
#   - OAuth2PasswordRequestForm : username, password 폼 데이터 파싱
#   - 비밀번호 검증 → access_token 발급
#   - /docs의 Authorize 버튼이 이 엔드포인트로 폼 데이터 전송
#
# GET /me : 내 정보 조회 (인증 필요)
#   - get_current_user 의존성 → 토큰 자동 검증 + User 객체 반환
#   - 미인증 요청 시 자동 401

@app.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        # 평문 비밀번호를 해싱하여 저장
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2PasswordRequestForm : Content-Type: application/x-www-form-urlencoded
    #   form_data.username, form_data.password 로 접근
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    # get_current_user가 토큰 검증 + DB 조회까지 처리
    # 토큰이 없거나 유효하지 않으면 자동으로 401 반환
    return current_user


# ============================================================
# [실습 5-1] 회원가입 & 로그인 흐름 직접 테스트
# ============================================================
# 서버를 실행하고 /docs 에서 순서대로 테스트하세요.
#
# Step 1. POST /register
#    Body: { "username": "alice", "email": "alice@test.com", "password": "1234" }
#    → 201 + UserResponse (id, username, email, is_active)
#
# Step 2. POST /login
#    username: alice, password: 1234  (폼 데이터)
#    → 200 + { "access_token": "eyJ...", "token_type": "bearer" }
#
# Step 3. /docs 우상단 [Authorize] 버튼 클릭
#    → username: alice, password: 1234 입력 후 Authorize
#    (내부적으로 /login 호출 후 토큰을 헤더에 자동 포함)
#
# Step 4. GET /me
#    → 200 + 내 정보 (alice)
#
# Step 5. [Authorize] 로그아웃 후 GET /me 재시도
#    → 401 Unauthorized
#
# 확인 포인트:
#   □ /register 두 번 호출 시 400 반환?
#   □ 틀린 비밀번호로 /login 시 401 반환?
#   □ 토큰 없이 /me 호출 시 401 반환?


# ============================================================
# [실습 5-2] 보호된 엔드포인트 추가하기
# ============================================================
# 아래 요구사항에 맞는 라우트를 작성하세요.
#
# 1) GET /users — 전체 사용자 목록 (인증 필요)
#    - get_current_user 의존성 추가 (반환값은 사용하지 않아도 됨)
#    - list[UserResponse] 반환
# 코드 작성 ↓

# [정답 코드]
@app.get("/users", response_model=list[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user)
    # _: 반환값은 사용하지 않지만 인증 강제 목적으로 의존성 추가
):
    return db.query(User).offset(skip).limit(limit).all()


# 2) PATCH /me/password — 내 비밀번호 변경 (인증 필요)
#    - 요청 Body: { "current_password": "...", "new_password": "..." }
#    - current_password가 틀리면 400 + "현재 비밀번호가 올바르지 않습니다."
#    - 성공 시 200 + { "message": "비밀번호가 변경되었습니다." }
# 코드 작성 ↓

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=4)

# [정답 코드]
@app.patch("/me/password")
def change_password(
    body: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다.")

    current_user.hashed_password = hash_password(body.new_password)
    db.commit()
    return {"message": "비밀번호가 변경되었습니다."}


# ============================================================
# [실습 5-3] 토큰 만료 직접 확인하기
# ============================================================
# 토큰이 만료되면 어떤 일이 일어나는지 직접 확인하세요.
#
# Step 1. ACCESS_TOKEN_EXPIRE_MINUTES 를 1로 변경
#         (파일 상단 ACCESS_TOKEN_EXPIRE_MINUTES = 1)
#
# Step 2. 서버 재시작 후 /login 으로 토큰 발급
#
# Step 3. 1분 대기 후 GET /me 호출
#    → 401 + "인증에 실패했습니다."
#    (토큰의 exp가 지나면 jose가 자동으로 JWTError 발생)
#
# Step 4. ACCESS_TOKEN_EXPIRE_MINUTES = 30 으로 원복
#
# Q. 토큰 만료 시 클라이언트는 어떻게 대응해야 할까요?
#    → ???
#
# [정답]
# Refresh Token (갱신 토큰)을 별도로 발급해두고,
# Access Token 만료 시 Refresh Token으로 새 Access Token을 재발급 요청.
# Refresh Token은 더 긴 유효기간을 가지며 DB에 저장하여 폐기(로그아웃) 가능.


# ============================================================
# 실행 진입점
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("stage4_04_auth:app", host="0.0.0.0", port=8000, reload=True)
