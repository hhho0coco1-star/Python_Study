# ============================================================
# Stage 5 - 01. 비동기 프로그래밍 (Async Programming)
# ============================================================


# ============================================================
# [이론 1] 동기 vs 비동기
# ============================================================
#
# 동기(Synchronous): 작업이 순서대로 실행. 앞 작업이 끝나야 다음 작업 시작.
# 비동기(Asynchronous): 기다리는 동안 다른 작업을 먼저 처리.
#
# 카페 비유:
#   동기  → 손님 A 커피 완성 → 손님 B 주문 받기 → 손님 B 커피 완성
#   비동기 → 손님 A 주문 받기 → 손님 B 주문 받기 → A 커피 완성 → B 커피 완성
#
# 언제 비동기가 유리한가?
#   - I/O 바운드 작업: 파일 읽기, 네트워크 요청, DB 쿼리
#   - "기다리는 시간"이 많은 작업
#   - CPU 연산이 많은 작업에는 multiprocessing이 더 적합
#
# Python 비동기 핵심 키워드:
#   - async def  : 비동기 함수(코루틴) 선언
#   - await      : 비동기 작업 완료까지 대기 (이벤트 루프에 제어권 넘김)
#   - asyncio    : 이벤트 루프 관리 표준 라이브러리

import asyncio
import time


# ============================================================
# [이론 2] async def 와 await 기초
# ============================================================
#
# async def 로 선언된 함수는 "코루틴(coroutine)" 객체를 반환한다.
# 일반 함수처럼 호출하면 실행되지 않고, await 또는 asyncio.run()이 필요.
#
# await 는 코루틴 내부에서만 사용 가능.
# await 를 만나면 현재 코루틴이 잠시 멈추고 이벤트 루프가 다른 작업 처리.

async def greet(name: str, delay: float) -> str:
    print(f"[{name}] 인사 시작")
    await asyncio.sleep(delay)   # 실제 코드에선 네트워크 요청, DB 쿼리 등
    print(f"[{name}] 인사 완료")
    return f"안녕하세요, {name}!"

async def main_basic():
    result = await greet("Alice", 1.0)
    print(result)

print("=" * 50)
print("[이론 2] async def / await 기초")
print("=" * 50)
asyncio.run(main_basic())
print()


# ============================================================
# [이론 3] 순차 실행 vs 동시 실행 (asyncio.gather)
# ============================================================
#
# await 를 하나씩 하면 순차 실행 (비동기의 장점 없음).
# asyncio.gather(*coros) 를 사용하면 여러 코루틴을 동시에 실행.
#
# gather는 모든 코루틴이 완료될 때까지 기다리고 결과를 리스트로 반환.

async def fetch_data(source: str, delay: float) -> str:
    print(f"  [{source}] 데이터 요청 시작")
    await asyncio.sleep(delay)
    print(f"  [{source}] 데이터 수신 완료")
    return f"{source}의 데이터"

async def main_sequential():
    print("--- 순차 실행 ---")
    start = time.perf_counter()
    r1 = await fetch_data("DB", 1.0)
    r2 = await fetch_data("API", 1.5)
    r3 = await fetch_data("파일", 0.5)
    elapsed = time.perf_counter() - start
    print(f"결과: {r1}, {r2}, {r3}")
    print(f"소요 시간: {elapsed:.2f}초 (순차: 1.0+1.5+0.5=3.0초 예상)")

async def main_concurrent():
    print("--- 동시 실행 (gather) ---")
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_data("DB", 1.0),
        fetch_data("API", 1.5),
        fetch_data("파일", 0.5),
    )
    elapsed = time.perf_counter() - start
    print(f"결과: {results}")
    print(f"소요 시간: {elapsed:.2f}초 (동시: max(1.0,1.5,0.5)≈1.5초 예상)")

print("=" * 50)
print("[이론 3] 순차 vs 동시 실행")
print("=" * 50)
asyncio.run(main_sequential())
print()
asyncio.run(main_concurrent())
print()


# ============================================================
# [이론 4] asyncio.create_task — 백그라운드 작업
# ============================================================
#
# create_task() 는 코루틴을 이벤트 루프에 즉시 등록하고 Task 객체를 반환.
# gather와 달리 등록 즉시 실행 시작 → 다른 코드와 더 세밀하게 병렬 제어 가능.
#
# 차이:
#   gather  : 여러 코루틴을 한꺼번에 넘기고 전부 완료 대기
#   create_task : 개별로 태스크 생성, 나중에 await 또는 gather로 수집

async def background_task(name: str, delay: float):
    await asyncio.sleep(delay)
    print(f"  [Task {name}] 완료")
    return name

async def main_tasks():
    print("태스크 생성 (즉시 이벤트 루프에 등록됨)")
    t1 = asyncio.create_task(background_task("A", 1.0))
    t2 = asyncio.create_task(background_task("B", 0.5))
    t3 = asyncio.create_task(background_task("C", 1.5))

    print("다른 작업 수행 중...")
    await asyncio.sleep(0.1)   # 잠깐 양보 → t1, t2, t3 실행 시작
    print("대기 중인 태스크 결과 수집")

    results = await asyncio.gather(t1, t2, t3)
    print(f"완료된 태스크: {results}")

print("=" * 50)
print("[이론 4] asyncio.create_task")
print("=" * 50)
asyncio.run(main_tasks())
print()


# ============================================================
# [이론 5] asyncio.timeout / wait_for — 타임아웃 처리
# ============================================================
#
# 네트워크 요청이 너무 오래 걸릴 때 강제 중단하는 패턴.
# asyncio.wait_for(coro, timeout=초) → 시간 초과 시 asyncio.TimeoutError 발생

async def slow_api_call(delay: float) -> str:
    await asyncio.sleep(delay)
    return "API 응답"

async def main_timeout():
    print("--- 타임아웃 없음 (성공) ---")
    try:
        result = await asyncio.wait_for(slow_api_call(0.5), timeout=2.0)
        print(f"성공: {result}")
    except asyncio.TimeoutError:
        print("타임아웃 발생!")

    print("--- 타임아웃 발생 ---")
    try:
        result = await asyncio.wait_for(slow_api_call(3.0), timeout=1.0)
        print(f"성공: {result}")
    except asyncio.TimeoutError:
        print("타임아웃! 1초 안에 응답 없음 → 요청 취소")

print("=" * 50)
print("[이론 5] asyncio.wait_for 타임아웃")
print("=" * 50)
asyncio.run(main_timeout())
print()


# ============================================================
# [이론 6] 비동기 제너레이터 & async for
# ============================================================
#
# async def 안에서 yield 를 사용하면 "비동기 제너레이터".
# async for 로 소비할 수 있다.

async def async_range(n: int, delay: float = 0.1):
    for i in range(n):
        await asyncio.sleep(delay)
        yield i

async def main_async_gen():
    print("비동기 스트림 수신:")
    async for value in async_range(5, 0.2):
        print(f"  수신: {value}")

print("=" * 50)
print("[이론 6] 비동기 제너레이터")
print("=" * 50)
asyncio.run(main_async_gen())
print()


# ============================================================
# [이론 7] aiohttp — 비동기 HTTP 요청
# ============================================================
#
# aiohttp 는 비동기 HTTP 클라이언트/서버 라이브러리.
# 설치: pip install aiohttp
#
# 기본 패턴:
#
#   import aiohttp
#
#   async def fetch(url: str) -> str:
#       async with aiohttp.ClientSession() as session:
#           async with session.get(url) as response:
#               return await response.text()
#
#   async def main():
#       urls = [
#           "https://httpbin.org/delay/1",
#           "https://httpbin.org/delay/1",
#           "https://httpbin.org/delay/1",
#       ]
#       results = await asyncio.gather(*[fetch(url) for url in urls])
#       print(f"{len(results)}개 요청 완료")
#
#   asyncio.run(main())
#
# 동기 requests 와 비교:
#   requests (동기): 3개 URL × 1초 = 3초
#   aiohttp  (비동기): 3개 동시 = ≈1초
#
# ClientSession 은 반드시 async with 로 사용 (연결 풀 정리 보장).

print("=" * 50)
print("[이론 7] aiohttp (설치 후 사용)")
print("  pip install aiohttp")
print("  async with aiohttp.ClientSession() as session:")
print("      async with session.get(url) as resp:")
print("          text = await resp.text()")
print("=" * 50)
print()


# ============================================================
# [이론 8] FastAPI에서의 비동기 — async def 라우트
# ============================================================
#
# FastAPI는 async def 라우트를 지원한다.
# DB 쿼리, 외부 API 호출이 있는 엔드포인트에 async def 사용하면 성능 향상.
#
#   # 동기 라우트 (blocking)
#   @app.get("/sync")
#   def sync_endpoint():
#       time.sleep(1)          # 이 동안 다른 요청 못 받음
#       return {"result": "ok"}
#
#   # 비동기 라우트 (non-blocking)
#   @app.get("/async")
#   async def async_endpoint():
#       await asyncio.sleep(1) # 이 동안 다른 요청 처리 가능
#       return {"result": "ok"}
#
# 주의: SQLAlchemy 기본 버전은 동기 → 비동기 ORM은 SQLAlchemy 1.4+ async 모드 또는 databases 라이브러리 사용.

print("=" * 50)
print("[이론 8] FastAPI async def 라우트")
print("  @app.get('/endpoint')")
print("  async def handler():")
print("      await some_async_operation()")
print("      return {'result': 'ok'}")
print("=" * 50)
print()


# ============================================================
# [실습 문제]
# ============================================================
#
# 문제 1: 아래 동기 함수를 비동기로 변환하시오.
#
#   import time
#   def download(url: str) -> str:
#       time.sleep(2)
#       return f"{url} 다운로드 완료"
#
#   def download_all():
#       urls = ["url1", "url2", "url3"]
#       return [download(u) for u in urls]
#
# 문제 2: asyncio.gather 로 3개의 작업을 동시에 실행하고,
#         각 작업의 소요 시간을 출력하는 코루틴을 작성하시오.
#         각 작업은 0.5, 1.0, 1.5 초 대기 후 완료.
#
# 문제 3: asyncio.wait_for 를 사용해 2초 안에 응답 없으면
#         "타임아웃"을 출력하는 코드를 작성하시오.


# --- 정답 ---

# 문제 1
async def download_async(url: str) -> str:
    await asyncio.sleep(0.3)   # 실제 네트워크 대기 시뮬레이션
    return f"{url} 다운로드 완료"

async def download_all_async():
    urls = ["url1", "url2", "url3"]
    results = await asyncio.gather(*[download_async(u) for u in urls])
    return results

# 문제 2
async def timed_task(name: str, delay: float):
    start = time.perf_counter()
    await asyncio.sleep(delay)
    elapsed = time.perf_counter() - start
    return f"{name}: {elapsed:.2f}초"

async def run_timed():
    results = await asyncio.gather(
        timed_task("작업A", 0.5),
        timed_task("작업B", 1.0),
        timed_task("작업C", 1.5),
    )
    for r in results:
        print(" ", r)

# 문제 3
async def slow_job():
    await asyncio.sleep(3.0)
    return "완료"

async def run_with_timeout():
    try:
        result = await asyncio.wait_for(slow_job(), timeout=2.0)
        print("결과:", result)
    except asyncio.TimeoutError:
        print("타임아웃!")

print("=" * 50)
print("[실습] 정답 실행")
print("=" * 50)

print("문제 1 - 비동기 다운로드:")
print(asyncio.run(download_all_async()))

print("\n문제 2 - 타이밍 측정:")
asyncio.run(run_timed())

print("\n문제 3 - 타임아웃:")
asyncio.run(run_with_timeout())
print()


# ============================================================
# [퀴즈]
# ============================================================
#
# Q1. async def 로 선언된 함수를 그냥 호출하면 어떻게 되는가?
#     a) 즉시 실행된다
#     b) 코루틴 객체가 반환된다
#     c) SyntaxError 가 발생한다
#     d) None 이 반환된다
#     → 정답: b
#
# Q2. asyncio.gather vs asyncio.wait_for 의 차이는?
#     → gather: 여러 코루틴 동시 실행 후 결과 수집
#       wait_for: 단일 코루틴에 타임아웃 적용
#
# Q3. CPU 집약적 연산(행렬 계산, 이미지 처리)에는 asyncio 대신 무엇을 쓰는가?
#     → multiprocessing (GIL 우회, 진정한 병렬 처리)
#
# Q4. await 는 어디서만 사용할 수 있는가?
#     → async def 로 선언된 함수(코루틴) 내부에서만 사용 가능
