import sys
import streamlit as st

# 일반 파이썬 실행(python app2.py 또는 VS Code 재생 버튼) 시 자동으로 streamlit run 모드로 전환
if not st.runtime.exists():
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())

# ==============================================================================
# 1. 개별 페이지 파일들을 st.Page 객체로 등록
# ==============================================================================

login_page = st.Page(
    "stream_pages/login.py",
    title="로그인",
    icon="🔑",
    url_path="login",
    default=True,
)

dashboard_page = st.Page(
    "stream_pages/dashboard.py",
    title="대시보드",
    icon="📊",
    url_path="dashboard",
)

settings_page = st.Page(
    "stream_pages/settings.py",
    title="환경 설정",
    icon="⚙️",
    url_path="settings",
)

links_page = st.Page(
    "stream_pages/links.py",
    title="링크 모음",
    icon="🔗",
    url_path="links",
)

# ==============================================================================
# 2. st.navigation 라우터 구성 (로그인 상태에 따른 동적 페이지 제어)
# ==============================================================================

# 로그인하지 않은 경우 로그인 페이지만 노출/접근 허용
if not st.user.is_logged_in:
    pages = [login_page]
else:
    # 로그인 성공 시 전체 서비스 및 설정 페이지 접근 허용
    pages = {
        "메인 서비스": [dashboard_page, links_page],
        "계정 및 설정": [login_page, settings_page],
    }

# 사이드바에서 네비게이션 위치(position)를 실시간으로 비교/변경할 수 있는 위젯
nav_position = st.sidebar.radio(
    "네비게이션 위치 (position)",
    ["sidebar", "top", "hidden"],
    index=0,
    help="st.navigation의 position 매개변수를 직접 변경해보세요.",
)

# 라우터 생성 및 현재 페이지 실행
pg = st.navigation(pages, position=nav_position)
pg.run()