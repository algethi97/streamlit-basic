import streamlit as st

st.title("Streamlit 로그인 예제")

# 로그인 여부 확인 및 분기 (공식 문서 표준)
if not st.user.is_logged_in:
    st.info("로그인이 필요합니다.")
    if st.button("로그인"):
        st.login()
else:
    st.success(f"안녕하세요, {st.user.name}님!")
    st.write(f"이메일: {st.user.email}")
    st.write("전체 사용자 정보:", st.user)
    
    if st.button("로그아웃"):
        st.logout()

