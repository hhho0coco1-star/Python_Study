# ============================================================
# Stage 2 - 04. 데코레이터 (Decorator)
# ============================================================


# ============================================================
# [이론 1] 데코레이터란?
# ============================================================
#
# 데코레이터는 기존 함수를 수정하지 않고 기능을 추가하는 방법이다.
# "함수를 인자로 받아 새로운 함수를 반환하는 함수"다.
#
# 언제 쓰나?
#   - 여러 함수에 공통 기능(로깅, 실행시간 측정, 인증 체크)을 붙일 때
#   - 원본 함수 코드를 건드리지 않고 동작을 추가하고 싶을 때
#
# @ 문법은 아래와 완전히 동일하다:
#
#   @my_decorator
#   def func(): ...
#
#   ↕ 동일
#
#   def func(): ...
#   func = my_decorator(func)


# ============================================================
# [이론 2] 데코레이터 기본 구조
# ============================================================
#
# 데코레이터를 만들려면 3가지가 필요하다:
#   1. 외부 함수: 원본 함수(func)를 인자로 받는다
#   2. 내부 함수(wrapper): 기능을 추가한 새 함수
#   3. return wrapper: 내부 함수를 반환

def my_decorator(func):
    def wrapper():
        print("함수 실행 전")
        func()
        print("함수 실행 후")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# 함수 실행 전
# Hello!
# 함수 실행 후


# ============================================================
# [이론 3] 인자가 있는 함수에 데코레이터 적용
# ============================================================
#
# wrapper가 원본 함수의 인자를 그대로 전달하려면
# *args, **kwargs 를 사용한다.
# 이렇게 하면 어떤 함수에도 데코레이터를 붙일 수 있다.

def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} 호출 — args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} 반환값: {result}")
        return result
    return wrapper

@log_call
def add(a, b):
    return a + b

@log_call
def greet(name, greeting="안녕"):
    return f"{greeting}, {name}!"

add(3, 5)
# [LOG] add 호출 — args=(3, 5), kwargs={}
# [LOG] add 반환값: 8

greet("철수", greeting="반가워")
# [LOG] greet 호출 — args=('철수',), kwargs={'greeting': '반가워'}
# [LOG] greet 반환값: 반가워, 철수!


# ============================================================
# [이론 4] functools.wraps — 함수 메타정보 보존
# ============================================================
#
# 데코레이터를 적용하면 함수 이름(__name__)과 문서(__doc__)가
# wrapper 로 덮어써진다.
# functools.wraps(func) 를 wrapper 에 붙이면 원본 정보가 보존된다.
# 실무에서는 거의 항상 @wraps 를 붙인다.

from functools import wraps

def log_call2(func):
    @wraps(func)        # 원본 함수의 __name__, __doc__ 등을 wrapper에 복사
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} 호출")
        return func(*args, **kwargs)
    return wrapper

@log_call2
def multiply(a, b):
    """두 수를 곱한다."""
    return a * b

print(multiply.__name__)   # multiply  (wraps 없으면 'wrapper' 출력됨)
print(multiply.__doc__)    # 두 수를 곱한다.


# ============================================================
# [이론 5] 실전 데코레이터 예시
# ============================================================

import time

# 5-1. 실행 시간 측정
def timer(func):
    @wraps(func) # @wraps(func) 적용하여 func의 메타정보 유지
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"[TIMER] {func.__name__}: {end - start:.4f}초")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(1_000_000)   # [TIMER] slow_sum: 0.0XXX초


# 5-2. 재시도 (retry)
def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] {attempt}/{times} 실패: {e}")
            print("[RETRY] 모든 시도 실패")
            return None
        return wrapper
    return decorator

import random

@retry(times=3)
def unstable_api():
    if random.random() < 0.7:   # 70% 확률로 실패
        raise ConnectionError("서버 연결 실패")
    return "성공"

result = unstable_api()
print(result)


# ============================================================
# [이론 6] 인자를 받는 데코레이터 (데코레이터 팩토리)
# ============================================================
#
# @retry(times=3) 처럼 데코레이터 자체에 인자를 전달하려면
# 함수를 한 겹 더 감싸야 한다.
#
# 구조: 인자받는함수(인자) → decorator(func) → wrapper(*args, **kwargs)
#
# 위의 retry 데코레이터가 이 패턴의 예시다.
# 정리하면:
#   @decorator          → decorator(func) 호출
#   @decorator(arg)     → decorator(arg) 가 먼저 호출 → 반환된 decorator(func) 호출

def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(msg):
    print(msg)

say("반복!")
# 반복!
# 반복!
# 반복!


# ============================================================
# [이론 7] 클래스 기반 데코레이터
# ============================================================
#
# __call__ 메서드를 구현하면 클래스 인스턴스를 함수처럼 호출할 수 있다.
# 상태(호출 횟수 등)를 저장해야 할 때 클래스 데코레이터가 편리하다.

class CallCounter:
    def __init__(self, func):
        wraps(func)(self)       # __name__, __doc__ 복사
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[COUNT] {self.func.__name__} 호출 횟수: {self.count}")
        return self.func(*args, **kwargs)

@CallCounter
def hello():
    print("Hello!")

hello()   # [COUNT] hello 호출 횟수: 1 / Hello!
hello()   # [COUNT] hello 호출 횟수: 2 / Hello!
hello()   # [COUNT] hello 호출 횟수: 3 / Hello!
print(hello.count)   # 3


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] 함수 실행 전후에 구분선을 출력하는 데코레이터 divider를 만드세요.
# 실행 전: "========== 함수명 시작 =========="
# 실행 후: "========== 함수명 종료 =========="
# functools.wraps 적용 필수
# 코드 작성 ↓
def divider(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"========== {func.__name__} 시작 ==========")
        result = func(*args, **kwargs)
        print(f"========== {func.__name__} 종료 ==========")
        return result
    return wrapper

@divider
def test():
    print("테스트 함수 실행")

# [문제 2] 함수의 반환값이 None이면 기본값을 대신 반환하는
# 데코레이터 default_value(value)를 만드세요.
# 예: @default_value(0) 적용 시 None 반환 함수 → 0 반환
# 코드 작성 ↓
def default_value(value):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result if result is not None else value
        return wrapper
    return decorator

@default_value(0)
def maybe_none(flag):
    if flag:
        return "값 있음"
    else:
        return None


# [문제 3] 함수 호출 결과를 캐싱하는 데코레이터 simple_cache를 만드세요.
# 같은 인자로 다시 호출하면 함수를 실행하지 않고 저장된 결과를 반환한다.
# (힌트: wrapper 안에서 딕셔너리로 {args: result} 저장)
# 코드 작성 ↓
class simple_cache:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = (args, frozenset(kwargs.items())) # frozenset으로 kwargs를 해시 가능한 형태로 변환
        if key in self.cache:
            print(f"[CACHE] {self.func.__name__} 캐시된 결과 반환")
            return self.cache[key]
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        return result
