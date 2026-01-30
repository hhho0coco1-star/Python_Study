# 상속 심화

class Car:
    def __init__(self, brand, color, price):
        self.brand = brand
        self.color = color
        self.price = price

class sCar(Car):
    def __init__(self, brand, color, price, mode):
        super().__init__(brand, color, price)
        self.mode = mode

class A:
    seq = 0

    def __init__(self):
        A.seq += 1
        self.num = A.seq

    def test(self):
        self.seq = 10

# 예외처리
# 에러 : 심각한 오류
# 예외 : 덜 심각한 오류
# try:
#   오류가 발생할 수 있는 문장
# except Exception as e: // alias:별칭
    # 오류 발생 시 실행한 문장

# except 모든 예외 클래스의 부모 클래스는 Exception
