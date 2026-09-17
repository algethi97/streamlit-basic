import streamlit as st
from widgets.input_group import show_input_group
from widgets.layout_group import show_layout_group
from widgets.text_elem_group import show_text_elements
from widgets.data_group import show_data_elements
from widgets.chart_group import show_chart_elements
from widgets.status_group import show_status_elements

# 페이지 기본 설정
st.set_page_config(page_title="Streamlit 기능 탐색 도감", layout="wide")
st.title("Streamlit 기능 탐색 도감")

# 최상위 메인 탭 그룹 (6대 핵심 카테고리)
tab_inputs, tab_layouts, tab_texts, tab_data, tab_charts, tab_status = st.tabs([
    "🧩 인풋 위젯", 
    "📐 레이아웃 & 컨테이너",
    "✍️ 텍스트 요소",
    "📊 데이터 표시",
    "📈 차트",
    "🔔 상태 & 알림"
])

with tab_inputs:
    show_input_group()

with tab_layouts:
    show_layout_group()

with tab_texts:
    show_text_elements()

with tab_data:
    show_data_elements()

with tab_charts:
    show_chart_elements()

with tab_status:
    show_status_elements()
