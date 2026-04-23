# ============================================================
# Stage 1 - 02. 컬렉션 (list, tuple, dict, set)
# ============================================================

# --- list: 순서 있음, 변경 가능 ---
fruits = ["apple", "banana", "cherry"]

print(fruits[0])       # apple  (인덱스 0부터 시작)
print(fruits[-1])      # cherry (음수 인덱스 = 뒤에서부터)
print(fruits[0:2])     # ['apple', 'banana'] (슬라이싱: 끝 인덱스 미포함)

fruits.append("mango")     # 맨 뒤에 추가
fruits.insert(1, "grape")  # 특정 위치에 추가
fruits.remove("banana")    # 값으로 삭제
popped = fruits.pop()      # 맨 뒤 꺼내기 (반환값 있음)

print(len(fruits))         # 길이


# --- tuple: 순서 있음, 변경 불가 ---
point = (3, 7)
x, y = point              # 언패킹
print(x, y)               # 3 7
# point[0] = 10           # TypeError! 변경 불가


# --- dict: 키-값 쌍, 변경 가능 ---
person = {
    "name": "김철수",
    "age": 28,
    "city": "서울"
}

print(person["name"])          # 김철수
print(person.get("email", "없음"))  # 키 없을 때 기본값 반환

person["email"] = "cs@email.com"  # 추가
person["age"] = 29                # 수정
del person["city"]                # 삭제

print(person.keys())     # 키 목록
print(person.values())   # 값 목록
print(person.items())    # (키, 값) 쌍 목록


# --- set: 순서 없음, 중복 없음 ---
nums = {1, 2, 3, 2, 1}
print(nums)              # {1, 2, 3} 중복 자동 제거

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a & b)             # 교집합: {3, 4}
print(a | b)             # 합집합: {1, 2, 3, 4, 5, 6}
print(a - b)             # 차집합: {1, 2}


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] 아래 리스트에서 슬라이싱으로 [30, 40, 50]만 출력하세요.
numbers = [10, 20, 30, 40, 50, 60, 70]
#           0   1   2   3   4   5   6
# 코드 작성 ↓
print(numbers[2:5])


# [문제 2] 아래 딕셔너리에서
# (1) "score" 키의 값을 95로 변경하고
# (2) "grade"라는 새 키에 "A"를 추가한 뒤
# (3) 딕셔너리 전체를 출력하세요.
student = {"name": "이영희", "score": 80}
# 코드 작성 ↓

student["score"] = 95
student["grade"] = "A"
print(student.items())


# [문제 3] 두 리스트에서 공통으로 들어있는 값만 추출해서 출력하세요.
# (set을 활용하세요)
list_a = [1, 2, 3, 4, 5]
list_b = [3, 4, 5, 6, 7]
# 코드 작성 ↓
print(set(list_a) & set(list_b))


# [문제 4] 아래 리스트에서 중복을 제거한 뒤 다시 list로 변환해서 출력하세요.
data = [1, 2, 2, 3, 4, 4, 4, 5]
# 코드 작성 ↓
unique_data = list(set(data))
print(unique_data)
