# ============================================================
# Stage 1 - 01. 변수 & 자료형 (Variables & Data Types)
# ============================================================

# --- 핵심 개념 ---
# 파이썬은 동적 타입 언어 → 타입 선언 없이 바로 할당

age = 25
height = 175.5
name = "파이썬"
is_student = True
data = None

# 타입 확인
print(type(age))       # <class 'int'>
print(type(height))    # <class 'float'>
print(type(name))      # <class 'str'>

# 타입 변환
x = "42"
x = int(x)
print(x + 8)           # 50

# 여러 변수 동시 할당
a, b, c = 1, 2, 3
a, b = b, a            # 값 교환 (임시 변수 불필요)


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] 아래 출력 결과를 주석으로 예측한 뒤, 실행해서 확인하세요.
a = 10
b = "10"
c = 10.0

print(a == b)           # 예측: False
print(a == c)           # 예측: True 
print(type(a) == type(c))  # 예측: False


# [문제 2] 아래 조건을 만족하는 변수를 선언하고 한 줄에 모두 출력하세요.
# - 이름: "김철수", 나이: 28, 키: 172.3, 취업 여부: False
# 여기에 코드 작성 ↓
name = "김철수"
age = 28
height = 172.3
is_employed = False
print(name, age, height, is_employed)


# [문제 3] 아래 코드는 에러가 납니다. 이유를 주석으로 쓰고 고치세요.
# score = "95"
# result = score + 5
# print(result)
# 이유: score는 문자열 형이므로 숫자 5와 더할 수 없다. 타입변환이 필요하다.
# 수정 코드 ↓
score = "95"
result = int(score) + 5

