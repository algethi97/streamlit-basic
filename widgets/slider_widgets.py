import streamlit as st

def show_slider_widgets():
    st.header("숫자 입력 및 슬라이더 예제")

    # 1. 기본 정수 입력 (st.number_input)
    age = st.number_input("나이 입력 (0~120세)", min_value=0, max_value=120, value=25, step=1)
    st.write("선택한 나이:", age)

    # 2. 소수점(실수) 입력 (format 옵션)
    height = st.number_input("키 입력 (cm)", min_value=50.0, max_value=250.0, value=175.5, step=0.1, format="%.1f")
    st.write("선택한 키:", height, "cm")

    # 3. 기본 슬라이더 (st.slider)
    score = st.slider("점수 선택", min_value=0, max_value=100, value=50, step=5)
    st.write("현재 점수:", score)

    # 4. 범위 선택 슬라이더 (튜플 값 사용)
    price_range = st.slider("가격 범위 선택 (만원)", 0, 100, (20, 80))
    st.write("선택한 가격 범위:", f"{price_range[0]}만원 ~ {price_range[1]}만원")

    # 5. 카테고리/단계형 슬라이더 (st.select_slider)
    size = st.select_slider("의류 사이즈 선택", options=["XS", "S", "M", "L", "XL", "XXL"], value="L")
    st.write("선택한 사이즈:", size)

