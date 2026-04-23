# ============================================================
# Stage 1 - 03. 제어문 (if / for / while)
# ============================================================

# --- if / elif / else ---
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")

# 한 줄 조건식 (삼항 연산자)
result = "합격" if score >= 60 else "불합격"
print(result)


# --- for 루프 ---
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit) # apple, banana, cherry 순서대로 출력

# range() — 숫자 반복
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):     # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8 (step=2)
    print(i)

# enumerate() — 인덱스 + 값 동시에
for i, fruit in enumerate(fruits):
    print(i, fruit) # 0 apple, 1 banana, 2 cherry

# dict 순회
person = {"name": "김철수", "age": 28}
for key, value in person.items():
    print(key, ":", value)


# --- while 루프 ---
count = 0
while count < 5:
    print(count)
    count += 1

# break / continue
for i in range(10):
    if i == 3:
        continue    # 3은 건너뜀
    if i == 7:
        break       # 7에서 종료
    print(i)


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] 1부터 100까지의 합을 for 루프로 구하세요.
# 코드 작성 ↓
total = 0
for i in range(101):
    total += i
print(total)



# [문제 2] 아래 리스트에서 짝수만 골라 새 리스트로 만들어 출력하세요.
numbers = [3, 8, 15, 22, 7, 44, 11, 6]
# 코드 작성 ↓
even_numbers = []
for number in numbers:
    if number % 2 == 0:
        even_numbers.append(number)

print(even_numbers)


# [문제 3] 아래 딕셔너리에서 score가 80 이상인 학생의 이름만 출력하세요.
students = {
    "김철수": 75,
    "이영희": 92,
    "박민준": 88,
    "최지우": 61,
    "정하은": 95,
}
# 코드 작성 ↓
good_students = []
for name, score in students.items():
    if score >= 80:
        good_students.append(name)

print(good_students)



# [문제 4] while을 사용해서 2의 거듭제곱을 1부터 시작해 1000을 넘지 않는
# 범위까지 모두 출력하세요. (1, 2, 4, 8, 16 ...)
# 코드 작성 ↓
power = 1
power_list = []
while power <= 1000:
    power_list.append(power)
    power *= 2

print(power_list)