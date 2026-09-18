from pathlib import Path
import streamlit as st

# ==============================================================================
# 1. 서브 페이지 함수 정의 (st.Page의 Callable 기능 활용)
# ==============================================================================

def page_dashboard():
    st.title("📊 대시보드 페이지")
    st.write("`st.Page(callable)` 함수 형태로 정의된 페이지입니다.")
    st.metric(label="방문자 수", value="1,240명", delta="12%")
    
    st.divider()
    st.subheader("🚀 st.switch_page 예제 (코드 제어 페이지 이동)")
    st.write("버튼 클릭 시 `st.switch_page`를 호출하여 다른 페이지로 즉시 이동합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚙️ 설정 페이지로 이동", use_container_width=True):
            st.switch_page(settings_page)
    with col2:
        if st.button("🔑 메인(로그인) 페이지로 이동", use_container_width=True):
            st.switch_page(main_page)


def page_settings():
    st.title("⚙️ 설정 페이지")
    st.write("환경 설정을 시뮬레이션하는 페이지입니다.")
    theme = st.selectbox("테마 선택", ["Light", "Dark", "System"])
    notifications = st.toggle("알림 활성화", value=True)
    st.write(f"선택된 테마: **{theme}**, 알림 상태: **{notifications}**")


def page_links():
    st.title("🔗 st.page_link 기능 모음")
    st.write("`st.page_link`의 다양한 옵션을 직접 확인하고 비교해볼 수 있습니다.")
    
    st.subheader("1. 기본 내부 페이지 링크")
    st.page_link(dashboard_page, label="대시보드로 이동", icon="📊")
    st.page_link(settings_page, label="설정 페이지로 이동", icon="⚙️")
    
    st.subheader("2. 컨테이너 너비(100%) 및 툴팁(help) 적용")
    st.page_link(
        main_page, 
        label="메인(로그인) 페이지로 이동", 
        icon="🔑", 
        help="stream_pages/main.py 파일로 연결됩니다.", 
        use_container_width=True
    )
    
    st.subheader("3. 비활성화(disabled) 상태")
    st.page_link(settings_page, label="비활성화된 링크 (disabled=True)", icon="🔒", disabled=True)
    
    st.subheader("4. 외부 URL 링크 (external)")
    st.page_link("https://docs.streamlit.io", label="Streamlit 공식 문서 (새 탭으로 열기)", icon="🌐")
    st.page_link("https://github.com", label="GitHub 바로가기 (새 탭으로 열기)", icon="🐙")


# ==============================================================================
# 2. st.Page 선언 (파일 기반 및 함수 기반, 다양한 매개변수)
# ==============================================================================

main_file = Path(__file__).resolve().parent / "main.py"
if not main_file.is_file():
    main_file = Path(r"c:\Projects\streamlit-basic\stream_pages\main.py")

# 파일 경로 기반 페이지 (stream_pages/main.py 연동)
main_page = st.Page(
    main_file, 
    title="로그인 & 메인", 
    icon="🔑", 
    url_path="login"
)

# 함수(Callable) 기반 페이지들
dashboard_page = st.Page(
    page_dashboard, 
    title="대시보드", 
    icon="📊", 
    url_path="dashboard", 
    default=True
)

links_page = st.Page(
    page_links, 
    title="링크 위젯 (page_link)", 
    icon="🔗", 
    url_path="links"
)

settings_page = st.Page(
    page_settings, 
    title="환경 설정", 
    icon="⚙️", 
    url_path="settings"
)


# ==============================================================================
# 3. st.navigation 구성 (섹션 딕셔너리 및 위치 옵션)
# ==============================================================================

# 딕셔너리를 사용하여 메뉴를 섹션별로 그룹화
pages = {
    "메인 서비스": [dashboard_page, links_page],
    "계정 및 설정": [main_page, settings_page],
}

# 사이드바에서 네비게이션 위치를 실시간으로 변경해볼 수 있는 컨트롤 (학습용)
nav_position = st.sidebar.radio(
    "네비게이션 위치 (position)", 
    ["sidebar", "top", "hidden"], 
    index=0,
    help="st.navigation의 position 매개변수를 직접 변경해보세요."
)

# 네비게이션 라우터 생성 및 현재 페이지 실행
pg = st.navigation(pages, position=nav_position)
pg.run()
