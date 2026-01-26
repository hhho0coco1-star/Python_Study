# list3
dataList = [0] * 100

for i in range(100):
    dataList[i] = i + 1

print(dataList)

dataList02 = [0] * 50

for i in range(len(dataList02)):
    dataList02[i] = (i+1) * 2

print(dataList02)

dataList03 = []

for i in range(6):
    dataList03.append(chr(65 + i))

print(dataList03)

dataList04 = []

for i in range(5):
    if i > 1 :
        i += 1
    dataList04.append(chr(65 + i))

print(dataList04)

strList = "ABC"
print(strList.replace("B", "Z"))
# replace 변환

num = int(input("자연수 입력 : "))
hangle = "공일이삼사오육칠팔구"

while num != 0:
    result += hangle[num % 10]
    num //= 10

print(result)