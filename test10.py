# 삼항 연산자
# 참 if 조건식 else 거짓 : 통채로를 값으로 봐야 한다.
# 값1 if 조건식 else 값2

num1 = 3
num2 = 2

result01 = num1 if num1 > num2 else num2
print("{result}".format(result=result01))

# 삼항 연산자(중첩)
result01 = num1 if num1 > num2 else '==' if num1 == num2 else num2

# 연산과 연결
# print('10' + 9) 문자열은 문자열끼리 연결 가능하다
print('10' + str(9))