import streamlit as st

@st.dialog("🔑 OpenAI API 키 등록")
def api_key_dialog():
    st.write("OpenAI API 키를 입력해 주세요.")
    st.caption("🔒 **보안 안내**: 입력하신 API 키는 세션 메모리(`st.session_state`)에만 임시 보관되며, 데이터베이스나 파일, 깃 리포지터리에는 절대 저장되지 않습니다.")
    
    current_key = st.session_state.get("openai_api_key", "")
    input_key = st.text_input("OpenAI API Key", value=current_key, type="password", placeholder="sk-...")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("키 저장", type="primary", use_container_width=True):
            if input_key.strip():
                st.session_state.openai_api_key = input_key.strip()
                st.success("API 키가 메모리에 등록되었습니다.")
                st.rerun()
            else:
                st.error("올바른 키를 입력해 주세요.")
    with col2:
        if st.button("키 삭제", use_container_width=True):
            st.session_state.openai_api_key = ""
            st.info("등록된 API 키가 삭제되었습니다.")
            st.rerun()

def has_api_key():
    """현재 세션에 API 키가 등록되어 있는지 확인"""
    return bool(st.session_state.get("openai_api_key"))

def render_api_key_sidebar():
    """사이드바에 API 키 등록 상태 및 버튼 표시"""
    st.sidebar.subheader("OpenAI API 키")
    if has_api_key():
        st.sidebar.success("✅ API 키 등록 완료")
        if st.sidebar.button("🔑 API 키 변경/삭제", use_container_width=True):
            api_key_dialog()
    else:
        st.sidebar.warning("⚠️ API 키 미등록")
        if st.sidebar.button("🔑 API 키 등록", use_container_width=True):
            api_key_dialog()

