import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager
from openai import OpenAI

# NanumGothic 폰트 파일 경로 지정 및 등록 (한글 폰트 필요시)
font_path = "./font/NanumGothic-Regular.ttf"
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'NanumGothic'

# 타이틀
st.markdown(
    """
    <h1 style="text-align: center;">
      <mark style="
        background-color: #e6f2ff;
        color: #0052cc;
        font-weight: bold;
        padding: 0.2em 0.4em;
        border-radius: 0.2em;
      ">
        🌏기후 변화 요인 탐색☀️
      </mark>
    </h1>
    """,
    unsafe_allow_html=True
)

# --- 사이드바: API 키 입력 ---
st.sidebar.title("🔐 OpenAI API 설정")
api_key = st.sidebar.text_input("API 키를 입력하세요", type="password")

# 한 줄 띄우기
st.markdown("<br><br>", unsafe_allow_html=True)

# 활동 설명
st.markdown(
    "<h4>💬기후 변화 요인에 대해 물어보세요!</h4>",
    unsafe_allow_html=True
)

user_input = st.text_area("나의 질문:")

if st.button("보내기"):
    if not api_key:
        st.error("❌ API 키를 먼저 입력해주세요.")
    elif not user_input.strip():
        st.warning("질문을 입력해주세요.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "친절한 선생님처럼 대답해주세요."},
                    {"role": "user", "content": user_input}
                ]
            )
            st.success("✅ GPT 응답:")
            st.markdown(response.choices[0].message.content)

        except AuthenticationError:
            st.error("🚫 API 키가 올바르지 않습니다. 다시 확인해주세요.")
        except Exception as e:
            st.error(f"⚠️ 오류 발생: {e}")

    # GPT 분석
    question = st.text_area("🤖 이 데이터에 대해 GPT에게 질문해보세요.")
    if st.button("GPT에게 물어보기") and api_key and question:
        prompt = f"다음은 환경 데이터입니다:\n{df.head().to_csv(index=False)}\n\n질문: {question}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        st.markdown("🧠 **GPT의 응답:**")
        st.write(response.choices[0].message.content)
