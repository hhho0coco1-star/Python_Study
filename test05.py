# chr(정수) : 정수 -> 문자
# ord(문자) : 문자 -> 정수

print(chr(ord('A') * 3)) # 65(아스키코드) * 3

# 암호화
pw = "a1b2c3"
en_pw = ""
de_pw = ""

for i in pw :
    en_pw += chr(ord(i) * 9)

print("{pw}".format(pw=en_pw))

# 복호화
for i in en_pw :
    de_pw += chr(ord(i) // 9)

print("{pw}".format(pw=de_pw))

# 입력함수(input)
name = input("이름 : ")
print(name)