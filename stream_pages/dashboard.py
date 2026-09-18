import streamlit as st

st.title("📊 대시보드 페이지")
st.write("개별 파일(`dashboard.py`)로 분리된 대시보드입니다.")

st.metric(label="오늘의 방문자 수", value="1,240명", delta="12%")
st.metric(label="활성 세션", value="85개", delta="-3%")

st.divider()
st.subheader("🚀 st.switch_page 예제 (코드 제어 페이지 이동)")
st.write("버튼 클릭 시 `st.switch_page`를 호출하여 다른 페이지로 이동합니다.")

col1, col2 = st.columns(2)
with col1:
    if st.button("⚙️ 설정 페이지로 이동", use_container_width=True):
        st.switch_page("stream_pages/settings.py")
with col2:
    if st.button("🔑 로그인 페이지로 이동", use_container_width=True):
        st.switch_page("stream_pages/login.py")

