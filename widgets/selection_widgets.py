import streamlit as st

def show_selection_widgets():
    st.header("선택 위젯 예제")

    # 1. 라디오 버튼 (st.radio - 세로 배치)
    genre = st.radio("좋아하는 영화 장르", ["코미디", "드라마", "SF", "액션"])
    st.write("선택한 장르:", genre)

    # 2. 가로형 라디오 버튼 (horizontal=True)
    food = st.radio("점심 메뉴 선택 (가로 정렬)", ["한식", "중식", "일식", "양식"], horizontal=True)
    st.write("선택한 메뉴:", food)

    # 3. 선택 박스 (st.selectbox - 드롭다운)
    contact = st.selectbox("선호하는 연락 수단", ["이메일", "전화", "문자메시지", "카카오톡"])
    st.write("선택한 연락 수단:", contact)

    # 4. 다중 선택 박스 (st.multiselect)
    hobbies = st.multiselect("취미 선택 (복수 선택 가능)", ["독서", "영화 감상", "운동", "게임", "여행"], default=["독서", "운동"])
    st.write("선택된 취미 목록:", hobbies)

