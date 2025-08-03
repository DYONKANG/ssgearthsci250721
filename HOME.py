import streamlit as st

st.title("🎈SSG_EARTHSCI_2025🎈")


st.header("헤더 예시")  # ② 헤더

st.subheader("서브헤더 예시")  # ③ 서브헤더

st.text("텍스트 예시입니다.")  # ④ 일반 텍스트

st.markdown("**마크다운 예시**: _굵게, 이탤릭, 링크 등 지원합니다._")  # ⑤ 마크다운

st.code("print('Hello, Streamlit!')", language='python')  # ⑥ 코드 블록

st.latex(r"\int_a^b f(x)dx")  # ⑦ LaTeX 수식

st.write("write 함수는 다양한 타입을 자동으로 렌더링합니다.")  # ⑧ write 함수

st.divider()  # ⑨ 구분선

st.image("https://static.streamlit.io/examples/dog.jpg", caption="이미지 예시")  # ⑩ 이미지

st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")  # ⑪ 오디오

st.video("https://www.w3schools.com/html/mov_bbb.mp4")  # ⑫ 비디오

st.button("버튼 예시")  # ⑬ 버튼

st.checkbox("체크박스 예시")  # ⑭ 체크박스

st.radio("라디오 버튼 예시", ["옵션 1", "옵션 2", "옵션 3"])  # ⑮ 라디오 버튼

st.selectbox("셀렉트박스 예시", ["A", "B", "C"])  # ⑯ 셀렉트박스

st.multiselect("멀티셀렉트 예시", ["Python", "Java", "C++"])  # ⑰ 멀티셀렉트

st.slider("슬라이더 예시", 0, 100, 50)  # ⑱ 슬라이더

st.number_input("숫자 입력 예시", min_value=0, max_value=100, value=10)  # ⑲ 숫자 입력

st.text_input("텍스트 입력 예시")  # ⑳ 텍스트 입력

st.text_area("텍스트 영역 예시")  # ㉑ 텍스트 영역

st.date_input("날짜 입력 예시")  # ㉒ 날짜 입력

st.time_input("시간 입력 예시")  # ㉓ 시간 입력

st.file_uploader("파일 업로더 예시")  # ㉔ 파일 업로더

st.progress(0.5)  # ㉕ 진행률 바

st.spinner("로딩 중...")  # ㉖ 스피너

st.success("성공 메시지 예시")  # ㉗ 성공 메시지

st.info("정보 메시지 예시")  # ㉘ 정보 메시지

st.warning("경고 메시지 예시")  # ㉙ 경고 메시지

st.error("에러 메시지 예시")  # ㉚ 에러 메시지

st.metric(label="온도", value="25°C", delta="+1°C")  # ㉛ 메트릭

import pandas as pd
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})
st.dataframe(df)  # ㉜ 데이터프레임

st.table(df)  # ㉝ 테이블

import numpy as np
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)
st.line_chart(chart_data)  # ㉞ 라인 차트

st.bar_chart(chart_data)  # ㉟ 바 차트