import streamlit as st
from modules.database import get_sessions, load_messages, delete_session

current_user = st.session_state.get("username")

st.title("과거 채팅 내역")

# 세션 목록 조회 (현재 로그인 사용자 기준)
sessions = get_sessions(username=current_user)

if not sessions:
    st.info("저장된 대화 기록이 없습니다.")
else:
    session_ids = [s[0] for s in sessions]
    session_dict = {s[0]: s[1] for s in sessions}

    # 대화방 선택
    selected_id = st.sidebar.selectbox(
        "확인할 대화방 선택",
        options=session_ids,
        format_func=lambda x: session_dict.get(x, x)
    )

    # 대화방 삭제 버튼
    if st.sidebar.button("🗑️ 선택한 대화방 삭제"):
        delete_session(selected_id)
        st.rerun()

    st.subheader(f"대화 주제: {session_dict.get(selected_id, '대화')}")

    # 선택한 대화방의 메시지 로드
    messages = load_messages(selected_id)

    if not messages:
        st.caption("이 대화방에는 메시지가 없습니다.")
    else:
        for msg in messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

