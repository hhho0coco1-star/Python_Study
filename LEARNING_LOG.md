# 파이썬 독학 학습 기록

> 시작일: 2026-04-24  
> 목표: 데이터 분석/AI + 백엔드 웹 개발 + 일반 코딩 실력 향상  
> 학습 방식: 개념 설명 → 예제 → 실습 문제 → 피드백

---

## 전체 진행 현황

| Stage | 주제 | 상태 |
|-------|------|------|
| Stage 1 | 파이썬 기초 | 🔄 진행 중 (5/7) |
| Stage 2 | 중급 파이썬 | ⏳ 예정 |
| Stage 3 | 데이터 분석 트랙 | ⏳ 예정 |
| Stage 4 | 백엔드 웹 개발 트랙 | ⏳ 예정 |
| Stage 5 | 심화 & 고급 | ⏳ 예정 |

---

## Stage 1 — 파이썬 기초

### 01. 변수 & 자료형 ✅
**파일:** `stage1_01_variables.py`

| 개념 | 내용 |
|------|------|
| 동적 타입 | 타입 선언 없이 바로 할당 |
| 기본 자료형 | int, float, str, bool, None |
| 타입 확인/변환 | `type()`, `int()`, `str()`, `float()` |
| 다중 할당 | `a, b, c = 1, 2, 3` |
| 값 교환 | `a, b = b, a` (임시 변수 불필요) |

**실습 결과:** 문제 1 예측 오류 (int==str → False, int==float → True 헷갈림), 문제 2·3 완벽

---

### 02. 컬렉션 ✅
**파일:** `stage1_02_collections.py`

| 타입 | 순서 | 중복 | 변경 | 특징 |
|------|------|------|------|------|
| list | O | O | O | 가장 범용적 |
| tuple | O | O | X | 불변, 언패킹 유용 |
| dict | O | 키 X | O | 키-값 쌍 |
| set | X | X | O | 집합 연산 |

**주요 패턴:**
- 중복 제거: `list(set(data))`
- 순서 유지 중복 제거: `list(dict.fromkeys(data))`
- 교집합: `set(a) & set(b)`

**실습 결과:** 4/4 완벽

---

### 03. 제어문 ✅
**파일:** `stage1_03_control_flow.py`

| 문법 | 용도 |
|------|------|
| `if / elif / else` | 조건 분기 |
| `for i in range(n)` | 숫자 반복 |
| `enumerate(list)` | 인덱스 + 값 동시 순회 |
| `dict.items()` | 키-값 동시 순회 |
| `break / continue` | 루프 제어 |
| 삼항 연산자 | `값 if 조건 else 다른값` |

**실습 결과:** 문제 1 변수 초기화 누락 (sum → total), 나머지 완벽

---

### 04. 함수 ✅
**파일:** `stage1_04_functions.py`

| 문법 | 용도 |
|------|------|
| `def func(a, b="기본값")` | 기본값 파라미터 |
| `return a, b` | 여러 값 동시 반환 (튜플) |
| `*args` | 개수 불정 위치 인자 |
| `**kwargs` | 키워드 인자 묶음 |
| `lambda x: x*2` | 한 줄 익명 함수 |
| `sorted(list, key=lambda)` | 정렬 기준 지정 |

**실습 결과:** 4/4 완벽 (방어 코드, 제너레이터 표현식까지 활용)

---

### 05. 문자열 ✅
**파일:** `stage1_05_strings.py`

| 문법/메서드 | 용도 |
|-------------|------|
| `f"{변수}"` | f-string 포맷팅 |
| `.strip()` | 앞뒤 공백 제거 |
| `.split("구분자")` | 문자열 → 리스트 |
| `"구분자".join(list)` | 리스트 → 문자열 |
| `.replace(a, b)` | 치환 |
| `.title()` | 각 단어 첫 글자 대문자 |
| `s[::-1]` | 문자열 뒤집기 |

**실습 결과:** 문제 1 닫는 괄호 오타, 문제 4 변수명 오타, 나머지 완벽

---

### 06. 파일 I/O ⏳
**파일:** `stage1_06_file_io.py` (예정)

| 개념 | 내용 |
|------|------|
| 파일 열기 | `open(path, mode)` — r/w/a/rb 모드 |
| with 구문 | 자동 close 보장 |
| 읽기 | `.read()`, `.readlines()`, `.readline()` |
| 쓰기 | `.write()`, `.writelines()` |
| 인코딩 | `encoding="utf-8"` |

---

### 07. 예외 처리 ⏳
**파일:** `stage1_07_exceptions.py` (예정)

| 개념 | 내용 |
|------|------|
| 기본 구조 | `try / except / else / finally` |
| 예외 잡기 | `except ValueError as e:` |
| 예외 발생 | `raise ValueError("메시지")` |
| 커스텀 예외 | `class MyError(Exception)` |

---

## Stage 2 — 중급 파이썬

### 01. OOP (객체지향) ⏳
**파일:** `stage2_01_oop.py` (예정)

| 개념 | 내용 |
|------|------|
| 클래스 | `class MyClass:` |
| 생성자 | `def __init__(self, ...)` |
| 인스턴스 메서드 | `def method(self)` |
| 클래스 메서드 | `@classmethod` |
| 정적 메서드 | `@staticmethod` |
| 상속 | `class Child(Parent)` |
| 메서드 오버라이딩 | 부모 메서드 재정의 |
| 매직 메서드 | `__str__`, `__len__`, `__eq__` 등 |

---

### 02. 컴프리헨션 ⏳
**파일:** `stage2_02_comprehension.py` (예정)

| 문법 | 예시 |
|------|------|
| 리스트 컴프리헨션 | `[x*2 for x in range(10) if x%2==0]` |
| 딕셔너리 컴프리헨션 | `{k: v for k, v in items}` |
| 셋 컴프리헨션 | `{x for x in data}` |
| 중첩 컴프리헨션 | `[x for row in matrix for x in row]` |

---

### 03. 제너레이터 ⏳
**파일:** `stage2_03_generator.py` (예정)

| 개념 | 내용 |
|------|------|
| `yield` | 값을 하나씩 반환 (lazy evaluation) |
| 제너레이터 함수 | `def gen(): yield ...` |
| 제너레이터 표현식 | `(x for x in range(10))` |
| `next()` | 다음 값 꺼내기 |
| 메모리 효율 | 대용량 데이터 처리에 유리 |

---

### 04. 데코레이터 ⏳
**파일:** `stage2_04_decorator.py` (예정)

| 개념 | 내용 |
|------|------|
| 기본 구조 | 함수를 인자로 받아 함수를 반환하는 함수 |
| `@decorator` 문법 | 함수 선언 위에 붙임 |
| `functools.wraps` | 원본 함수 메타정보 보존 |
| 실전 활용 | 로깅, 실행시간 측정, 인증 체크 |

---

### 05. 모듈 & 패키지 ⏳
**파일:** `stage2_05_modules.py` (예정)

| 개념 | 내용 |
|------|------|
| import | `import os`, `from os import path` |
| `__name__` | 직접 실행 vs 임포트 구분 |
| 가상환경 | `venv` 생성 및 활성화 |
| pip | 패키지 설치/관리 |

---

### 06. 표준 라이브러리 ⏳
**파일:** `stage2_06_stdlib.py` (예정)

| 모듈 | 주요 기능 |
|------|-----------|
| `os` | 파일/디렉토리 조작 |
| `sys` | 인터프리터 정보 |
| `datetime` | 날짜/시간 처리 |
| `collections` | Counter, defaultdict, deque |
| `itertools` | 순열, 조합, chain |
| `json` | JSON 직렬화/역직렬화 |

---

### 07. 타입 힌트 ⏳
**파일:** `stage2_07_type_hints.py` (예정)

| 개념 | 예시 |
|------|------|
| 기본 타입 힌트 | `def func(x: int) -> str:` |
| 컬렉션 힌트 | `list[int]`, `dict[str, int]` |
| Optional | `Optional[str]` = str 또는 None |
| Union | `Union[int, str]` |

---

## Stage 3 — 데이터 분석 트랙

### 01. NumPy ⏳
**파일:** `stage3_01_numpy.py` (예정)

| 개념 | 내용 |
|------|------|
| 배열 생성 | `np.array()`, `np.zeros()`, `np.arange()` |
| 브로드캐스팅 | 크기 다른 배열 간 연산 |
| 인덱싱/슬라이싱 | 다차원 배열 접근 |
| 수학 연산 | `np.sum()`, `np.mean()`, `np.std()` |

---

### 02. Pandas ⏳
**파일:** `stage3_02_pandas.py` (예정)

| 개념 | 내용 |
|------|------|
| DataFrame | 2차원 테이블 자료구조 |
| Series | 1차원 배열 |
| 데이터 로드 | `pd.read_csv()`, `pd.read_excel()` |
| 필터링 | 조건식으로 행 선택 |
| groupby | 그룹별 집계 |
| merge/join | 테이블 결합 |
| 결측치 처리 | `fillna()`, `dropna()` |

---

### 03. 시각화 ⏳
**파일:** `stage3_03_visualization.py` (예정)

| 라이브러리 | 주요 차트 |
|------------|-----------|
| Matplotlib | 선 그래프, 막대, 산점도, 히스토그램 |
| Seaborn | heatmap, boxplot, pairplot |

---

### 04. EDA 실전 프로젝트 ⏳
**파일:** `stage3_04_eda_project.py` (예정)

공개 데이터셋(예: 타이타닉, 아이리스)을 활용한 탐색적 데이터 분석

---

### 05. Scikit-learn 입문 ⏳
**파일:** `stage3_05_sklearn.py` (예정)

| 개념 | 내용 |
|------|------|
| 선형 회귀 | `LinearRegression` |
| 분류 | `LogisticRegression`, `RandomForest` |
| 모델 평가 | `train_test_split`, 정확도, F1 |
| 전처리 | `StandardScaler`, `LabelEncoder` |

---

## Stage 4 — 백엔드 웹 개발 트랙

### 01. HTTP 기초 ⏳
**파일:** `stage4_01_http.py` (예정)

| 개념 | 내용 |
|------|------|
| REST | 자원 기반 API 설계 원칙 |
| HTTP 메서드 | GET, POST, PUT, DELETE |
| 상태 코드 | 200, 201, 400, 401, 404, 500 |
| 요청/응답 구조 | Header, Body, Status |

---

### 02. FastAPI ⏳
**파일:** `stage4_02_fastapi.py` (예정)

| 개념 | 내용 |
|------|------|
| 라우팅 | `@app.get()`, `@app.post()` |
| Pydantic 모델 | 요청/응답 데이터 검증 |
| 경로 매개변수 | `/items/{item_id}` |
| 쿼리 매개변수 | `/items?skip=0&limit=10` |
| 의존성 주입 | `Depends()` |
| 자동 문서화 | `/docs` (Swagger UI) |

---

### 03. 데이터베이스 ⏳
**파일:** `stage4_03_database.py` (예정)

| 개념 | 내용 |
|------|------|
| SQLite | 파일 기반 경량 DB |
| SQLAlchemy | ORM (객체-관계 매핑) |
| 모델 정의 | `Base`, `Column`, `relationship` |
| CRUD | Create, Read, Update, Delete |
| 세션 관리 | `SessionLocal`, `get_db` |

---

### 04. JWT 인증 ⏳
**파일:** `stage4_04_auth.py` (예정)

| 개념 | 내용 |
|------|------|
| JWT 구조 | Header.Payload.Signature |
| 토큰 발급 | 로그인 성공 시 access token 반환 |
| 토큰 검증 | 요청 헤더 `Authorization: Bearer` |
| `python-jose` | JWT 라이브러리 |

---

### 05. CRUD API 프로젝트 ⏳
**파일:** `stage4_05_project/` (예정)

회원가입/로그인 + 게시글 CRUD 기능을 갖춘 REST API 서버 완성

---

## Stage 5 — 심화 & 고급

### 01. 비동기 프로그래밍 ⏳
**파일:** `stage5_01_async.py` (예정)

| 개념 | 내용 |
|------|------|
| `asyncio` | 이벤트 루프 기반 비동기 |
| `async def` | 비동기 함수 선언 |
| `await` | 비동기 작업 대기 |
| `aiohttp` | 비동기 HTTP 클라이언트 |

---

### 02. 테스팅 ⏳
**파일:** `stage5_02_testing.py` (예정)

| 개념 | 내용 |
|------|------|
| pytest | 테스트 프레임워크 |
| 단위 테스트 | 함수/메서드 단위 검증 |
| 픽스처 | `@pytest.fixture` |
| 모킹 | `unittest.mock`, `pytest-mock` |

---

### 03. 성능 최적화 ⏳
**파일:** `stage5_03_performance.py` (예정)

| 개념 | 내용 |
|------|------|
| 프로파일링 | `cProfile`, `timeit` |
| 캐싱 | `functools.lru_cache` |
| 제너레이터 활용 | 메모리 효율화 |

---

### 04. 디자인 패턴 ⏳
**파일:** `stage5_04_patterns.py` (예정)

싱글톤, 팩토리, 옵저버, 전략 패턴 등 파이썬에서의 구현

---

### 05. Docker 기초 ⏳
**파일:** `stage5_05_docker.md` (예정)

| 개념 | 내용 |
|------|------|
| Dockerfile | 파이썬 앱 이미지 빌드 |
| docker-compose | 멀티 컨테이너 구성 |
| 환경변수 | `.env` 파일 활용 |

---

## 메모 & 자주 하는 실수

| 실수 | 올바른 방법 |
|------|-------------|
| `sum` 을 변수명으로 사용 | `total` 등 다른 이름 사용 (내장 함수 덮어씀) |
| 변수 초기화 없이 `+=` 사용 | 먼저 `total = 0` 초기화 |
| `print(dict.items())` | `print(dict)` 로 전체 출력 |
| 연산자 우선순위 모호할 때 | 괄호로 명확하게 `(a / b if b != 0 else None)` |
| 문자열은 변경 불가 | 새 문자열 생성: `s = s[0].upper() + s[1:]` |
