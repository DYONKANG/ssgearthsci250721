import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# NanumGothic 폰트 파일 경로 지정 및 등록
font_path = "./font/NanumGothic-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'NanumGothic'

st.title("CSV 파일 업로드 및 데이터 시각화")  # 페이지 제목

# CSV 파일 업로드 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # CSV 파일을 데이터프레임으로 읽기
    df = pd.read_csv(uploaded_file)
    st.subheader("업로드된 데이터 미리보기")
    st.dataframe(df)  # 데이터 미리보기

    # 수치형 컬럼만 선택
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) >= 2:
        st.subheader("컬럼 간 상관분석")
        col1 = st.selectbox("첫 번째 컬럼 선택", numeric_cols, key="col1")
        col2 = st.selectbox("두 번째 컬럼 선택", [c for c in numeric_cols if c != col1], key="col2")

        # 선택된 두 컬럼의 상관계수 계산
        corr_value = df[[col1, col2]].corr().iloc[0, 1]
        st.write(f"**{col1}**와 **{col2}**의 상관계수: **{corr_value:.3f}**")

        # 산점도 시각화
        fig, ax = plt.subplots()
        ax.scatter(df[col1], df[col2])
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.set_title(f"{col1} vs {col2} 산점도")
        st.pyplot(fig)
    else:
        st.warning("수치형 컬럼이 2개 이상 있어야 상관분석을 할 수 있습니다.")
else:
    st.info("CSV 파일을 업로드하면 데이터와 상관분석 결과가 표시됩니다.")

# 주요 기능:
# 1. CSV 파일 업로드
# 2. 데이터 미리보기
# 3. 두 수치형 컬럼 선택