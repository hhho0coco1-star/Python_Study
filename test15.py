# 기타 제어문
# break : 반복문 탈출
# continue : 아래 문장을 하지 않고 다음 반복

for i in range(100):
    if  (i+1) % 3 == 0 and (i+1) % 5 == 0:
        print(i+1)