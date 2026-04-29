# ============================================================
# Stage 2 - 06. 표준 라이브러리 심화 (Standard Library)
# ============================================================
# stage2_05에서 다룬 모듈: os, sys, datetime, random, collections, itertools, json
# 이번 챕터: pathlib, re, functools, logging, contextlib


# ============================================================
# [이론 1] pathlib — 현대적인 파일 경로 처리
# ============================================================
#
# os.path 대신 Path 객체를 사용하는 방식 (Python 3.4+)
# 문자열이 아닌 객체로 경로를 다루기 때문에 코드가 더 직관적
#
#   Path("폴더") / "파일.txt"   → 경로 연결 (OS 구분자 자동 처리)
#   p.exists()                  → 존재 여부
#   p.is_file() / p.is_dir()    → 파일/디렉토리 여부
#   p.name                      → 파일명 (확장자 포함)
#   p.stem                      → 파일명 (확장자 제외)
#   p.suffix                    → 확장자 (.py, .txt 등)
#   p.parent                    → 부모 디렉토리
#   p.glob("*.py")              → 패턴 매칭으로 파일 목록

from pathlib import Path

cwd = Path.cwd()               # 현재 작업 디렉토리
print(cwd)
print(cwd.name)                # 디렉토리 이름
print(cwd.parent)              # 상위 디렉토리

# 경로 연결 — / 연산자 사용 가능
p = cwd / "stage2_06_stdlib.py"
print(p)
print(p.exists())              # True (자기 자신)
print(p.is_file())             # True
print(p.name)                  # stage2_06_stdlib.py
print(p.stem)                  # stage2_06_stdlib
print(p.suffix)                # .py
print(p.parent)                # 부모 디렉토리

# 현재 디렉토리의 .py 파일 목록
py_files = sorted(cwd.glob("*.py"))
for f in py_files:
    print(f.name)

# 파일 쓰기/읽기 (open() 없이도 가능)
temp = cwd / "temp_test.txt"
temp.write_text("pathlib 테스트\n두 번째 줄", encoding="utf-8")
content = temp.read_text(encoding="utf-8")
print(content)
temp.unlink()    # 파일 삭제


# ============================================================
# [이론 2] re — 정규 표현식 (Regular Expression)
# ============================================================
#
# 문자열에서 패턴을 찾거나 바꿀 때 사용
#
# 주요 함수:
#   re.match(pattern, string)    → 문자열 시작 부분이 패턴과 일치하면 매치 객체 반환
#   re.search(pattern, string)   → 문자열 전체에서 첫 번째 일치 반환
#   re.findall(pattern, string)  → 일치하는 모든 것을 리스트로 반환
#   re.sub(pattern, repl, str)   → 일치하는 부분을 repl로 치환
#   re.compile(pattern)          → 패턴 미리 컴파일 (반복 사용 시 성능 향상)
#
# 자주 쓰는 패턴:
#   \d     숫자 (0-9)
#   \w     단어 문자 (a-z, A-Z, 0-9, _)
#   \s     공백 문자 (스페이스, 탭, 줄바꿈)
#   .      임의의 문자 1개 (줄바꿈 제외)
#   *      0회 이상 반복
#   +      1회 이상 반복
#   ?      0 또는 1회
#   {n}    정확히 n회
#   {n,m}  n~m회
#   ^      문자열 시작
#   $      문자열 끝
#   []     문자 클래스 (예: [a-z], [0-9])
#   ()     그룹

import re

text = "전화번호: 010-1234-5678, 이메일: user@example.com, 홈페이지: www.python.org"

# findall: 모든 숫자 추출
numbers = re.findall(r'\d+', text)
print(numbers)    # ['010', '1234', '5678']

# search: 이메일 주소 찾기
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' # %는 문자 클래스 안에서 리터럴로 사용  
match = re.search(email_pattern, text)
if match: 
    print(match.group())    # user@example.com
    # group()은 매치된 전체 문자열 반환

# findall로 전화번호 패턴 추출
phone_pattern = r'\d{3}-\d{4}-\d{4}'
phones = re.findall(phone_pattern, text) # findall은 패턴과 일치하는 모든 부분을 "리스트"로 반환
print(phones)    # ['010-1234-5678']

# sub: 전화번호 마스킹
masked = re.sub(r'\d{4}-\d{4}', '****-****', text)
print(masked)    # 010-****-**** ...

# compile: 패턴을 미리 컴파일해서 재사용
pattern = re.compile(r'\d+')
print(pattern.findall("사과 3개, 바나나 12개, 포도 100송이"))
# ['3', '12', '100']

# 그룹 활용
date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
m = re.search(date_pattern, "오늘 날짜: 2026-04-27")
if m:
    print(m.group(0))   # 2026-04-27 (전체 매치)
    print(m.group(1))   # 2026 (첫 번째 그룹)
    print(m.group(2))   # 04
    print(m.group(3))   # 27


# ============================================================
# [이론 3] functools — 함수형 도구 모음
# ============================================================
#
# lru_cache: 함수 결과를 캐싱해서 같은 인자로 호출 시 재계산 없이 반환
#            (Least Recently Used — 최근 사용이 적은 캐시 항목부터 제거)
#
# partial: 함수의 일부 인자를 미리 고정한 새 함수 생성
#
# reduce: 리스트의 요소를 누적 연산으로 하나의 값으로 합침

from functools import lru_cache, partial, reduce
import time

# lru_cache 없이 — 매번 재귀 계산
def fib_slow(n):
    if n <= 1:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)

# lru_cache 적용 — 한 번 계산한 값은 캐시에서 꺼냄
# 결과만 보고 값을 반환하기 때문에 maxsize=None으로 무제한 캐시
@lru_cache(maxsize=None)
def fib_fast(n):
    if n <= 1:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)

start = time.time()
print(fib_slow(35))
print(f"캐시 없음: {time.time() - start:.4f}초")

start = time.time()
print(fib_fast(35))
print(f"캐시 있음: {time.time() - start:.4f}초")

# partial: 인자 일부를 미리 고정
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)     # exp=2 고정
cube   = partial(power, exp=3)     # exp=3 고정
print(square(5))    # 25
print(cube(3))      # 27

# reduce: 리스트 → 단일 값
total = reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5])
print(total)    # 15

product = reduce(lambda acc, x: acc * x, [1, 2, 3, 4, 5])
print(product)  # 120


# ============================================================
# [이론 4] logging — 로깅
# ============================================================
#
# print() 대신 logging을 써야 하는 이유:
#   - 레벨별로 메시지를 분류 가능 (DEBUG < INFO < WARNING < ERROR < CRITICAL)
#   - 파일 저장, 형식 지정, 출력 켜기/끄기를 쉽게 제어
#   - 운영 환경에서 DEBUG 로그를 한 줄로 비활성화 가능
#
# 기본 레벨:
#   DEBUG    → 개발 중 세부 정보 (기본적으로 출력 안 됨)
#   INFO     → 정상 동작 확인
#   WARNING  → 예상치 못한 상황 (아직 오류는 아님)
#   ERROR    → 처리 중 오류 발생
#   CRITICAL → 프로그램 중단 수준의 심각한 오류

import logging

# basicConfig: 로거 기본 설정
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)   # 모듈 이름으로 로거 생성

logger.debug("디버그: 상세 정보")
logger.info("정보: 정상 처리됨")
logger.warning("경고: 주의 필요")
logger.error("오류: 처리 실패")
logger.critical("심각: 프로그램 중단 위험")

# 실전 예시: 점수 처리에 로깅 적용
def process_score(name, score):
    if score < 0 or score > 100:
        logger.error(f"{name}: 유효하지 않은 점수 {score}")
        return None
    if score < 60:
        logger.warning(f"{name}: 점수 미달 ({score}점)")
    else:
        logger.info(f"{name}: 통과 ({score}점)")
    return score

process_score("철수", 85)
process_score("영희", 45)
process_score("민준", 150)


# ============================================================
# [이론 5] contextlib — 커스텀 with 블록 만들기
# ============================================================
#
# with 구문은 __enter__ / __exit__ 매직 메서드로 동작함
# contextlib.contextmanager 데코레이터를 쓰면
# 클래스 없이 제너레이터 함수로 간단하게 컨텍스트 매니저를 만들 수 있음
#
#   yield 앞 코드 → __enter__ (with 블록 진입 시 실행)
#   yield 값      → as 뒤에 바인딩되는 값
#   yield 뒤 코드 → __exit__ (with 블록 종료 시 실행, 예외 여부 무관)

from contextlib import contextmanager
import time

@contextmanager
def timer(label):
    start = time.time()
    yield                                           # with 블록 실행
    elapsed = time.time() - start
    print(f"[{label}] 실행 시간: {elapsed:.4f}초")

with timer("리스트 생성"):
    result = [x ** 2 for x in range(100_000)]

# 파일 처리 + 예외 안전 보장
@contextmanager
def managed_file(path, mode="r", encoding="utf-8"):
    f = open(path, mode, encoding=encoding)
    try:
        yield f
    finally:
        f.close()
        print(f"{path} 파일 닫힘")

temp = Path.cwd() / "ctx_test.txt"
with managed_file(str(temp), "w") as f:
    f.write("contextlib 테스트")
with managed_file(str(temp)) as f:
    print(f.read())
temp.unlink()


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] pathlib를 사용해서 아래를 수행하세요.
# - 현재 디렉토리의 .py 파일 중 이름에 "stage2"가 포함된 파일 목록을 출력
# - 형식: "stage2 파일 목록: ['stage2_01_oop.py', ...]"
# 코드 작성 ↓
from pathlib import Path
cwd = Path.cwd() # 현재 작업 디렉토리
stage2_files = sorted(cwd.glob("*stage2*.py"))
print(f"stage2 파일 목록 : {[f.name for f in stage2_files]}") # 파일 이름만 리스트로 출력


# [문제 2] re를 사용해서 아래를 수행하세요.
# text에서 이메일 주소를 모두 추출하여 리스트로 출력하세요.
text = "문의: support@company.co.kr, 개인: hong.gildong@gmail.com, 오류형식: @noemail, not-email"
# 코드 작성 ↓
import re
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' # %는 문자 클래스 안에서 리터럴로 사용
emails = re.findall(email_pattern, text)
print(emails) 


# [문제 3] functools.lru_cache를 사용해서 아래를 수행하세요.
# - 재귀로 n번째 피보나치 수를 구하는 함수를 lru_cache로 최적화하세요.
# - fib(40)의 결과와 캐시 정보(cache_info())를 출력하세요.
# 코드 작성 ↓
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)
print(fib(40))
print(fib.cache_info())




# [문제 4] logging을 사용해서 아래를 수행하세요.
# - 아래 상품 리스트를 처리하면서 재고가 0인 경우 WARNING, 재고가 음수이면 ERROR를 남기세요.
# - 정상 재고는 INFO로 출력하세요.
products = [
    {"name": "사과", "stock": 50},
    {"name": "바나나", "stock": 0},
    {"name": "포도", "stock": -3},
    {"name": "딸기", "stock": 20},
]
# 코드 작성 ↓
import logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)
for product in products:
    name = product["name"]
    stock = product["stock"]
    if stock < 0:
        logger.error(f"{name}: 재고 음수 ({stock})")
    elif stock == 0:
        logger.warning(f"{name}: 재고 없음")
    else:
        logger.info(f"{name}: 재고 {stock}개")


