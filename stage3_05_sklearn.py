# ============================================================
# Stage 3 - 05. Scikit-learn 입문 (머신러닝 기초)
# ============================================================
# Scikit-learn: 파이썬 대표 머신러닝 라이브러리
# 전처리 → 모델 학습 → 평가 파이프라인을 간결하게 구현 가능
#
# 사용 라이브러리: pandas, numpy, sklearn, seaborn
# 데이터셋: 타이타닉 (seaborn 내장)
#
# 학습 순서
#   1. 데이터 분리 (train_test_split)
#   2. 전처리 (StandardScaler, LabelEncoder)
#   3. 선형 회귀 (LinearRegression)
#   4. 분류 (LogisticRegression, RandomForestClassifier)
#   5. 모델 평가 (confusion_matrix, classification_report, cross_val_score)

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# -----------------------------------------------
# 타이타닉 데이터 로드 및 결측치 전처리 (stage3_04에서 이어받은 전처리)
# -----------------------------------------------
titanic = sns.load_dataset('titanic')
# age 결측치 → 중앙값으로 대체 (이상치에 덜 민감한 중앙값 사용)
titanic['age'] = titanic['age'].fillna(titanic['age'].median())
# embarked 결측치 → 최빈값(가장 많이 등장한 항구)으로 대체
titanic['embarked'] = titanic['embarked'].fillna(titanic['embarked'].mode()[0])
# embark_town 결측치 → 최빈값으로 대체
titanic['embark_town'] = titanic['embark_town'].fillna(titanic['embark_town'].mode()[0])
# deck 컬럼은 결측치 77%로 과도하게 많아 분석에서 제외
titanic = titanic.drop(columns=['deck'])


# ============================================================
# [이론 1] 데이터 분리 — train_test_split
# ============================================================
#
# 머신러닝 모델은 학습(train)에 사용하지 않은 데이터로 성능을 평가해야 한다.
# → 전체 데이터를 훈련셋 / 테스트셋으로 나누는 작업이 필수
#
# from sklearn.model_selection import train_test_split
#
# X_train, X_test, y_train, y_test = train_test_split(
#     X,          # 입력 변수 (특성)
#     y,          # 타깃 변수 (레이블)
#     test_size=0.2,      # 테스트 비율 (0.2 = 20%)
#     random_state=42     # 재현성 확보를 위한 시드값
# )
#
# 주요 개념
#   X (Feature)   : 모델이 학습에 사용하는 입력 컬럼들
#   y (Target)    : 예측하려는 정답 컬럼
#   train set     : 모델이 패턴을 학습하는 데이터 (보통 70~80%)
#   test set      : 모델 성능을 검증하는 데이터 (보통 20~30%)
#   random_state  : 동일한 결과 재현을 위한 난수 고정값

from sklearn.model_selection import train_test_split
# sklearn(사이킷런)의 model_selection 모듈에서 train_test_split 함수 가져오기
# model_selection: 데이터 분리, 교차검증 등 모델 선택 관련 도구 모음

features = ['pclass', 'age', 'sibsp', 'parch', 'fare']
# 모델 학습에 사용할 컬럼(특성) 목록을 리스트로 정의
# pclass(등급), age(나이), sibsp(형제/배우자 수), parch(부모/자녀 수), fare(운임)

X = titanic[features]
# titanic DataFrame에서 features 리스트에 해당하는 컬럼만 추출 → 입력 행렬 X
# X의 형태: (891행, 5열) — 행=승객 1명, 열=특성 5개

y = titanic['survived']
# 예측 대상인 'survived' 컬럼만 추출 → 타깃 벡터 y
# y의 형태: (891행,) — 0(사망) 또는 1(생존)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# train_test_split 호출 → 4개의 변수를 한 번에 반환
#   X_train : 훈련용 입력 데이터 (전체 891행의 80% = 712행)
#   X_test  : 테스트용 입력 데이터 (전체 891행의 20% = 179행)
#   y_train : 훈련용 정답 레이블 (712행)
#   y_test  : 테스트용 정답 레이블 (179행)
# test_size=0.2  → 전체 데이터의 20%를 테스트셋으로 사용
# random_state=42 → 42라는 숫자로 난수를 고정, 코드를 다시 실행해도 동일한 분리 결과 보장

print("=== 데이터 분리 결과 ===")
print(f"전체: {len(X)}행")         # len(X) → X의 총 행 수 = 891
print(f"훈련셋: {len(X_train)}행") # len(X_train) → 훈련셋 행 수 = 712
print(f"테스트셋: {len(X_test)}행") # len(X_test) → 테스트셋 행 수 = 179


# ============================================================
# [실습 1] 데이터 분리
# ============================================================
# titanic 데이터에서 아래 조건으로 train/test를 분리하세요.
#   - 특성(X): 'pclass', 'age', 'fare'
#   - 타깃(y): 'survived'
#   - 테스트 비율: 30%, random_state=0
# 분리 후 훈련셋과 테스트셋의 행 수를 출력하세요.
# 코드 작성 ↓
# x1 = titanic[['pclass', 'age', 'fare']]
# y1 = titanic['survived']

# [정답 코드]
X1 = titanic[['pclass', 'age', 'fare']]
# 특성 3개만 선택 (fare 포함, sibsp/parch 제외)
y1 = titanic['survived']
# 타깃은 생존 여부(0/1)

X1_train, X1_test, y1_train, y1_test = train_test_split(
    X1, y1, test_size=0.3, random_state=0
)
# X1_train, X1_test, y1_train, y1_test = train_test_split(
#   X1, y1, tset_size=0.3(30%), ramdom_state=0
# )
# X1_train -> 시험용 문제지 X1_test -> 테스트 문제지
# Y1_train -> 시험용 답안지 Y1_test -> 테스트 답안지 
# test_size=0.3 → 전체의 30%를 테스트셋으로 사용 (891행의 30% = 267행)
# random_state=0 → 0이라는 시드값으로 난수 고정

print("=== [실습 1] 데이터 분리 결과 ===")
print(f"훈련셋: {len(X1_train)}행")   # 891 * 0.7 = 623행
print(f"테스트셋: {len(X1_test)}행")  # 891 * 0.3 = 268행




# ============================================================
# [이론 2] 전처리 — StandardScaler & LabelEncoder
# ============================================================
#
# 모델은 숫자만 이해한다. 또한 컬럼 간 스케일 차이가 크면 학습이 왜곡된다.
# → 수치형 컬럼은 스케일링, 범주형 컬럼은 수치로 변환(인코딩) 필요
#
# StandardScaler (표준화)
#   - 평균 0, 표준편차 1이 되도록 변환
#   - 공식: z = (x - 평균) / 표준편차
#   - fit(): 훈련 데이터에서 평균/표준편차 계산
#   - transform(): 계산된 값으로 데이터 변환
#   - 주의: fit은 훈련셋에만, transform은 훈련셋·테스트셋 모두에 적용
#
# LabelEncoder (레이블 인코딩)
#   - 범주형 문자열 → 정수로 변환 (male→1, female→0 등)
#   - 이진 범주형 컬럼에 주로 사용

from sklearn.preprocessing import StandardScaler, LabelEncoder
# preprocessing 모듈: 데이터 전처리 도구 모음
# StandardScaler: 수치형 데이터 표준화 클래스
# LabelEncoder  : 범주형 문자열을 정수로 변환하는 클래스

scaler = StandardScaler()
# StandardScaler 객체 생성 — 아직 아무 계산도 하지 않은 빈 스케일러

X_train_scaled = scaler.fit_transform(X_train)
# fit_transform = fit(학습) + transform(변환) 한 번에 수행
# fit    : X_train 데이터를 보고 각 컬럼의 평균과 표준편차를 계산해서 기억
# transform: 기억한 평균/표준편차로 X_train 데이터를 (값-평균)/표준편차 공식으로 변환
# 결과: 각 컬럼의 평균이 0, 표준편차가 1인 numpy 배열 반환

X_test_scaled = scaler.transform(X_test)
# transform만 수행 (fit 하지 않음!)
# 테스트셋에는 fit을 다시 하지 않고, 훈련셋에서 계산한 평균/표준편차를 그대로 사용
# 이유: 테스트셋은 "처음 보는 데이터" 역할 → 훈련셋 기준으로만 변환해야 공정한 평가 가능

print("\n=== 스케일링 전 (age 앞 3개) ===")
print(X_train['age'].values[:3])
# X_train DataFrame의 'age' 컬럼에서 numpy 배열로 변환(.values) 후 앞 3개 출력
# 예: [22. 38. 26.] 같은 실제 나이값

print("=== 스케일링 후 (age 앞 3개) ===")
print(X_train_scaled[:3, features.index('age')])
# X_train_scaled는 numpy 배열 → [행, 열] 인덱싱 사용
# features.index('age') → features 리스트에서 'age'의 위치(인덱스) 번호 반환 (=1)
# X_train_scaled[:3, 1] → 앞 3행의 age 열 값 출력
# 예: [-0.53  0.57 -0.25] 같은 표준화된 값

le = LabelEncoder()
# LabelEncoder 객체 생성

titanic['sex_encoded'] = le.fit_transform(titanic['sex'])
# titanic['sex'] 컬럼(female/male 문자열)을 정수로 변환
# fit_transform이 알파벳 순서로 0부터 번호 부여 → female=0, male=1
# 변환 결과를 새 컬럼 'sex_encoded'에 저장

print("\n=== 성별 인코딩 결과 ===")
print(titanic[['sex', 'sex_encoded']].drop_duplicates())
# titanic에서 'sex', 'sex_encoded' 두 컬럼만 선택 후
# drop_duplicates()로 중복 행 제거 → 변환 매핑 관계만 출력 (female→0, male→1)


# ============================================================
# [실습 2] 전처리
# ============================================================
# 1) X_train, X_test를 StandardScaler로 스케일링하세요.
#    (위에서 분리한 변수를 재사용해도 됩니다)
# 2) titanic의 'embarked' 컬럼을 LabelEncoder로 인코딩하여
#    'embarked_encoded' 컬럼에 저장하세요.
# 3) 인코딩 전후를 비교해서 출력하세요.
# 코드 작성 ↓

# [정답 코드]
# 1) 실습 1에서 분리한 X1_train, X1_test를 스케일링
scaler2 = StandardScaler()
# 실습 1 데이터용 별도 스케일러 생성 (이론 2의 scaler와 독립)

X1_train_sc = scaler2.fit_transform(X1_train)
# X1_train의 평균/표준편차를 계산(fit)하고 변환(transform)을 한 번에 수행

X1_test_sc = scaler2.transform(X1_test)
# 훈련셋에서 계산한 평균/표준편차로 테스트셋만 변환 (fit 없이 transform만)

print("=== [실습 2] 스케일링 결과 (fare 앞 3개) ===")
print("스케일링 전:", X1_train['fare'].values[:3])
# X1_train은 DataFrame이므로 .values로 numpy 배열 변환 후 앞 3개 출력
print("스케일링 후:", X1_train_sc[:3, 2])
# X1_train_sc는 numpy 배열 → [행, 열] 인덱싱 사용
# fare는 X1 컬럼 순서상 index 2 (pclass=0, age=1, fare=2)

# 2) embarked 컬럼 LabelEncoder 인코딩
le2 = LabelEncoder()
titanic['embarked_encoded'] = le2.fit_transform(titanic['embarked'])
# embarked 컬럼(C/Q/S 문자열)을 정수로 변환 (알파벳 순: C=0, Q=1, S=2)
# 결과를 새 컬럼 'embarked_encoded'에 저장

# 3) 인코딩 전후 비교 출력
print("\n=== [실습 2] embarked 인코딩 결과 ===")
print(titanic[['embarked', 'embarked_encoded']].drop_duplicates())
# drop_duplicates(): 같은 매핑은 중복 제거 → C→0, Q→1, S→2 매핑 관계만 출력




# ============================================================
# [이론 3] 선형 회귀 — LinearRegression
# ============================================================
#
# 선형 회귀: 입력 변수(X)와 연속형 출력값(y) 사이의 선형 관계를 학습
# → "나이, 등급, 운임으로 운임을 예측" 같은 수치 예측 문제에 사용
#
# 사용 패턴:
#   model = LinearRegression()
#   model.fit(X_train, y_train)     # 학습
#   y_pred = model.predict(X_test)  # 예측
#
# 주요 평가 지표 (회귀)
#   MSE  (Mean Squared Error)   : 예측값과 실제값 차이의 제곱 평균 → 낮을수록 좋음
#   RMSE (Root MSE)             : MSE의 제곱근 → 원래 단위로 해석 가능
#   R²   (결정계수)              : 모델이 분산을 얼마나 설명하는지 (0~1, 1에 가까울수록 좋음)

from sklearn.linear_model import LinearRegression
# linear_model 모듈: 선형 기반 모델들의 모음
# LinearRegression: 최소제곱법으로 선형 관계를 학습하는 회귀 모델

from sklearn.metrics import mean_squared_error, r2_score
# metrics 모듈: 모델 성능 평가 지표 함수 모음
# mean_squared_error: MSE(평균 제곱 오차) 계산 함수
# r2_score          : R²(결정계수) 계산 함수

features_reg = ['pclass', 'age', 'sibsp', 'parch']
# 운임(fare)을 예측하기 위한 입력 특성 목록
# fare 자체는 타깃이므로 특성에서 제외

X_reg = titanic[features_reg]   # 회귀 모델용 입력 행렬
y_reg = titanic['fare']         # 회귀 모델 타깃: 운임(연속형 수치)

X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)
# 회귀용 데이터를 80% 훈련 / 20% 테스트로 분리

lr_model = LinearRegression()
# 선형 회귀 모델 객체 생성 (학습 전 상태)

lr_model.fit(X_reg_train, y_reg_train)
# 훈련셋으로 모델 학습
# 내부적으로 X_reg_train과 y_reg_train의 관계를 수식 y = w1*pclass + w2*age + ... + b 로 표현하는
# 최적의 가중치(w)와 절편(b)을 계산해서 저장

y_reg_pred = lr_model.predict(X_reg_test)
# 테스트셋 입력(X_reg_test)을 학습된 수식에 넣어 운임을 예측
# 반환값: 예측된 운임값 배열 (실제값과 비교용)

mse = mean_squared_error(y_reg_test, y_reg_pred)
# MSE = (실제값 - 예측값)² 의 평균
# y_reg_test: 실제 운임값, y_reg_pred: 모델이 예측한 운임값
# 값이 작을수록 예측이 정확 (단위: 운임²)

r2 = r2_score(y_reg_test, y_reg_pred)
# R² = 1 - (잔차 제곱합 / 전체 분산)
# 1.0에 가까울수록 모델이 데이터를 잘 설명, 0이면 평균 예측과 동일 수준

print("\n=== 선형 회귀 — 운임 예측 ===")
print(f"MSE : {mse:.2f}")
print(f"RMSE: {np.sqrt(mse):.2f}")
# RMSE = MSE의 제곱근 → 운임과 동일한 단위로 오차 해석 가능
# 예: RMSE=30 이면 평균적으로 실제 운임에서 ±30 정도 빗나간다는 의미

print(f"R²  : {r2:.4f}")
print(f"회귀 계수: {dict(zip(features_reg, lr_model.coef_.round(3)))}")
# lr_model.coef_ : 각 특성의 가중치(기울기) 배열 — 학습 후에만 존재하는 속성
# zip(features_reg, lr_model.coef_) → 특성명과 가중치를 쌍으로 묶기
# dict(...)  → {특성명: 가중치} 딕셔너리로 변환해서 출력
# 예: {'pclass': -10.5, 'age': 0.3, ...} → pclass가 1 오를수록 운임이 10.5 감소


# ============================================================
# [실습 3] 선형 회귀
# ============================================================
# 'age', 'pclass', 'fare' 3개 특성으로 'sibsp'(형제/배우자 수)를 예측하세요.
#   - test_size=0.2, random_state=0
#   - MSE, RMSE, R² 출력
# 코드 작성 ↓

# [정답 코드]
X3 = titanic[['age', 'pclass', 'fare']]
# 선형 회귀 입력 특성 3개 선택
y3 = titanic['sibsp']
# 예측 대상: sibsp(형제/배우자 수) — 연속형으로 취급해 회귀 적용

X3_train, X3_test, y3_train, y3_test = train_test_split(
    X3, y3, test_size=0.2, random_state=0
)
# test_size=0.2 → 20% 테스트셋, random_state=0으로 난수 고정

lr3 = LinearRegression()
# 선형 회귀 모델 객체 생성

lr3.fit(X3_train, y3_train)
# 훈련셋으로 최적의 가중치와 절편 계산

y3_pred = lr3.predict(X3_test)
# 테스트 입력으로 sibsp 예측

mse3 = mean_squared_error(y3_test, y3_pred)
# 예측값과 실제값 차이의 제곱 평균 계산

r2_3 = r2_score(y3_test, y3_pred)
# 모델이 sibsp 분산을 얼마나 설명하는지 계산 (0~1)

print("=== [실습 3] sibsp 예측 선형 회귀 ===")
print(f"MSE : {mse3:.2f}")
print(f"RMSE: {np.sqrt(mse3):.2f}")  # RMSE = MSE의 제곱근 → sibsp와 같은 단위로 해석
print(f"R²  : {r2_3:.4f}")




# ============================================================
# [이론 4] 분류 — LogisticRegression & RandomForestClassifier
# ============================================================
#
# 분류: 입력값을 범주(클래스)로 예측하는 문제
#       예) 생존(1) / 사망(0) → 이진 분류
#
# LogisticRegression (로지스틱 회귀)
#   - 이름은 "회귀"지만 분류 알고리즘
#   - 각 클래스에 속할 확률을 계산 후 0.5 기준으로 분류
#   - 빠르고 해석 가능, 선형 경계만 학습
#   - max_iter: 수렴을 위한 최대 반복 횟수 (데이터에 따라 늘려야 할 수 있음)
#
# RandomForestClassifier (랜덤 포레스트)
#   - 여러 개의 결정 트리를 앙상블로 학습 → 다수결로 최종 예측
#   - 비선형 관계도 학습 가능, 과적합에 강함
#   - n_estimators: 결정 트리 개수 (많을수록 안정적이나 느림)
#
# accuracy_score: 전체 예측 중 맞춘 비율 (정확도)

from sklearn.linear_model import LogisticRegression
# LogisticRegression: 선형 경계로 이진(또는 다중) 분류하는 모델
# 내부적으로 시그모이드 함수를 사용해 확률 계산 후 0.5 기준으로 클래스 결정

from sklearn.ensemble import RandomForestClassifier
# ensemble 모듈: 여러 모델을 합쳐 성능을 높이는 앙상블 기법 모음
# RandomForestClassifier: 다수의 결정 트리를 독립적으로 학습 후 다수결로 최종 분류

from sklearn.metrics import accuracy_score
# accuracy_score: 전체 예측 중 정답 비율 계산 — accuracy = 맞춘 수 / 전체 수

features_clf = ['pclass', 'age', 'sibsp', 'parch', 'fare', 'sex_encoded']
# 분류에 사용할 특성 목록 (sex는 문자열이라 위에서 인코딩한 sex_encoded 사용)

X_clf = titanic[features_clf]   # 분류 모델용 입력 행렬 (6개 특성)
# == X_clf = titanic[['pclass', 'age', 'sibsp', 'parch', 'fare', 'sex_encoded']]
y_clf = titanic['survived']     # 분류 모델 타깃: 생존 여부 (0 또는 1)

X_clf_train, X_clf_test, y_clf_train, y_clf_test = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=42
)
# 분류용 데이터를 80% 훈련 / 20% 테스트로 분리

scaler_clf = StandardScaler()
X_clf_train_sc = scaler_clf.fit_transform(X_clf_train)
# 분류 모델용 스케일러 (이론 2의 scaler와 별도로 생성)
# 로지스틱 회귀는 스케일에 민감하므로 스케일링 필요

X_clf_test_sc = scaler_clf.transform(X_clf_test)
# 테스트셋도 동일한 스케일러로 변환 (fit은 훈련셋에만 했음)

log_model = LogisticRegression(max_iter=1000, random_state=42)
# max_iter=1000: 최적의 가중치를 찾기 위한 반복 횟수 상한
#                기본값(100)이 부족하면 ConvergenceWarning 발생 → 늘려서 해결
# random_state=42: 일부 solver에서 난수 사용 → 재현성 확보

log_model.fit(X_clf_train_sc, y_clf_train)
# 스케일링된 훈련 데이터로 로지스틱 회귀 학습
# 내부적으로 각 특성의 가중치를 조정해 생존 확률을 가장 잘 예측하는 수식 완성

log_pred = log_model.predict(X_clf_test_sc)
# 스케일링된 테스트 입력으로 생존 여부 예측 → 0 또는 1 배열 반환

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
# n_estimators=100: 결정 트리를 100개 독립적으로 만들어 앙상블
#                   트리가 많을수록 안정적이지만 학습 시간 증가
# random_state=42: 각 트리의 난수 고정 → 재현성 확보

rf_model.fit(X_clf_train, y_clf_train)
# 스케일링하지 않은 원본 데이터로 랜덤 포레스트 학습
# 결정 트리는 분기점(임계값)을 기준으로 나누므로 스케일 영향 없음

rf_pred = rf_model.predict(X_clf_test)
# 테스트 데이터로 생존 여부 예측 → 100개 트리의 다수결 결과 반환

print("\n=== 분류 모델 정확도 비교 ===")
print(f"로지스틱 회귀 정확도: {accuracy_score(y_clf_test, log_pred):.4f}")
print(f"랜덤 포레스트 정확도: {accuracy_score(y_clf_test, rf_pred):.4f}")
# accuracy_score(실제값, 예측값): 두 배열을 비교해 일치율 계산
# :.4f → 소수점 4자리까지 출력 (예: 0.8268 → 82.68% 정확도)


# ============================================================
# [실습 4] 분류 모델 학습
# ============================================================
# 위의 features_clf를 사용하여:
# 1) LogisticRegression으로 생존 예측 모델을 만들고 정확도를 출력하세요.
#    (스케일링 적용, max_iter=1000, random_state=0)
# 2) RandomForestClassifier (n_estimators=50, random_state=0)로도 학습 후 정확도를 출력하세요.
# 3) 어느 모델이 더 높은 정확도를 보이는지 출력하세요.
# 코드 작성 ↓

# [정답 코드]
# 이론 4의 X_clf(features_clf 기반)를 그대로 사용, random_state만 0으로 변경
X4_train, X4_test, y4_train, y4_test = train_test_split(
    X_clf, y_clf, test_size=0.2, random_state=0
)
# random_state=0 → 이론 4(random_state=42)와 다른 분리 결과

# 1) LogisticRegression
scaler4 = StandardScaler()
X4_train_sc = scaler4.fit_transform(X4_train)  # 훈련셋 스케일링
X4_test_sc  = scaler4.transform(X4_test)        # 테스트셋 변환만

log4 = LogisticRegression(max_iter=1000, random_state=0)
log4.fit(X4_train_sc, y4_train)
log4_pred = log4.predict(X4_test_sc)
log4_acc = accuracy_score(y4_test, log4_pred)

# 2) RandomForestClassifier
rf4 = RandomForestClassifier(n_estimators=50, random_state=0)
# n_estimators=50 → 이론 4(100개)의 절반으로 줄인 버전
rf4.fit(X4_train, y4_train)     # 랜덤 포레스트는 스케일 불필요
rf4_pred = rf4.predict(X4_test)
rf4_acc = accuracy_score(y4_test, rf4_pred)

print("=== [실습 4] 분류 모델 정확도 ===")
print(f"로지스틱 회귀: {log4_acc:.4f}")
print(f"랜덤 포레스트: {rf4_acc:.4f}")

# 3) 더 높은 정확도 모델 출력
best4 = "로지스틱 회귀" if log4_acc > rf4_acc else "랜덤 포레스트"
print(f"더 높은 정확도 모델: {best4}")




# ============================================================
# [이론 5] 모델 평가 — confusion_matrix, classification_report, cross_val_score
# ============================================================
#
# 정확도(accuracy)만으로는 모델을 제대로 평가하기 어렵다.
# 예) 클래스 불균형(95% 사망, 5% 생존) 시 항상 "사망"으로 예측해도 정확도 95%
#
# Confusion Matrix (혼동 행렬)
#   실제 \ 예측   | 예측 0 | 예측 1
#   실제 0 (사망) |  TN    |  FP
#   실제 1 (생존) |  FN    |  TP
#
#   TN: 사망 → 사망 예측 (맞음)   TP: 생존 → 생존 예측 (맞음)
#   FP: 사망 → 생존 예측 (틀림)   FN: 생존 → 사망 예측 (틀림)
#
# classification_report 주요 지표
#   Precision (정밀도): 생존으로 예측한 것 중 실제 생존 비율 = TP / (TP + FP)
#   Recall    (재현율): 실제 생존자 중 생존으로 예측한 비율 = TP / (TP + FN)
#   F1 Score          : Precision과 Recall의 조화 평균 (균형 지표)
#
# cross_val_score (교차 검증)
#   - 데이터를 k개 폴드로 나눠 k번 반복 학습/평가
#   - 특정 분리 방식에 의한 편향 제거 → 더 신뢰할 수 있는 성능 추정

from sklearn.metrics import confusion_matrix, classification_report
# confusion_matrix      : 실제값 vs 예측값을 2x2(또는 NxN) 행렬로 정리
# classification_report : precision, recall, f1-score를 클래스별로 정리해서 출력

from sklearn.model_selection import cross_val_score
# cross_val_score: 데이터를 k개로 나눠 k번 반복 평가하는 교차 검증 함수

print("\n=== 혼동 행렬 (랜덤 포레스트) ===")
cm = confusion_matrix(y_clf_test, rf_pred)
# y_clf_test: 실제 생존 여부 (정답), rf_pred: 랜덤 포레스트 예측값
# 반환값: [[TN, FP], [FN, TP]] 형태의 2x2 numpy 배열
# TN(좌상): 실제 사망 → 사망 예측 (올바름)
# FP(우상): 실제 사망 → 생존 예측 (오류, 거짓 양성)
# FN(좌하): 실제 생존 → 사망 예측 (오류, 거짓 음성)
# TP(우하): 실제 생존 → 생존 예측 (올바름)
print(cm)

plt.figure(figsize=(5, 4))   # 그래프 크기: 가로 5인치, 세로 4인치
sns.heatmap(
    cm,
    annot=True,                              # 각 셀 안에 숫자 직접 표시
    fmt='d',                                 # 'd' = 정수 형식으로 표시 (소수점 없이)
    cmap='Blues',                            # 파란 계열 색상맵 (값이 클수록 진한 파랑)
    xticklabels=['예측 사망', '예측 생존'],   # x축(열) 레이블: 모델의 예측값
    yticklabels=['실제 사망', '실제 생존']    # y축(행) 레이블: 실제 정답값
)
plt.title('혼동 행렬')
plt.tight_layout()
plt.show()

print("\n=== 분류 리포트 (랜덤 포레스트) ===")
print(classification_report(y_clf_test, rf_pred, target_names=['사망', '생존']))
# classification_report: 클래스별 precision, recall, f1-score, support 출력
# target_names=['사망', '생존'] → 0=사망, 1=생존으로 레이블 이름 지정
# support: 해당 클래스의 실제 샘플 수
# macro avg   : 클래스별 지표의 단순 평균 (클래스 불균형 무시)
# weighted avg: 클래스별 지표를 샘플 수로 가중 평균 (클래스 불균형 반영)

cv_scores = cross_val_score(rf_model, X_clf, y_clf, cv=5, scoring='accuracy')
# rf_model  : 평가할 모델 (랜덤 포레스트)
# X_clf     : 전체 입력 데이터 (분리 전 원본)
# y_clf     : 전체 타깃 데이터
# cv=5      : 데이터를 5개 구간(폴드)으로 나눠 5번 반복 학습/평가
#             1회차: 폴드1=테스트, 폴드2~5=훈련
#             2회차: 폴드2=테스트, 나머지=훈련 ... (5번 반복)
# scoring='accuracy': 각 반복에서 정확도를 계산해 반환
# 반환값: 5번 평가의 정확도 배열 (예: [0.82, 0.84, 0.79, 0.83, 0.81])

print("\n=== 5-폴드 교차 검증 (랜덤 포레스트) ===")
print(f"각 폴드 정확도: {cv_scores.round(4)}")
# 각 폴드별 정확도를 소수점 4자리로 출력 → 폴드마다 성능이 얼마나 다른지 확인

print(f"평균 정확도: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
# cv_scores.mean() : 5번 평가의 평균 정확도 → 모델의 대표 성능
# cv_scores.std()  : 5번 평가의 표준편차 → 값이 작을수록 안정적인 모델
# 예: 0.8210 ± 0.0152 → 평균 82.1% 정확도, 폴드 간 편차 1.5%


# ============================================================
# [실습 5] 모델 평가 종합
# ============================================================
# 로지스틱 회귀 모델(log_model)을 기준으로:
# 1) 혼동 행렬을 히트맵으로 출력하세요. (cmap='Oranges')
# 2) classification_report를 출력하세요.
# 3) cross_val_score로 5-폴드 교차 검증 후 평균 정확도를 출력하세요.
#    (로지스틱 회귀는 스케일링된 X_clf를 사용하세요)
# 코드 작성 ↓

# [정답 코드]
# 이론 4에서 학습한 log_model과 log_pred(X_clf_test_sc 기반) 재사용

# 1) 혼동 행렬 히트맵 (cmap='Oranges')
cm5 = confusion_matrix(y_clf_test, log_pred)
# y_clf_test: 실제 생존 여부, log_pred: 로지스틱 회귀 예측값

plt.figure(figsize=(5, 4))
sns.heatmap(
    cm5,
    annot=True,                              # 셀 안에 숫자 표시
    fmt='d',                                 # 정수 형식 출력
    cmap='Oranges',                          # 주황 계열 색상맵 (이론 5의 Blues와 비교)
    xticklabels=['예측 사망', '예측 생존'],
    yticklabels=['실제 사망', '실제 생존']
)
plt.title('[실습 5] 혼동 행렬 (로지스틱 회귀)')
plt.tight_layout()
plt.show()

# 2) classification_report
print("=== [실습 5] 분류 리포트 (로지스틱 회귀) ===")
print(classification_report(y_clf_test, log_pred, target_names=['사망', '생존']))
# log_pred는 이론 4에서 X_clf_test_sc(스케일링된 테스트셋)로 예측한 결과

# 3) 5-폴드 교차 검증 (전체 X_clf 스케일링 후 사용)
scaler5 = StandardScaler()
X_clf_all_sc = scaler5.fit_transform(X_clf)
# 교차 검증은 전체 데이터셋(X_clf)을 넘겨야 하므로 전체를 먼저 스케일링
# 주의: 실제 업무에서는 Pipeline을 사용해 각 폴드마다 fit/transform을 분리해야 정확함

cv5 = cross_val_score(log_model, X_clf_all_sc, y_clf, cv=5, scoring='accuracy')
# log_model: 이론 4에서 학습한 로지스틱 회귀 모델
# cv=5: 5개 폴드로 나눠 5번 반복 평가

print("=== [실습 5] 5-폴드 교차 검증 (로지스틱 회귀) ===")
print(f"각 폴드 정확도: {cv5.round(4)}")
print(f"평균 정확도: {cv5.mean():.4f} ± {cv5.std():.4f}")
