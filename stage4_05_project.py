# ============================================================
# Stage 4 - 05. CRUD API 프로젝트 (최종 통합)
# ============================================================
# 지금까지 배운 것을 모두 합칩니다:
#   stage4_02 FastAPI 라우팅
#   stage4_03 SQLAlchemy DB 연동
#   stage4_04 JWT 인증
#
# 만들 것: 회원가입/로그인 + 게시글 CRUD REST API
#
# [API 목록]
#   POST   /register          회원가입 (공개)
#   POST   /login             로그인 → JWT 발급 (공개)
#   GET    /me                내 정보 (인증 필요)
#   POST   /posts             게시글 작성 (인증 필요)
#   GET    /posts             전체 게시글 목록 (공개)
#   GET    /posts/{id}        게시글 상세 조회 (공개)
#   PUT    /posts/{id}        게시글 수정 (인증 필요 + 본인 글만)
#   DELETE /posts/{id}        게시글 삭제 (인증 필요 + 본인 글만)
#
# [실행 방법]
#   uvicorn stage4_05_project:app --reload
#   → http://127.0.0.1:8000/docs 에서 테스트
#
# [사전 설치]
#   pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography]
#
# 학습 순서
#   1. 전체 구조 이해 (레이어 설계)
#   2. DB 모델 설계 (User + Post 관계)
#   3. 인증 재사용 (stage4_04 복습)
#   4. 게시글 CRUD 엔드포인트 작성
#   5. 권한 제어 (본인 글만 수정/삭제)

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy import (
    create_engine, Column, Integer, String,
    Boolean, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship


# ============================================================
# [이론 1] 프로젝트 구조 설계
# ============================================================
#
# 실제 FastAPI 프로젝트는 파일을 나눠서 관리하지만,
# 학습을 위해 한 파일에 전부 작성합니다.
#
# 레이어 역할:
#   Models    : DB 테이블 정의 (SQLAlchemy)
#   Schemas   : 요청/응답 데이터 형식 정의 (Pydantic)
#   Auth      : JWT 토큰 생성/검증
#   Routes    : HTTP 엔드포인트
#
# Spring 비교:
#   Models   ↔ Entity
#   Schemas  ↔ DTO (RequestDTO, ResponseDTO)
#   Auth     ↔ JwtTokenProvider + SecurityConfig
#   Routes   ↔ Controller + Service + Repository
#
# [관계 설계]
#   User (1) ─── Post (N)
#   한 명의 유저가 여러 게시글을 작성할 수 있음
#   → Post.author_id = FK → User.id


# ============================================================
# 설정값
# ============================================================

DATABASE_URL = "sqlite:///./stage4_project.db"
SECRET_KEY = "project-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ============================================================
# DB 설정
# ============================================================

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================
# [이론 2] DB 모델 — User + Post 관계
# ============================================================
#
# ForeignKey: 다른 테이블의 컬럼을 참조하는 외래키
#   author_id = Column(Integer, ForeignKey("users.id"))
#   → posts.author_id 는 users.id 를 참조
#
# relationship: ORM 수준의 객체 연결
#   User.posts → 해당 유저의 게시글 목록 (list)
#   Post.author → 게시글 작성자 (User 객체)
#
# back_populates: 양방향 관계 설정
#   user.posts 로 접근 가능 ↔ post.author 로 접근 가능
#
# Spring 비교:
#   @OneToMany / @ManyToOne 와 동일한 개념

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="author")
    # user.posts → 이 유저가 작성한 모든 게시글


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    # Text: 길이 제한 없는 문자열 (String은 길이 지정 필요)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 외래키: posts.author_id → users.id

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    # onupdate: UPDATE 쿼리 실행 시 자동으로 현재 시각으로 갱신

    author = relationship("User", back_populates="posts")
    # post.author → 이 게시글 작성자 (User 객체)


Base.metadata.create_all(bind=engine)


# ============================================================
# [실습 1] 관계형 모델 이해하기
# ============================================================
#
# Q1. 아래 코드에서 post.author 를 출력하면 어떤 타입이 나오나요?
#     post = db.query(Post).first()
#     print(type(post.author))
#     → ???
#
# Q2. user.posts 를 출력하면?
#     user = db.query(User).first()
#     print(type(user.posts))
#     → ???
#
# Q3. ForeignKey("users.id") 에서 "users.id" 는 무엇을 의미하나요?
#     → ???
#
# [정답]
# Q1. <class 'User'> — SQLAlchemy가 JOIN 없이 자동으로 User 객체 가져옴
# Q2. <class 'list'> — 해당 유저의 Post 객체 리스트
# Q3. "테이블명.컬럼명" — posts.author_id 가 참조할 users 테이블의 id 컬럼


# ============================================================
# 인증 (stage4_04 재사용)
# ============================================================

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증에 실패했습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# ============================================================
# [이론 3] Pydantic 스키마 설계
# ============================================================
#
# 요청(Request)용 스키마와 응답(Response)용 스키마를 분리합니다.
#
# 왜 분리하나요?
#   - 요청: 클라이언트가 보내는 데이터 (password 포함)
#   - 응답: 서버가 반환하는 데이터 (password 절대 포함 X)
#   - 생성 시 필드 ≠ 수정 시 필드 (수정은 일부만)
#
# Spring 비교:
#   UserCreateRequest DTO / UserResponse DTO 와 동일

# 회원 스키마
class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    email: str = Field(min_length=5)
    password: str = Field(min_length=4)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


# 토큰 스키마
class Token(BaseModel):
    access_token: str
    token_type: str


# 게시글 스키마
class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class PostUpdate(BaseModel):
    # 수정 시 title/content 중 일부만 보낼 수 있도록 Optional
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, min_length=1)


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    author_username: str   # author 객체에서 꺼낸 필드
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ============================================================
# [실습 2] 스키마 설계 이해하기
# ============================================================
#
# Q1. PostUpdate의 title, content 가 Optional인 이유는?
#     → ???
#
# Q2. PostResponse에 password 필드가 없는 이유는?
#     → ???
#
# Q3. PostCreate에서 author_id를 받지 않는 이유는?
#     → ???
#
# [정답]
# Q1. PATCH/PUT 시 일부 필드만 수정할 수 있도록 하기 위해.
#     None인 필드는 기존 값 유지.
# Q2. 응답에 민감한 정보(비밀번호)를 절대 포함시키면 안 됨.
# Q3. author_id는 JWT 토큰에서 꺼낸 현재 로그인 유저 ID를 사용.
#     클라이언트가 임의로 다른 사람 ID를 보낼 수 없도록 서버에서 결정.


# ============================================================
# FastAPI 앱
# ============================================================

app = FastAPI(title="Stage 4-05 CRUD API 프로젝트", version="1.0.0")


# ============================================================
# [이론 4] 인증 라우트 (stage4_04 복습)
# ============================================================

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
    return current_user


# ============================================================
# [이론 5] 게시글 CRUD 라우트
# ============================================================
#
# [권한 제어 핵심]
# 수정/삭제 시 두 가지를 확인해야 합니다:
#   1. 로그인했는가? → Depends(get_current_user)
#   2. 본인 글인가? → post.author_id == current_user.id
#
# Spring 비교:
#   @PreAuthorize("@postService.isOwner(#id, authentication.name)")
#   와 동일한 역할을 수동으로 구현하는 것
#
# [HTTP 상태 코드 정리]
#   201 Created    : 리소스 생성 성공
#   200 OK         : 조회/수정 성공
#   204 No Content : 삭제 성공 (본문 없음)
#   403 Forbidden  : 인증은 됐지만 권한 없음 (남의 글 수정 시도)
#   404 Not Found  : 게시글 없음


def get_post_or_404(post_id: int, db: Session) -> Post:
    # 중복 제거: 게시글 조회 + 없으면 404를 한 함수로
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post


@app.post("/posts", response_model=PostResponse, status_code=201)
def create_post(
    body: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    # Depends(get_current_user): 토큰 없으면 자동 401
):
    post = Post(
        title=body.title,
        content=body.content,
        author_id=current_user.id,
        # 서버에서 결정: 클라이언트가 임의로 설정 불가
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        author_username=post.author.username,
        # post.author → relationship 으로 자동 조회된 User 객체
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@app.get("/posts", response_model=list[PostResponse])
def list_posts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    # Query(): 쿼리 파라미터 유효성 검증
    # ge=0: 0 이상, le=100: 100 이하
    db: Session = Depends(get_db)
    # 인증 불필요: 누구나 게시글 목록 조회 가능
):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return [
        PostResponse(
            id=p.id,
            title=p.title,
            content=p.content,
            author_id=p.author_id,
            author_username=p.author.username,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in posts
    ]


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = get_post_or_404(post_id, db)
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        author_username=post.author.username,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    body: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_or_404(post_id, db)

    # 본인 글인지 확인
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인 게시글만 수정할 수 있습니다.")
        # 403 Forbidden: 인증은 됐지만 권한 없음

    # None이 아닌 필드만 업데이트
    if body.title is not None:
        post.title = body.title
    if body.content is not None:
        post.content = body.content

    db.commit()
    db.refresh(post)

    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author_id=post.author_id,
        author_username=post.author.username,
        created_at=post.created_at,
        updated_at=post.updated_at,
    )


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = get_post_or_404(post_id, db)

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="본인 게시글만 삭제할 수 있습니다.")

    db.delete(post)
    db.commit()
    # 204 No Content: 삭제 성공, 반환 본문 없음


# ============================================================
# [실습 3] 전체 흐름 직접 테스트
# ============================================================
# 서버를 실행하고 /docs 에서 순서대로 테스트하세요.
#
# Step 1. 유저 2명 생성
#   POST /register → { "username": "alice", "email": "alice@test.com", "password": "1234" }
#   POST /register → { "username": "bob",   "email": "bob@test.com",   "password": "1234" }
#
# Step 2. alice로 로그인 → Authorize 버튼으로 토큰 등록
#   POST /login → username: alice, password: 1234
#
# Step 3. alice가 게시글 작성
#   POST /posts → { "title": "안녕하세요", "content": "alice의 첫 게시글입니다." }
#   → 201 + PostResponse (author_username: "alice")
#
# Step 4. 전체 목록 / 상세 조회 (로그아웃 상태에서도 가능)
#   GET /posts        → 목록 확인
#   GET /posts/1      → alice의 게시글 확인
#
# Step 5. bob으로 로그인 후 alice 게시글 수정 시도
#   PUT /posts/1 → { "title": "해킹 시도" }
#   → 403 Forbidden ("본인 게시글만 수정할 수 있습니다.")
#
# Step 6. alice로 다시 로그인 후 본인 글 수정
#   PUT /posts/1 → { "title": "수정된 제목" }
#   → 200 + 수정된 PostResponse
#
# Step 7. alice가 본인 글 삭제
#   DELETE /posts/1
#   → 204 No Content
#
# 확인 포인트:
#   □ 인증 없이 POST /posts 시 401?
#   □ 남의 글 수정 시 403?
#   □ 없는 글 조회 시 404?
#   □ skip/limit 파라미터 동작 확인?


# ============================================================
# [실습 4] 기능 추가 도전
# ============================================================
#
# 아래 기능을 직접 추가해보세요.
#
# 1) GET /posts?author={username} — 특정 유저의 게시글만 필터링
#    힌트: Query 파라미터로 author: Optional[str] = None 추가
#          author가 있으면 .filter(Post.author.has(username=author)) 적용
#
# 2) GET /users/{username}/posts — 특정 유저의 게시글 목록
#    힌트: User 조회 후 user.posts 반환
#
# 3) POST /posts/{id}/like — 게시글 좋아요 (인증 필요)
#    힌트: Post 모델에 likes = Column(Integer, default=0) 추가
#          likes += 1 후 commit


# [정답 코드 - 1번]
@app.get("/posts/search/by-author", response_model=list[PostResponse])
def list_posts_by_author(
    author: str = Query(..., description="작성자 username"),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == author).first()
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 사용자입니다.")

    posts = db.query(Post).filter(Post.author_id == user.id).all()
    return [
        PostResponse(
            id=p.id,
            title=p.title,
            content=p.content,
            author_id=p.author_id,
            author_username=p.author.username,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in posts
    ]


# ============================================================
# [실습 5] 핵심 개념 복습 퀴즈
# ============================================================
#
# Q1. 아래 코드에서 403이 아닌 404를 먼저 반환해야 하는 이유는?
#
#     post = get_post_or_404(post_id, db)        # 먼저 실행
#     if post.author_id != current_user.id:       # 그 다음 확인
#         raise HTTPException(status_code=403)
#
#     → ???
#
# Q2. DELETE 엔드포인트가 status_code=204를 사용하는 이유는?
#     → ???
#
# Q3. get_post_or_404 함수를 별도로 만든 이유는?
#     → ???
#
# Q4. author_id를 클라이언트 요청 Body에서 받지 않는 이유는?
#     → ???
#
# [정답]
# Q1. 존재하지 않는 글에 대한 접근은 404가 맞음.
#     403을 먼저 반환하면 "존재는 하는데 권한이 없다"는 정보가 노출됨.
#     → 보안상 존재 여부를 먼저 확인해야 함.
#
# Q2. 204 No Content: 삭제 성공 시 반환할 본문이 없음을 명시.
#     본문을 반환하면 FastAPI가 경고를 발생시킴.
#
# Q3. get/update/delete 세 곳에서 동일한 "게시글 조회 + 404 처리" 로직이 반복됨.
#     → 중복 제거(DRY 원칙)를 위해 함수로 추출.
#
# Q4. 클라이언트가 임의로 다른 유저의 ID를 넣어 다른 사람 글인 척 작성할 수 있음.
#     → 서버가 JWT 토큰에서 신뢰할 수 있는 current_user.id 를 사용해야 함.


# ============================================================
# 실행 진입점
# ============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("stage4_05_project:app", host="0.0.0.0", port=8000, reload=True)
