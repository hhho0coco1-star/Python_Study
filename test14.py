# for문 2
# start가 0일 때에는 생략이 가능하다.
# step이 1일 때에는 생략이 가능하다.

# for i in range(0, 6, 1):
#     print("%c" %(i+65))

for i in range(5): # start, step 생략 
    if i > 1:
        i += 1
    print(chr(i + 65))