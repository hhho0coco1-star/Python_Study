# ============================================================
# Stage 3 - 03. 시각화 (Matplotlib & Seaborn)
# ============================================================
# Matplotlib: 파이썬 기본 시각화 라이브러리 (저수준, 세밀한 제어)
# Seaborn   : Matplotlib 기반, 통계 시각화 특화 (고수준, 간결한 코드)
#
# 설치: pip install matplotlib seaborn

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd

# 한글 폰트 설정 (Windows)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False


# ============================================================
# [이론 1] Matplotlib 기본 — 선 그래프 & 산점도
# ============================================================
#
# plt.plot(x, y)          → 선 그래프
# plt.scatter(x, y)       → 산점도
#
# 꾸미기 옵션:
#   title='제목'           → 그래프 제목
#   xlabel='x축 이름'      → x축 레이블
#   ylabel='y축 이름'      → y축 레이블
#   color='색상'           → 색상 (red, blue, green, #FF0000 등)
#   linewidth=숫자         → 선 두께
#   marker='o'            → 점 마커 (o, s, ^, * 등)
#   label='범례명'         → 범례 이름
#   linestyle='--'         → 선 스타일 (-, --, :, -. 등)
#
# plt.legend()            → 범례 표시
# plt.grid(True)          → 격자 표시
# plt.show()              → 그래프 출력
# plt.savefig('파일명.png') → 이미지 저장

x = [1, 2, 3, 4, 5]
y1 = [2, 4, 6, 8, 10]
y2 = [1, 3, 5, 4, 7]

plt.figure(figsize=(8, 5))   # 그래프 크기 설정 (가로, 세로 인치)
plt.plot(x, y1, color='blue', linewidth=2, marker='o', label='데이터1')
plt.plot(x, y2, color='red', linestyle='--', marker='s', label='데이터2')
plt.title('선 그래프 예시')
plt.xlabel('X축')
plt.ylabel('Y축')
plt.legend()
plt.grid(True)
plt.show()

# 산점도
np.random.seed(42)
x = np.random.randn(100)
y = x * 2 + np.random.randn(100)

plt.figure(figsize=(6, 5))
plt.scatter(x, y, color='purple', alpha=0.6)   # alpha: 투명도 (0~1)
plt.title('산점도 예시')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()


# ============================================================
# [실습 1] 선 그래프
# ============================================================
# 아래 데이터를 사용하세요.
months = [1, 2, 3, 4, 5, 6]
sales_a = [150, 180, 200, 170, 220, 250]
sales_b = [120, 140, 160, 190, 175, 210]

# 1) A제품과 B제품의 월별 판매량을 한 그래프에 선 그래프로 그리세요.
def plot_sales(months, sales_a, sales_b):
    plt.figure(figsize=(8, 5)) # 그래프 크기 설정
    plt.plot(months, sales_a, color='blue', linewidth=2, marker='o', label='A제품') # A제품 선 그래프
    plt.plot(months, sales_b, color='red', linestyle='--', marker='s', label='B제품') # B제품 선 그래프
    plt.title('월별 제품 판매량') # 그래프 제목
    plt.xlabel('월') # x축 레이블
    plt.ylabel('판매량') # y축 레이블
    plt.legend() # 범례 표시
    plt.grid(True) # 격자 표시
    plt.show() # 그래프 출력
# 2) 제목: '월별 제품 판매량', x축: '월', y축: '판매량'
plot_sales(months, sales_a, sales_b)


# 코드 작성 ↓



# ============================================================
# [이론 2] 막대 그래프 & 히스토그램
# ============================================================
#
# 막대 그래프:
#   plt.bar(x, height)         → 수직 막대
#   plt.barh(y, width)         → 수평 막대
#
# 히스토그램:
#   plt.hist(data, bins=10)    → 구간 수(bins)에 따라 빈도 분포 표시
#   edgecolor='black'          → 막대 테두리 색상

categories = ['사과', '바나나', '포도', '딸기']
values = [40, 70, 30, 55]

plt.figure(figsize=(7, 4))
plt.bar(categories, values, color=['red', 'yellow', 'purple', 'pink'])
plt.title('과일 판매량')
plt.ylabel('판매량')
plt.show()

# 히스토그램
data = np.random.normal(loc=70, scale=15, size=300)   # 평균 70, 표준편차 15, 300개

plt.figure(figsize=(7, 4))
plt.hist(data, bins=20, color='steelblue', edgecolor='black')
plt.title('점수 분포')
plt.xlabel('점수')
plt.ylabel('빈도')
plt.show()


# ============================================================
# [실습 2] 막대 그래프 & 히스토그램
# ============================================================
# 1) 아래 데이터로 수평 막대 그래프(barh)를 그리세요.
#    제목: '부서별 평균 연봉', x축: '연봉(만원)'
departments = ['개발', '마케팅', '영업', '인사']
avg_salary = [520, 430, 460, 400]

plt.figure(figsize=(8, 4)) # 그래프 크기 설정
plt.barh(departments, avg_salary, color=['blue', 'green', 'orange', 'purple']) # 수평 막대 그래프
plt.title('부서별 평균 연봉') # 그래프 제목
plt.xlabel('연봉(만원)') # x축 레이블
plt.show() # 그래프 출력

# 2) np.random.normal(mean=60, scale=10, size=200)으로 데이터를 생성하고
#    bins=15인 히스토그램을 그리세요.
#    제목: '시험 점수 분포', x축: '점수', y축: '학생 수'
# 코드 작성 ↓
np.random.seed(42) # 재현 가능한 결과를 위해 시드 설정
scores = np.random.normal(loc=60, scale=10, size=200) # 평균 60, 표준편차 10, 200 개
plt.figure(figsize=(8, 5)) # 그래프 크기 설정
plt.hist(scores, bins=15, color='skyblue', edgecolor='black') # 히스토그램
plt.title('시험 점수 분포') # 그래프 제목
plt.xlabel('점수') # x축 레이블
plt.ylabel('학생 수') # y축 레이블
plt.show() # 그래프 출력


# ============================================================
# [이론 3] 서브플롯 (여러 그래프 한 번에)
# ============================================================
#
# plt.subplot(행, 열, 번호)   → 그리드에서 번호 위치에 그래프
# plt.subplots(행, 열)        → fig, axes 객체 반환 (권장 방식)
#
# axes[i].plot(...)           → i번째 서브플롯에 그래프 그리기
# plt.tight_layout()          → 서브플롯 간격 자동 조정

fig, axes = plt.subplots(1, 2, figsize=(12, 4))  # 1행 2열

x = [1, 2, 3, 4, 5]

axes[0].plot(x, [i**2 for i in x], color='blue', marker='o') # x : 1, 2, 3, 4, 5 / y : 1, 4, 9, 16, 25
axes[0].set_title('제곱 함수')
axes[0].set_xlabel('x')
axes[0].set_ylabel('x²')

axes[1].bar(['A', 'B', 'C'], [10, 25, 15], color=['red', 'green', 'blue'])
axes[1].set_title('막대 그래프')

plt.tight_layout()
plt.show()


# ============================================================
# [실습 3] 서브플롯
# ============================================================
# 1행 3열 서브플롯을 만드세요.
#   - 첫 번째: months vs sales_a 선 그래프 (제목: 'A제품')
#   - 두 번째: months vs sales_b 선 그래프 (제목: 'B제품')
#   - 세 번째: 두 제품의 막대 그래프 비교
#              x축: ['1월', '2월', '3월', '4월', '5월', '6월']
# tight_layout 적용 후 출력하세요.
months = [1, 2, 3, 4, 5, 6]
sales_a = [150, 180, 200, 170, 220, 250]
sales_b = [120, 140, 160, 190, 175, 210]
# 코드 작성 ↓
fig, axes = plt.subplots(1, 3, figsize=(18, 5)) # 1행 3열 서브플롯
# 첫 번째 서브플롯 - A제품 선 그래프
axes[0].plot(months, sales_a, color='blue', marker='o')
axes[0].set_title('A제품') # 제목 설정
axes[0].set_xlabel('월') # x축 레이블
axes[0].set_ylabel('판매량') # y축 레이블
# 두 번째 서브플롯 - B제품 선 그래프
axes[1].plot(months, sales_b, color='red', linestyle='--', marker='s')
axes[1].set_title('B제품')
axes[1].set_xlabel('월')
axes[1].set_ylabel('판매량')
# 세 번째 서브플롯 - 두 제품의 막대 그래프 비교
x_labels = ['1월', '2월', '3월', '4월', '5월', '6월']
x = np.arange(len(months)) # x축 위치
width = 0.35
axes[2].bar(x - width/2, sales_a, width, label='A제품', color='blue')
axes[2].bar(x + width/2, sales_b, width, label='B제품', color='red')
axes[2].set_title('제품 비교')
axes[2].set_xticks(x)
axes[2].set_xticklabels(x_labels) # 눈금 위치에 '1월'~'6월' 글자 입히기
axes[2].legend()
plt.tight_layout()
plt.show()



# ============================================================
# [이론 4] Seaborn 기본
# ============================================================
#
# Seaborn은 DataFrame을 바로 넣을 수 있어 편리
#
# sns.histplot(data, x='컬럼')     → 히스토그램 (kde=True: 밀도 곡선 추가)
# sns.boxplot(data, x='그룹', y='값') → 박스플롯 (분포, 이상치 확인)
# sns.scatterplot(data, x=, y=, hue='그룹') → 산점도 (hue: 색상으로 그룹 구분)
# sns.heatmap(df.corr(), annot=True) → 상관관계 히트맵
#
# sns.set_theme()                  → Seaborn 기본 스타일 적용

sns.set_theme()

# 내장 데이터셋 사용
tips = sns.load_dataset('tips')   # 식당 팁 데이터
print(tips.head())
# total_bill: 총 금액, tip: 팁, sex: 성별, smoker: 흡연여부, day: 요일, time: 점심/저녁

# 히스토그램 + 밀도 곡선
plt.figure(figsize=(7, 4))
sns.histplot(tips, x='total_bill', bins=20, kde=True)
plt.title('총 금액 분포')
plt.show()

# 박스플롯
plt.figure(figsize=(7, 4))
sns.boxplot(data=tips, x='day', y='total_bill')
plt.title('요일별 총 금액 분포')
plt.show()

# 산점도 (hue로 그룹 구분)
plt.figure(figsize=(7, 5))
sns.scatterplot(data=tips, x='total_bill', y='tip', hue='sex')
plt.title('총 금액 vs 팁')
plt.show()


# ============================================================
# [실습 4] Seaborn
# ============================================================
# tips 데이터셋을 사용하세요.
# tips = sns.load_dataset('tips')
#
# 1) total_bill 히스토그램을 kde=True 옵션으로 그리세요.
#    제목: '총 금액 분포'
# 2) 흡연 여부(smoker)에 따른 팁(tip) 박스플롯을 그리세요.
#    제목: '흡연 여부에 따른 팁'
# 3) total_bill vs tip 산점도를 time(점심/저녁)으로 색상 구분해서 그리세요.
#    제목: '식사 시간대별 금액-팁 관계'
# 코드 작성 ↓
tips = sns.load_dataset('tips')

plt.figure(figsize=(7, 4))
sns.histplot(tips, x='total_bill', bins=20, kde=True)
plt.title('총 금액 분포')
plt.show()

plt.figure(figsize=(7, 4))
sns.boxplot(data=tips, x='smoker', y='tip')
plt.title('흡연 여부에 따른 팁')
plt.show()

plt.figure(figsize=(7, 5))
sns.scatterplot(data=tips, x='total_bill', y='tip', hue='time')
plt.title('식사 시간대별 금액-팁 관계')
plt.show()


# ============================================================
# [이론 5] 히트맵 & 상관관계
# ============================================================
#
# 상관관계: 두 변수 간의 선형 관계 강도 (-1 ~ +1)
#   +1에 가까울수록 양의 상관, -1에 가까울수록 음의 상관
#
# df.corr()                          → 수치형 컬럼 간 상관계수 계산
# sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
#   annot=True  → 셀 안에 수치 표시
#   fmt='.2f'   → 소수 둘째 자리까지 표시
#   cmap        → 색상 맵 (coolwarm, Blues, RdYlGn 등)

tips = sns.load_dataset('tips')
numeric_tips = tips.select_dtypes(include='number')  # 수치형 컬럼만 선택
corr = numeric_tips.corr()
print(corr)

plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm')
plt.title('팁 데이터 상관관계')
plt.show()


# ============================================================
# [실습 5] 히트맵 & 상관관계
# ============================================================
# 아래 데이터를 사용하세요.
students = pd.DataFrame({
    '공부시간': [2, 5, 3, 8, 1, 6, 4, 7],
    '수면시간': [8, 6, 7, 5, 9, 6, 7, 5],
    '시험점수': [55, 80, 65, 95, 45, 85, 70, 90],
    '결석횟수': [3, 1, 2, 0, 5, 1, 2, 0]
})
# 1) 상관계수 행렬을 출력하세요.
# 2) 히트맵을 그리세요. (annot=True, cmap='Blues')
#    제목: '학습 데이터 상관관계'
# 3) 공부시간 vs 시험점수 산점도를 그리세요.
#    제목: '공부시간과 시험점수의 관계'
# 코드 작성 ↓
corr = students.corr()
print(corr)

plt.figure(figsize=(6, 5))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='Blues')
plt.title('학습 데이터 상관관계')
plt.show()

plt.figure(figsize=(6, 5))
plt.scatter(students['공부시간'], students['시험점수'], color='steelblue', s=80)
plt.title('공부시간과 시험점수의 관계')
plt.xlabel('공부시간')
plt.ylabel('시험점수')
plt.show()
