import streamlit as st

st.title("🔗 링크 모음 페이지 (st.page_link)")
st.write("`st.page_link`를 사용한 다양한 내부 및 외부 이동 링크 예제입니다.")

st.subheader("1. 내부 페이지 링크")
st.page_link("stream_pages/dashboard.py", label="대시보드로 이동", icon="📊")
st.page_link("stream_pages/settings.py", label="설정 페이지로 이동", icon="⚙️")
st.page_link("stream_pages/login.py", label="로그인 페이지로 이동", icon="🔑", use_container_width=True)

st.subheader("2. 비활성화된 링크")
st.page_link("stream_pages/settings.py", label="접근 불가능한 링크 (disabled=True)", icon="🔒", disabled=True)

st.subheader("3. 외부 URL 링크 (새 탭으로 열기)")
st.page_link("https://docs.streamlit.io", label="Streamlit 공식 문서 바로가기", icon="🌐")
st.page_link("https://github.com", label="GitHub 바로가기", icon="🐙")

