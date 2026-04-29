# ============================================================
# Stage 2 - 07. 타입 힌트 (Type Hints)
# ============================================================
# Python 3.5+부터 지원하는 타입 힌트로 코드 가독성과 IDE 지원을 향상시킴
# 실행에는 영향 없음 — 타입 검사기(mypy)나 IDE가 정적 분석에 사용
#
# 새 형식 안내: 이론 바로 아래 실습 문제가 주어집니다.
# 각 이론을 읽고 바로 풀어보세요.


# ============================================================
# [이론 1] 기본 타입 힌트
# ============================================================
#
# 변수와 함수에 타입을 명시하는 기본 문법
#
#   변수:     name: str = "홍길동"
#   함수 인자: def func(x: int, y: float) -> str:
#   반환 없음: def greet(name: str) -> None:
#
# 기본 타입: int, float, str, bool, bytes, None

def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"안녕하세요, {name}님!"

def is_adult(age: int) -> bool:
    return age >= 18

score: int = 95
message: str = greet("철수")
print(add(3, 7))        # 10
print(message)          # 안녕하세요, 철수님!
print(is_adult(20))     # True


# ============================================================
# [실습 1] 기본 타입 힌트
# ============================================================
# 원의 넓이를 계산하는 함수를 타입 힌트를 사용해 작성하세요.
# - 함수명: circle_area
# - 인자: radius (float)
# - 반환: float (넓이 = 3.14159 * radius ** 2)
# - circle_area(5.0)의 결과를 출력하세요.
# 코드 작성 ↓
import math

def circle_area(radius: float) -> float:
    return math.pi * radius ** 2

print(circle_area(5.0)) 


# ============================================================
# [이론 2] 컬렉션 타입 힌트
# ============================================================
#
# Python 3.9+: list[int], dict[str, int], tuple[int, ...], set[str]
# Python 3.8 이하: from typing import List, Dict, Tuple, Set
#
# 컬렉션은 [안에 원소 타입]을 명시한다
#
#   list[int]           → 정수 리스트
#   dict[str, int]      → 문자열 키, 정수 값 딕셔너리
#   tuple[int, str]     → (정수, 문자열) 튜플
#   set[str]            → 문자열 집합

def sum_scores(scores: list[int]) -> int:
    return sum(scores)

def get_grade(grades: dict[str, int]) -> dict[str, str]:
    result: dict[str, str] = {}
    for name, score in grades.items():
        result[name] = "합격" if score >= 60 else "불합격"
    return result

def first_last(items: list[str]) -> tuple[str, str]:
    return items[0], items[-1]

print(sum_scores([80, 90, 70, 85]))          # 325
print(get_grade({"철수": 75, "영희": 45}))    # {'철수': '합격', '영희': '불합격'}
print(first_last(["사과", "바나나", "포도"])) # ('사과', '포도')


# ============================================================
# [실습 2] 컬렉션 타입 힌트
# ============================================================
# 학생별 점수 딕셔너리를 받아 평균 점수를 반환하는 함수를 작성하세요.
# - 함수명: average_score
# - 인자: scores (dict[str, int]) — {"이름": 점수}
# - 반환: float (전체 점수의 평균)
# - 아래 데이터로 결과를 출력하세요.
students = {"철수": 80, "영희": 92, "민준": 68, "지수": 75}
# 코드 작성 ↓
def average_score(scores: dict[str, int]) -> float:
    total = sum(scores.values())
    count = len(scores)
    return total / count if count > 0 else 0.0

print(average_score(students))

# ============================================================
# [이론 3] Optional / Union
# ============================================================
#
# Optional[X] → X 또는 None (= Union[X, None])
# Union[X, Y] → X 또는 Y 중 하나
#
# Python 3.10+: X | Y 형식으로 쓸 수 있음
#               Optional[X] → X | None
#
# 언제 씀?
#   - 반환값이 없을 수도 있을 때 → Optional
#   - 여러 타입을 허용할 때    → Union

from typing import Optional, Union

def find_user(user_id: int) -> Optional[str]:
    db = {1: "철수", 2: "영희"}
    return db.get(user_id)   # 없으면 None 반환

def stringify(value: Union[int, float, str]) -> str:
    return str(value)

# Python 3.10+ 문법 (동일한 의미)
def find_user_modern(user_id: int) -> str | None:
    db = {1: "철수", 2: "영희"}
    return db.get(user_id)

print(find_user(1))     # 철수
print(find_user(99))    # None
print(stringify(3.14))  # 3.14
print(stringify("abc")) # abc


# ============================================================
# [실습 3] Optional / Union
# ============================================================
# 이름을 받아 인사 문자열을 반환하는 함수를 작성하세요.
# - 함수명: make_greeting
# - 인자: name (Optional[str]) — None이면 "손님"으로 대체
# - 반환: str
# - make_greeting("영희")와 make_greeting(None) 모두 출력하세요.
# 코드 작성 ↓
def make_greeting(name: Optional[str]) -> str:
    if name is None:
        name = "손님"
    return f"안녕하세요, {name}님!"
print(make_greeting("영희"))
print(make_greeting(None))

# ============================================================
# [이론 4] TypedDict — 딕셔너리 구조 타입 지정
# ============================================================
#
# 딕셔너리의 키와 값 타입을 명시적으로 정의
# dict[str, Any]보다 훨씬 구체적 — IDE가 키 이름까지 자동완성해줌
#
#   class Product(TypedDict):
#       name: str
#       price: int
#       in_stock: bool


from typing import TypedDict

class Product(TypedDict):
    name: str
    price: int
    in_stock: bool

def print_product(p: Product) -> None:
    status = "재고 있음" if p["in_stock"] else "품절"
    print(f"{p['name']} — {p['price']:,}원 ({status})")

apple: Product = {"name": "사과", "price": 1500, "in_stock": True}
grape: Product = {"name": "포도", "price": 3000, "in_stock": False}

print_product(apple)   # 사과 — 1,500원 (재고 있음)
print_product(grape)   # 포도 — 3,000원 (품절)


# ============================================================
# [실습 4] TypedDict
# ============================================================
# 직원 정보를 TypedDict로 정의하고 사용하세요.
# - TypedDict 이름: Employee
# - 키: name (str), department (str), salary (int)
# - 함수명: print_employee(e: Employee) -> None
#   → "{이름} / {부서} / 월급: {salary:,}원" 형식으로 출력
# - 아래 두 직원 데이터로 각각 출력하세요.
#   {"name": "김철수", "department": "개발팀", "salary": 4500000}
#   {"name": "이영희", "department": "디자인팀", "salary": 4000000}
# 코드 작성 ↓
class Employee(TypedDict):
    name: str
    department: str
    salary: int

def print_employee(e: Employee) -> None:
    print(f"{e['name']} / {e['department']} / 월급: {e['salary']:,}원")

employee1: Employee = {"name": "김철수", "department": "개발팀", "salary": 4500000}
employee2: Employee = {"name": "이영희", "department": "디자인팀", "salary": 4000000}
print_employee(employee1)
print_employee(employee2)


# ============================================================
# [이론 5] dataclasses — 타입 힌트 기반 데이터 클래스
# ============================================================
#
# @dataclass 데코레이터를 붙이면
# 타입 힌트로 정의한 필드를 기반으로 __init__, __repr__, __eq__를 자동 생성
#
#   @dataclass
#   class Point:
#       x: float
#       y: float
#       label: str = "기본값"  ← 기본값 지정 가능
#
# field(default_factory=list) → 가변 기본값(리스트, 딕셔너리)을 안전하게 지정
# @dataclass(order=True)      → __lt__ 등 비교 연산자도 자동 생성

from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = "기본"

@dataclass(order=True)
class Student:
    name: str
    score: int
    tags: list[str] = field(default_factory=list)

p1 = Point(1.0, 2.0)
p2 = Point(3.0, 4.0, "목표")
print(p1)              # Point(x=1.0, y=2.0, label='기본')
print(p2)              # Point(x=3.0, y=4.0, label='목표')
print(p1 == Point(1.0, 2.0))   # True

s1 = Student("철수", 85, ["수학", "영어"])
s2 = Student("영희", 92)
s3 = Student("민준", 78)
students_list = [s1, s2, s3]
for s in sorted(students_list, key=lambda s: s.score, reverse=True):
    print(f"{s.name}: {s.score}점") # 영희: 92점, 철수: 85점, 민준: 78점


# ============================================================
# [실습 5] dataclasses
# ============================================================
# 책 정보를 관리하는 데이터클래스를 작성하세요.
# - 클래스명: Book
# - 필드: title (str), author (str), price (int), in_stock (bool = True)
# - 아래 책 3권을 생성하고, price 기준 오름차순으로 정렬하여 출력하세요.
#   Book("파이썬 완전정복", "홍길동", 28000)
#   Book("데이터 분석 입문", "김철수", 35000, False)
#   Book("알고리즘의 이해", "이영희", 22000)
# - 출력 형식: "{title} / {author} / {price:,}원 / {'재고있음' if in_stock else '품절'}"
# 코드 작성 ↓
@dataclass
class Book:
    title: str
    author: str
    price: int
    in_stock: bool = True

book1 = Book("파이썬 완전정복", "홍길동", 28000)
book2 = Book("데이터 분석 입문", "김철수", 35000, False)
book3 = Book("알고리즘의 이해", "이영희", 22000)
books = [book1, book2, book3]

for book in sorted(books, key=lambda b: b.price):
    stock_status = "재고있음" if book.in_stock else "품절"
    print(f"{book.title} / {book.author} / {book.price:,}원 / {stock_status}")
    

