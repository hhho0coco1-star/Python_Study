# list and tuple
# list : 변할 수 있는 [ ]
# tuple : 변할 수 없는 ( ) 소괄호 생략 가능

dataTuple = 1, 2, 3
dataTuple2 = dataTuple

dataTuple += 4, 5

print(dataTuple)

# dict
# 한 쌍으로 저장되어 관리한다.
# len() 사용하면 한 쌍을 1로 카운트 한다
# 키 값은 중복이 될 수 없으며, 값은 중복이 가능하다

# dict 선업
    # dict = {key: value}

# dict 사용
# 추가(키 값이 없을 때)
# dict[키] = 값
# 수정(키 값이 있을 때)
# dict[키] = 값
# 삭제(한 쌍이 삭제된다)
# del dict명[키]
# 검색
    # 키 in dict
    # 키 not in

    # key 분리 list(dict명.keys())
    # value 분리 dict명.values()

중국집 = {"자장면" : 1500, "짬뽕" : 2500}
print(len(중국집))
print(중국집["자장면"])