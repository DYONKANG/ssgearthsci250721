import streamlit as st

st.set_page_config(page_title="SSG_EARTHSCI_2025", layout="centered")

st.title("🎈SSG_EARTHSCIENCE_2025🎈")

st.markdown(
    """
    <div style="text-align: right; font-size: 20px; margin-top: 30px;">
        선사고등학교 지구과학교사 강지연
    </div>
    """,
    unsafe_allow_html=True
)

# 한 줄 띄우기
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("#### 🌎 기후 변화 수업 계획 및 차시별 내용 안내")

# 전체 수업 계획 표
st.markdown("#### 📌 전체 수업 계획")
st.markdown("""
<table style='width:100%; border-collapse: collapse;'>
  <tr style='background-color:#ffda7c; font-weight:bold;'>
    <td>수업주제</td><td>기후 변화 탐구</td>
  </tr>
  <tr><td>수업대상</td><td>고등학교 2학년</td></tr>
  <tr><td>예상차시</td><td>3</td></tr>
  <tr><td>주요과목</td><td> <b>지구과학Ⅰ / IV. 대기와 해양의 상호작용</b><br>
  <tr>
    <td>관련 역량 및 성취기준</td>
    <td>
      <b>- 관련 역량</b><br>
      논리적 사고, 의사소통 및 협업 능력, 기후 문해력, 기후 감수성, 디지털 역량<br>
      <b>- 성취 기준</b><br>
      [12지과Ⅰ 04-03] 해수의 순환 및 순환 작용의 사례로서 해수의 용승과 침강, 남방진동의 발생 과정과 관련 현상을 이해한다.<br>
      [12지과Ⅰ 04-04] 기후 변화의 원인을 자연적 요인과 인위적 요인으로 구분하여 설명하고, 인간 활동에 의한 기후 변화의 환경적, 사회적 및 경제적 영향과 기후 변화 문제를 과학적으로 해결하는 방법에 대해 토의할 수 있다.
    </td>
  </tr>
  <tr>
    <td>수업목표</td>
    <td>
      1. 남방진동(ENSO)의 원리 이해<br>
      2. 기후 변화의 자연적 요인/인위적 요인 구분<br>
      3. 기후 변화 데이터 분석
    </td>
  </tr>
  <tr>
    <td>애플리케이션 사용 계획(간략히)</td>
    <td>
      1. 연쇄적으로 발생하는 대기-해양의 변화 시뮬레이션<br>
      2. 기후 변화의 요인 탐색 챗봇<br>
      3. 기후변화 데이터 분석 앱
    </td>
  </tr>
</table>
""", unsafe_allow_html=True)

# 차시별 수업 내용 표
st.markdown("#### 📌 차시별 수업 내용")
st.markdown("""
<table style='width:100%; border-collapse: collapse;'>
  <tr style='background-color:#d6e7ff;; font-weight:bold;'>
    <td>1차시<br>(프로젝트2)</td>
    <td>[남방진동(ENSO) 원리 이해] <br>무역풍 강도 변화에 따라 '동태평양 표층 해수의 이동 강도 → 용승 강도 → 표층 수온 → 해수면 기온 → 해수면 기압 → 날씨/강수량'과 같이 연쇄적인 변화가 발생하는 것을 탐구/확인할 수 있는 시뮬레이션을 설계하여 학생들이 주도적으로 ‘엘니뇨’와 ‘라니냐’의 개념을 이해해나가는 과정<br>을 지원한다.</td>
  </tr>
  <tr>
    <td>2차시</td>
    <td>[기후 변화 요인 탐색]<br>기후 변화에 영향을 미치는 자연적 요인과 인위적 요인에 대해 탐색할 수 있는 챗봇을 개발하여 학생들이 주어진 과제 해결 시 챗봇과의 소통을 통해 능동적으로 참여할 수 있도록 유도한다.</td>
  </tr>
  <tr style='background-color:#d6e7ff;'>
    <td>3차시<br>(중간 프로젝트)</td>
    <td>[기후 변화 데이터 분석]<br>기후 변화 데이터를 2가지 방법(시계열/상관관계)으로 분석하여 시각화해주는 앱을 개발하여 학생들이 기후 변화를 체감하고 그 결정적 원인이 인간에게 있음을 입증하는 데이터 기반 탐구 활동을 진행한다.</td>
  </tr>
</table>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)



