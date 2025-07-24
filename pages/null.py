# Streamlit_app.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# NanumGothic 폰트 파일 경로 지정 및 등록
font_path = "./font/NanumGothic-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'NanumGothic'

st.title("Matplotlib 한글 그래프")  # ① 페이지 제목

# 데이터 생성
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(x, y, label='사인 곡선')
ax.set_title('한글 제목: 사인 그래프')
ax.set_xlabel('X축 (시간)')
ax.set_ylabel('Y축 (진폭)')
ax.legend()

st.pyplot(fig)  # ② Streamlit에 그래프 출력

st.caption("Matplotlib을 활용한 데이터 시각화 예시")