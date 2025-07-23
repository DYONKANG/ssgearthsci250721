import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import hashlib
import numpy as np  # np.ndenumerate 사용을 위해 추가

# NanumGothic 폰트 파일 경로 지정 및 등록
font_path = "./font/NanumGothic-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'NanumGothic'

st.title("수치형 컬럼 간 상관분석")  # 페이지 제목

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

        # 선택된 컬럼 조합에 따라 색상 결정
        def get_color(col1, col2):
            combo = col1 + col2
            hash_val = int(hashlib.md5(combo.encode()).hexdigest(), 16)
            cmap = plt.get_cmap('tab10')
            return cmap(hash_val % 10)

        scatter_color = get_color(col1, col2)

        # 산점도 시각화
        fig, ax = plt.subplots()
        ax.scatter(df[col1], df[col2], color=scatter_color)
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)
        ax.set_title(f"{col1} vs {col2} 산점도")
        st.pyplot(fig)

        # 모든 컬럼 조합에 대한 상관계수 표 및 색상 시각화
        st.subheader("컬럼 간 상관계수 비교")
        corr = df[numeric_cols].corr()

        fig2, ax2 = plt.subplots(figsize=(1.2*len(numeric_cols), 1.2*len(numeric_cols)))
        cax = ax2.matshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
        fig2.colorbar(cax)
        ax2.set_xticks(range(len(numeric_cols)))
        ax2.set_yticks(range(len(numeric_cols)))
        ax2.set_xticklabels(numeric_cols, rotation=90)
        ax2.set_yticklabels(numeric_cols)
        ax2.set_title("상관계수 히트맵", pad=20)

        # 각 칸에 상관계수 값 표시 (칸 크기에 맞춰 폰트 크기 자동 조정)
        cell_width = fig2.get_size_inches()[0] * fig2.dpi / len(numeric_cols)
        font_size = max(int(cell_width // 7), 8)
        for (i, j), val in np.ndenumerate(corr.values):
            ax2.text(j, i, f"{val:.2f}", ha='center', va='center', color='black', fontsize=font_size)

        st.pyplot(fig2)
    else:
        st.warning("수치형 컬럼이 2개 이상 있어야 상관분석을 할 수 있습니다.")
else:
    st.info("CSV 파일을 업로드하면 데이터와 상관분석 결과가 표시됩니다.")

# 주요 기능:
# 1. CSV 파일 업로드
# 2. 데이터 미리보기
# 3. 두 수치형 컬럼 선택 및 조합별 산점도 색상
# 4. 전체 수치형 컬럼 간 상관계수 표와 색상 히트맵 (숫자 크기 자동 조정)