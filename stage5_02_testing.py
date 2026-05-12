# ============================================================
# Stage 5 - 02. 테스팅 (Testing)
# ============================================================
#
# 설치 필요:
#   pip install pytest pytest-mock
#
# 실행 방법:
#   pytest stage5_02_testing.py -v
#   (또는 이 파일 단독 실행 시 unittest 방식으로도 동작)


# ============================================================
# [이론 1] 왜 테스트를 작성하는가?
# ============================================================
#
# 테스트가 없으면:
#   - 기능 추가할 때마다 기존 코드가 망가졌는지 수동 확인해야 함
#   - "이 함수 건드리면 어디가 깨질지 모른다" → 리팩토링 기피
#
# 테스트가 있으면:
#   - 코드 변경 후 pytest 한 번으로 전체 회귀(regression) 확인
#   - 테스트 자체가 코드 사용법의 문서 역할
#
# 테스트 종류:
#   단위 테스트(Unit Test)    : 함수/메서드 하나를 독립적으로 검증
#   통합 테스트(Integration)  : 여러 컴포넌트가 함께 동작하는지 검증
#   E2E 테스트               : 실제 사용자 흐름 전체를 검증


# ============================================================
# [이론 2] pytest 기초 — assert 와 테스트 함수
# ============================================================
#
# pytest 규칙:
#   - 파일 이름: test_*.py 또는 *_test.py
#   - 함수 이름: test_ 로 시작
#   - 클래스 이름: Test 로 시작 (클래스 기반 테스트 시)
#   - assert 문으로 검증
#
# assert 실패 시 AssertionError → pytest가 어떤 값이었는지 자동 출력.

def add(a: int, b: int) -> int:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -2) == -3

def test_add_zero():
    assert add(0, 0) == 0

def test_divide_normal():
    assert divide(10, 2) == 5.0

def test_divide_float():
    result = divide(1, 3)
    assert abs(result - 0.3333) < 0.001   # 부동소수점은 근사 비교


# ============================================================
# [이론 3] pytest.raises — 예외 테스트
# ============================================================
#
# 예외가 발생해야 정상인 경우:
#   with pytest.raises(예외타입) as exc_info:
#       코드()
#   assert "메시지" in str(exc_info.value)

import pytest

def test_divide_by_zero():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "0으로 나눌 수 없습니다" in str(exc_info.value)

def test_divide_by_zero_type():
    with pytest.raises(ValueError):
        divide(5, 0)


# ============================================================
# [이론 4] 픽스처 (@pytest.fixture)
# ============================================================
#
# 픽스처(fixture): 테스트 실행 전후에 공통으로 필요한 설정/해제 작업.
# 예) DB 연결, 테스트 데이터, 임시 파일
#
# @pytest.fixture 로 선언하고 테스트 함수의 매개변수로 받으면 자동 주입.
#
# scope:
#   "function" (기본): 테스트 함수마다 새로 실행
#   "module"         : 모듈(파일)당 한 번 실행
#   "session"        : 전체 테스트 세션에서 한 번 실행

class ShoppingCart:
    def __init__(self):
        self.items: list[dict] = []

    def add_item(self, name: str, price: int, qty: int = 1):
        self.items.append({"name": name, "price": price, "qty": qty})

    def remove_item(self, name: str):
        self.items = [i for i in self.items if i["name"] != name]

    def total(self) -> int:
        return sum(i["price"] * i["qty"] for i in self.items)

    def count(self) -> int:
        return len(self.items)

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.fixture
def cart_with_items():
    cart = ShoppingCart()
    cart.add_item("사과", 1000, 2)
    cart.add_item("바나나", 500, 3)
    return cart

def test_cart_empty_at_start(empty_cart):
    assert empty_cart.count() == 0
    assert empty_cart.total() == 0

def test_cart_add_item(empty_cart):
    empty_cart.add_item("커피", 3000)
    assert empty_cart.count() == 1
    assert empty_cart.total() == 3000

def test_cart_total(cart_with_items):
    # 사과: 1000*2=2000, 바나나: 500*3=1500 → 합계 3500
    assert cart_with_items.total() == 3500

def test_cart_remove(cart_with_items):
    cart_with_items.remove_item("사과")
    assert cart_with_items.count() == 1
    assert cart_with_items.total() == 1500

@pytest.fixture
def db_session():
    """DB 연결 픽스처 (실제로는 SQLAlchemy 세션)"""
    print("\n  [픽스처] DB 연결")
    session = {"connected": True, "data": []}
    yield session              # yield 이후는 정리(teardown) 코드
    print("\n  [픽스처] DB 연결 해제")
    session["connected"] = False

def test_db_connected(db_session):
    assert db_session["connected"] is True


# ============================================================
# [이론 5] 파라미터화 테스트 (@pytest.mark.parametrize)
# ============================================================
#
# 같은 테스트를 다양한 입력값으로 반복하고 싶을 때.
# 코드 중복 없이 여러 케이스를 한번에 커버.

@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
    (999, 1, 1000),
])
def test_add_parametrize(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize("password, is_valid", [
    ("abc", False),        # 너무 짧음
    ("abcdef", False),     # 숫자 없음
    ("abc123", True),      # 정상
    ("", False),           # 빈 문자열
    ("A1b2C3d4", True),    # 혼합
])
def test_password_validation(password, is_valid):
    def validate_password(pw: str) -> bool:
        return len(pw) >= 6 and any(c.isdigit() for c in pw)

    assert validate_password(password) == is_valid


# ============================================================
# [이론 6] 모킹 (Mocking) — unittest.mock
# ============================================================
#
# 모킹: 외부 의존성(API 호출, DB, 파일)을 가짜 객체로 대체.
#
# 왜 필요한가?
#   - 실제 API를 테스트마다 호출하면 느리고 비용 발생
#   - 네트워크 없이도 테스트 가능
#   - 특정 응답(오류, 엣지케이스)을 강제로 만들 수 있음
#
# unittest.mock 주요 도구:
#   Mock()         : 아무 속성/메서드나 있는 가짜 객체
#   MagicMock()    : Magic method(__len__, __str__ 등)까지 지원
#   patch()        : 특정 경로의 객체를 Mock으로 교체 (컨텍스트 매니저 / 데코레이터)

from unittest.mock import Mock, MagicMock, patch

# --- Mock 기본 ---
def test_mock_basic():
    mock_obj = Mock()
    mock_obj.get_price.return_value = 5000

    price = mock_obj.get_price("사과")
    assert price == 5000
    mock_obj.get_price.assert_called_once_with("사과")

# --- 실제 시나리오: 외부 API를 의존하는 함수 ---
def get_exchange_rate(currency: str) -> float:
    """실제로는 외부 환율 API 호출 (여기선 구현 생략)"""
    raise NotImplementedError("실제 API 필요")

def convert_to_krw(amount_usd: float, rate_fetcher) -> float:
    rate = rate_fetcher("USD")
    return amount_usd * rate

def test_convert_to_krw():
    mock_fetcher = Mock()
    mock_fetcher.return_value = 1300.0   # 1 USD = 1300 KRW 가정

    result = convert_to_krw(10.0, mock_fetcher)
    assert result == 13000.0
    mock_fetcher.assert_called_once_with("USD")

# --- patch() 사용 ---
import os

def get_home_dir() -> str:
    return os.path.expanduser("~")

def test_patch_os():
    with patch("os.path.expanduser") as mock_expand:
        mock_expand.return_value = "/fake/home"
        result = get_home_dir()
        assert result == "/fake/home"
        mock_expand.assert_called_once_with("~")

# --- side_effect: 예외 발생 또는 동적 반환값 ---
def test_mock_side_effect_exception():
    mock_api = Mock()
    mock_api.call.side_effect = ConnectionError("서버 연결 실패")

    with pytest.raises(ConnectionError):
        mock_api.call()

def test_mock_side_effect_dynamic():
    mock_fn = Mock()
    mock_fn.side_effect = [10, 20, 30]   # 호출마다 다른 값 반환

    assert mock_fn() == 10
    assert mock_fn() == 20
    assert mock_fn() == 30


# ============================================================
# [이론 7] 클래스 기반 테스트
# ============================================================
#
# 관련 테스트를 클래스로 묶으면 구조화가 쉬움.
# pytest는 Test 로 시작하는 클래스를 자동 인식.

class TestShoppingCart:
    def setup_method(self):
        """각 테스트 메서드 실행 전 호출 (픽스처 없이 간단히 초기화)"""
        self.cart = ShoppingCart()

    def test_초기_상태(self):
        assert self.cart.count() == 0

    def test_아이템_추가(self):
        self.cart.add_item("노트", 2000)
        assert self.cart.count() == 1
        assert self.cart.total() == 2000

    def test_여러_아이템(self):
        self.cart.add_item("펜", 500, 3)
        self.cart.add_item("지우개", 300, 2)
        assert self.cart.total() == 500 * 3 + 300 * 2

    def test_아이템_제거(self):
        self.cart.add_item("A", 1000)
        self.cart.add_item("B", 2000)
        self.cart.remove_item("A")
        assert self.cart.count() == 1
        assert self.cart.total() == 2000


# ============================================================
# [실습 문제]
# ============================================================
#
# 문제 1: 아래 함수에 대한 테스트를 작성하시오.
#         엣지케이스(빈 리스트, 음수, 중복값)를 포함할 것.
#
#   def find_max(nums: list[int]) -> int:
#       if not nums:
#           raise ValueError("빈 리스트")
#       return max(nums)
#
# 문제 2: @pytest.mark.parametrize 를 사용해
#         is_palindrome("기러기") → True,
#         is_palindrome("python") → False 등 5개 케이스를 테스트하시오.
#
# 문제 3: Mock을 사용해 send_email(to, subject) 함수가
#         올바른 인자로 호출되었는지 검증하는 테스트를 작성하시오.


# --- 정답 ---

def find_max(nums: list) -> int:
    if not nums:
        raise ValueError("빈 리스트")
    return max(nums)

# 문제 1
def test_find_max_normal():
    assert find_max([3, 1, 4, 1, 5, 9]) == 9

def test_find_max_single():
    assert find_max([42]) == 42

def test_find_max_negative():
    assert find_max([-3, -1, -7]) == -1

def test_find_max_duplicates():
    assert find_max([5, 5, 5]) == 5

def test_find_max_empty():
    with pytest.raises(ValueError, match="빈 리스트"):
        find_max([])

# 문제 2
def is_palindrome(s: str) -> bool:
    return s == s[::-1]

@pytest.mark.parametrize("word, expected", [
    ("기러기", True),
    ("python", False),
    ("abcba", True),
    ("hello", False),
    ("a", True),
])
def test_is_palindrome(word, expected):
    assert is_palindrome(word) == expected

# 문제 3
def notify_user(email_sender, to: str, subject: str):
    email_sender.send(to, subject)

def test_email_called_correctly():
    mock_sender = Mock()
    notify_user(mock_sender, "user@test.com", "가입 완료")
    mock_sender.send.assert_called_once_with("user@test.com", "가입 완료")


# ============================================================
# 이 파일을 직접 실행하면 아래가 출력됩니다.
# 실제 테스트는 'pytest stage5_02_testing.py -v' 로 실행하세요.
# ============================================================

if __name__ == "__main__":
    print("pytest 로 실행하세요:")
    print("  pytest stage5_02_testing.py -v")
    print()
    print("설치:")
    print("  pip install pytest pytest-mock")


# ============================================================
# [퀴즈]
# ============================================================
#
# Q1. pytest 에서 테스트 함수 이름은 어떻게 시작해야 하는가?
#     → test_ 로 시작
#
# Q2. @pytest.fixture 에서 yield 를 사용하는 이유는?
#     → yield 이전: 설정(setup), yield 이후: 정리(teardown)
#       with 구문처럼 테스트 후 자동으로 정리 코드 실행
#
# Q3. Mock의 assert_called_once_with() 는 무엇을 검증하는가?
#     → 모의 객체가 정확히 한 번, 지정된 인자로 호출되었는지 검증
#
# Q4. @pytest.mark.parametrize 의 장점은?
#     → 동일한 테스트 로직을 여러 입력값에 대해 반복 작성 없이 실행
