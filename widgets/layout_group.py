import streamlit as st

# 모달 다이얼로그 함수 정의 (@st.dialog)
@st.dialog("기본 모달 다이얼로그")
def show_modal_dialog():
    st.write("이것은 화면 위에 팝업되는 기본 크기 모달 창입니다.")
    name = st.text_input("다이얼로그 안의 이름 입력")
    if st.button("확인"):
        st.write(f"입력된 이름: {name}")

@st.dialog("넓은 모달 다이얼로그 (width='large')", width="large")
def show_large_dialog():
    st.write("가로 폭이 넓게 열리는 모달 다이얼로그입니다.")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("성 (First name)")
    with col2:
        st.text_input("이름 (Last name)")
    st.date_input("생년월일")
    if st.button("저장 완료"):
        st.success("저장되었습니다!")

def show_layout_group():

    # 레이아웃의 하위 서브 탭들
    tab_cols, tab_popups, tab_expand, tab_side_bottom, tab_space_tabs = st.tabs([
        "컬럼 & 컨테이너",
        "다이얼로그 & 팝오버",
        "확장 패널 & 플레이스홀더",
        "사이드바 & 하단 고정",
        "여백 & 중첩 탭"
    ])

    # 1. 컬럼 & 컨테이너
    with tab_cols:
        st.subheader("1. st.columns (컬럼 분할 및 비율)")
        # 3열 균등 분할
        col1, col2, col3 = st.columns(3)
        col1.metric("온도", "24 °C", "1.2 °C")
        col2.metric("습도", "48%", "-4%")
        col3.metric("풍속", "3 m/s", "0.5 m/s")

        # 2:1 비율 분할
        col_a, col_b = st.columns([2, 1])
        col_a.info("비율 [2, 1] 중 너비가 넓은 왼쪽 컬럼 (비율 2)")
        col_b.success("오른쪽 컬럼 (비율 1)")

        st.divider()

        # 컬럼 간격(gap) 및 수직 정렬(vertical_alignment)
        st.subheader("2. 컬럼 간격(gap) & 수직 정렬(vertical_alignment)")
        st.caption("입력창과 버튼의 세로 위치를 하단(bottom)으로 딱 맞출 때 유용합니다.")
        col_input, col_action = st.columns([3, 1], vertical_alignment="bottom", gap="medium")
        with col_input:
            st.text_input("검색어 입력", placeholder="검색어를 입력하세요...")
        with col_action:
            st.button("즉시 검색", use_container_width=True)

        st.divider()

        # 컨테이너 기본 및 테두리(border)
        st.subheader("3. st.container (테두리 카드 형태)")
        with st.container(border=True):
            st.write("📦 `border=True` 옵션으로 감싸진 카드 형태의 컨테이너입니다.")
            st.text_input("컨테이너 내부 입력창")
            st.button("컨테이너 내부 전송 버튼")

        st.divider()

        # 스크롤 가능한 고정 높이 컨테이너 (height)
        st.subheader("4. 스크롤 가능한 컨테이너 (`height=150`)")
        st.caption("내용이 많아지면 컨테이너 내부에 스크롤바가 자동으로 생성됩니다.")
        with st.container(height=150, border=True):
            st.write("스크롤 테스트용 긴 텍스트 목록:")
            for i in range(1, 11):
                st.write(f"- 로그 항목 #{i}: 정상 동작 중")

        st.divider()

        # 순서 제어 (Out-of-order) 컨테이너
        st.subheader("5. 순서 제어 (Out-of-order Container)")
        st.caption("코드 상에서는 아래에서 작성했지만, 상단에 선언된 컨테이너에 먼저 표시됩니다.")
        top_container = st.container(border=True)
        st.write("👉 코드 순서상 중간에 위치한 텍스트")
        top_container.success("✨ 맨 위에 나타난 텍스트 (코드에서는 나중에 top_container.success로 호출됨)")


    # 2. 다이얼로그 & 팝오버
    with tab_popups:
        st.subheader("1. st.dialog (모달 팝업 창 및 크기 옵션)")
        st.caption("@st.dialog 데코레이터를 사용하여 화면 중앙에 뜨는 모달 창을 생성합니다.")
        col_dlg1, col_dlg2 = st.columns(2)
        with col_dlg1:
            if st.button("기본 모달 창 열기"):
                show_modal_dialog()
        with col_dlg2:
            if st.button("넓은(large) 모달 창 열기"):
                show_large_dialog()

        st.divider()

        st.subheader("2. st.popover (아이콘 및 드롭다운 메뉴)")
        st.caption("버튼 클릭 시 해당 위치 바로 아래에 플로팅 형태로 펼쳐집니다.")
        col_pop1, col_pop2 = st.columns(2)
        with col_pop1:
            with st.popover("⚙️ 환경 설정", use_container_width=True):
                st.write("사용자 환경 설정:")
                st.toggle("다크 모드 적용", value=True)
                st.slider("알림 볼륨", 0, 100, 70)
        with col_pop2:
            with st.popover("필터 옵션", icon=":material/filter_list:", use_container_width=True):
                st.radio("정렬 기준", ["최신순", "인기순", "이름순"])
                st.checkbox("품절 상품 제외")

    # 3. 확장 패널 & 플레이스홀더
    with tab_expand:
        st.subheader("1. st.expander (접기/펼치기 아코디언)")
        
        # 기본 접힘 상태 + 아이콘
        with st.expander("❓ 자주 묻는 질문 (기본 닫힘)", icon=":material/help:"):
            st.write("Q: Streamlit은 무료인가요?")
            st.write("A: 네, 오픈소스 라이브러리로 누구나 무료로 사용할 수 있습니다.")

        # 기본 펼침 상태 (expanded=True)
        with st.expander("💡 주요 안내 사항 (기본 펼침: expanded=True)", expanded=True):
            st.info("이 패널은 expanded=True 옵션으로 처음부터 내용이 펼쳐져 있습니다.")

        st.divider()

        st.subheader("2. st.empty (내용 교체 및 지우기)")
        st.caption("단일 요소를 예약해 두고, 다른 내용으로 바꾸거나 완전히 지울 수 있습니다.")
        status_placeholder = st.empty()
        status_placeholder.info("대기 중... 아래 버튼을 눌러보세요.")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("내용 변경 (Success)"):
                status_placeholder.success("✅ 작업이 완료되었습니다!")
        with col_btn2:
            if st.button("내용 완전히 지우기 (empty.empty())"):
                status_placeholder.empty()

    # 4. 사이드바 & 하단 고정
    with tab_side_bottom:
        st.subheader("1. st.sidebar (좌측 사이드바 패널)")
        st.write("브라우저 좌측의 사이드바 패널을 확인해보세요. 사이드바 전용 위젯들이 배치되어 있습니다.")
        with st.sidebar:
            st.header("📌 사이드바 설정")
            st.selectbox("언어 선택", ["한국어", "English", "日本語"])
            st.slider("글자 크기", 12, 24, 16)

        st.divider()

        st.subheader("2. st.bottom (화면 하단 고정 입력 및 알림)")
        st.write("화면 맨 아래쪽에 고정된 바가 생성되었습니다. (화면 최하단 확인)")
        with st.bottom:
            st.info("💡 st.bottom: 브라우저 뷰포트 맨 아래에 고정되어 항상 노출되는 영역입니다.")

    # 5. 여백 & 중첩 탭
    with tab_space_tabs:
        st.subheader("1. st.space (크기별 여백 추가)")
        st.caption("위젯 사이에 일정한 간격을 줄 때 사용합니다 ('small', 'medium', 'large').")
        st.write("--- 텍스트 1 ---")
        st.space("small")
        st.write("--- small 간격 후 텍스트 2 ---")
        st.space("large")
        st.write("--- large 간격 후 텍스트 3 ---")

        st.divider()

        st.subheader("2. st.tabs (아이콘이 포함된 중첩 탭)")
        sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📊 차트 뷰", "📋 데이터 뷰", "⚙️ 설정 뷰"])
        with sub_tab1:
            st.write("차트 관련 내용이 들어가는 탭입니다.")
        with sub_tab2:
            st.write("데이터 테이블이 들어가는 탭입니다.")
        with sub_tab3:
            st.write("세부 설정 옵션이 들어가는 탭입니다.")


