# ============================================================
# Stage 1 - 04. 함수 (Functions)
# ============================================================

# --- 기본 함수 ---
def greet(name):
    return f"안녕하세요, {name}님!"

print(greet("김철수"))  # 안녕하세요, 김철수님!


# --- 기본값 파라미터 ---
def greet(name, msg="반갑습니다"):
    return f"{name}님, {msg}"

print(greet("이영희"))             # 이영희님, 반갑습니다
print(greet("박민준", "오랜만이에요"))  # 박민준님, 오랜만이에요


# --- 여러 값 반환 ---
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 7, 2, 9])
print(lo, hi)  # 1 9


# --- *args: 개수 불정 인자 ---
def total(*args):
    return sum(args)

print(total(1, 2, 3))        # 6
print(total(10, 20, 30, 40)) # 100


# --- **kwargs: 키워드 인자 묶음 ---
def show_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_info(name="김철수", age=28, city="서울")


# --- 함수는 변수처럼 사용 가능 ---
def double(x):
    return x * 2

def apply(func, value):
    return func(value)

print(apply(double, 5))  # 10


# --- lambda: 한 줄 익명 함수 ---
square = lambda x: x ** 2
print(square(4))  # 16

# 주로 sorted, map, filter와 함께 사용
nums = [3, 1, 4, 1, 5, 9, 2]
print(sorted(nums, reverse=True))          # 내림차순
print(list(map(lambda x: x * 2, nums)))   # 각 요소 2배
print(list(filter(lambda x: x > 3, nums))) # 3 초과만


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] 숫자 리스트를 받아 평균을 반환하는 함수 average()를 작성하세요.
# average([10, 20, 30, 40]) → 25.0
# 코드 작성 ↓
def average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0


# [문제 2] 두 수를 받아 (합, 차, 곱, 몫)을 한 번에 반환하는 함수를 작성하세요.
# calculate(10, 3) → (13, 7, 30, 3.333...)
# 코드 작성 ↓
def calculate(a, b):
    return a + b, a - b, a * b, (a / b if b != 0 else None)

# [문제 3] 아래 학생 리스트를 score 기준 내림차순으로 정렬해서 출력하세요.
# lambda를 활용하세요.
students = [
    {"name": "김철수", "score": 75},
    {"name": "이영희", "score": 92},
    {"name": "박민준", "score": 88},
    {"name": "최지우", "score": 61},
]
# 코드 작성 ↓
sorted_students = sorted(students, key=lambda s: s["score"], reverse=True)
# reverse=True 내림차순 정렬, Faslse 오름차순 정렬
for student in sorted_students:
    print(student)



# [문제 4] *args를 활용해서 전달된 숫자 중 짝수만 골라 합산하는
# 함수 sum_evens()를 작성하세요.
# sum_evens(1, 2, 3, 4, 5, 6) → 12
# 코드 작성 ↓
def sum_evens(*args):
    return sum(x for x in args if x % 2 == 0)

