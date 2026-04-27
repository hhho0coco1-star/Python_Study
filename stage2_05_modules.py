# ============================================================
# Stage 2 - 05. 모듈 & 패키지 (Modules & Packages)
# ============================================================


# ============================================================
# [이론 1] 모듈이란?
# ============================================================
#
# 모듈 = .py 파일 하나
# 함수, 클래스, 변수를 모듈로 분리하면:
#   - 코드를 재사용할 수 있다
#   - 파일이 커지는 것을 막고 역할별로 나눌 수 있다
#   - 다른 사람이 만든 코드를 가져다 쓸 수 있다
#
# import 방식 3가지:
#
#   import math                  → math.sqrt(4) 처럼 모듈명.함수명 으로 접근
#   from math import sqrt        → sqrt(4) 처럼 바로 사용 가능
#   from math import sqrt as sq  → sq(4) 처럼 별칭으로 사용

import math
print(math.sqrt(16))      # 4.0
print(math.pi)            # 3.141592653589793

from math import sqrt, ceil, floor
print(sqrt(9))            # 3.0
print(ceil(3.2))          # 4
print(floor(3.8))         # 3

from math import factorial as fact
print(fact(5))            # 120


# ============================================================
# [이론 2] 표준 라이브러리 주요 모듈
# ============================================================
#
# 파이썬 설치 시 기본 제공되는 모듈들 — 별도 설치 없이 바로 import 가능

# --- os: 운영체제 파일/디렉토리 작업 ---
import os

print(os.getcwd())                        # 현재 작업 디렉토리
print(os.path.exists("stage2_05_modules.py"))  # 파일 존재 여부
print(os.path.join("folder", "file.txt"))      # 경로 합치기 (OS에 맞는 구분자)
print(os.path.basename("/a/b/c.txt"))          # c.txt
print(os.path.dirname("/a/b/c.txt"))           # /a/b
print(os.path.splitext("report.pdf"))          # ('report', '.pdf')

# --- sys: 파이썬 인터프리터 정보 ---
import sys

print(sys.version)          # 파이썬 버전
print(sys.platform)         # 운영체제 (win32, linux, darwin)
# sys.argv → 명령줄 인자 리스트 (스크립트 실행 시 사용)
# sys.exit(0) → 프로그램 종료

# --- datetime: 날짜/시간 처리 ---
from datetime import datetime, date, timedelta

now = datetime.now()
print(now)                                    # 현재 날짜+시간
print(now.strftime("%Y-%m-%d %H:%M:%S"))      # 포맷 출력
print(now.year, now.month, now.day)           # 연, 월, 일

d1 = date(2026, 1, 1)
d2 = date(2026, 4, 27)
diff = d2 - d1
print(diff.days)                              # 116 (날짜 차이)

tomorrow = now + timedelta(days=1)
print(tomorrow.strftime("%Y-%m-%d"))          # 내일 날짜

# 문자열 → datetime
parsed = datetime.strptime("2026-04-27", "%Y-%m-%d")
print(parsed)

# --- random: 난수 생성 ---
import random

print(random.randint(1, 10))            # 1~10 정수 난수
print(random.random())                  # 0.0 ~ 1.0 실수
print(random.choice(["a", "b", "c"]))  # 리스트에서 무작위 선택
items = [1, 2, 3, 4, 5]
random.shuffle(items)
print(items)                            # 섞인 리스트
print(random.sample(items, 3))         # 중복 없이 3개 선택


# ============================================================
# [이론 3] collections 모듈
# ============================================================
#
# 파이썬 내장 컬렉션(list, dict, set)의 확장 버전 제공

from collections import Counter, defaultdict, deque

# Counter: 요소 개수를 자동으로 세는 딕셔너리
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
cnt = Counter(words)
print(cnt)                          # Counter({'apple': 3, 'banana': 2, 'cherry': 1})
print(cnt["apple"])                 # 3
print(cnt.most_common(2))           # [('apple', 3), ('banana', 2)]

text = "hello world"
print(Counter(text))                # 문자별 개수

# defaultdict: 키가 없을 때 기본값을 자동 생성하는 딕셔너리
#   일반 dict: 없는 키 접근 시 KeyError
#   defaultdict: 없는 키 접근 시 기본값 자동 생성
dd = defaultdict(list)
dd["a"].append(1)
dd["a"].append(2)
dd["b"].append(3)
print(dict(dd))     # {'a': [1, 2], 'b': [3]}

dd_int = defaultdict(int)   # 기본값 0
for ch in "mississippi":
    dd_int[ch] += 1
print(dict(dd_int))         # {'m': 1, 'i': 4, 's': 4, 'p': 2}

# deque: 양쪽 끝에서 O(1) 삽입/삭제 가능한 큐
#   list는 앞쪽 삽입/삭제가 O(n) → 대량 데이터에서 느림
dq = deque([1, 2, 3])
dq.appendleft(0)    # 왼쪽에 추가
dq.append(4)        # 오른쪽에 추가
print(dq)           # deque([0, 1, 2, 3, 4])
dq.popleft()        # 왼쪽에서 제거
print(dq)           # deque([1, 2, 3, 4])

dq_fixed = deque([1, 2, 3], maxlen=3)  # 최대 크기 제한
dq_fixed.append(4)
print(dq_fixed)     # deque([2, 3, 4], maxlen=3) — 오래된 것 자동 제거


# ============================================================
# [이론 4] itertools 모듈
# ============================================================
#
# 반복자(이터레이터)를 조합하는 도구 모음
# 제너레이터 기반이라 메모리 효율적

import itertools

# product: 데카르트 곱 (중복 순열)
for p in itertools.product([1, 2], ["a", "b"]):
    print(p, end=" ")   # (1, 'a') (1, 'b') (2, 'a') (2, 'b')
print()

# permutations: 순열 (순서 있음, 중복 없음)
print(list(itertools.permutations([1, 2, 3], 2))) # 뒤에 숫자 2 : 몇 개씩 뽑을지
# [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]

# combinations: 조합 (순서 없음, 중복 없음)
print(list(itertools.combinations([1, 2, 3, 4], 2)))
# [(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]

# chain: 여러 이터러블을 하나로 연결
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print(combined)     # [1, 2, 3, 4, 5]

# groupby: 연속된 같은 값끼리 그룹핑 (정렬 후 사용해야 제대로 동작)
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4), ("C", 5)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A [('A', 1), ('A', 2)]
# B [('B', 3), ('B', 4)]
# C [('C', 5)]


# ============================================================
# [이론 5] json 모듈
# ============================================================
#
# JSON: 웹 API, 설정 파일에서 가장 많이 쓰이는 데이터 형식
#
# json.dumps()  : 파이썬 객체 → JSON 문자열 (직렬화)
# json.loads()  : JSON 문자열 → 파이썬 객체 (역직렬화)
# json.dump()   : 파이썬 객체 → JSON 파일로 저장
# json.load()   : JSON 파일 → 파이썬 객체로 읽기

import json

# 직렬화
data = {"name": "철수", "age": 25, "scores": [90, 85, 92]}
json_str = json.dumps(data, ensure_ascii=False, indent=2)
# ensure_ascii=False → 한글이 깨지지 않도록
# indent = 2 -> 보기 좋게 들여쓰기
print(json_str)
# {
#   "name": "철수",
#   "age": 25,
#   "scores": [90, 85, 92]
# }

# 역직렬화
parsed = json.loads(json_str)
print(parsed["name"])       # 철수
print(type(parsed))         # <class 'dict'>

# 파일 저장/읽기
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded)               # {'name': '철수', 'age': 25, 'scores': [90, 85, 92]}

# 정리 후 삭제
os.remove("data.json")


# ============================================================
# [이론 6] __name__ == "__main__"
# ============================================================
#
# 파이썬 파일은 두 가지 방식으로 실행된다:
#   1. 직접 실행: python my_module.py  → __name__ == "__main__"
#   2. 임포트됨: import my_module      → __name__ == "my_module"
#
# if __name__ == "__main__": 블록은
# 파일을 직접 실행할 때만 실행되고,
# import 될 때는 실행되지 않는다.
#
# 사용 이유:
#   - 모듈로도 쓰고 스크립트로도 쓸 수 있게 하기 위해
#   - 테스트 코드를 모듈 하단에 넣고 import 시 자동 실행 방지

def add(a, b):
    return a + b

if __name__ == "__main__":
    # 이 블록은 직접 실행 시에만 동작
    print("직접 실행됨")
    print(add(3, 4))


# ============================================================
# [이론 7] 패키지와 가상환경
# ============================================================
#
# 패키지: 여러 모듈을 디렉토리로 묶은 것
#   my_package/
#   ├── __init__.py    ← 이 파일이 있어야 파이썬이 패키지로 인식
#   ├── utils.py
#   └── models.py
#
# from my_package import utils
# from my_package.models import MyModel
#
# 가상환경 (venv): 프로젝트별로 독립된 파이썬 환경을 만드는 것
#   생성:    python -m venv .venv
#   활성화:  .venv\Scripts\activate   (Windows)
#            source .venv/bin/activate (Mac/Linux)
#   비활성화: deactivate
#
# pip: 외부 패키지 설치 도구
#   pip install requests          ← 설치
#   pip uninstall requests        ← 제거
#   pip list                      ← 설치된 패키지 목록
#   pip freeze > requirements.txt ← 의존성 파일로 저장
#   pip install -r requirements.txt ← 의존성 일괄 설치


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] datetime을 사용해서 아래를 구하세요.
# - 오늘 날짜 기준으로 D-day(2026-12-31)까지 며칠 남았는지 출력
# - 형식: "D-day까지 XXX일 남았습니다."
# 코드 작성 ↓
dday = date(2026, 12, 31)
today = date.today()
diff = dday - today
print(f"D-day까지 {diff.days}일 남았습니다.")


# [문제 2] Counter를 사용해서 아래를 구하세요.
# sentence에서 가장 많이 등장한 단어 3개를 출력하세요.
# (대소문자 무시, 구두점 제외)
sentence = "to be or not to be that is the question to be"
# 코드 작성 ↓
import re # re 모듈은 정규 표현식 처리용
from collections import Counter
# 1. 소문자로 변환
sentence = sentence.lower() # 소문자로 변환

# 2. 구두점 제거 (정규 표현식 사용)
sentence = re.sub(r'[^\w\s]', '', sentence) # 구두점 제거 -> 문자나 공백이 아닌 것 제거
# \w는 단어 문자, \s는 공백 문자, ^는 부정, []는 문자 클래스

# 3. 단어 리스트로 분리
words = sentence.split() # 단어 리스트로 분리

# 4. Counter로 단어 개수 세기
cnt = Counter(words)

# 5. 가장 많이 등장한 단어 3개 출력
most_common = cnt.most_common(3) # 가장 많이 등장한 단어 3개
for word, count in most_common:
    print(f"{word} : {count}회") # 단어 : 개수회



# [문제 3] itertools.combinations를 사용해서
# 로또 번호(1~45 중 6개)의 모든 조합 개수를 구하고 출력하세요.
# 형식: "로또 조합 경우의 수: 8,145,060"
# 코드 작성 ↓
import itertools
numbers = range(1, 46) # 1~45
combinations = itertools.combinations(numbers, 6) # 6개씩 조합
# itertools.combinations는 제너레이터 형태로 모든 조합을 생성
# combinations 객체는 메모리를 절약하기 위해 실제 조합을 한 번에 모두 생성하지 않고 필요할 때마다 생성
# .combinations(리스트, 조합 개수) -> 조합 생성
count = sum(1 for _ in combinations) # 조합 개수 세기
# _는 반복 변수로 사용하지 않을 때 관례적으로 사용
print(f"로또 조합 경우의 수 : {count:,}") # 천 단위 구분자 추가 

# [문제 4] json 모듈을 사용해서 아래를 수행하세요.
# 1) students 리스트를 "students.json" 파일로 저장
# 2) 저장한 파일을 다시 읽어서 점수 평균을 출력
# 3) 파일 삭제
students = [
    {"name": "철수", "score": 85},
    {"name": "영희", "score": 92},
    {"name": "민준", "score": 78},
]
# 코드 작성 ↓
import json

# 1) students 리스트를 "students.json" 파일로 저장
with open("students.json", "w", encoding="utf-8") as f:
    json.dump(students, f, ensure_ascii=False, indent=2) # dump() 함수로 파일에 저장

# 2) 저장한 파일을 다시 읽어서 점수 평균을 출력
with open("students.json", "r", encoding="utf-8") as f:
    loaded_students = json.load(f) # load() 함수로 파일에서 읽기
    total_score = sum(student["score"] for student in loaded_students) # 점수 합계 계산
    # "score" 키의 값을 모두 더하기(딕셔너리에서 "score" 키의 값 추출하여 합산)
    average_score = total_score / len(loaded_students) # 평균 계산
    print(f"학생 점수 평균 : {average_score:.2f}") # 소수점 둘째 자리까지 출력

# 3) 파일 삭제
import os
os.remove("students.json") # 파일 삭제
