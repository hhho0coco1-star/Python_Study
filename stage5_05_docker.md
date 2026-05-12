# Stage 5 - 05. Docker 기초

## 학습 목표

- Docker가 무엇인지, 왜 쓰는지 이해
- 파이썬 앱의 Dockerfile 작성
- docker-compose 로 멀티 컨테이너 구성
- `.env` 파일로 환경변수 관리

---

## 이론 1 — Docker란?

> **"내 컴퓨터에서는 되는데..."** 를 없애는 기술

Docker는 앱과 실행 환경(OS 라이브러리, 파이썬 버전, pip 패키지)을 **컨테이너**에 함께 묶는다.  
어느 서버에서든 동일한 환경으로 실행 보장.

### 핵심 개념

| 용어 | 설명 |
|------|------|
| 이미지(Image) | 컨테이너의 설계도 (읽기 전용, Dockerfile로 빌드) |
| 컨테이너(Container) | 이미지를 실행한 인스턴스 (실행 중인 프로세스) |
| Dockerfile | 이미지 빌드 지시서 (어떤 OS, 어떤 패키지, 어떤 명령) |
| 레지스트리(Registry) | 이미지 저장소 (Docker Hub, GitHub Container Registry) |
| docker-compose | 여러 컨테이너를 한 번에 정의·실행하는 도구 |

### VM vs Docker

```
VM (가상머신)                Docker (컨테이너)
┌──────────────────┐        ┌──────────────────┐
│   App A  │ App B │        │   App A  │ App B │
│  Guest OS│GuestOS│        │  Libs A  │ Libs B│
│  Hypervisor      │        │  Docker Engine   │
│  Host OS         │        │  Host OS         │
└──────────────────┘        └──────────────────┘
→ OS 전체 복제 (수 GB)       → OS 커널 공유 (수십 MB)
→ 느린 시작 (분)             → 빠른 시작 (초)
```

---

## 이론 2 — Dockerfile 작성

### FastAPI 앱 기준 Dockerfile

```dockerfile
# 1. 베이스 이미지 선택 (파이썬 공식 이미지)
FROM python:3.11-slim

# 2. 작업 디렉토리 설정 (컨테이너 내부 경로)
WORKDIR /app

# 3. 의존성 파일 먼저 복사 (캐시 최적화)
COPY requirements.txt .

# 4. 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 복사
COPY . .

# 6. 포트 명시 (문서 목적, 실제 바인딩은 docker run -p)
EXPOSE 8000

# 7. 컨테이너 시작 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 레이어 캐시 최적화 이유

```
# 나쁜 순서 (소스 변경마다 pip install 재실행)
COPY . .
RUN pip install -r requirements.txt

# 좋은 순서 (requirements.txt 변경 없으면 pip install 캐시 재사용)
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

### 기본 명령어

```bash
# 이미지 빌드 (-t: 태그명, .: Dockerfile 위치)
docker build -t my-fastapi-app .

# 컨테이너 실행
# -d: 백그라운드, -p 호스트포트:컨테이너포트
docker run -d -p 8000:8000 my-fastapi-app

# 실행 중인 컨테이너 목록
docker ps

# 로그 확인
docker logs <컨테이너ID>

# 컨테이너 중지 & 삭제
docker stop <컨테이너ID>
docker rm <컨테이너ID>

# 이미지 삭제
docker rmi my-fastapi-app
```

---

## 이론 3 — .env 파일로 환경변수 관리

민감한 정보(비밀번호, API 키, JWT 시크릿)는 코드에 하드코딩하지 않고 환경변수로 분리.

### .env 파일

```env
# .env (절대 git에 올리면 안 됨!)
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=my-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=false
```

### .gitignore에 반드시 추가

```
.env
*.db
__pycache__/
```

### 파이썬에서 읽기 (python-dotenv)

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()   # .env 파일 읽어서 환경변수로 설정

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./default.db")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
```

### docker run 에서 환경변수 주입

```bash
# 개별 변수 직접 지정
docker run -e SECRET_KEY=abc123 -e DEBUG=true my-app

# .env 파일 통째로 주입
docker run --env-file .env my-app
```

---

## 이론 4 — docker-compose.yml

여러 컨테이너(앱 + DB + Redis)를 하나의 파일로 정의하고 함께 실행.

### FastAPI + PostgreSQL 예시

```yaml
# docker-compose.yml
version: "3.9"

services:
  # FastAPI 앱
  app:
    build: .                        # 현재 디렉토리 Dockerfile 빌드
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - SECRET_KEY=${SECRET_KEY}    # 호스트 환경변수 또는 .env 에서 읽음
    depends_on:
      - db                          # db 서비스가 먼저 시작된 후 실행
    volumes:
      - .:/app                      # 소스 코드 마운트 (개발용 hot-reload)
    restart: unless-stopped

  # PostgreSQL DB
  db:
    image: postgres:15              # 직접 빌드 없이 공식 이미지 사용
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data   # 데이터 영속화

  # Redis (캐시/세션)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:    # Named volume: 컨테이너 삭제해도 데이터 유지
```

### docker-compose 명령어

```bash
# 전체 서비스 빌드 + 실행 (백그라운드)
docker-compose up -d --build

# 실행 중인 서비스 상태 확인
docker-compose ps

# 특정 서비스 로그 실시간 확인
docker-compose logs -f app

# 컨테이너 내부 셸 접속
docker-compose exec app bash
docker-compose exec db psql -U user -d mydb

# 전체 서비스 중지 (컨테이너 삭제)
docker-compose down

# 볼륨까지 삭제 (DB 데이터 초기화)
docker-compose down -v
```

---

## 이론 5 — .dockerignore

`.gitignore` 처럼 Docker 빌드 컨텍스트에서 제외할 파일 지정.  
불필요한 파일이 이미지에 포함되면 크기가 커지고 빌드가 느려짐.

```
# .dockerignore
.env
.git
__pycache__
*.pyc
*.pyo
.pytest_cache
*.db
node_modules
```

---

## 이론 6 — 멀티스테이지 빌드 (빌드 최적화)

개발 의존성(pytest, mypy 등)을 최종 이미지에 포함하지 않는 기법.

```dockerfile
# 빌드 스테이지 (builder)
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .
RUN pytest                          # 빌드 중 테스트 실행

# 최종 스테이지 (production)
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /app .          # 빌더에서 소스만 복사

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 실습 — Stage 4 프로젝트 Docker화

Stage 4에서 만든 FastAPI CRUD API (`stage4_05_project.py`)를 Docker로 실행해보자.

### 1. 프로젝트 구조

```
stage4_project/
├── main.py               # stage4_05_project.py 복사
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

### 2. requirements.txt

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy==2.0.30
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
python-dotenv==1.0.1
```

### 3. Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 4. .env

```env
SECRET_KEY=change-this-in-production-please
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. docker-compose.yml

```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - .:/app
      - sqlite_data:/app/data
    restart: unless-stopped

volumes:
  sqlite_data:
```

### 6. 실행 순서

```bash
# 1. 빌드 & 실행
docker-compose up -d --build

# 2. 로그 확인
docker-compose logs -f api

# 3. Swagger UI 접속
# http://localhost:8000/docs

# 4. 중지
docker-compose down
```

---

## 퀴즈

**Q1. Dockerfile에서 COPY requirements.txt를 소스 코드보다 먼저 하는 이유는?**  
→ Docker는 명령어 단위로 레이어를 캐싱. requirements.txt가 변경되지 않으면  
  pip install 레이어 캐시를 재사용 → 빌드 속도 향상.

**Q2. docker-compose에서 depends_on의 한계는?**  
→ 컨테이너가 "시작"된 것만 보장. DB가 완전히 준비(ready) 되었는지는 보장 안 함.  
  실제로는 healthcheck 또는 wait-for-it 스크립트 사용 권장.

**Q3. Named volume과 bind mount의 차이는?**  
→ Named volume (`postgres_data:/var/lib/...`): Docker가 관리, 컨테이너 삭제해도 데이터 유지  
  Bind mount (`.:/app`): 호스트 경로를 직접 마운트, 개발 시 hot-reload에 사용

**Q4. .env 파일을 git에 올리면 안 되는 이유는?**  
→ 비밀번호, API 키, JWT 시크릿 등 민감 정보가 공개 저장소에 노출됨.  
  대신 `.env.example` (빈 값)을 커밋해서 필요한 변수 이름만 공유.

---

## 참고 자료

- Docker 공식 문서: https://docs.docker.com
- Docker Hub (공식 이미지): https://hub.docker.com
- python:3.11-slim 이미지 선택 이유: 경량(Debian 기반), 보안 패치 적용됨
- FastAPI + Docker 공식 가이드: https://fastapi.tiangolo.com/deployment/docker/
