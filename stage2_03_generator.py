# ============================================================
# Stage 2 - 03. 제너레이터 (Generator)
# ============================================================


# ============================================================
# [이론 1] 제너레이터란?
# ============================================================
#
# 제너레이터는 값을 한 번에 모두 만들지 않고, 요청할 때마다 하나씩 만들어 반환한다.
# 이미 stage2_02에서 제너레이터 표현식 (x for x in range(n)) 을 짧게 다뤘는데,
# 이번 챕터에서는 yield 키워드로 만드는 제너레이터 함수를 중점으로 학습한다.
#
# 일반 함수 vs 제너레이터 함수:
#
#   def normal():           def gen():
#       return [1, 2, 3]        yield 1
#                               yield 2
#                               yield 3
#
#   normal() 호출 → 리스트 [1,2,3] 즉시 생성 후 반환
#   gen()    호출 → 제너레이터 객체 반환 (아직 아무것도 계산 안 함)
#
# 핵심 특성:
#   - Lazy evaluation: 값이 필요한 시점에 그때그때 계산
#   - 메모리 효율: 전체 결과를 저장하지 않음
#   - 한 방향 순회: 한 번 소진되면 다시 순회 불가


# ============================================================
# [이론 2] yield 키워드
# ============================================================
#
# yield 는 함수 실행을 "일시 정지"하고 값을 반환한다.
# next()가 호출되면 yield 직후부터 다음 yield 까지 실행이 재개된다.
#
# 동작 흐름:
#   1. gen() 호출 → 제너레이터 객체 생성 (함수 본문은 실행 안 됨)
#   2. next(g) 호출 → 첫 번째 yield 까지 실행, 값 반환 후 정지
#   3. next(g) 호출 → 두 번째 yield 까지 실행, 값 반환 후 정지
#   4. 더 이상 yield 없으면 → StopIteration 예외 발생

def count_up(n):
    print("시작")
    for i in range(1, n + 1):
        print(f"  yield 전: {i}")
        yield i
        print(f"  yield 후: {i}")
    print("종료")

g = count_up(3)
print(next(g))   # 시작 → yield 전: 1 → 1 출력 → 정지
print(next(g))   # yield 후: 1 → yield 전: 2 → 2 출력 → 정지
print(next(g))   # yield 후: 2 → yield 전: 3 → 3 출력 → 정지
# next(g)      # StopIteration 발생


# ============================================================
# [이론 3] for 루프로 제너레이터 소비하기
# ============================================================
#
# for 루프는 내부적으로 next()를 호출하고 StopIteration이 발생하면 멈춘다.
# 그래서 제너레이터를 for 루프에 그냥 사용할 수 있다.

def squares(n):
    for i in range(1, n + 1):
        yield i ** 2

for val in squares(5):
    print(val, end=" ")     # 1 4 9 16 25
print()

# list(), sum(), max() 등도 내부적으로 for 루프를 사용 → 제너레이터에 바로 사용 가능
print(list(squares(5)))     # [1, 4, 9, 16, 25]
print(sum(squares(5)))      # 55
print(max(squares(5)))      # 25


# ============================================================
# [이론 4] 무한 제너레이터
# ============================================================
#
# 일반 리스트로는 "무한히 긴" 시퀀스를 만들 수 없다.
# 제너레이터는 while True 로 무한히 값을 생성할 수 있고,
# 필요한 만큼만 꺼내서 쓰면 된다.

def infinite_counter(start=0, step=1):
    n = start
    while True:
        yield n
        n += step

counter = infinite_counter(start=10, step=5)
print(next(counter))   # 10
print(next(counter))   # 15
print(next(counter))   # 20

# 처음 5개만 꺼내기
import itertools # itertools.islice() → 이터러블에서 원하는 개수만큼 슬라이스해서 반환
first_five = list(itertools.islice(infinite_counter(), 5))
print(first_five)      # [0, 1, 2, 3, 4]


# ============================================================
# [이론 5] 제너레이터 표현식 vs 리스트 컴프리헨션
# ============================================================
#
# 리스트 컴프리헨션: [ ] → 즉시 모든 값 생성, 메모리에 저장
# 제너레이터 표현식: ( ) → 제너레이터 객체 반환, 값은 나중에 계산
#
# 결과를 반복 한 번만 쓰고 저장이 필요 없다면 → 제너레이터 표현식이 유리

import sys # sys 모듈의 getsizeof() 함수로 객체의 메모리 크기 확인

list_comp = [x ** 2 for x in range(100_000)]
gen_expr  = (x ** 2 for x in range(100_000))

print(sys.getsizeof(list_comp))   # 약 800,984 bytes (대용량)
print(sys.getsizeof(gen_expr))    # 208 bytes (고정 크기)

# 합계만 필요하면 리스트 저장 없이 바로 계산
total = sum(x ** 2 for x in range(100_000))
print(total)    # 333328333350000


# ============================================================
# [이론 6] yield from — 중첩 제너레이터 위임
# ============================================================
#
# yield from 이터러블 을 쓰면 다른 이터러블(또는 제너레이터)의 값을
# 하나씩 자동으로 yield 해준다.
# 중첩 반복문 대신 코드를 간결하게 만들 때 유용하다.

def flatten(nested):
    for sublist in nested:
        yield from sublist          # for x in sublist: yield x 와 동일

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(list(flatten(matrix)))        # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 제너레이터를 yield from 으로 연결하기
def first_n(gen, n):
    yield from itertools.islice(gen, n) # itertools.islice()로 gen에서 n개만 슬라이스해서 yield

print(list(first_n(squares(100), 5)))   # [1, 4, 9, 16, 25]


# ============================================================
# [이론 7] 실전 활용 패턴
# ============================================================
#
# 1) 대용량 파일을 한 줄씩 읽기
#    → 파일 전체를 메모리에 올리지 않고 처리 가능

def read_lines(filepath):
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

# for line in read_lines("big_file.txt"):
#     process(line)   # 한 줄씩 처리

# 2) 파이프라인 패턴: 제너레이터를 연결해서 데이터를 단계별로 처리

def read_numbers(lst):
    yield from lst

def filter_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n

def multiply(numbers, factor):
    for n in numbers:
        yield n * factor

data = range(1, 11)
pipeline = multiply(filter_even(read_numbers(data)), 3)
print(list(pipeline))   # [6, 12, 18, 24, 30]


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] yield를 사용해서 피보나치 수열 제너레이터를 만드세요.
# fib(n) → n개의 피보나치 수를 순서대로 yield
# fib(7) → 0, 1, 1, 2, 3, 5, 8
# 코드 작성 ↓
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b




# [문제 2] 아래 함수를 제너레이터로 구현하세요.
# chunked(lst, size) → 리스트를 size 크기로 잘라서 하나씩 yield
# chunked([1,2,3,4,5,6,7], 3) → [1,2,3], [4,5,6], [7]
# 코드 작성 ↓
def chunked(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]




# [문제 3] 아래 조건의 제너레이터를 만드세요.
# running_average(numbers) → 숫자를 하나씩 받아서 누적 평균을 yield
# 입력: [10, 20, 30, 40]
# 출력: 10.0, 15.0, 20.0, 25.0
# 코드 작성 ↓
def running_average(numbers):
    total = 0
    count = 0
    for n in numbers:
        total += n
        count += 1
        yield total / count

