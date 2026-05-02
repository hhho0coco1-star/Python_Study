print("hello", end="")
print("hello")
print("hello")

# 서식문자
# %d(정수) %f(실수) %c(문자) %s(문자열)
# %o(8진수) %x(16진수)

for i in range(2, 5): # 2 3 4
    for j in range(1, 10): # 1 2 3 4 5 6 7 8 9
        print(f"{i} * {j} = {(i*j)}")