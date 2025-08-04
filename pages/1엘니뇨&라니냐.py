import os
import streamlit as st
from PIL import Image
import openai
import io
import json
import tempfile

# 페이지 설정
st.set_page_config(page_title="ENSO 방탈출", layout="centered")
st.sidebar.title("🔐 설정 영역")
api_key = st.sidebar.text_input("OpenAI API 키", type="password")

# 세션 초기화
if "is_correct" not in st.session_state:
    st.session_state.is_correct = None
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0
if "chat_ended" not in st.session_state:
    st.session_state.chat_ended = False
if "match" not in st.session_state:
    st.session_state.match = False

# 타이틀
st.markdown("""
<h1 style="text-align: center;">
  <mark style="background-color: #e6f2ff; color: #0052cc; font-weight: bold; padding: 0.2em 0.4em; border-radius: 0.2em;">
    🌏엘니뇨와 라니냐☀
  </mark>
</h1>
""", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# 이미지
img = Image.open("./data/normal.png")
st.image(img, caption="남태평양의 대기와 해양(정상 상태)", width=580)
st.info(" **[미션1] 위의 그림을 참고하여 남태평양 대기와 해양의 특징을 파악해봅시다.**")

# 탐구 결과 입력
with st.expander("🧪 탐구 결과 입력하기"):
    st.markdown("#### 아래 질문에 답해보세요:")
    ans1 = st.text_input("1) 남태평양에 영향을 주는, 대기 대순환에 의해 발생한 지상풍의 명칭은? (5글자)", key="q1")
    ans2 = st.text_input("2) 서태평양을 향해 흐르는 표층 해류의 발생 원인은? (5글자)", key="q2")
    ans3 = st.text_input("3) 평상 시 동태평양(페루 연안)은 서태평양(호주)에 비해 표층 수온이 낮다. 그 원인은? (2글자)", key="q3")
    ans4 = st.text_input("4) 평상 시 동태평양(페루 연안)은 서태평양(호주)에 비해 강수량이 적다. 그 원인은? (3글자)", key="q4")

    if st.button("✅ 정답 확인", key="check_answers"):
        if ans1.strip() == "남동무역풍" and ans2.strip() == "남동무역풍" and ans3.strip() == "용승" and ans4.strip() == "고기압":
            st.session_state.is_correct = True
        else:
            st.session_state.is_correct = False

# 미션2
if st.session_state.is_correct:
    st.success("🎉 정답입니다! **미션2**로 넘어가세요.")
    st.info(" **[미션2] 기후 변화로 인해 무역풍의 강도가 달라지면?**")
    wind_choice = st.selectbox("💨무역풍 강도 변화", ["선택", "강해짐", "약해짐"])
    if wind_choice in ["강해짐", "약해짐"]:
        current_choice = st.selectbox("🌊표층 해류 강도 변화", ["선택", "강해짐", "약해짐"])

        if (wind_choice, current_choice) in [("강해짐", "강해짐"), ("약해짐", "약해짐")]:
            st.info("**[미션2-2] 동태평양 페루연안의 연쇄적 변화 탐색**")
            labels = ["용승", "표층 수온", "기온", "기압", "기후"]
            default_options = ["선택", "증가", "감소"]
            climate_options = ["선택", "더 건조해짐", "강수량 증가"]
            cols_label = st.columns(len(labels))
            for i, col in enumerate(cols_label):
                with col:
                    st.markdown(f"<div style='background-color:#dbeafe; text-align:center; font-weight:bold; padding:10px;'>{labels[i]}</div>", unsafe_allow_html=True)

            selections = {}
            cols_select = st.columns(len(labels))
            for i, col in enumerate(cols_select):
                with col:
                    opt = climate_options if labels[i] == "기후" else default_options
                    selections[labels[i]] = st.selectbox("", opt, key=f"{wind_choice}_{current_choice}_{labels[i]}")

            expected = {
                "강해짐": {"용승": "증가", "표층 수온": "감소", "기온": "감소", "기압": "증가", "기후": "더 건조해짐"},
                "약해짐": {"용승": "감소", "표층 수온": "증가", "기온": "증가", "기압": "감소", "기후": "강수량 증가"}
            }[wind_choice]

            if all(selections[k] == v for k, v in expected.items()):
                st.session_state.match = True
                if wind_choice == "강해짐":
                    st.error("⚠ 라니냐 발생!")
                    st.image(Image.open("./data/lanina.png"), width=700)
                else:
                    st.error("⚠ 엘니뇨 발생!")
                    st.image(Image.open("./data/elnino.png"), width=700)
                st.info("**[미션3] 엘니뇨/라니냐에 대해 GPT에게 질문해보세요!**")
            else:
                st.warning("❗ 다시 생각해보세요")

# GPT 대화
if api_key and st.session_state.match:
    if not st.session_state.chat_ended:
        with st.expander("💡 질문 가이드"):
            st.markdown("""
- 엘니뇨의 판단 기준은?
- 엘니뇨 시기에 남태평양 일대에 발생하는 피해는?
- 라니냐 시기에 우리나라가 겪는 변화는?
- 라니냐와 지구 온난화의 관련성은?
            """)
        user_question = st.text_input("💬 질문을 입력하세요:")
        if user_question:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("GPT가 생각 중입니다..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "당신은 고등학생을 위한 기후 과학 설명 전문가입니다."},
                            {"role": "user", "content": user_question}
                        ]
                    )
                    answer = response.choices[0].message.content
                    st.success("🤖 GPT의 답변:")
                    st.write(answer)
                    st.session_state.chat_log.append({"질문": user_question, "답변": answer})
                    st.session_state.chat_count += 1
                    if st.session_state.chat_count >= 3:
                        st.session_state.chat_ended = True
                except Exception as e:
                    st.error(f"⚠ 에러 발생:\n\n{e}")
    else:
        st.warning("✅ GPT와의 대화가 종료되었습니다 (총 3회 진행됨)")
        buffer = io.StringIO()
        for i, entry in enumerate(st.session_state.chat_log):
            buffer.write(f"[질문 {i+1}]\n{entry['질문']}\n[답변 {i+1}]\n{entry['답변']}\n\n")
        txt_data = buffer.getvalue().encode("utf-8")
        st.download_button("📄 대화 내역 TXT 다운로드", txt_data, file_name="gpt_대화기록.txt")

        # 추가 학습 링크
        st.markdown("""
        <div style='text-align: center; margin-top: 20px;'>
            <a href='https://chatgpt.com/g/g-688366dc3ee081919a9e7fd6b4a02c66-enso-seolmyeonggi' target='_blank'>
                <button style='background-color:#5b9bd5; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:5px;'>
                    ☞ 챗봇과 추가 학습하러 가기
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.is_correct is False:
    st.warning("❗ 다시 생각해보세요")