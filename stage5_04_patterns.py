# ============================================================
# Stage 5 - 04. 디자인 패턴 (Design Patterns)
# ============================================================
#
# GoF(Gang of Four) 디자인 패턴: 반복되는 소프트웨어 설계 문제에 대한
# 검증된 해결책. 생성/구조/행동 패턴 3가지로 분류.
#
# 이 챕터에서 다루는 패턴:
#   생성 패턴: 싱글톤(Singleton), 팩토리(Factory)
#   행동 패턴: 옵저버(Observer), 전략(Strategy)


# ============================================================
# [이론 1] 싱글톤 패턴 (Singleton)
# ============================================================
#
# 목적: 클래스의 인스턴스를 하나만 생성하고, 전역 접근 제공.
#
# 사용처:
#   - DB 연결 풀 (매번 새 연결을 만들면 낭비)
#   - 설정 관리자 (앱 전체에서 동일한 설정 공유)
#   - 로거 (하나의 로그 핸들러)
#
# 파이썬 구현 방법:
#   1. __new__ 오버라이드
#   2. 모듈 수준 변수 (파이썬에서 가장 간단)
#   3. 데코레이터

print("=" * 55)
print("[이론 1] 싱글톤 패턴")
print("=" * 55)

# 방법 1: __new__ 오버라이드
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connected = False
            cls._instance.host = "localhost"
        return cls._instance

    def connect(self, host: str):
        self.host = host
        self.connected = True
        print(f"  DB 연결: {self.host}")

    def disconnect(self):
        self.connected = False
        print("  DB 연결 해제")

db1 = DatabaseConnection()
db2 = DatabaseConnection()
db1.connect("db.example.com")

print(f"  db1 is db2: {db1 is db2}")          # True
print(f"  db2.host: {db2.host}")              # db.example.com (같은 인스턴스)
print(f"  db2.connected: {db2.connected}")    # True
print()

# 방법 2: 데코레이터로 싱글톤 만들기
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Config:
    def __init__(self):
        self.debug = False
        self.version = "1.0.0"

cfg1 = Config()
cfg2 = Config()
cfg1.debug = True
print(f"  cfg1 is cfg2: {cfg1 is cfg2}")      # True
print(f"  cfg2.debug: {cfg2.debug}")           # True (같은 인스턴스)
print()


# ============================================================
# [이론 2] 팩토리 패턴 (Factory Method)
# ============================================================
#
# 목적: 객체 생성 로직을 캡슐화. 어떤 클래스를 생성할지 런타임에 결정.
#
# 사용처:
#   - 조건에 따라 다른 구현체 반환 (결제수단, 알림 방식 등)
#   - 객체 생성 복잡도를 숨길 때
#
# 효과: 클라이언트 코드가 구체적인 클래스 이름을 몰라도 됨.

print("=" * 55)
print("[이론 2] 팩토리 패턴")
print("=" * 55)

from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> str:
        pass

class EmailNotification(Notification):
    def __init__(self, address: str):
        self.address = address

    def send(self, message: str) -> str:
        return f"[이메일 → {self.address}] {message}"

class SMSNotification(Notification):
    def __init__(self, phone: str):
        self.phone = phone

    def send(self, message: str) -> str:
        return f"[SMS → {self.phone}] {message}"

class PushNotification(Notification):
    def __init__(self, device_id: str):
        self.device_id = device_id

    def send(self, message: str) -> str:
        return f"[PUSH → {self.device_id}] {message}"

class NotificationFactory:
    @staticmethod
    def create(ntype: str, target: str) -> Notification:
        if ntype == "email":
            return EmailNotification(target)
        elif ntype == "sms":
            return SMSNotification(target)
        elif ntype == "push":
            return PushNotification(target)
        else:
            raise ValueError(f"알 수 없는 알림 타입: {ntype}")

# 클라이언트 코드: 구체적인 클래스 이름 몰라도 됨
for ntype, target in [
    ("email", "user@test.com"),
    ("sms", "010-1234-5678"),
    ("push", "device-abc-123"),
]:
    notifier = NotificationFactory.create(ntype, target)
    result = notifier.send("회원 가입을 축하합니다!")
    print(f"  {result}")
print()


# ============================================================
# [이론 3] 옵저버 패턴 (Observer)
# ============================================================
#
# 목적: 한 객체(Subject)의 상태 변경을 다수의 객체(Observer)에게 자동 통보.
#
# 사용처:
#   - 이벤트 시스템 (클릭, 키 입력)
#   - MVC에서 Model 변경 → View 자동 업데이트
#   - 주식 가격 변동 알림
#
# 구성:
#   Subject (Publisher): 상태 보유 + 옵저버 등록/해제/통보
#   Observer: 통보 받아 처리하는 인터페이스

print("=" * 55)
print("[이론 3] 옵저버 패턴")
print("=" * 55)

class Observer(ABC):
    @abstractmethod
    def update(self, event: str, data) -> None:
        pass

class EventEmitter:
    def __init__(self):
        self._observers: dict[str, list[Observer]] = {}

    def subscribe(self, event: str, observer: Observer) -> None:
        if event not in self._observers:
            self._observers[event] = []
        self._observers[event].append(observer)

    def unsubscribe(self, event: str, observer: Observer) -> None:
        if event in self._observers:
            self._observers[event].remove(observer)

    def emit(self, event: str, data=None) -> None:
        for obs in self._observers.get(event, []):
            obs.update(event, data)

class StockPriceBoard(Observer):
    def update(self, event: str, data) -> None:
        print(f"  [전광판] {event}: {data['stock']} = {data['price']:,}원")

class PriceAlertService(Observer):
    def __init__(self, threshold: int):
        self.threshold = threshold

    def update(self, event: str, data) -> None:
        if data["price"] >= self.threshold:
            print(f"  [알림] {data['stock']} 가격이 {self.threshold:,}원 이상! 현재: {data['price']:,}원")

class StockMarket(EventEmitter):
    def update_price(self, stock: str, price: int) -> None:
        self.emit("price_change", {"stock": stock, "price": price})

market = StockMarket()
board = StockPriceBoard()
alert = PriceAlertService(threshold=50_000)

market.subscribe("price_change", board)
market.subscribe("price_change", alert)

market.update_price("삼성전자", 72_000)
market.update_price("카카오", 45_000)
market.update_price("NAVER", 180_000)

print("  --- 알림 서비스 구독 해제 ---")
market.unsubscribe("price_change", alert)
market.update_price("삼성전자", 80_000)   # 전광판만 출력
print()


# ============================================================
# [이론 4] 전략 패턴 (Strategy)
# ============================================================
#
# 목적: 알고리즘(전략)을 캡슐화하고 런타임에 교체 가능하게 만들기.
#
# 사용처:
#   - 정렬 알고리즘 선택 (버블/퀵/병합)
#   - 결제 방식 선택 (카드/현금/포인트)
#   - 할인 정책 적용 (정률/정액/VIP)
#
# if/elif 가 많아지면 전략 패턴을 고려하라.

print("=" * 55)
print("[이론 4] 전략 패턴")
print("=" * 55)

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, price: int) -> int:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

class NoDiscount(DiscountStrategy):
    def apply(self, price: int) -> int:
        return price

    def description(self) -> str:
        return "할인 없음"

class PercentDiscount(DiscountStrategy):
    def __init__(self, percent: int):
        self.percent = percent

    def apply(self, price: int) -> int:
        return int(price * (1 - self.percent / 100))

    def description(self) -> str:
        return f"{self.percent}% 할인"

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount: int):
        self.amount = amount

    def apply(self, price: int) -> int:
        return max(0, price - self.amount)

    def description(self) -> str:
        return f"{self.amount:,}원 할인"

class BuyOneGetOne(DiscountStrategy):
    def apply(self, price: int) -> int:
        return price // 2   # 2개 중 1개 무료 = 1개 가격의 절반

    def description(self) -> str:
        return "1+1 행사"

class ShoppingCart:
    def __init__(self):
        self.items: list[tuple[str, int]] = []
        self.strategy: DiscountStrategy = NoDiscount()

    def add_item(self, name: str, price: int):
        self.items.append((name, price))

    def set_strategy(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def checkout(self) -> int:
        subtotal = sum(p for _, p in self.items)
        final = self.strategy.apply(subtotal)
        print(f"  [{self.strategy.description()}] 원가: {subtotal:,}원 → 최종: {final:,}원")
        return final

cart = ShoppingCart()
cart.add_item("노트북", 1_200_000)
cart.add_item("마우스", 50_000)
cart.add_item("키보드", 80_000)

strategies = [
    NoDiscount(),
    PercentDiscount(10),
    FixedDiscount(100_000),
    BuyOneGetOne(),
]

for s in strategies:
    cart.set_strategy(s)
    cart.checkout()
print()


# ============================================================
# [이론 5] 데코레이터 패턴 (Decorator — 구조 패턴)
# ============================================================
#
# 목적: 기존 객체를 수정하지 않고 기능을 동적으로 추가.
#       파이썬의 @decorator 함수 데코레이터와 개념이 같다.
#
# 사용처:
#   - 로깅/타이밍 추가
#   - 인증/권한 확인 추가
#   - 캐싱 추가

print("=" * 55)
print("[이론 5] 데코레이터 패턴 (함수 버전)")
print("=" * 55)

import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] 소요 시간: {elapsed:.4f}초")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 0.1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"  [{func.__name__}] 시도 {attempt} 실패: {e}. 재시도...")
                    time.sleep(delay)
        return wrapper
    return decorator

@timer
def slow_computation():
    total = sum(i ** 2 for i in range(100_000))
    return total

@retry(max_attempts=3, delay=0.05)
def flaky_function(calls=[0]):
    calls[0] += 1
    if calls[0] < 3:
        raise ConnectionError("네트워크 오류")
    return "성공"

result = slow_computation()
print(f"  결과: {result}")

try:
    result = flaky_function()
    print(f"  최종 결과: {result}")
except ConnectionError as e:
    print(f"  최종 실패: {e}")
print()


# ============================================================
# [실습 문제]
# ============================================================
#
# 문제 1: 싱글톤 패턴으로 Logger 클래스를 구현하시오.
#         log(message) 메서드는 "[로그] message" 형태로 출력.
#         여러 곳에서 Logger()를 호출해도 같은 인스턴스임을 증명.
#
# 문제 2: 전략 패턴으로 정렬기(Sorter)를 구현하시오.
#         오름차순, 내림차순, 절댓값 기준 세 가지 전략.
#         Sorter.sort([3, -1, 4, -1, 5, -9]) 호출 가능.
#
# 문제 3: 옵저버 패턴으로 간단한 이벤트 버스를 구현하시오.
#         on(event, callback), emit(event, data) 인터페이스.
#         emit 시 해당 이벤트에 등록된 콜백들이 모두 호출.


# --- 정답 ---

# 문제 1
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message: str):
        self.logs.append(message)
        print(f"  [로그] {message}")

print("=" * 55)
print("[실습] 정답")
print("=" * 55)

logger1 = Logger()
logger2 = Logger()
logger1.log("서버 시작")
logger2.log("사용자 로그인")
print(f"  logger1 is logger2: {logger1 is logger2}")
print(f"  전체 로그: {logger1.logs}")

# 문제 2
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

class AscendingSort(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data)

class DescendingSort(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data, reverse=True)

class AbsoluteSort(SortStrategy):
    def sort(self, data: list) -> list:
        return sorted(data, key=abs)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort(self, data: list) -> list:
        return self.strategy.sort(data)

nums = [3, -1, 4, -1, 5, -9]
print(f"\n  원본: {nums}")
print(f"  오름차순: {Sorter(AscendingSort()).sort(nums)}")
print(f"  내림차순: {Sorter(DescendingSort()).sort(nums)}")
print(f"  절댓값:   {Sorter(AbsoluteSort()).sort(nums)}")

# 문제 3
class EventBus:
    def __init__(self):
        self._handlers: dict[str, list] = {}

    def on(self, event: str, callback) -> None:
        self._handlers.setdefault(event, []).append(callback)

    def emit(self, event: str, data=None) -> None:
        for cb in self._handlers.get(event, []):
            cb(data)

bus = EventBus()
bus.on("login", lambda d: print(f"  [이벤트] 로그인: {d['user']}"))
bus.on("login", lambda d: print(f"  [이벤트] 로그인 시각 기록: {d['user']}"))
bus.on("logout", lambda d: print(f"  [이벤트] 로그아웃: {d['user']}"))

print()
bus.emit("login", {"user": "alice"})
bus.emit("logout", {"user": "alice"})
print()


# ============================================================
# [퀴즈]
# ============================================================
#
# Q1. 싱글톤 패턴의 단점은?
#     → 전역 상태를 만들어 테스트 격리가 어려움.
#       멀티스레드 환경에서 인스턴스 중복 생성 가능 (lock 필요).
#
# Q2. 팩토리 패턴이 if/elif 체인보다 좋은 이유는?
#     → 새 타입 추가 시 기존 코드 수정 없이 새 클래스만 추가(개방-폐쇄 원칙).
#       클라이언트가 구체 클래스를 몰라도 됨.
#
# Q3. 옵저버와 전략 패턴의 차이는?
#     → 옵저버: 1:N 관계, 이벤트 발생 시 여러 객체에 자동 통보
#       전략:   1:1 관계, 알고리즘을 교체 가능하게 캡슐화
#
# Q4. 언제 전략 패턴을 도입해야 하는가?
#     → if/elif로 알고리즘을 선택하는 코드가 반복될 때,
#       새 알고리즘 추가 시 기존 코드를 수정해야 할 때
