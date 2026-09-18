import sqlite3
import uuid

DB_NAME = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 사용자 테이블 (닉네임 관리)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 대화방(세션) 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            username TEXT,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 메시지 테이블
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            image_data BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 기존 DB 테이블 컬럼 호환 유지 및 비밀번호 컬럼 삭제
    cursor.execute("PRAGMA table_info(users)")
    user_cols = [col[1] for col in cursor.fetchall()]
    if "password" in user_cols:
        cursor.execute("ALTER TABLE users DROP COLUMN password")

    cursor.execute("PRAGMA table_info(sessions)")
    session_cols = [col[1] for col in cursor.fetchall()]
    if "username" not in session_cols:
        cursor.execute("ALTER TABLE sessions ADD COLUMN username TEXT")
    if "created_at" not in session_cols:
        cursor.execute("ALTER TABLE sessions ADD COLUMN created_at TIMESTAMP")
        cursor.execute("UPDATE sessions SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")

    cursor.execute("PRAGMA table_info(messages)")
    columns = [col[1] for col in cursor.fetchall()]
    if "session_id" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN session_id TEXT")
    if "image_data" not in columns:
        cursor.execute("ALTER TABLE messages ADD COLUMN image_data BLOB")

    conn.commit()
    conn.close()

# --- 사용자(닉네임) 관리 관련 ---
def get_or_create_user(username):
    username = username.strip()
    if not username:
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

# --- 세션(대화방) 관리 관련 ---
def get_sessions(username=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if username:
        cursor.execute("SELECT id, title FROM sessions WHERE username = ? ORDER BY rowid DESC", (username,))
    else:
        cursor.execute("SELECT id, title FROM sessions ORDER BY rowid DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_session(username=None, title="새 대화"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 해당 유저의 기존 세션 목록 조회 (오래된 순서대로 정렬)
    if username:
        cursor.execute("SELECT id FROM sessions WHERE username = ? ORDER BY created_at ASC, rowid ASC", (username,))
    else:
        cursor.execute("SELECT id FROM sessions ORDER BY created_at ASC, rowid ASC")
    existing_sessions = cursor.fetchall()

    # 최대 10개 유지: 10개 이상이면 가장 오래된 세션부터 삭제 (요구사항 6번)
    while len(existing_sessions) >= 10:
        oldest_id = existing_sessions.pop(0)[0]
        cursor.execute("DELETE FROM messages WHERE session_id = ?", (oldest_id,))
        cursor.execute("DELETE FROM sessions WHERE id = ?", (oldest_id,))

    new_id = uuid.uuid4().hex[:8]
    cursor.execute("INSERT INTO sessions (id, username, title) VALUES (?, ?, ?)", (new_id, username, title))
    conn.commit()
    conn.close()
    return new_id

def update_session_title(session_id, title):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE sessions SET title = ? WHERE id = ?", (title, session_id))
    conn.commit()
    conn.close()

def delete_session(session_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

# --- 메시지 이력 관리 관련 ---
def load_messages(session_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def save_message(session_id, role, content):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def get_turn_count(session_id):
    """해당 세션의 대화 횟수(사용자 질문 개수) 반환 (요구사항 5번)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM messages WHERE session_id = ? AND role = 'user'", (session_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

