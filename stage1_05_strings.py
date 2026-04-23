# ============================================================
# Stage 1 - 05. 문자열 (Strings)
# ============================================================

# --- f-string (가장 많이 쓰는 포맷팅) ---
name = "김철수"
age = 28
print(f"이름: {name}, 나이: {age}")        # 이름: 김철수, 나이: 28
print(f"내년 나이: {age + 1}")             # 내년 나이: 29
print(f"{'왼쪽':<10}")                     # 왼쪽 정렬 (10칸)
print(f"{3.14159:.2f}")                    # 소수점 2자리: 3.14
print(f"{1000000:,}")                      # 천 단위 콤마: 1,000,000


# --- 자주 쓰는 문자열 메서드 ---
s = "  Hello, Python World!  "

print(s.strip())            # 양쪽 공백 제거
print(s.lower())            # 소문자
print(s.upper())            # 대문자
print(s.replace("Python", "파이썬"))  # 치환

sentence = "apple,banana,cherry"
parts = sentence.split(",")         # 분리 → 리스트
print(parts)                        # ['apple', 'banana', 'cherry']
print("-".join(parts))              # 합치기 → 'apple-banana-cherry'
# "".join : 빈 문자열로 합치기 => 'applebananacherry'

print("Python" in s)       # 포함 여부: True
print(s.strip().startswith("Hello"))  # 시작 확인: True
print(s.strip().endswith("!"))        # 끝 확인: True
print(s.strip().count("o"))           # 'o' 개수: 2


# --- 슬라이싱 ---
s = "Hello, Python!"

print(s[0:5])      # Hello
print(s[7:])       # Python!
print(s[:5])       # Hello
print(s[-7:])      # Python!
print(s[::-1])     # !nohtyP ,olleH (뒤집기)


# --- 문자열은 불변 (immutable) ---
s = "hello"
# s[0] = "H"  # TypeError! 문자열은 변경 불가
s = s[0].upper() + s[1:]  # 새 문자열 생성
print(s)  # Hello


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] 아래 문자열에서 이름, 나이, 직업을 f-string으로 출력하세요.
# 출력 형식: "홍길동(30세)의 직업은 개발자입니다."
person_name = "홍길동"
person_age = 30
person_job = "개발자"
# 코드 작성 ↓
print(f"{person_name}({person_age}세)의 직업은 {person_job}입니다.")


# [문제 2] 아래 문자열을 처리해서 단어 개수를 출력하세요.
# (앞뒤 공백 제거 후 단어 분리)
text = "  파이썬은 배우기 쉽고 강력한 언어입니다  "
# 코드 작성 ↓
words = text.strip().split() # 공백 제거 후 단어 분리
print(f"단어 개수: {len(words)}") # 단어 개수 출력


# [문제 3] 아래 이메일 주소에서 아이디(@ 앞)와 도메인(@ 뒤)을 분리해서 출력하세요.
email = "kimcheolsu@gmail.com"
# 출력 예:
# 아이디: kimcheolsu
# 도메인: gmail.com
# 코드 작성 ↓
user_id, domain = email.split("@") # '@' 기준으로 분리
print(f"아이디: {user_id}") # 아이디 출력
print(f"도메인: {domain}") # 도메인 출력


# [문제 4] 아래 문장에서 각 단어의 첫 글자만 대문자로 바꿔서 출력하세요.
# (파이썬 내장 메서드 하나로 가능합니다)
sentence = "hello world from python"
# 코드 작성 ↓
capitalized_sentence = sentence.title() # 각 단어의 첫 글자 대문자로 변환
print(capitalized_sentence) # 결과 출력
