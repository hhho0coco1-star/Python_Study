# ============================================================
# Stage 5 - 03. 성능 최적화 (Performance Optimization)
# ============================================================


# ============================================================
# [이론 1] 성능 측정 먼저 — "측정 없이 최적화하지 마라"
# ============================================================
#
# 성능 최적화 순서:
#   1. 프로파일링으로 병목(bottleneck) 찾기
#   2. 병목만 최적화
#   3. 다시 측정해서 개선 확인
#
# 흔한 실수: 성능과 무관한 부분을 최적화해 코드만 복잡해짐.
#
# 도구:
#   timeit   : 짧은 코드 조각의 실행 시간 측정
#   cProfile : 함수별 호출 횟수 + 소요 시간 분석
#   line_profiler (pip 설치) : 줄 단위 분석

import timeit
import cProfile
import pstats
import io
import time
import functools
import sys


# ============================================================
# [이론 2] timeit — 코드 조각 속도 비교
# ============================================================
#
# timeit.timeit(stmt, number=반복횟수) : 실행 시간(초) 반환
# timeit.repeat(stmt, number=n, repeat=r) : r번 반복 측정 → 최솟값 사용 권장
#
# 주의: 단일 측정은 신뢰도 낮음. repeat 후 min() 사용.

print("=" * 55)
print("[이론 2] timeit — 문자열 연결 방법 비교")
print("=" * 55)

N = 1000

# 방법 1: + 연산자 (매번 새 문자열 생성 → O(n²))
def concat_plus(n):
    result = ""
    for i in range(n):
        result += str(i)
    return result

# 방법 2: join (한 번에 연결 → O(n))
def concat_join(n):
    return "".join(str(i) for i in range(n))

# 방법 3: list 누적 후 join
def concat_list(n):
    parts = []
    for i in range(n):
        parts.append(str(i))
    return "".join(parts)

t_plus = timeit.timeit(lambda: concat_plus(N), number=500)
t_join = timeit.timeit(lambda: concat_join(N), number=500)
t_list = timeit.timeit(lambda: concat_list(N), number=500)

print(f"  + 연산자 : {t_plus:.4f}초")
print(f"  join    : {t_join:.4f}초")
print(f"  list+join: {t_list:.4f}초")
print()


# ============================================================
# [이론 3] cProfile — 함수 단위 프로파일링
# ============================================================
#
# cProfile.run('코드') 또는 cProfile.Profile() 컨텍스트로 사용.
# pstats.Stats 로 결과를 정렬/필터링.
#
# 출력 열 의미:
#   ncalls   : 호출 횟수
#   tottime  : 함수 자체 소요 시간 (자식 함수 제외)
#   cumtime  : 누적 소요 시간 (자식 함수 포함)
#   percall  : 호출당 평균 시간

def slow_function():
    total = 0
    for i in range(100_000):
        total += i ** 2
    return total

def fast_function():
    n = 100_000 - 1
    return n * (n + 1) * (2 * n + 1) // 6   # 수학 공식

def profiling_target():
    slow_function()
    fast_function()
    slow_function()

print("=" * 55)
print("[이론 3] cProfile 프로파일링")
print("=" * 55)

profiler = cProfile.Profile()
profiler.enable()
profiling_target()
profiler.disable()

stream = io.StringIO()
stats = pstats.Stats(profiler, stream=stream)
stats.sort_stats("cumulative")
stats.print_stats(8)
output = stream.getvalue()
for line in output.split("\n")[:15]:
    print(" ", line)
print()


# ============================================================
# [이론 4] functools.lru_cache — 메모이제이션
# ============================================================
#
# lru_cache: 함수 호출 결과를 캐싱. 같은 인자로 재호출 시 즉시 반환.
# LRU = Least Recently Used → 가장 오래 미사용 항목부터 캐시에서 제거.
#
# maxsize=None : 크기 제한 없는 캐시 (functools.cache 와 동일)
# maxsize=128  : 최대 128개 항목 캐싱 (기본값)
#
# 적합한 경우:
#   - 순수 함수 (같은 입력 → 항상 같은 출력)
#   - 재귀 알고리즘 (피보나치, 동적 프로그래밍)
#   - 비싼 연산 (DB 조회, 파일 파싱)

print("=" * 55)
print("[이론 4] functools.lru_cache 메모이제이션")
print("=" * 55)

# 캐시 없는 피보나치 — O(2^n)
def fib_no_cache(n: int) -> int:
    if n <= 1:
        return n
    return fib_no_cache(n - 1) + fib_no_cache(n - 2)

# 캐시 있는 피보나치 — O(n)
@functools.lru_cache(maxsize=None)
def fib_cached(n: int) -> int:
    if n <= 1:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

N_FIB = 30

start = time.perf_counter()
result1 = fib_no_cache(N_FIB)
t1 = time.perf_counter() - start

start = time.perf_counter()
result2 = fib_cached(N_FIB)
t2 = time.perf_counter() - start

print(f"  fib({N_FIB}) 결과: {result1}")
print(f"  캐시 없음: {t1:.6f}초")
print(f"  캐시 있음: {t2:.6f}초")
print(f"  캐시 정보: {fib_cached.cache_info()}")
print()

# 두 번째 호출은 즉시 반환
start = time.perf_counter()
_ = fib_cached(N_FIB)
t3 = time.perf_counter() - start
print(f"  두 번째 호출(캐시 히트): {t3:.8f}초")
print()


# ============================================================
# [이론 5] 제너레이터로 메모리 효율화
# ============================================================
#
# 큰 데이터를 처리할 때 리스트 대신 제너레이터를 사용하면
# 전체 데이터를 메모리에 올리지 않고 하나씩 처리 가능.

print("=" * 55)
print("[이론 5] 제너레이터 vs 리스트 메모리 비교")
print("=" * 55)

import sys

N_ITEMS = 100_000

list_data = [i ** 2 for i in range(N_ITEMS)]
gen_data = (i ** 2 for i in range(N_ITEMS))

list_size = sys.getsizeof(list_data)
gen_size = sys.getsizeof(gen_data)

print(f"  리스트 크기: {list_size:,} bytes ({list_size // 1024} KB)")
print(f"  제너레이터 크기: {gen_size} bytes")
print(f"  메모리 절약: 약 {list_size // gen_size}배")
print()

# 파일 처리 예시 (제너레이터가 특히 유용)
def read_large_file_lazy(filepath: str):
    """대용량 파일을 한 줄씩 읽는 제너레이터"""
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# 사용:
# for line in read_large_file_lazy("huge.csv"):
#     process(line)   # 메모리에 한 줄만 올라와 있음


# ============================================================
# [이론 6] 리스트 컴프리헨션 vs 루프
# ============================================================
#
# 리스트 컴프리헨션은 C로 구현된 내부 최적화로 일반 for 루프보다 빠름.
# 단, 가독성을 해칠 정도로 복잡하면 루프가 낫다.

print("=" * 55)
print("[이론 6] 컴프리헨션 vs for 루프")
print("=" * 55)

N_LOOP = 50_000

def squares_loop(n):
    result = []
    for i in range(n):
        if i % 2 == 0:
            result.append(i ** 2)
    return result

def squares_comprehension(n):
    return [i ** 2 for i in range(n) if i % 2 == 0]

t_loop = timeit.timeit(lambda: squares_loop(N_LOOP), number=100)
t_comp = timeit.timeit(lambda: squares_comprehension(N_LOOP), number=100)

print(f"  for 루프        : {t_loop:.4f}초")
print(f"  컴프리헨션      : {t_comp:.4f}초")
print(f"  컴프리헨션이 {t_loop / t_comp:.1f}배 빠름")
print()


# ============================================================
# [이론 7] 딕셔너리 lookup vs 선형 탐색
# ============================================================
#
# 딕셔너리는 해시 테이블 → 조회 O(1).
# 리스트는 선형 탐색 → 조회 O(n).
# 자주 조회하는 데이터는 딕셔너리/셋으로 변환하면 성능 향상.

print("=" * 55)
print("[이론 7] dict lookup vs list lookup")
print("=" * 55)

SIZE = 10_000
data_list = list(range(SIZE))
data_dict = {i: True for i in range(SIZE)}
data_set = set(range(SIZE))

target = SIZE - 1   # 최악의 경우 (맨 마지막)

t_list = timeit.timeit(lambda: target in data_list, number=100_000)
t_dict = timeit.timeit(lambda: target in data_dict, number=100_000)
t_set = timeit.timeit(lambda: target in data_set, number=100_000)

print(f"  list 탐색 : {t_list:.4f}초")
print(f"  dict 탐색 : {t_dict:.4f}초")
print(f"  set 탐색  : {t_set:.4f}초")
print()


# ============================================================
# [이론 8] 슬롯(__slots__) — 객체 메모리 최적화
# ============================================================
#
# 기본 파이썬 클래스는 인스턴스 딕셔너리(__dict__)를 가짐.
# __slots__ 를 정의하면 딕셔너리 대신 고정 배열 사용 → 메모리 감소.
# 수백만 개의 객체를 만드는 경우에 유효.

class PointNormal:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class PointSlots:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

normal_obj = PointNormal(1.0, 2.0)
slots_obj = PointSlots(1.0, 2.0)

print("=" * 55)
print("[이론 8] __slots__ 메모리 비교")
print("=" * 55)
print(f"  일반 객체: {sys.getsizeof(normal_obj)} bytes + __dict__ {sys.getsizeof(normal_obj.__dict__)} bytes")
print(f"  __slots__ 객체: {sys.getsizeof(slots_obj)} bytes (딕셔너리 없음)")
print()


# ============================================================
# [실습 문제]
# ============================================================
#
# 문제 1: 아래 두 함수의 실행 시간을 timeit으로 비교하시오.
#         n=10,000 에 대해 각각 number=1000 반복.
#
#   def sum_loop(n):
#       total = 0
#       for i in range(n): total += i
#       return total
#
#   def sum_formula(n):
#       return n * (n - 1) // 2
#
# 문제 2: 아래 함수를 lru_cache로 최적화하고, 전후 성능을 비교하시오.
#
#   def is_prime(n: int) -> bool:
#       if n < 2: return False
#       for i in range(2, int(n**0.5) + 1):
#           if n % i == 0: return False
#       return True
#
# 문제 3: 1~1,000,000 의 짝수 제곱수 합을 구할 때
#         리스트 컴프리헨션 방식과 제너레이터 방식의
#         메모리 크기(sys.getsizeof)를 비교하시오.


# --- 정답 ---

# 문제 1
def sum_loop(n):
    total = 0
    for i in range(n):
        total += i
    return total

def sum_formula(n):
    return n * (n - 1) // 2

print("=" * 55)
print("[실습] 정답")
print("=" * 55)

n = 10_000
t1 = timeit.timeit(lambda: sum_loop(n), number=1000)
t2 = timeit.timeit(lambda: sum_formula(n), number=1000)
print(f"문제 1 — loop: {t1:.4f}초, formula: {t2:.6f}초, 차이: {t1/t2:.0f}배")

# 문제 2
def is_prime_no_cache(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

@functools.lru_cache(maxsize=None)
def is_prime_cached(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

primes_no = [i for i in range(2, 500) if is_prime_no_cache(i)]
is_prime_cached.cache_clear()

t_nc = timeit.timeit(lambda: [i for i in range(2, 500) if is_prime_no_cache(i)], number=200)
t_c = timeit.timeit(lambda: [i for i in range(2, 500) if is_prime_cached(i)], number=200)
print(f"문제 2 — 캐시 없음: {t_nc:.4f}초, 캐시 있음: {t_c:.4f}초")

# 문제 3
M = 1_000_000
list_version = [i ** 2 for i in range(1, M + 1) if i % 2 == 0]
gen_version = (i ** 2 for i in range(1, M + 1) if i % 2 == 0)
print(f"문제 3 — 리스트: {sys.getsizeof(list_version):,} bytes, 제너레이터: {sys.getsizeof(gen_version)} bytes")
print()


# ============================================================
# [퀴즈]
# ============================================================
#
# Q1. lru_cache 가 적합하지 않은 함수의 특징은?
#     → 같은 입력에 다른 출력(랜덤, 현재 시간, 외부 상태 변경)을 반환하는 함수
#
# Q2. 제너레이터가 리스트보다 메모리 효율적인 이유는?
#     → 전체 결과를 메모리에 저장하지 않고 값을 하나씩 생성(lazy evaluation)
#
# Q3. cProfile에서 tottime과 cumtime의 차이는?
#     → tottime: 해당 함수 자체 실행 시간 (자식 함수 제외)
#       cumtime: 자식 함수 포함 누적 실행 시간
#
# Q4. 딕셔너리/셋 조회가 O(1)인 이유는?
#     → 해시 함수로 키의 저장 위치를 직접 계산하기 때문
