# 논리 연산자
# & 논리곱
# | 논리합
#  ^ 배타논리합

# 단항 연산자
# ~ 논리 부정

# 쉬프트 연산자
# >> 오른쪽으로 이동
# << 왼쪽으로 이동

print(0.1 + 0.2) # 0.30000000000000004
print(0.1 + 0.2 == 0.3) # False

print("%f" %0.3)

# 실수의 오류 해결
import math

float01 = math.isclose(0.1 + 0.2, 0.3) # True
print(float01)

# 실수의 오류 해결2
from decimal import Decimal
print(float(Decimal('0.1') + Decimal('0.2')))