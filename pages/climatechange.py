import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import hashlib
from matplotlib import font_manager

# NanumGothic 폰트 파일 경로 지정 및 등록 (한글 폰트 필요시)
font_path = "./font/NanumGothic-Regular.ttf"
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'NanumGothic'

        

# 1. CSV 파일 로드 함수 (캐싱 + 업로더 + 기본 경로 지원)
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)
    default_path = 'data/climate_change.csv'
    if os.path.exists(default_path):
        return pd.read_csv(default_path)
    st.error(f"CSV 파일을 찾을 수 없습니다: {default_path}")
    st.stop()

# 사이드바에 파일 업로더 추가
st.sidebar.markdown("## 데이터 업로드")
uploaded = st.sidebar.file_uploader(
    label="CSV 파일을 업로드하거나, 업로드하지 않으면 기본 데이터를 불러옵니다.",
    type=['csv']
)

# 데이터 로드
df = load_data(uploaded)

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

# 넓은 줄 간격
st.markdown(
    "<div style='height:85px'></div>",
    unsafe_allow_html=True
)

st.markdown(
    "<h3 style='color:#000080;'>활동1. 데이터 탐색</h3>",
    unsafe_allow_html=True
)
st.dataframe(df, height=235)

# A. 각 열의 의미 설명 표 (원본 데이터 아래에 위치)
st.markdown("###### ☞ 참고 자료")

col_desc = pd.DataFrame({
    "용어": ["Temp", "TSI", "CO2", "CH4", "N2O", "CFC-11", "CFC-12"],
    "정의": [
        "지표면 평균 온도 편차( anomaly, 단위: °C, 기준시점 평균과의 차이)",
        "총 태양복사량( Total Solar Irradiance, 단위: W/m² )",
        "대기 중 이산화탄소 농도 (단위: ppm)",
        "대기 중 메탄 농도 (단위: ppb)",
        "대기 중 아산화질소 농도 (단위: ppb)",
        "대기 중 프레온가스(CFC-11, CFCl₃) 농도 (단위: ppt)",
        "대기 중 프레온가스(CFC-12, CF₂Cl₂) 농도 (단위: ppt)"
    ]
})

with st.expander("각 열(용어) 설명 보기", expanded=False):
    st.table(col_desc)


numeric_cols = df.select_dtypes(include=[np.number]).columns
filtered_numeric_cols = [c for c in numeric_cols if c.lower() not in ['year', 'month']]
value_cols = filtered_numeric_cols  # 2번 항목에서 사용
corr = df[filtered_numeric_cols].corr()  # 3번 항목에서 사용
color_list = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']

# 넓은 줄 간격
st.markdown(
    "<div style='height:85px'></div>",
    unsafe_allow_html=True
)

# 2. 시간에 따른 컬럼의 수치 변화 그래프 조회
st.markdown(
    "<h3 style='color:#000080;'>활동2. 시간에 따른 각 요소의 수치 변화 탐색</h3>",
    unsafe_allow_html=True
)

# 드롭다운에 표시할 요소를 순서대로 정의
cols = ["Temp", "TSI", "CO2", "CH4", "N2O", "CFC-11", "CFC-12"]

selected_col = st.selectbox(
    "※ x축: 시간(1983~2008) / y축: 선택한 요소",
    ["요소 선택"] + cols,  # 첫 옵션 이후에 원하는 순서대로
    index=0,               
    key="trend_col"
)

# "요소 선택"이 아닐 때만 그래프 생성
if selected_col != "요소 선택":
    # 시간축 설정 (이전과 동일)
    if 'Year' in df.columns and 'Month' in df.columns:
        time = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str) + '-01')
        x_label = "연도-월"
    elif 'Year' in df.columns:
        time = df['Year']
        x_label = "연도"
    elif 'Month' in df.columns:
        time = df['Month']
        x_label = "월"
    else:
        time = df.index
        x_label = "Index"

    # 컬러 인덱스도 cols 기준으로 잡아줍니다
    color_idx = cols.index(selected_col) % len(color_list)
    line_color = color_list[color_idx]

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(time, df[selected_col], marker='o', linestyle='-', color=line_color)
    ax.set_xlabel(x_label)
    ax.set_ylabel(selected_col)

    if selected_col.lower() == "temp":
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:+.2f}"))

    ax.set_title(f"{selected_col}의 시간에 따른 수치 변화")
    fig.autofmt_xdate()
    st.pyplot(fig)
else:
    st.markdown(
        """
        <div style="height:220px; background:#eee; border-radius:8px;
                    display:flex; align-items:center; justify-content:center;">
            <span style="color:#888;">그래프가 이 영역에 표시됩니다.</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# 넓은 줄 간격
st.markdown(
    "<div style='height:85px'></div>",
    unsafe_allow_html=True
)

# 3. 기온 변화에 영향 미치는 요인 분석
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='color:#000080;'>활동3. 지표면 온도 변화에 영향 미치는 요인 탐색</h3>",
    unsafe_allow_html=True
)

# 3-1. 상관관계 조회(기온 편차 ~ 요인 변화)
st.markdown("#####   가. 상관관계(온도편차 ~ 요인변화) 그래프 조회")

factor_cols = ["TSI", "CO2", "CH4", "N2O", "CFC-11", "CFC-12"]

if len(filtered_numeric_cols) >= 2:
    # x축은 'Temp'로 고정
    if 'Temp' in filtered_numeric_cols:
        col1 = 'Temp'
    else:
        st.warning("'Temp' 컬럼이 데이터에 없습니다. x축을 고정할 수 없습니다.")
        col1 = filtered_numeric_cols[0]

    # '요인 선택' 초기값 + 지정된 순서의 컬럼들만 드롭다운
    col2 = st.selectbox(
        "※ x축: 온도 편차 / y축: 요인 크기",
        ["요인 선택"] + factor_cols,
        index=0,
        key="col2"
    )

    if col2 != "요인 선택":
        corr_value = df[[col1, col2]].corr().iloc[0, 1]
        st.write(f"**{col1}**와 **{col2}**의 상관계수: **{corr_value:.3f}**")

        def get_color(col1, col2):
            combo = col1 + col2
            hash_val = int(hashlib.md5(combo.encode()).hexdigest(), 16)
            cmap = plt.get_cmap('tab10')
            return cmap(hash_val % 10)

        scatter_color = get_color(col1, col2)

        fig_scatter, ax_scatter = plt.subplots(figsize=(5, 3))
        ax_scatter.scatter(df[col1], df[col2], color=scatter_color)
        ax_scatter.set_xlabel(col1)
        ax_scatter.set_ylabel(col2)
        ax_scatter.set_title(f"{col1} vs {col2} 산점도")
        st.pyplot(fig_scatter)
    else:
        st.markdown(
            """
            <div style="height:180px; background:#eee; border-radius:8px; display:flex; align-items:center; justify-content:center;">
                <span style="color:#888;">그래프가 이 영역에 표시됩니다.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.warning("분석 가능한 수치형 컬럼이 2개 이상 필요합니다.")



# 한 줄 띄우기
st.markdown("<br><br>", unsafe_allow_html=True)

# 3-2. 전체 상관관계 비교
st.markdown("#####   나. 전체 상관계수 비교")
with st.expander("#### 펼쳐보기", expanded=False):
    styled_corr = (
        corr.style
            .background_gradient(cmap='coolwarm', vmin=-1, vmax=1)
            .format("{:.2f}")
    )
    st.write(styled_corr)

st.markdown(
    """
    <h6 style="
        text-align: right;
        color: #4a4a4a;
        font-style: italic;
        font-size: 90%;
        font-weight: 365;
    ">
        ※ 상관계수: -1 ≤ r ≤ 1 (+1:완전한 양의 상관, 0은 무상관, -1:완전한 음의 상관)
    </h6>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# 퀴즈

st.markdown("###### Q1. Temp와 가장 강한 상관을 갖는 요인은?")
with st.form("q1_form"):
    col_input, col_btn, col_ans = st.columns([3, 1, 2])
    with col_input:
        q1_answer = st.text_input("정답 입력", key="q1_input")
    with col_btn:
        q1_submitted = st.form_submit_button("제출")
    with col_ans:
        if q1_submitted:
            st.markdown(
                "<span style='color:#0052cc;'> 1위: CO2, 2위: N2O</span>",
                unsafe_allow_html=True
            )

st.markdown("<br>", unsafe_allow_html=True)


st.markdown("###### Q2. TSI와 Temp 간의 상관계수는 타 요인에 비해 작다. 그 의미는?")
with st.form("q2_form"):
    col_input, col_btn, col_ans = st.columns([3, 1, 2])
    with col_input:
        q2_answer = st.text_input("정답 입력", key="q2_input")
    with col_btn:
        q2_submitted = st.form_submit_button("제출")
    with col_ans:
        if q2_submitted:
            st.markdown(
                "<span style='color:#0052cc;'> 태양복사량 변화(자연적 요인)는 기온 변화의 주요 원인이 아니다!</span>",
                unsafe_allow_html=True
            )

st.markdown("<br>", unsafe_allow_html=True)


st.markdown("###### Q3. CO2와 N2O, CH4와 CFC-12 간의 상관계수는 크게 나타난다. 그 의미는?")
with st.form("q3_form"):
    col_input, col_btn, col_ans = st.columns([3, 1, 2])
    with col_input:
        q3_answer = st.text_input("정답 입력", key="q3_input")
    with col_btn:
        q3_submitted = st.form_submit_button("제출")
    with col_ans:
        if q3_submitted:
            st.markdown(
                "<span style='color:#0052cc;'> 각 요인의 발생 원인/메커니즘의 유사성? ☞ 탐구해보자!</span>",
                unsafe_allow_html=True
            )


