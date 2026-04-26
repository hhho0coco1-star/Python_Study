# ============================================================
# Stage 1 - 07. 예외 처리 (Exception Handling)
# ============================================================

# sep : 파이썬 출력에서 여러 값을 구분하는 문자열(기본값은 공백)
# end : 파이썬 출력에서 줄바꿈 대신 사용할 문자열(기본값은 개행 문자)

# ============================================================
# [이론 1] 예외란 무엇인가?
# ============================================================
#
# 파이썬 인터프리터는 코드를 위에서 아래로 한 줄씩 실행한다.
# 실행 도중 "처리할 수 없는 상황"을 만나면 실행을 멈추고
# 예외(Exception) 객체를 만들어 던진다(raise).
#
# 아무도 이 예외를 잡지(catch) 않으면 → 프로그램이 종료되고 traceback 출력
# try/except 로 잡으면 → 프로그램을 계속 실행할 수 있다
#
# 예시: 아래 코드는 "ZeroDivisionError" 를 발생시킨다
#   result = 10 / 0   ← 파이썬이 ZeroDivisionError 객체를 만들어 던짐
#                       잡는 코드가 없으면 프로그램 종료


# ============================================================
# [이론 2] 예외 계층 구조 (상속 트리)
# ============================================================
#
# 파이썬의 모든 예외는 클래스이고 상속 관계를 가진다.
#
#   BaseException           ← 모든 예외의 최상위
#   ├── SystemExit          ← sys.exit() 호출 시
#   ├── KeyboardInterrupt   ← Ctrl+C 입력 시
#   └── Exception           ← 일반적인 프로그램 오류의 최상위
#       ├── ValueError      ← 값의 타입은 맞지만 내용이 부적절할 때 (예: int("abc"))
#       ├── TypeError       ← 타입이 잘못됐을 때 (예: 1 + "a")
#       ├── ZeroDivisionError ← 0으로 나눌 때
#       ├── IndexError      ← 리스트 인덱스 범위 초과
#       ├── KeyError        ← 딕셔너리에 없는 키 접근
#       ├── FileNotFoundError ← 없는 파일 열기 시도
#       ├── AttributeError  ← 없는 속성/메서드 접근
#       └── ... (수십 가지)
#
# 중요: except Exception 은 SystemExit, KeyboardInterrupt 는 잡지 않는다.
#       일반적으로 except Exception 또는 구체적인 예외 타입을 사용한다.


# ============================================================
# [이론 3] try/except 실행 흐름
# ============================================================
#
#   try:
#       코드 A   ← 정상 실행
#       코드 B   ← 여기서 예외 발생!  → 코드 C는 실행 안 됨
#       코드 C   ← 건너뜀
#   except SomeError:
#       코드 D   ← 예외 처리 코드 실행
#   코드 E       ← try/except 이후 코드는 정상 실행됨
#
# 핵심: 예외가 발생한 줄의 이후 코드는 try 블록 안에서 모두 건너뛴다.

try:
    x = int("hello")   # ValueError 발생 → 아래 줄은 실행 안 됨
    print("이 줄은 실행되지 않음")
except ValueError:
    print("숫자로 변환할 수 없는 문자열입니다.")
# 출력: 숫자로 변환할 수 없는 문자열입니다.


# ============================================================
# [이론 4] except 다양한 사용법
# ============================================================

# 4-1. 예외 메시지 변수로 받기
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"에러 내용: {e}")      # division by zero

# 4-2. 여러 예외를 따로 처리
try:
    items = [1, 2, 3]
    print(items[10])
except IndexError:
    print("인덱스 범위를 벗어났습니다.")
except TypeError:
    print("잘못된 타입입니다.")

# 4-3. 여러 예외를 한 번에 처리 (튜플 사용)
try:
    value = int(input("숫자를 입력하세요: ") if False else "abc")
except (ValueError, TypeError) as e:
    print(f"입력 오류: {e}")

# 4-4. 모든 예외 잡기 (권장하지 않음 — 어떤 에러인지 모르게 됨)
try:
    pass
except Exception as e:
    print(f"알 수 없는 오류: {e}")


# ============================================================
# [이론 5] else 와 finally
# ============================================================
#
# ┌──────────┬────────────────────────────────────────────┐
# │  블록    │  언제 실행되나?                             │
# ├──────────┼────────────────────────────────────────────┤
# │ except   │ 예외가 발생했을 때                          │
# │ else     │ 예외가 발생하지 않았을 때 (정상 완료 시)    │
# │ finally  │ 예외 발생 여부에 관계없이 항상              │
# └──────────┴────────────────────────────────────────────┘
#
# finally 의 대표적인 사용처: 파일 닫기, DB 연결 해제, 네트워크 소켓 정리
# (사실 with 구문이 이 역할을 대신하므로 파일에서는 with 를 쓰는 게 낫다)

def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("0으로 나눌 수 없습니다.")
        return None
    else:
        print(f"계산 성공: {result}")   # 예외 없을 때만 실행
        return result
    finally:
        print("divide() 함수 종료")     # 항상 실행

divide(10, 2)
# 출력:
# 계산 성공: 5.0
# divide() 함수 종료

divide(10, 0)
# 출력:
# 0으로 나눌 수 없습니다.
# divide() 함수 종료


# ============================================================
# [이론 6] raise — 의도적으로 예외 던지기
# ============================================================
#
# raise 를 쓰는 이유:
#   파이썬 자체는 에러로 보지 않지만, 비즈니스 규칙상 허용하면 안 되는 값이 있을 때.
#   예) 나이는 음수가 될 수 없다. 점수는 0~100 사이여야 한다.
#
# raise 를 쓰면:
#   - 함수 내부에서 잘못된 값을 즉시 차단할 수 있다
#   - 호출한 쪽에서 try/except 로 처리할 수 있다

def set_age(age):
    if age < 0:
        raise ValueError(f"나이는 0 이상이어야 합니다. 입력값: {age}")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(e)   # 나이는 0 이상이어야 합니다. 입력값: -5


# ============================================================
# [이론 7] 커스텀 예외 클래스
# ============================================================
#
# 커스텀 예외를 만드는 이유:
#   - 에러의 종류를 더 명확하게 표현할 수 있다
#   - 호출한 쪽에서 except 로 구체적으로 구분해서 처리할 수 있다
#   - 라이브러리나 모듈을 만들 때 자체 에러 체계를 정의하기 위해
#
# 만드는 법: Exception 을 상속받는 클래스를 선언하면 끝.
# 보통 이름을 ~Error 또는 ~Exception 으로 짓는다.

class InsufficientStockError(Exception):
    """재고 부족 예외"""
    pass

class InvalidPriceError(Exception):
    """가격 유효성 예외"""
    def __init__(self, price, message="가격은 0보다 커야 합니다"):
        self.price = price
        super().__init__(f"{message} (입력값: {price})")

def sell_item(stock, price, quantity):
    if price <= 0:
        raise InvalidPriceError(price)
    if stock < quantity:
        raise InsufficientStockError(f"재고 부족: 요청 {quantity}개, 현재 재고 {stock}개")
    return stock - quantity

try:
    sell_item(3, 1000, 10)
except InsufficientStockError as e:
    print(f"[재고 오류] {e}")
except InvalidPriceError as e:
    print(f"[가격 오류] {e}")
# 출력: [재고 오류] 재고 부족: 요청 10개, 현재 재고 3개


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] 사용자 입력을 정수로 변환하는 함수 safe_int()를 작성하세요.
# - 변환 성공 시 정수를 반환
# - ValueError 발생 시 None을 반환하고 "변환 실패: <입력값>" 출력
# 예:
#   safe_int("42")   → 42
#   safe_int("abc")  → 출력: "변환 실패: abc", 반환: None
# 코드 작성 ↓
def safe_int(s):
    try:
        return int(s)
    except ValueError:
        print(f"변환 실패 : {s}")
        return None


# [문제 2] 파일을 안전하게 읽는 함수 read_file(path)을 작성하세요.
# - 파일이 존재하면 내용을 문자열로 반환
# - FileNotFoundError 발생 시 "파일을 찾을 수 없습니다: <path>" 출력 후 None 반환
# - finally 블록에서 "파일 읽기 시도 완료" 출력
# 코드 작성 ↓
def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다. {path}")
        return None
    finally:
        print("파일 읽기 시도 완료")


# [문제 3] 아래 조건을 만족하는 validate_score(score) 함수를 작성하세요.
# - score가 0~100 사이 정수가 아니면 ValueError를 raise
# - 정상이면 "유효한 점수: <score>" 출력
# 호출 예:
#   validate_score(85)   → "유효한 점수: 85"
#   validate_score(110)  → ValueError: "점수는 0~100 사이여야 합니다. 입력값: 110"
# 코드 작성 ↓
def validate_score(score):
    if not isinstance(score, int) or score < 0 or score > 100:
        # isinstance(obj, type) : obj 가 type 의 인스턴스인지 확인하는 함수
        raise ValueError(f"점수는 0~100 사이여야 합니다. 입력값 : {score}")
    print(f"유효한 점수 : {score}")

# [문제 4] 커스텀 예외 NegativeAmountError 를 정의하고
# withdraw(balance, amount) 함수를 작성하세요.
# - amount 가 0 이하이면 NegativeAmountError 발생 (메시지: "출금액은 0보다 커야 합니다")
# - amount 가 balance 보다 크면 ValueError 발생 (메시지: "잔액 부족")
# - 정상이면 남은 잔액 반환
# 코드 작성 ↓
class NegativeAmountError(Exception):
    pass

def withdraw(balance, amount):
    if amount <= 0:
        raise NegativeAmountError("출금액은 0보다 커야 합니다.")
    if amount > balance:
        raise ValueError("잔액 부족")
    return balance - amount
