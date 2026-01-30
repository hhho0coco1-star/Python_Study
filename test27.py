# 상속
# 기존에 사용중인 클래스의 필드 중
# 새롭게 만든 클래스에서 필요한 것들이 있다면 
# 상속을 받아서 그대로 상속한다.

# 여러 클래스를 선언할 때 중복되는 기능들이 존재한다면
# 공통 기능들을 담아놓을 클래스를 선언한다

# class A(B, C):
    # 필드

# 다중 상속 : 부모 클래스가 한 개가 아니라 여러 개이다.
# 모호성 : 여러 부모의 필드 중 같은 이름의 필드를 자식 클래스에서 사용한다면
# 어느 부모의 필드인지 알 수 없기 때문에 이러한 성질을 모호성이라고 한다.

# 생성자
# 부모 클래스 생성자가 선언되어 있고,
# 자식 클래스에는 기본 생성자가 있다면, 부모 클래스 생성자를
# 자동으로 호출해준다. 하지만 자식 클래스에서 생성자를 직접 선언하면
# 부모 생성자를 자식 생성자에서 직접 호출해주어야 한다.

# 자식 클래스 생성자가 있을 때
#   부모에 있는 필드와 자식에서 필요한 필드가 있을 때
#   부모 생성자를 호출하여 부모 필드를 초기화 해주고
#   추가된 자식 필드를 추가로 초기화 해주어야 할 때

# 자식 클래스에 생성자가 없을 때(기본 생성자만 있을 때)
#   부모 생성자를 그대로 사용

class A:
    def __init__(self, data = 10):
        self.data = data

    def printData(self):
        print(self.data)

    def show(self):
        print("부모")

class B(A): # 상속
    pass
    def __init__(self, data, data2):
        super().__init__(data) # == # A.__init__(self, data)
        self.data2 = data2
    
    def printData2(self):
        print(self.data, self.data2)

    #Overriding
    def printData(self):
        print(self.data, self.data2)

# b = B()
# b.printData()

b = B(30, 20)
b.printData()