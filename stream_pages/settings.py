import streamlit as st

st.title("⚙️ 환경 설정 페이지")
st.write("개별 파일(`settings.py`)로 분리된 설정 화면입니다.")

theme = st.selectbox("테마 선택", ["Light", "Dark", "System"])
notifications = st.toggle("알림 활성화", value=True)
language = st.radio("언어 설정", ["한국어", "English", "日本語"])

st.write(f"현재 설정: 테마=**{theme}**, 알림=**{notifications}**, 언어=**{language}**")

