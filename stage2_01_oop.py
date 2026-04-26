# ============================================================
# Stage 2 - 01. OOP (객체지향 프로그래밍)
# ============================================================


# ============================================================
# [이론 1] OOP란 무엇인가?
# ============================================================
#
# 절차지향 프로그래밍: 함수들을 순서대로 호출하며 데이터를 처리
# 객체지향 프로그래밍: 데이터(속성)와 동작(메서드)을 하나의 "객체"로 묶어서 관리
#
# 왜 OOP를 쓰나?
#   - 코드가 커질수록 관련 데이터와 함수가 흩어지면 관리가 어려워진다
#   - 클래스로 묶으면 관련된 것들이 한 곳에 모여 있어 이해/수정이 쉬워진다
#   - 상속으로 공통 코드를 재사용하고, 차이점만 따로 정의할 수 있다
#
# 비유: 클래스는 "붕어빵 틀", 인스턴스는 "붕어빵"
#   - 틀(클래스)은 하나지만, 붕어빵(인스턴스)은 여러 개 찍어낼 수 있다
#   - 각 붕어빵은 속재료(속성값)가 다를 수 있다


# ============================================================
# [이론 2] 클래스와 인스턴스 기본 구조
# ============================================================
#
# class 키워드로 클래스를 정의한다.
# __init__ 은 인스턴스가 생성될 때 파이썬이 자동으로 호출하는 메서드다.
# self 는 "지금 이 메서드를 호출한 인스턴스 자신"을 가리키는 참조다.
#   → self.name 처럼 쓰면 인스턴스마다 따로 저장되는 데이터(인스턴스 변수)가 된다.

class Dog:
    # __init__: 생성자 (constructor)
    # Dog("바둑이", 3) 처럼 호출하면 name="바둑이", age=3 으로 초기화됨
    def __init__(self, name, age):
        self.name = name    # 인스턴스 변수: 각 객체마다 따로 저장됨
        self.age = age

    def bark(self):
        print(f"{self.name}: 왈왈!")

    def info(self):
        print(f"이름: {self.name}, 나이: {self.age}살")

# 인스턴스 생성
dog1 = Dog("바둑이", 3)
dog2 = Dog("초코", 5)

dog1.bark()     # 바둑이: 왈왈!
dog2.info()     # 이름: 초코, 나이: 5살

# dog1과 dog2는 같은 클래스로 만들었지만, 각자 독립적인 데이터를 갖는다
print(dog1.name, dog2.name)   # 바둑이 초코


# ============================================================
# [이론 3] 클래스 변수 vs 인스턴스 변수
# ============================================================
#
# 인스턴스 변수: self.xxx → 각 인스턴스마다 따로 저장 (인스턴스별로 다른 값)
# 클래스 변수:   클래스 블록 안에 선언 → 모든 인스턴스가 공유하는 값
#
# 언제 클래스 변수를 쓰나?
#   - 생성된 인스턴스 수 세기
#   - 모든 인스턴스에 공통적인 상수값 (예: 회사명, 버전)

class Counter:
    count = 0   # 클래스 변수: 모든 인스턴스가 공유

    def __init__(self, name):
        self.name = name        # 인스턴스 변수
        Counter.count += 1      # 클래스 변수에 접근할 때는 클래스명.변수명

c1 = Counter("A")
c2 = Counter("B")
c3 = Counter("C")

print(Counter.count)    # 3 (총 생성 횟수)
print(c1.name)          # A (인스턴스별 고유값)


# ============================================================
# [이론 4] 메서드 종류 3가지
# ============================================================
#
# 1. 인스턴스 메서드: 첫 번째 인자가 self → 인스턴스 데이터에 접근 가능
# 2. 클래스 메서드:  @classmethod 데코레이터, 첫 번째 인자가 cls → 클래스 자체에 접근
# 3. 정적 메서드:   @staticmethod 데코레이터, self/cls 없음 → 클래스와 관련 있지만 독립적인 유틸 함수

class Temperature:
    unit = "섭씨"   # 클래스 변수

    def __init__(self, value):
        self.value = value   # 인스턴스 변수

    # 인스턴스 메서드: self 를 통해 인스턴스 데이터 사용
    def display(self):
        print(f"{self.value}°C")

    # 클래스 메서드: cls 를 통해 클래스 변수/클래스 자체에 접근
    @classmethod
    def get_unit(cls):
        return cls.unit

    # 정적 메서드: 클래스와 연관되지만 self/cls 불필요한 유틸 함수
    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

t = Temperature(100)
t.display()                                    # 100°C
print(Temperature.get_unit())                  # 섭씨
print(Temperature.celsius_to_fahrenheit(100))  # 212.0


# ============================================================
# [이론 5] 상속 (Inheritance)
# ============================================================
#
# 상속이란 부모 클래스의 속성과 메서드를 자식 클래스가 물려받는 것.
# 공통 코드는 부모에 한 번만 작성하고, 차이점만 자식에서 정의한다.
#
# super() : 부모 클래스를 가리키는 참조
#   → super().__init__() 으로 부모의 초기화 코드를 먼저 실행한 뒤, 추가 초기화를 한다.

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name}이(가) 소리를 냅니다.")

    def info(self):
        print(f"동물 이름: {self.name}")

class Cat(Animal):      # Animal 을 상속
    def __init__(self, name, color):
        super().__init__(name)   # 부모의 __init__ 실행 (self.name 초기화)
        self.color = color       # 자식만의 추가 속성

    # 메서드 오버라이딩: 부모의 speak() 를 자식에서 재정의
    def speak(self):
        print(f"{self.name}: 야옹~")

class Parrot(Animal):
    def speak(self):
        print(f"{self.name}: 안녕하세요!")

cat = Cat("나비", "흰색")
parrot = Parrot("코코")

cat.speak()     # 나비: 야옹~ (오버라이딩된 버전)
parrot.speak()  # 코코: 안녕하세요!
cat.info()      # 동물 이름: 나비 (부모 메서드 그대로 사용)
print(cat.color)  # 흰색 (자식만의 속성)


# ============================================================
# [이론 6] 매직 메서드 (Magic / Dunder Methods) 규격화된 사용자 정의 함수
# ============================================================
#
# 앞뒤로 __ 가 붙은 특수 메서드. 파이썬이 특정 상황에서 자동으로 호출한다.
#
# __str__  : print(obj) 또는 str(obj) 할 때 호출 → 사람이 읽기 좋은 문자열 반환
# __repr__ : repr(obj) 또는 디버거에서 호출 → 개발자용 상세 문자열 반환
# __len__  : len(obj) 호출 시
# __eq__   : obj1 == obj2 비교 시
# __lt__   : obj1 < obj2 비교 시 (sorted() 등에서 활용)

class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"『{self.title}』 ({self.pages}쪽)"

    def __repr__(self):
        return f"Book(title={self.title!r}, pages={self.pages})"

    def __len__(self):
        return self.pages

    def __eq__(self, other):
        return self.title == other.title

    def __lt__(self, other):
        return self.pages < other.pages

b1 = Book("파이썬 기초", 300)
b2 = Book("파이썬 심화", 500)

print(b1)           # 『파이썬 기초』 (300쪽)  ← __str__ 호출
print(len(b1))      # 300                       ← __len__ 호출
print(b1 == b2)     # False                     ← __eq__ 호출
print(b1 < b2)      # True                      ← __lt__ 호출

books = [b2, b1]
print(sorted(books))   # b1이 먼저 옴 (__lt__ 기반 정렬)


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] BankAccount 클래스를 작성하세요.
# 속성: owner(예금주), balance(잔액, 기본값 0)
# 메서드:
#   - deposit(amount): 입금. 잔액 증가 후 "입금 완료: <amount>원, 잔액: <balance>원" 출력
#   - withdraw(amount): 출금. 잔액 부족 시 "잔액 부족" 출력, 성공 시 잔액 감소 후 출력
#   - __str__: "[<owner>] 잔액: <balance>원" 형식으로 반환
# 코드 작성 ↓
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"입금 완료 : {amount}원, 잔액 : {self.balance}원")

    def withdraw(self, amount):
        if self.balance < amount:
            print("잔액 부족")
        else:
            self.balance -= amount
            print(f"출금 완료 : {amount}원, 잔액 : {self.balance}원")

    def __str__(self):
        return f"[{self.owner}] 잔액 : {self.balance}원"

my_acc = BankAccount("홍길동", 10000)
print(my_acc) # [홍길동] 잔액 : 10000원

# [문제 2] 문제 1의 BankAccount 를 상속받아 SavingsAccount 클래스를 작성하세요.
# 추가 속성: interest_rate(이자율, 예: 0.03 = 3%)
# 추가 메서드:
#   - apply_interest(): 잔액에 이자율만큼 이자를 더하고 "이자 적용: +<이자>원" 출력
# __str__ 오버라이딩: "[적금 - <owner>] 잔액: <balance>원 (이자율: <rate>%)" 형식
# 코드 작성 ↓

class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, interest_rate=0.03):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        print(f"이자 적용 : +{interest}원")

    def __str__(self):
        return f"[적금 - {self.owner}] \n잔액 : {self.balance}원(이자율 : {self.interest_rate*100}%)"


# [문제 3] Product 클래스를 작성하세요.
# 속성: name, price
# 클래스 변수: total_products = 0 (생성될 때마다 증가)
# 클래스 메서드: get_total() → "총 상품 수: <N>개" 출력
# 정적 메서드: is_expensive(price) → price > 100000 이면 True 반환
# __lt__ 정의: price 기준 비교 (sorted() 사용 가능하도록)
# 코드 작성 ↓
class Product:
    total_products = 0

    def __init__(self, name, price):
        self.name = name
        self.price = price
        Product.total_products += 1

    @classmethod
    def get_total(cls):
        print(f"총 상품 수: {cls.total_products}개")

    @staticmethod
    def is_expensive(price):
        return price > 100000
    
    def __lt__(self, other):
        return self.price < other.price
    


# [문제 4] 아래 요구사항을 만족하는 클래스 설계를 직접 해보세요.
# Shape(도형) 부모 클래스:
#   - 속성: color
#   - 메서드: describe() → "<color> 색의 도형입니다." 출력
#   - area() → 0 반환 (자식에서 오버라이딩 예정)
#
# Circle(원) 자식 클래스:
#   - 추가 속성: radius(반지름)
#   - area() 오버라이딩: 원의 넓이 반환 (π * r²)
#   - __str__: "원 (반지름: <radius>, 넓이: <area>)"
#
# Rectangle(직사각형) 자식 클래스:
#   - 추가 속성: width, height
#   - area() 오버라이딩: 가로 * 세로
#   - __str__: "직사각형 (<width>x<height>, 넓이: <area>)"
# 코드 작성 ↓
import math

class Shape:
    def __init__(self, color):
        self.color = color
    
    def describe(self):
        print(f"{self.color} 색의 도형입니다.")

    def area(self):
        return 0
    
class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2
    
    def __str__(self):
        return f"원 (반지름 : {self.radius}, 넓이 : {self.area()})"
    
class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
    
    def __str__(self):
        return f"직사각형 ({self.width}*{self.height}, 넓이 : {self.area()})"