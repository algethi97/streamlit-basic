import streamlit as st
import pandas as pd

def show_chart_elements():
    tab_basic_charts, tab_scatter_map = st.tabs([
        "기본 차트 (선, 막대, 영역)",
        "산점도 & 지도 차트"
    ])

    # 차트용 샘플 시계열 데이터
    chart_data = pd.DataFrame({
        "제품 A": [10, 25, 18, 30, 45, 38],
        "제품 B": [15, 12, 28, 35, 20, 42],
        "제품 C": [5, 19, 22, 14, 31, 29]
    })

    # 1. 기본 차트
    with tab_basic_charts:
        st.subheader("1. st.line_chart (꺾은선 그래프)")
        st.line_chart(chart_data)

        st.divider()

        st.subheader("2. st.bar_chart (막대 그래프)")
        st.bar_chart(chart_data)

        st.divider()

        st.subheader("3. st.area_chart (영역 차트)")
        st.area_chart(chart_data)

    # 2. 산점도 & 지도
    with tab_scatter_map:
        st.subheader("4. st.scatter_chart (산점도 그래프)")
        scatter_data = pd.DataFrame({
            "x": [1, 2, 3, 4, 5, 6, 7, 8],
            "y": [10, 15, 13, 17, 20, 19, 25, 24],
            "size": [10, 20, 30, 40, 50, 60, 70, 80]
        })
        st.scatter_chart(scatter_data, x="x", y="y", size="size")

        st.divider()

        st.subheader("5. st.map (지도 시각화)")
        # 서울 주요 지점 위도/경도 샘플 (서울 시청 근방)
        map_data = pd.DataFrame({
            "latitude": [37.5665, 37.5650, 37.5680],
            "longitude": [126.9780, 126.9750, 126.9810]
        })
        st.map(map_data)

