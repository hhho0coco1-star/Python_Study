# 함수 심화
# list.append(x) : 리스트 추가
# return num1, num2 - 소괄호()가 생략되었으며, tuple로 반환한다.
# return 가져온 tuple 값은 인덱스로 접근한다.

def changeToInteger(hangle):
    hangle_org = "공일이삼사오육칠팔구"
    result = ""
    
    for i in hangle:
        result += str(hangle_org.index(i))
    return int(result)
# .index(인덱스 위치?) : 반환
print(changeToInteger("일공이사"))

def add(num1, num2=0): # 기본값 설정은 앞이 아니라 뒤에 설정한다
    return num1 + num2

# 전역변수
result = 0
def sub(num1, num2):
    global result
    result = num1 - num2

#               전역변수      지역변수
# 함수 내 읽기  가능            가능
# 함수 내 수정  불가            가능

# 함수 밖 읽기  가능            불가능
# 함수 밖 수정  가능            불가능