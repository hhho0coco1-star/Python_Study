# 관계 연산자
isTrue = 10 == 11
print(isTrue)

# 논리 연산자
isTrue02 = 10 == 11 and 10 > 1
isTrue03 = 10 == 11 or 10 > 1

print(isTrue02)
print(isTrue03)

# 논리 연산자
# & and : 두 비트가 모두 1이면 1
# | or : 둘 중 하나라도 1이면 1
# ^ xor : 두 비트가 서로 다르면 1

# 단항 연산자
# ~ not : 0 -> 1 / 1 -> 0
num1 = ~10
# -1010
#  0110
# -1001(9)
# ~a = -a-1
print(num1)

# 부호비트 : 0 양수 1 음수
