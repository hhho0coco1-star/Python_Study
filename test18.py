# list 사용

# 값 넣기 : list.dppend(값) - 맨 뒤 값 추가
# 값 삽입 : list.insert(인덱스번호, 값)

# 값 삭제 : list.remove(값) - 값이 중복될 경우, 앞에 있는 것부터 삭제한다.
# del list[인덱스번호]

# list.clear() 모든 값 삭제

# 값 검색 list.index(값) - 중복될 경우 좌에서 우방향으로 가장 먼저 나온 값 번호를 가져온다.

# 값 수정 list[인덱스번호] = 새로운 값

# for문 사용
# for i in range(len(list명)):
    # list[i]

# 향상된 for문 / for each문
    # for i in list:

# 값 유무 확인
# 값 in list : True or False
# 값 not in list

dataList = [1, 2, 3, 4]
print(len(dataList)) # 리스트 길이
print(dataList[1])

dataList.append(5)
print(dataList)

dataList.insert(2, 3)
print(dataList)

# dataList.clear()
# print(dataList)

print(dataList[-1]) # 리스트 가장 맨 마지막 값

print(dataList[0:3]) # 0 1 2 인덱스 출력
print(type(dataList))

dataList02 = [0] * 100
print(len(dataList02))

dataList03 = list(range(5))
print(dataList03)
