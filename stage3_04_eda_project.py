# ============================================================
# Stage 3 - 04. EDA 실전 프로젝트 (탐색적 데이터 분석)
# ============================================================
# EDA(Exploratory Data Analysis): 데이터를 분석하기 전에
# 통계·시각화로 데이터의 구조, 분포, 패턴, 이상치를 파악하는 과정
#
# 사용 라이브러리: pandas, numpy, matplotlib, seaborn
# 데이터셋: 타이타닉 (seaborn 내장)
#
# EDA 순서
#   1. 데이터 로드 & 기본 정보 확인
#   2. 결측치 확인 & 처리
#   3. 수치형 변수 분포 확인
#   4. 범주형 변수 분포 확인
#   5. 변수 간 관계 분석 (상관관계, 그룹 비교)
#   6. 인사이트 정리

import pandas as pd                  # 데이터프레임 처리 라이브러리
import numpy as np                   # 수치 연산 라이브러리
import matplotlib.pyplot as plt      # 그래프 출력 라이브러리
import matplotlib                    # 폰트 등 전역 설정용
import seaborn as sns                # 통계 시각화 라이브러리

matplotlib.rcParams['font.family'] = 'Malgun Gothic'   # 한글 폰트 설정 (Windows)
matplotlib.rcParams['axes.unicode_minus'] = False       # 마이너스 기호 깨짐 방지
sns.set_theme()                                         # seaborn 기본 테마 적용


# ============================================================
# [이론 1] 데이터 로드 & 기본 정보 확인
# ============================================================
#
# df.shape          → (행 수, 열 수)
# df.info()         → 컬럼명, 타입, 결측치 개수
# df.describe()     → 수치형 컬럼 기초 통계 (평균, 표준편차, 최솟값 등)
# df.head(n)        → 처음 n행 확인 (기본값 5)
# df.tail(n)        → 마지막 n행 확인
# df.columns        → 컬럼명 목록
# df.dtypes         → 각 컬럼의 데이터 타입

titanic = sns.load_dataset('titanic')   # seaborn 내장 타이타닉 데이터셋 로드

# 결측치 : 데이터 수집 or 저장 과정에서 누락되어 값이 비어 있는 상태

print("=== shape ===")
print(titanic.shape)           # (행 수, 열 수) 출력 → (891, 15)

print("\n=== 컬럼 목록 ===")
print(titanic.columns.tolist())   # 컬럼명을 리스트로 변환해서 출력

print("\n=== info ===")
titanic.info()   # 컬럼별 데이터 타입 + 결측치 없는 행 수 출력

print("\n=== describe ===")
print(titanic.describe())   # 수치형 컬럼의 기초 통계량 (평균, 표준편차, 최솟값, 사분위수, 최댓값)

print("\n=== head ===")
print(titanic.head())   # 데이터프레임의 상위 5행 출력

# 주요 컬럼 설명
# survived  : 생존 여부 (0=사망, 1=생존)
# pclass    : 객실 등급 (1=1등석, 2=2등석, 3=3등석)
# sex       : 성별
# age       : 나이
# sibsp     : 함께 탑승한 형제/배우자 수
# parch     : 함께 탑승한 부모/자녀 수
# fare      : 운임
# embarked  : 탑승 항구 (C=Cherbourg, Q=Queenstown, S=Southampton)


# ============================================================
# [실습 1] 데이터 기본 확인
# ============================================================
# 타이타닉 데이터를 로드한 후 아래를 출력하세요.
# 1) 전체 행/열 수
print(titanic.shape)
# 2) 각 컬럼의 데이터 타입
print(titanic.dtypes)
# 3) 수치형 컬럼의 기초 통계량
print(titanic.describe())   # describe()는 함수 호출 — 괄호 필수
# 코드 작성 ↓
"""
print(titanic.shape)        # 1) 전체 행/열 수 출력
print(titanic.dtypes)       # 2) 각 컬럼의 데이터 타입 출력
print(titanic.describe())   # 3) 수치형 컬럼의 기초 통계량 출력
"""

# ============================================================
# [이론 2] 결측치 확인 & 처리
# ============================================================
#
# df.isnull().sum()          → 컬럼별 결측치 개수
# df.isnull().mean() * 100   → 컬럼별 결측치 비율(%)
#
# 결측치 처리 방법:
#   df.dropna()                     → 결측치 있는 행 전체 삭제
#   df.dropna(subset=['컬럼명'])    → 특정 컬럼 기준으로 삭제
#   df['컬럼'].fillna(값)           → 특정 값으로 대체
#   df['컬럼'].fillna(df['컬럼'].mean())  → 평균으로 대체
#   df['컬럼'].fillna(df['컬럼'].median()) → 중앙값으로 대체
#   df['컬럼'].fillna(df['컬럼'].mode()[0]) → 최빈값으로 대체

print("\n=== 결측치 개수 ===")
print(titanic.isnull().sum())   # 각 컬럼에서 NaN(결측치)인 행 수 출력

print("\n=== 결측치 비율(%) ===")
print((titanic.isnull().mean() * 100).round(1))   # 결측치 비율(%) 소수점 1자리로 출력

titanic['age'] = titanic['age'].fillna(titanic['age'].median())
# age 결측치를 중앙값으로 대체 (평균보다 이상치 영향을 덜 받음)

titanic['embarked'] = titanic['embarked'].fillna(titanic['embarked'].mode()[0])
# embarked 결측치를 최빈값(가장 많이 등장한 항구)으로 대체 / mode()는 Series 반환 → [0]으로 첫 번째 값 추출

titanic = titanic.drop(columns=['deck'])
# deck 컬럼은 결측치가 77%로 너무 많아 분석에서 제외 (drop으로 컬럼 삭제)

print("\n=== 처리 후 결측치 ===")
print(titanic.isnull().sum())   # 결측치 처리 후 남은 결측치 수 재확인


# ============================================================
# [실습 2] 결측치 처리
# ============================================================
# 위에서 처리된 titanic 데이터를 기준으로:
# 1) 결측치가 남아 있는 컬럼을 확인하세요.
print(titanic.isnull().sum())
# 2) 'embark_town' 컬럼의 결측치를 최빈값으로 채우세요.
titanic['embark_town'] = titanic['embark_town'].fillna(titanic['embark_town'].mode()[0])
# 3) 처리 후 전체 결측치 합계를 출력하세요.
print(titanic.isnull().sum().sum())
# 코드 작성 ↓
print(titanic.isnull().sum())   # 1) 컬럼별 결측치 개수 출력 → 남아 있는 컬럼 확인
titanic['embark_town'] = titanic['embark_town'].fillna(titanic['embark_town'].mode()[0])
# 2) embark_town 결측치를 최빈값으로 대체 / mode()[0]으로 Series에서 첫 번째 최빈값 추출
print(titanic.isnull().sum().sum())   # 3) 전체 결측치 합계 출력 (.sum() 두 번: 컬럼별 합계 → 전체 합계)




# ============================================================
# [이론 3] 수치형 변수 분포 확인
# ============================================================
#
# 히스토그램    → 단일 변수 분포
# 박스플롯      → 분포 + 이상치 시각화
# KDE 곡선     → 히스토그램의 부드러운 버전

fig, axes = plt.subplots(1, 3, figsize=(16, 4))   # 1행 3열 서브플롯 생성, 가로 16인치 세로 4인치

sns.histplot(titanic['age'], bins=30, kde=True, ax=axes[0], color='steelblue')
# age 컬럼 히스토그램 / bins=30: 막대 30개 / kde=True: 밀도 곡선 추가 / ax=axes[0]: 첫 번째 칸에 그리기
axes[0].set_title('나이 분포')    # 첫 번째 서브플롯 제목
axes[0].set_xlabel('나이')        # 첫 번째 서브플롯 x축 레이블

sns.histplot(titanic['fare'], bins=30, kde=True, ax=axes[1], color='salmon')
# fare 컬럼 히스토그램 / 색상 salmon(연어색) / 두 번째 칸에 그리기
axes[1].set_title('운임 분포')    # 두 번째 서브플롯 제목
axes[1].set_xlabel('운임')        # 두 번째 서브플롯 x축 레이블

sns.boxplot(data=titanic, x='sex', y='age', ax=axes[2])
# 성별(x)에 따른 나이(y) 박스플롯 / 박스 안 선=중앙값, 박스=IQR, 점=이상치
axes[2].set_title('성별 나이 분포')   # 세 번째 서브플롯 제목

plt.tight_layout()   # 서브플롯 간 간격 자동 조정
plt.show()           # 그래프 화면 출력


# ============================================================
# [실습 3] 수치형 분포 시각화
# ============================================================
# 1행 2열 서브플롯을 만드세요.
#   - 왼쪽: fare 컬럼의 박스플롯 (객실 등급 pclass 기준 비교)
#           제목: '등급별 운임 분포'
#   - 오른쪽: age 히스토그램 (bins=20, kde=True)
#             제목: '나이 분포'
# 코드 작성 ↓
fig, axes = plt.subplots(1, 2, figsize=(12, 4))   # 1행 2열 서브플롯 생성
sns.boxplot(data=titanic, x='pclass', y='fare', ax=axes[0])
# 왼쪽: 객실 등급(x)별 운임(y) 박스플롯 → 등급이 높을수록 운임 분포가 어떻게 다른지 확인
axes[0].set_title('등급별 운임 분포')   # 왼쪽 제목
sns.histplot(titanic['age'], bins=20, kde=True, ax=axes[1])
# 오른쪽: 나이 히스토그램 / bins=20: 막대 20개 / kde=True: 밀도 곡선 추가
axes[1].set_title('나이 분포')          # 오른쪽 제목
plt.tight_layout()   # 서브플롯 간격 자동 조정
plt.show()           # 그래프 출력

flg, axes = plt.subplot(1, 2, figsize=(12, 4)) # 1행 2열 서브플롯 생성
sns.boxplot(data=titanic, x='places', y='fare', ax=axes[0])
axes[0].set_title('등급별 운임 분포') # 왼쪽 제목
sns.histplot(titanic['age'], bins=20, kde=True, ax=axes[1])
axes[1].set_title('나이 분포') # 오른쪽 제목
plt.tight_layout() # 서브플롯 간격 자동 조정
plt.show() # 그래프 출력




# ============================================================
# [이론 4] 범주형 변수 분포 & 생존율 비교
# ============================================================
#
# df['컬럼'].value_counts()              → 각 값의 빈도수
# df.groupby('그룹컬럼')['값컬럼'].mean() → 그룹별 평균
#
# 막대 그래프로 범주형 비교:
#   sns.countplot(data, x='컬럼')         → 빈도 막대
#   sns.barplot(data, x='그룹', y='값')   → 평균 막대 (신뢰구간 자동 표시)

print("\n=== 성별 빈도 ===")
print(titanic['sex'].value_counts())   # sex 컬럼의 각 값(male/female) 등장 횟수 출력

print("\n=== 객실 등급별 생존율 ===")
print(titanic.groupby('pclass')['survived'].mean().round(3))
# pclass(1/2/3등석)로 그룹을 나눈 뒤, 각 그룹의 survived 평균(생존율) 계산 / round(3): 소수점 3자리

fig, axes = plt.subplots(1, 3, figsize=(16, 4))   # 1행 3열 서브플롯 생성

sns.countplot(data=titanic, x='pclass', ax=axes[0], palette='Blues')
# pclass 컬럼의 값별 빈도를 막대 그래프로 표시 / palette='Blues': 파란 계열 색상
axes[0].set_title('객실 등급 분포')   # 첫 번째 칸 제목

sns.barplot(data=titanic, x='sex', y='survived', ax=axes[1], palette='Set2')
# 성별(x)에 따른 생존율(y 평균)을 막대로 표시 / 오차 막대는 신뢰구간 95%
axes[1].set_title('성별 생존율')      # 두 번째 칸 제목
axes[1].set_ylabel('생존율')          # y축 레이블

sns.barplot(data=titanic, x='pclass', y='survived', ax=axes[2], palette='coolwarm')
# 객실 등급(x)에 따른 생존율(y 평균)을 막대로 표시
axes[2].set_title('등급별 생존율')    # 세 번째 칸 제목
axes[2].set_ylabel('생존율')          # y축 레이블

plt.tight_layout()   # 서브플롯 간격 자동 조정
plt.show()           # 그래프 출력


# ============================================================
# [실습 4] 범주형 분석
# ============================================================
# 1) 탑승 항구(embarked)별 생존율을 groupby로 계산해서 출력하세요.
# print(titanic.groupby('embarked')['survived'].mean().round(3))
# 2) 1행 2열 서브플롯:
#    - 왼쪽: embarked별 승객 수 countplot
#            제목: '탑승 항구별 승객 수'
#    - 오른쪽: embarked별 생존율 barplot
#              제목: '탑승 항구별 생존율'
# 코드 작성 ↓
print(titanic.groupby('embarked')['survived'].mean().round(3))
# 1) embarked로 그룹을 나눈 뒤 survived 평균(생존율)을 계산해서 출력 / round(3): 소수점 3자리

fig, axes = plt.subplots(1, 2, figsize=(12, 4))   # 1행 2열 서브플롯 생성
sns.countplot(data=titanic, x='embarked', ax=axes[0])
# 왼쪽: 탑승 항구별 승객 수를 막대 그래프로 표시 (각 항구에 몇 명이 탔는지)
axes[0].set_title('탑승 항구별 승객 수')   # 왼쪽 제목
sns.barplot(data=titanic, x='embarked', y='survived', ax=axes[1])
# 오른쪽: 탑승 항구별 생존율(survived 평균)을 막대 그래프로 표시 / 오차 막대는 95% 신뢰구간
axes[1].set_title('탑승 항구별 생존율')    # 오른쪽 제목
plt.tight_layout()   # 서브플롯 간격 자동 조정
plt.show()           # 그래프 출력

fig, axes = plt.subplot(1, 2, figsize=(12, 4)) # 1행 2열 서브플롯 생성
sns.countplot(data=titanic, x='embarked', ax=axes[0])
axes[0].set_title('탑승 항구별 승객 수')

sns.barplot(data=titanic, x='embarked', y='survived', ax=axes[1])
axes[1].set_title('탑승 항구별 생존율')

plt.tight_layout()
plt.show()




# ============================================================
# [이론 5] 상관관계 분석 & 히트맵
# ============================================================
#
# df.corr()           → 수치형 컬럼 간 상관계수 (-1 ~ +1)
# sns.heatmap()       → 상관관계 시각화
# sns.pairplot()      → 변수 쌍별 산점도 + 히스토그램 한 번에

numeric_cols = titanic.select_dtypes(include='number')   # 수치형(int, float) 컬럼만 추출
corr = numeric_cols.corr()                               # 컬럼 간 상관계수 행렬 계산

plt.figure(figsize=(8, 6))   # 그래프 크기 설정
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', square=True)
# annot=True: 각 셀에 수치 표시 / fmt='.2f': 소수점 2자리 / cmap: 색상맵 / square=True: 셀을 정사각형으로
plt.title('타이타닉 상관관계 히트맵')   # 그래프 제목
plt.tight_layout()                       # 여백 자동 조정
plt.show()                               # 그래프 출력

sns.pairplot(titanic[['age', 'fare', 'pclass', 'survived']], hue='survived', plot_kws={'alpha': 0.5})
# 선택한 4개 컬럼의 모든 쌍 조합을 한 번에 산점도로 표시
# hue='survived': 생존 여부로 색상 구분 / alpha=0.5: 점 투명도 50% (겹치는 점 식별 용이)
plt.suptitle('변수 쌍별 산점도', y=1.02)   # 전체 그래프 상단 제목 (y=1.02: 제목 위치 위로 살짝 올림)
plt.show()                                  # 그래프 출력


# ============================================================
# [실습 5] 상관관계 & 종합 인사이트
# ============================================================
# 1) 수치형 컬럼만 골라 상관계수 행렬을 출력하세요.
corr = titanic.select_dtypes(include='number').corr()
print(corr)
# 2) 상관관계 히트맵을 그리세요. (cmap='Blues', annot=True)
#    제목: '수치형 변수 상관관계'
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='Blues')
plt.title('수치형 변수 상관관계')
plt.tight_layout()
plt.show()
# 3) 아래 질문에 답하는 코드를 작성하세요.
#    - 생존자(survived=1)의 평균 운임 vs 사망자(survived=0)의 평균 운임
#    - 나이가 10세 미만인 아이의 생존율
# 코드 작성 ↓
print(titanic.groupby('survived')['fare'].mean())

children2 = titanic[titanic['age'] < 10] # 10세 미만
print(children2['survived'].mean())

corr = titanic.select_dtypes(include='number').corr()   # 1) 수치형 컬럼만 추출 후 상관계수 행렬 계산
print(corr)                                             # 상관계수 행렬 출력

plt.figure(figsize=(8, 6))                              # 그래프 크기 설정
sns.heatmap(corr, annot=True, fmt='.2f', cmap='Blues')  # 2) 히트맵 / cmap='Blues': 파란 계열 색상
# heatmap : 색으로 만든 그래프(값을 색상으로 매핑)
# annot == Annotation -> 숫자를 직접 표시함 True /= 그래프로만 표시 False
plt.title('수치형 변수 상관관계')                       # 그래프 제목
plt.tight_layout()                                      # 여백 자동 조정
plt.show()                                              # 그래프 출력

print(titanic.groupby('survived')['fare'].mean())
# 3-1) survived(0=사망, 1=생존)로 그룹을 나눈 뒤 fare 평균 출력 → 생존자와 사망자의 평균 운임 비교

children = titanic[titanic['age'] < 10]   # 나이가 10세 미만인 행만 필터링
print(children['survived'].mean())        # 3-2) 필터링된 아이들의 생존율(survived 평균) 출력

# 상관 계수 : 상관계수(Correlation Coefficient)는 두 변수가 서로 얼마나 밀접하게, 
# 그리고 어떤 방향으로 움직이는지를 나타내는 수치적 지표예요.
# $r = 1.0$ (강한 양의 상관관계): 한 변수가 증가하면 다른 변수도 똑같은 비율로 완벽하게 증가합니다. (예: 정비례 그래프)
# $r = -1.0$ (강한 음의 상관관계): 한 변수가 증가하면 다른 변수는 똑같은 비율로 완벽하게 감소합니다. (예: 반비례 그래프)
# $r = 0$ (상관관계 없음): 두 변수 사이에 선형적인 관계가 전혀 없습니다. 한쪽이 변해도 다른 쪽이 어떻게 변할지 예측할 수 없어요.

