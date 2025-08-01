import streamlit as st
from PIL import Image
import os
import openai

# --- 사이드바: API 키 입력 ---
st.sidebar.title("🔐 OpenAI API")
api_key = st.sidebar.text_input("API 키를 입력하세요", type="password")


st.set_page_config(page_title="ENSO 시뮬레이터", layout="centered")

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
        🌏엘니뇨와 라니냐☀️
      </mark>
    </h1>
    """,
    unsafe_allow_html=True
)

# 넓은 줄 간격
st.markdown(
    "<div style='height:85px'></div>",
    unsafe_allow_html=True
)

# 무역풍 강도 조절
wind_choice = st.selectbox("💨**무역풍 강도 변화**", ["선택", "강해짐", "약해짐"])


# 2단계: 무역풍 선택 후 해류 선택 UI 노출
if wind_choice in ["강해짐", "약해짐"]:
    current_choice = st.selectbox("🌊**표층 해류 강도 변화**", ["선택", "강해짐", "약해짐"])


    
# 조건 충족 여부 확인
if (wind_choice == "강해짐" and current_choice == "강해짐") or \
   (wind_choice == "약해짐" and current_choice == "약해짐"):
    
    # 한 줄 띄우기
    st.markdown("<br><br>", unsafe_allow_html=True)

    # 2단계 결과 출력
    if current_choice == "강해짐":
        st.info(" **무역풍/표층해류 강화에 따라 🚩동태평양 페루연안🚩에 연쇄적으로 발생하는 변화는?**")
    elif current_choice == "약해짐":
        st.info(" **무역풍/표층해류 약화에 따라 🚩동태평양 페루연안🚩에 연쇄적으로 발생하는 변화는?**")

    # 테이블 출력
    # 항목과 옵션 정의
    labels = ["용승", "표층 수온", "기온", "기압", "기후"]
    default_options = ["선택", "증가", "감소"]
    climate_options = ["선택", "더 건조해짐", "강수량 증가"] 

    # 1행에 라벨, 2행에 selectbox 수평 배치
    cols_label = st.columns(len(labels))
    for i, col in enumerate(cols_label):
        with col:
            st.markdown(
                f"<div style='background-color:#dbeafe; text-align:center; font-weight:bold; padding:10px;'>{labels[i]}</div>",
                unsafe_allow_html=True
            )

    cols_select = st.columns(len(labels))
    selections = {}

    for i, col in enumerate(cols_select):
        with col:
            opt = climate_options if labels[i] == "기후" else default_options
            # ✅ 단 한 번만 호출
            selections[labels[i]] = st.selectbox(label="", options=opt, key=f"{wind_choice}_{current_choice}_{labels[i]}_sel")

    # --- 결과 판별 로직 ---
if wind_choice == "강해짐" and current_choice == "강해짐":
    if all(v != "선택" for v in selections.values()):
        if (
            selections["용승"] == "증가" and
            selections["표층 수온"] == "감소" and
            selections["기온"] == "감소" and
            selections["기압"] == "증가" and
            selections["기후"] == "더 건조해짐"
        ):
            st.error("⚠️ **라니냐 발생 😱😱😱**")

            # 한 줄 띄우기
            st.markdown("<br><br>", unsafe_allow_html=True)

            # ✅ GPT 챗봇 노출
            st.markdown("### 🦸‍♂️ 라니냐에 대해 GPT에게 질문해보세요!")
            if api_key:
                # 2. 질문 입력 (→ 여기서 user_question 정의됨)
                user_question = st.text_input("💬 질문을 입력하세요:")

                # 3. 질문이 입력되었을 때 GPT 호출
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
                        except Exception as e:
                            st.error(f"⚠️ 에러 발생:\n\n{e}")
        else:
            st.warning("❗❗❗**다시 생각해보세요 🤔🤔🤔**")

    elif wind_choice == "약해짐" and current_choice == "약해짐":
        if all(v != "선택" for v in selections.values()):  # ✅ 모든 항목이 선택되었을 때만 판단
            if (
                selections["용승"] == "감소" and
                selections["표층 수온"] == "증가" and
                selections["기온"] == "증가" and
                selections["기압"] == "감소" and
                selections["기후"] == "강수량 증가"
            ):
                st.error("⚠️ 엘니뇨 발생!!!")
                # 한 줄 띄우기
                st.markdown("<br><br>", unsafe_allow_html=True)

                # ✅ GPT 챗봇 노출
                st.markdown("### 🦸‍♂️ 엘니뇨에 대해 GPT에게 질문해보세요!")
                if api_key:
                    # 2. 질문 입력 (→ 여기서 user_question 정의됨)
                    user_question = st.text_input("💬 질문을 입력하세요:")

                    # 3. 질문이 입력되었을 때 GPT 호출
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
                            except Exception as e:
                                st.error(f"⚠️ 에러 발생:\n\n{e}")
            else:
                st.warning("❗ 다시 생각해보세요^^")