# OpenAI 채팅 앱 기능 개선 및 로그인 시스템 구현 계획서

사용자 요청에 따라 OpenAI API 키 동적 등록(메모리 전용), 파일 업로드 제거, Git 추적 SQLite DB, 세션/대화 횟수 제한(최대 10개 세션 / 세션당 100회 대화), 간이 로그인 시스템 및 보안 안내를 반영한 계획서입니다.

---

## 🗺️ 기능도 및 시스템 흐름도

### 1. 사용자 인증 및 시스템 진입 흐름 (Auth Flow)

```mermaid
flowchart TD
    Start(["🚀 사용자 웹앱 접속"]) --> AuthCheck{"로그인 상태인가?"}

    %% 미로그인 상태
    AuthCheck -- "No (비로그인)" --> LoginPage["📄 로그인 / 회원가입 페이지"]
    LoginPage --> Banner["⚠️ 보안 취약 안내 배너 상시 노출\n(비밀번호 평문 관리 주의)"]
    Banner --> AuthAction["아이디 / 비밀번호 입력 및 로그인"]
    AuthAction --> AuthCheck

    %% 로그인 완료 상태
    AuthCheck -- "Yes (인증 완료)" --> Nav["🧭 사이드바 통합 네비게이션"]
    Nav --> Tab1["💬 OpenAI 채팅"]
    Nav --> Tab2["📜 과거 채팅 내역 (/history)"]
    Nav --> Logout["🚪 로그아웃"]
    Logout --> Start
```

---

### 2. OpenAI API 키 등록 및 보안 격리 흐름 (API Key Security)

> **핵심 원칙**: API 키는 **오직 Streamlit 메모리(`st.session_state`)**에만 임시 보관되며, 어떠한 파일이나 DB에도 기록되지 않습니다.

```mermaid
flowchart LR
    subgraph ClientUI ["사용자 화면 (Streamlit UI)"]
        direction TB
        BtnKey["'🔑 API 키 등록' 버튼 클릭"] --> Dialog["모달 팝업 활성화 (@st.dialog)"]
        Dialog --> InputKey["OpenAI API 키 입력"]
    end

    subgraph MemoryOnly ["임시 메모리 (보안 격리)"]
        direction TB
        InputKey ==> SaveSession["st.session_state 저장\n(브라우저 닫거나 새로고침 시 소멸)"]
    end

    subgraph Storage ["영구 저장소 (저장 원천 차단)"]
        direction TB
        BlockDB["❌ SQLite DB 저장 금지"]
        BlockGit["❌ Git 커밋/파일 저장 금지"]
    end

    SaveSession -.-> BlockDB
    SaveSession -.-> BlockGit
```

---

### 3. 세션 수 (10개) 및 대화 턴 수 (100회) 제약 조건 흐름 (Lifecycle)

```mermaid
flowchart TD
    subgraph SessionLimit ["1. 대화방(세션) 생성 규칙 (최대 10개)"]
        NewChat["'➕ 새로운 대화 시작' 클릭"] --> CountSessions{"해당 유저의\n기존 세션 수 >= 10?"}
        CountSessions -- "Yes (10개 초과)" --> DeleteOldest["가장 오래된 세션 1개 자동 삭제 (FIFO)"]
        CountSessions -- "No (여유 있음)" --> CreateSession["새 대화방 생성 (UUID 발급)"]
        DeleteOldest --> CreateSession
    end

    subgraph TurnLimit ["2. 메시지 발송 규칙 (세션당 최대 100회)"]
        CreateSession --> UserInput["사용자 메시지 입력"]
        UserInput --> CountTurns{"현재 대화방\n대화 횟수 >= 100회?"}
        CountTurns -- "Yes (한도 도달)" --> BlockMsg["⚠️ 100회 한도 도달 안내 및 입력 차단"]
        CountTurns -- "No (발송 가능)" --> SendMsg["OpenAI API 스트리밍 호출\n(gpt-5.6-luna)"]
        SendMsg --> SaveHistory["SQLite DB (chat_history.db) 저장\n(Git 리포지터리 추적)"]
    end
```

---

### 4. 데이터베이스 관계도 (ERD)

```mermaid
erDiagram
    USERS ||--o{ SESSIONS : "유저당 최대 10개 세션 보유"
    SESSIONS ||--o{ MESSAGES : "세션당 최대 100회 대화 기록"

    USERS {
        string username PK "사용자 아이디"
        string password "비밀번호 (간이 평문)"
        timestamp created_at "가입 일시"
    }

    SESSIONS {
        string id PK "대화방 식별자 (UUID)"
        string username FK "소유자 아이디"
        string title "대화방 제목 (첫 질문 20자)"
        timestamp created_at "생성 일시 (FIFO 정렬 기준)"
    }

    MESSAGES {
        int id PK "메시지 ID"
        string session_id FK "소속 대화방 ID"
        string role "작성자 (user / assistant)"
        string content "메시지 텍스트"
        timestamp created_at "전송 일시"
    }
```

---

## 📋 세부 구현 명세

### 1. 보안 정책
- **API 키 메모리 유지**: `st.session_state.openai_api_key`에만 보관하고, DB나 `.env` 등 파일에 기록하지 않음.
- **간이 로그인 보안 한계 고지**: 암호화되지 않은 간이 계정 시스템임을 안내하는 상시 경고 배너 노출.

### 2. 세션 및 대화 제한
- **유저당 최대 10개 세션**: 11번째 세션 생성 시 가장 오래된 세션 및 관련 메시지를 DB에서 자동 삭제.
- **세션당 100회 대화 한도**: 사용자 질문과 AI 답변 1세트를 1회로 간주하며, 100회 도달 시 입력 차단.

### 3. 파일/이미지 업로드 기능 제거
- 기존의 이미지/파일 업로드 관련 UI 및 로직을 모두 제거하고 순수 텍스트 대화로 경량화.

### 4. Git 리포지터리 DB 연동
- `.gitignore`에서 `*.db` 제외 설정을 해제하여 `chat_history.db`가 Git 버전 관리에 포함되도록 설정.

