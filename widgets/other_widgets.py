import streamlit as st

def show_other_widgets():
    st.header("체크박스 및 토글 예제")

    # 1. 체크박스 (st.checkbox)
    agree = st.checkbox("이용 약관에 동의합니다")
    st.write("동의 여부:", agree)

    # 2. 토글 스위치 (st.toggle)
    notifications = st.toggle("알림 받기")
    st.write("알림 설정 상태:", "켜짐" if notifications else "꺼짐")

    st.divider()

    st.header("날짜, 시간 및 기타 위젯 예제")

    # 3. 날짜 입력 (st.date_input)
    selected_date = st.date_input("날짜 선택")
    st.write("선택한 날짜:", selected_date)

    # 4. 시간 입력 (st.time_input)
    selected_time = st.time_input("시간 설정")
    st.write("설정된 시간:", selected_time)

    # 5. 색상 선택기 (st.color_picker)
    color = st.color_picker("원하는 색상 선택", "#00f900")
    st.write("선택한 색상 코드:", color)

