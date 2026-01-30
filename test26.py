# 클래스

class A:
    data = 10

    def prinData(self): # self : 나 자신
        print(self)
        print(self.data)
    def intro():
        print("aaa")

obj1 = A()
obj2 = A()

obj1.data = 20
obj1.prinData()
print(obj2)
obj2.prinData()

class Car:
    brand = ""
    color = ""
    price = 0

    def __init__(self, brand, color, price): # 초기화 목적
        self.brand = brand
        self.color = color
        self.price = price