import streamlit as st

def show_text_widgets():
    st.header("텍스트 입력 예제")

    # 1. 기본 텍스트 입력 (기본값 설정)
    title = st.text_input("영화 제목", "Life of Brian")
    st.write("현재 입력된 영화 제목:", title)

    # 2. 플레이스홀더(안내 문구)를 포함한 텍스트 입력
    user_name = st.text_input("사용자 이름", placeholder="이름을 입력하세요")
    if user_name:
        st.write(f"안녕하세요, {user_name}님!")

    # 3. 비밀번호 입력 (마스킹 처리)
    password = st.text_input("비밀번호", type="password")
    if password:
        st.write("비밀번호가 입력되었습니다.")

    # 4. 글자 수 제한 (최대 10자)
    nickname = st.text_input("닉네임 (최대 10자)", max_chars=10)
    st.write("닉네임:", nickname)

    # 5. 여러 줄 텍스트 입력 (st.text_area)
    article = st.text_area(
        "분석할 텍스트",
        "Streamlit을 사용하면 간편하게 대시보드를 구축할 수 있습니다.",
    )
    st.write(f"작성된 글자 수: {len(article)}자")

    # 6. 도움말 툴팁(help)이 포함된 텍스트 입력
    website = st.text_input("웹사이트 주소", help="도움말: 프로토콜(https://)을 포함하여 입력해주세요.")
    st.write("입력된 웹사이트:", website)

    # 7. 비활성화(disabled) 상태의 텍스트 입력
    readonly_code = st.text_input("고정 코드 (수정 불가)", value="STREAMLIT-2026", disabled=True)
    st.write("고정 코드 값:", readonly_code)

    # 8. 검색 전용 텍스트 입력 (type="search", 자동 클리어 버튼 포함)
    query = st.text_input("검색창", type="search", placeholder="검색어를 입력해보세요")
    if query:
        st.write(f"검색 결과: '{query}'")

    # 9. 라벨 숨김 (label_visibility="collapsed")
    st.write("▼ 아래 입력창은 라벨 공간을 숨긴(collapsed) 예시입니다:")
    no_label = st.text_input("숨겨진 라벨", placeholder="라벨 없이 깔끔하게 표시되는 입력창", label_visibility="collapsed")
    if no_label:
        st.write("입력 내용:", no_label)

    # 10. 높이 조절이 가능한 여러 줄 텍스트 (height 옵션)
    memo = st.text_area("장문 메모 작성 (높이 150px)", height=150, placeholder="여러 줄을 넉넉하게 입력할 수 있습니다.")
    st.write("메모 미리보기:", memo)

