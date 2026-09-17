import streamlit as st
from modules.database import register_user, authenticate_user

def login_page():
    st.title("🔐 로그인")

    # 보안 취약 안내 경고 배너 (요구사항 8번)
    st.warning(
        "⚠️ **보안 안내**: 본 시스템은 학습 및 사용자 구분을 위한 간이 로그인 시스템으로, "
        "비밀번호가 암호화되지 않고 평문으로 저장됩니다. 실제 사용하는 중요한 비밀번호를 절대 입력하지 마세요."
    )

    tab_login, tab_register = st.tabs(["로그인", "회원가입"])

    with tab_login:
        st.subheader("로그인")
        login_id = st.text_input("아이디", key="login_id")
        login_pw = st.text_input("비밀번호", type="password", key="login_pw")
        if st.button("로그인", key="btn_login", type="primary"):
            if authenticate_user(login_id, login_pw):
                st.session_state.logged_in = True
                st.session_state.username = login_id.strip()
                st.session_state.messages = []
                st.session_state.current_session_id = None
                st.success(f"{login_id}님, 환영합니다!")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    with tab_register:
        st.subheader("회원가입")
        reg_id = st.text_input("새 아이디", key="reg_id")
        reg_pw = st.text_input("새 비밀번호", type="password", key="reg_pw")
        reg_pw_confirm = st.text_input("비밀번호 확인", type="password", key="reg_pw_confirm")
        if st.button("회원가입", key="btn_register"):
            if reg_pw != reg_pw_confirm:
                st.error("비밀번호 확인이 일치하지 않습니다.")
            else:
                success, msg = register_user(reg_id, reg_pw)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

