data = "%d" %100 # 문자열 타입(str)
print(data)
print(type(data))

# format 함수
data1 = 10
print("data1 : {}".format(data1))
print("{} : {}".format(data, data1))

str01 = 'A'
str02 = "ABC"

print("%s" %str01)
print("%c" %str01)

print("%s" %str02)
# print("%c" %str02) type error

# 아스키코드
print("data : %c" %65)
print("data : %c" %97)

# 자동 형변환 / 강제 형변환
# 정수 + 실수 = 실수 (자동)

# // 몫 연산자

print(float(10)//3) # 강제 형변환

