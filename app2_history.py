import sqlite3
import streamlit as st

# --- SQLite 데이터베이스 함수 ---
def get_sessions():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT
        )
    """)
    cursor.execute("SELECT id, title FROM sessions ORDER BY rowid DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def load_messages(session_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            image_data BLOB
        )
    """)
    cursor.execute("SELECT role, content, image_data FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1], "image": row[2]} for row in rows]

def delete_session(session_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

st.title("과거 채팅 내역")

# 세션 목록 조회
sessions = get_sessions()

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
                if msg.get("image"):
                    st.image(msg["image"])
                st.write(msg["content"])

