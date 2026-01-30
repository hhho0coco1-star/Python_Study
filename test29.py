# 사용자 예외 처리, 파일 입출력

class NickNameError(Exception):
    pass

def checkNickName(name):
    if name == "as":
        raise NickNameError
    
nickname = input("nickname : ")

try:
    checkNickName(nickname)
except NickNameError:
    print("xxx")

# 파일 입출력( 파일 객체  = open("경로", "목적") )
# w : 해당 경로 내용 덮어쓰기(기존 내용 삭제)
# a : 해당 경로 내용 추가하기(기존 내용 유지)
# r : 해당 경로 내용 읽기(해당 경로에 파일이 없으면 오류)

# 출력하기
#   파일 객체.write("문자열")

# 입력하기
#   파일 객체.readlines()

# close(): 버퍼를 비워주어야 파일에 적용된다.

# 절대 경로 / 상대 경로
# 절대 경로 : 내 위치가 어디든 찾아갈 수 있는 경로
# 상대 경로 : 내 위치에 따라 경로가 변경된다.
#  .: 현재 위치
#  ..: 이전 폴더
name_file = open("name.txt", "w")
name_file.write("안세웅")
name_file.close()

name_file = open("name.txt", "r")
for i in name_file.readlines():
    print(i, end="")
