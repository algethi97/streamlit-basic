import streamlit as st
from modules.database import get_or_create_user

def login_page():
    st.title("🚀 시작하기")

    # API 키 보안 보장 안내
    st.info(
        "🔒 **보안 안내**: 입력하신 OpenAI API 키는 브라우저 세션 메모리(`st.session_state`)에만 "
        "임시 보관되며, 데이터베이스나 로컬 파일 등 어디에도 저장되지 않습니다."
    )

    nickname = st.text_input("닉네임", placeholder="대화에 사용할 닉네임을 입력하세요")
    api_key = st.text_input("OpenAI API 키", type="password", placeholder="sk-...")

    if st.button("접속하기", type="primary", use_container_width=True):
        if not nickname.strip():
            st.error("닉네임을 입력해 주세요.")
        elif not api_key.strip():
            st.error("OpenAI API 키를 입력해 주세요.")
        else:
            clean_name = nickname.strip()
            get_or_create_user(clean_name)
            st.session_state.logged_in = True
            st.session_state.username = clean_name
            st.session_state.openai_api_key = api_key.strip()
            st.session_state.messages = []
            st.session_state.current_session_id = None
            st.success(f"{clean_name}님, 접속되었습니다!")
            st.rerun()
