import base64
import sqlite3
import uuid
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# 환경변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI()

# --- SQLite 데이터베이스 함수 ---
def init_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            image_data BLOB
        )
    """)
    # 기존 DB 테이블 컬럼 호환
    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]
    if "session_id" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN session_id TEXT")
    if "image_data" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN image_data BLOB")
    conn.commit()
    conn.close()

def get_sessions():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM sessions ORDER BY rowid DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_session(title="새 대화"):
    new_id = uuid.uuid4().hex[:8]
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (id, title) VALUES (?, ?)", (new_id, title))
    conn.commit()
    conn.close()
    return new_id

def update_session_title(session_id, title):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET title = ? WHERE id = ?", (title, session_id))
    conn.commit()
    conn.close()

def load_messages(session_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role, content, image_data FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1], "image": row[2]} for row in rows]

def save_message(session_id, role, content, image_data=None):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content, image_data) VALUES (?, ?, ?, ?)",
        (session_id, role, content, image_data)
    )
    conn.commit()
    conn.close()

def delete_session(session_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

# --- 이미지 업로드 팝업 다이얼로그 ---
@st.dialog("이미지 업로드")
def image_upload_dialog():
    st.write("이미지를 선택하거나 아래 영역에 드래그앤드롭하세요.")
    img_file = st.file_uploader("이미지 파일", type=["png", "jpg", "jpeg"])
    if img_file:
        st.session_state.attached_image = img_file
        st.image(img_file, caption="선택한 이미지 미리보기")
        if st.button("첨부 완료"):
            st.rerun()

# --- 채팅 페이지 함수 ---
def chat_page():
    # DB 초기화
    init_db()

    # 세션 목록 조회 및 기본 세션 보장
    sessions = get_sessions()
    if not sessions:
        initial_id = create_session("새 대화")
        sessions = get_sessions()
    else:
        initial_id = sessions[0][0]

    if "current_session_id" not in st.session_state:
        st.session_state.current_session_id = initial_id

    # 현재 세션 ID 유효성 점검
    session_ids = [s[0] for s in sessions]
    if st.session_state.current_session_id not in session_ids:
        st.session_state.current_session_id = session_ids[0]

    # 세션 상태에 첨부 이미지 변수 초기화
    if "attached_image" not in st.session_state:
        st.session_state.attached_image = None

    st.title("OpenAI 채팅")

    # 사이드바: 대화방 관리
    st.sidebar.header("대화방 관리")

    # 새 대화 시작 버튼
    if st.sidebar.button("➕ 새로운 대화 시작"):
        new_session_id = create_session("새 대화")
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
        remaining_sessions = get_sessions()
        if remaining_sessions:
            st.session_state.current_session_id = remaining_sessions[0][0]
        else:
            st.session_state.current_session_id = create_session("새 대화")
        st.session_state.messages = load_messages(st.session_state.current_session_id)
        st.session_state.loaded_session_id = st.session_state.current_session_id
        st.rerun()

    st.sidebar.divider()

    # 사이드바: 모델 설정 및 파일 첨부
    st.sidebar.header("설정 및 파일 첨부")
    AVAILABLE_MODELS = [
        "gpt-5.6-luna",
        "gpt-5.6-terra",
        "gpt-5.6-sol",
        "gpt-5.5",
    ]
    model_name = st.sidebar.selectbox("모델 선택 (GPT 5.5+)", AVAILABLE_MODELS, index=0)

    # 이미지 업로드 버튼 (팝업 모달 활성화)
    if st.sidebar.button("🖼️ 이미지 업로드"):
        image_upload_dialog()

    # 첨부된 이미지 미리보기 및 취소
    if st.session_state.attached_image:
        st.sidebar.image(st.session_state.attached_image, caption="첨부된 이미지")
        if st.sidebar.button("이미지 첨부 취소"):
            st.session_state.attached_image = None
            st.rerun()

    # 일반 파일 업로드
    uploaded_file = st.sidebar.file_uploader(
        "📄 파일 업로드",
        type=["txt", "py", "md", "csv", "json"]
    )
    if uploaded_file:
        st.sidebar.caption(f"첨부된 파일: {uploaded_file.name}")

    # 세션 상태 메시지 동기화
    if "messages" not in st.session_state or st.session_state.get("loaded_session_id") != st.session_state.current_session_id:
        st.session_state.messages = load_messages(st.session_state.current_session_id)
        st.session_state.loaded_session_id = st.session_state.current_session_id

    # 이전 대화 내용 화면에 출력
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("image"):
                st.image(msg["image"])
            st.write(msg["content"])

    # 채팅 입력
    prompt = st.chat_input("메시지를 입력하세요...")

    if prompt:
        # 첫 대화 시 세션 제목을 첫 질문으로 갱신
        if session_dict.get(st.session_state.current_session_id) == "새 대화":
            new_title = prompt[:20] + ("..." if len(prompt) > 20 else "")
            update_session_title(st.session_state.current_session_id, new_title)

        # 사용자 메시지 콘텐츠 구성
        user_content = []
        attached_image_bytes = None

        # 첨부된 이미지가 있는 경우 처리
        if st.session_state.attached_image:
            img_bytes = st.session_state.attached_image.getvalue()
            attached_image_bytes = img_bytes
            img_type = st.session_state.attached_image.type
            base64_image = base64.b64encode(img_bytes).decode("utf-8")
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{img_type};base64,{base64_image}"
                }
            })
            st.session_state.attached_image = None

        # 일반 파일이 첨부되어 있는 경우 처리
        if uploaded_file:
            file_text = uploaded_file.getvalue().decode("utf-8")
            user_content.append({
                "type": "text",
                "text": f"--- 첨부 파일 내용 ({uploaded_file.name}) ---\n{file_text}\n--- 파일 내용 끝 ---\n"
            })

        user_content.append({"type": "text", "text": prompt})

        # 세션 상태 및 SQLite DB에 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "api_content": user_content,
            "image": attached_image_bytes
        })
        save_message(st.session_state.current_session_id, "user", prompt, attached_image_bytes)

        # 사용자 메시지 화면 출력
        with st.chat_message("user"):
            if attached_image_bytes:
                st.image(attached_image_bytes)
            st.write(prompt)

        # API 전송용 메시지 목록 구성
        api_messages = []
        for msg in st.session_state.messages:
            api_messages.append({
                "role": msg["role"],
                "content": msg.get("api_content", msg["content"])
            })

        # 어시스턴트 응답 스트리밍 출력
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=model_name,
                messages=api_messages,
                stream=True,
            )
            response_text = st.write_stream(stream)

        # 세션 상태 및 SQLite DB에 어시스턴트 응답 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text
        })
        save_message(st.session_state.current_session_id, "assistant", response_text)
        st.rerun()

# --- 멀티페이지 네비게이션 설정 ---
chat_page_def = st.Page(chat_page, title="OpenAI 채팅", icon="💬", default=True)
history_page_def = st.Page("app2_history.py", title="과거 채팅 내역", icon="📜", url_path="history")

pg = st.navigation([chat_page_def, history_page_def])
pg.run()
