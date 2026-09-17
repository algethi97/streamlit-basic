# Streamlit Basic

Streamlit의 기본 위젯 학습 및 OpenAI 최신 모델(GPT 5.5+)을 연동한 멀티모달 챗봇 프로젝트입니다.

---

## 🚀 주요 기능

### 1. OpenAI 멀티모달 챗봇 (`app2.py`)
- **최신 OpenAI 모델 지원**: `gpt-5.6-luna` (기본값), `gpt-5.6-terra`, `gpt-5.6-sol`, `gpt-5.5` 드롭다운 선택 제공
- **이미지 첨부 팝업 (`@st.dialog`)**: 이미지 업로드 버튼 클릭 시 모달 팝업이 활성화되어 드래그앤드롭으로 손쉽게 이미지 첨부 및 미리보기 지원
- **일반 문서/파일 첨부**: 텍스트, 코드, 문서 파일(`.txt`, `.py`, `.md`, `.csv`, `.json`) 내용 자동 분석
- **스트리밍 답변**: `st.write_stream`을 통한 실시간 타이핑 효과

### 2. SQLite 기반 대화 세션 및 이력 관리
- **대화 세션(대화방) 분리**: `➕ 새로운 대화 시작` 버튼으로 대화방을 생성하고, 첫 질문으로 방 제목을 자동 설정
- **이미지 바이너리(`BLOB`) 저장**: 대화 시 첨부된 이미지를 SQLite에 바이너리로 저장하여 대화방 전환 및 새로고침 후에도 온전히 복원
- **대화방 삭제 및 관리**: 불필요한 대화방을 사이드바에서 개별 삭제 가능

### 3. 멀티페이지 통합 네비게이션 (`st.navigation`)
- **`💬 OpenAI 채팅`**: 실시간 멀티모달 대화 페이지
- **`📜 과거 채팅 내역` (`/history`)**: 저장된 대화방 목록과 질문/답변 타임라인을 한눈에 확인할 수 있는 열람 페이지

---

## 🛠️ 시작 가이드

### 1. 패키지 설치
`uv` 패키지 관리자를 사용하여 프로젝트 의존성을 설치합니다:
```bash
uv sync
```

### 2. 환경 변수 설정
루트 디렉터리에 `.env` 파일을 생성하고 OpenAI API 키를 설정합니다:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 실행 방법
Windows 배치 파일을 실행하거나 uv 명령어로 실행할 수 있습니다:
```bash
# 배치 파일 실행
run.bat

# 또는 직접 실행
uv run streamlit run app2.py
```

---

## 📁 프로젝트 구조

```plaintext
streamlit-basic/
├── app.py              # Streamlit 기본 위젯 예제 앱
├── app2.py             # OpenAI 챗봇 메인 앱 (네비게이션 엔트리포인트)
├── modules/            # 기능별 분리 모듈
│   ├── database.py     # SQLite DB 관리 (users, sessions, messages CRUD)
│   ├── auth.py         # 간이 로그인/회원가입 시스템
│   ├── api_key.py      # OpenAI API 키 모달 등록 및 상태 관리
│   ├── app2_history.py # 과거 채팅 내역 조회 페이지 (/history)
│   └── theme.py        # 해수면 ↔ 심해 수직 잠수 오션 테마
├── widgets/            # 컴포넌트별 Streamlit 위젯 예제 모듈
├── pyproject.toml      # uv 의존성 및 프로젝트 설정
├── run.bat             # 앱 실행 배치 스크립트
├── .env.example        # 환경 변수 템플릿
└── README.md           # 프로젝트 문서
```

