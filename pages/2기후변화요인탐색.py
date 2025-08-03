import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager
from openai import OpenAI
import io


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

import streamlit as st
from openai import OpenAI, AuthenticationError
import pandas as pd
import io

# --- 세션 상태 초기화 ---
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0
if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False

# --- 사이드바: API 키 입력 ---
st.sidebar.title("🔐 OpenAI API 설정")
api_key = st.sidebar.text_input("API 키를 입력하세요", type="password")

# 한 줄 띄우기
st.markdown("<br><br>", unsafe_allow_html=True)

# 활동 설명
st.markdown("<h5>💬GPT에게 기후 변화 요인과 관련된 🎉5개🎉의 질문을 던져보세요</h5>", unsafe_allow_html=True)

# ✅ 10세트가 끝났을 경우 종료 메시지
if st.session_state.chat_ended:
    st.warning("✅ GPT와의 대화가 종료되었습니다.")

    # 대화 내용을 DataFrame으로 정리
    df = pd.DataFrame(st.session_state.chat_log)

    # txt 파일 만들기
    txt_io = io.StringIO()
    for i, row in df.iterrows():
        txt_io.write(f"[질문{i+1}] {row['질문']}\n[답변{i+1}] {row['답변']}\n\n")
    txt_data = txt_io.getvalue().encode()

    # csv 파일 만들기
    csv_data = df.to_csv(index=False).encode()

    # 다운로드 버튼
    st.download_button("📄 대화 내역 TXT 다운로드", txt_data, file_name="gpt_chat.txt")

# ✅ 대화 가능할 경우 질문 입력
if not st.session_state.chat_ended:
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
                gpt_answer = response.choices[0].message.content

                # 결과 출력
                st.success("✅ GPT 응답:")
                st.markdown(gpt_answer)

                # 로그에 저장
                st.session_state.chat_log.append({"질문": user_input, "답변": gpt_answer})
                st.session_state.chat_count += 1

                # 대화 5세트 도달 시 종료
                if st.session_state.chat_count >= 5:
                    st.session_state.chat_ended = True

            except AuthenticationError:
                st.error("🚫 API 키가 올바르지 않습니다. 다시 확인해주세요.")
            except Exception as e:
                st.error(f"⚠️ 오류 발생: {e}")
