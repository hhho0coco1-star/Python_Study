# ============================================================
# Stage 1 - 06. 파일 I/O (File Input/Output)
# ============================================================

# --- 파일 쓰기 (w 모드: 새로 쓰기, 기존 내용 덮어씀) ---
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("첫 번째 줄\n")
    f.write("두 번째 줄\n")
    f.write("세 번째 줄\n")
# with 블록을 벗어나면 자동으로 파일이 닫힘 (f.close() 불필요)


# --- 파일 읽기 (r 모드: 읽기 전용) ---
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 전체 내용을 문자열 하나로 읽기
print(content)
# 출력:
# 첫 번째 줄
# 두 번째 줄
# 세 번째 줄


# --- readlines(): 줄 단위로 읽어서 리스트로 반환 ---
with open("sample.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()       # ['첫 번째 줄\n', '두 번째 줄\n', '세 번째 줄\n']
print(lines)
print(lines[0].strip())        # '첫 번째 줄' (줄바꿈 제거)


# --- for 루프로 한 줄씩 읽기 (대용량 파일에 효율적) ---
with open("sample.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())    # 한 줄씩 출력


# --- 파일 추가 (a 모드: 기존 내용 유지하고 뒤에 이어 씀) ---
with open("sample.txt", "a", encoding="utf-8") as f:
    f.write("네 번째 줄 (추가)\n")


# --- writelines(): 리스트를 한 번에 쓰기 ---
data = ["사과\n", "바나나\n", "체리\n"]
with open("fruits.txt", "w", encoding="utf-8") as f:
    f.writelines(data)         # 줄바꿈은 직접 포함해야 함


# --- 파일 모드 정리 ---
# "r"  : 읽기 전용 (파일 없으면 에러)
# "w"  : 쓰기 전용 (파일 없으면 생성, 있으면 덮어씀)
# "a"  : 추가 쓰기 (파일 없으면 생성, 있으면 뒤에 이어 씀)
# "rb" : 바이너리 읽기 (이미지, 동영상 등)
# "wb" : 바이너리 쓰기


# --- os 모듈로 파일/폴더 다루기 ---
import os

print(os.path.exists("sample.txt"))    # 파일 존재 여부: True
print(os.path.getsize("sample.txt"))   # 파일 크기 (바이트)

os.makedirs("test_dir", exist_ok=True) # 폴더 생성 (이미 있어도 에러 안 남)
print(os.listdir("."))                 # 현재 폴더의 파일/폴더 목록


# ============================================================
# 실습 문제
# ============================================================

# [문제 1] "score.txt" 파일에 아래 성적 데이터를 한 줄씩 저장하세요.
# 저장 형식: "이름,점수" (예: 철수,85)
scores = [("철수", 85), ("영희", 92), ("민준", 78), ("지아", 95)]
# 코드 작성 ↓
with open("score.txt", "w", encoding="utf-8") as f:
    for name, score in scores:
        f.write(f"{name},{score}\n")


# [문제 2] 위에서 만든 "score.txt"를 읽어서
# 평균 점수와 최고 점수를 출력하세요.
# 출력 예:
# 평균: 87.5점
# 최고: 95점 (지아)
# 코드 작성 ↓
total_score = 0
max_score = 0
max_name = ""
count = 0
with open("score.txt", "r", encoding="utf-8") as f:
    for line in f:
        name, score_str = line.strip().split(",")
        score = int(score_str)
        total_score += score
        count += 1
        if score > max_score:
            max_score = score
            max_name = name

avg_score = total_score / count 
# 파일만 독립적으로 읽는 상황에서는 깨질 수 있어요. 파일을 읽으면서 카운터를 직접 세는 게 더 견고합니다:
"""
count = 0
with open("score.txt", "r", encoding="utf-8") as f:
    for line in f:
        ...
        count += 1
avg_score = total_score / count
"""

print(f"평균 : {avg_score:.1f}점")
print(f"최고 : {max_score} 점 ({max_name})")


# [문제 3] "log.txt" 파일에 아래 메시지를 3번 반복해서 추가(append)하세요.
# 각 줄 형식: "[1회] 시스템 정상 작동"  "[2회] 시스템 정상 작동" ...
# 코드 작성 ↓
with open("log.txt", "a", encoding="utf-8") as f:
    for i in range(1, 4):
        f.write(f"[{i}회] 시스템 정상 작동\n")


# [문제 4] os 모듈을 사용해서 "score.txt" 파일이 존재하면
# 파일 크기(바이트)를 출력하고, 없으면 "파일이 없습니다."를 출력하세요.
# 코드 작성 ↓
if os.path.exists("score.txt"):
    size = os.path.getsize("score.txt")
    print(f"파일 크기 : {size} 바이트")
else:
    print("파일이 없습니다.")
