from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

from modules.database import (
    init_db,
    get_sessions,
    create_session,
    update_session_title,
    load_messages,
    save_message,
    delete_session,
    get_turn_count,
)
from modules.auth import login_page
from modules.api_key import render_api_key_sidebar, has_api_key
from modules.theme import apply_theme

# 환경변수 로드
load_dotenv()

# --- 채팅 페이지 함수 ---
def chat_page():
    current_user = st.session_state.get("username")

    # 세션 목록 조회 및 기본 세션 보장 (로그인 사용자 기준, 최대 10개)
    sessions = get_sessions(username=current_user)
    if not sessions:
        initial_id = create_session(username=current_user, title="새 대화")
        sessions = get_sessions(username=current_user)
    else:
        initial_id = sessions[0][0]

    if "current_session_id" not in st.session_state or not st.session_state.current_session_id:
        st.session_state.current_session_id = initial_id

    # 현재 세션 ID 유효성 점검
    session_ids = [s[0] for s in sessions]
    if st.session_state.current_session_id not in session_ids:
        st.session_state.current_session_id = session_ids[0]

    st.title("OpenAI 채팅")

    # 사이드바: 대화방 관리 (최대 10개 세션 제한)
    st.sidebar.header("대화방 관리")
    st.sidebar.caption(f"보유 세션: {len(sessions)} / 10개 (11번째 생성 시 가장 오래된 세션 자동 삭제)")

    # 새 대화 시작 버튼 (10개 초과 시 FIFO 자동 삭제)
    if st.sidebar.button("➕ 새로운 대화 시작"):
        new_session_id = create_session(username=current_user, title="새 대화")
        st.session_state.current_session_id = new_session_id
        st.session_state.messages = []
        st.session_state.loaded_session_id = new_session_id
        st.rerun()

    # 대화 목록 선택 드롭다운
    session_dict = {s[0]: s[1] for s in sessions}
    current_idx = session_ids.index(st.session_state.current_session_id)
    selected_id = st.sidebar.selectbox(
        "대화 목록",
        options=session_ids,
        index=current_idx,
        format_func=lambda x: session_dict.get(x, x)
    )

    # 대화방 변경 감지
    if selected_id != st.session_state.current_session_id:
        st.session_state.current_session_id = selected_id
        st.session_state.messages = load_messages(selected_id)
        st.session_state.loaded_session_id = selected_id
        st.rerun()

    # 현재 대화방 삭제 버튼
    if st.sidebar.button("🗑️ 현재 대화방 삭제"):
        delete_session(st.session_state.current_session_id)
        remaining_sessions = get_sessions(username=current_user)
        if remaining_sessions:
            st.session_state.current_session_id = remaining_sessions[0][0]
        else:
            st.session_state.current_session_id = create_session(username=current_user, title="새 대화")
        st.session_state.messages = load_messages(st.session_state.current_session_id)
        st.session_state.loaded_session_id = st.session_state.current_session_id
        st.rerun()

    st.sidebar.divider()

    # 사이드바: 설정 영역 (API 키 및 모델)
    st.sidebar.header("설정")
    
    # 1) API 키 관리 (modules.api_key)
    render_api_key_sidebar()

    # 2) 모델 선택
    AVAILABLE_MODELS = [
        "gpt-5.6-luna",
        "gpt-5.6-terra",
        "gpt-5.6-sol",
        "gpt-5.5",
    ]
    model_name = st.sidebar.selectbox("모델 선택 (GPT 5.5+)", AVAILABLE_MODELS, index=0)

    # 3) 현재 대화방 턴 수 정보 표시 (요구사항 5번: 세션당 최대 100회)
    turn_count = get_turn_count(st.session_state.current_session_id)
    st.sidebar.caption(f"💬 대화 횟수: {turn_count} / 100회")
    st.sidebar.progress(turn_count / 100)

    # 세션 상태 메시지 동기화
    if "messages" not in st.session_state or st.session_state.get("loaded_session_id") != st.session_state.current_session_id:
        st.session_state.messages = load_messages(st.session_state.current_session_id)
        st.session_state.loaded_session_id = st.session_state.current_session_id

    # 이전 대화 내용 화면에 출력 (텍스트 전용)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # 채팅 입력 제어 (API 키 등록 여부 & 100회 한도 검사)
    if not has_api_key():
        st.warning("⚠️ OpenAI API 키가 등록되지 않았습니다. 사이드바의 **'🔑 API 키 등록'** 버튼을 눌러 키를 먼저 등록해 주세요.")
        prompt = st.chat_input("API 키를 등록해야 대화할 수 있습니다...", disabled=True)
    elif turn_count >= 100:
        st.error("🚫 이 대화방의 최대 대화 한도(100회)에 도달했습니다. 새로운 대화를 시작해 주세요.")
        prompt = st.chat_input("대화 한도(100회)에 도달했습니다...", disabled=True)
    else:
        prompt = st.chat_input("메시지를 입력하세요...")

    if prompt:
        # 첫 대화 시 세션 제목을 첫 질문(앞 20자)으로 갱신
        if session_dict.get(st.session_state.current_session_id) == "새 대화":
            new_title = prompt[:20] + ("..." if len(prompt) > 20 else "")
            update_session_title(st.session_state.current_session_id, new_title)

        # 사용자 메시지 화면 출력 및 세션 상태 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        save_message(st.session_state.current_session_id, "user", prompt)

        with st.chat_message("user"):
            st.write(prompt)

        # API 전송용 메시지 목록 구성 (순수 텍스트)
        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # 어시스턴트 응답 스트리밍 출력
        with st.chat_message("assistant"):
            client = OpenAI(api_key=st.session_state.openai_api_key)
            stream = client.chat.completions.create(
                model=model_name,
                messages=api_messages,
                stream=True,
            )
            response_text = st.write_stream(stream)

        # 어시스턴트 응답 세션 상태 및 DB 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text
        })
        save_message(st.session_state.current_session_id, "assistant", response_text)
        st.rerun()

# --- 메인 실행부 및 멀티페이지 네비게이션 제어 ---
init_db()
apply_theme()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

if not st.session_state.logged_in:
    # 미로그인 상태: 로그인 페이지만 노출
    pg = st.navigation([st.Page(login_page, title="로그인", icon="🔒")])
    pg.run()
else:
    # 로그인 상태: 상단 유저 안내 및 로그아웃 버튼, 메인 네비게이션 노출
    st.sidebar.markdown(f"👤 **{st.session_state.username}**님 접속 중")
    if st.sidebar.button("🚪 로그아웃"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.messages = []
        st.session_state.current_session_id = None
        st.session_state.openai_api_key = ""
        st.rerun()

    chat_page_def = st.Page(chat_page, title="OpenAI 채팅", icon="💬", default=True)
    history_page_def = st.Page("modules/app2_history.py", title="과거 채팅 내역", icon="📜", url_path="history")

    pg = st.navigation([chat_page_def, history_page_def])
    pg.run()
