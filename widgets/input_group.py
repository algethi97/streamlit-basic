import streamlit as st
from widgets.text_widgets import show_text_widgets
from widgets.slider_widgets import show_slider_widgets
from widgets.selection_widgets import show_selection_widgets
from widgets.other_widgets import show_other_widgets

def show_input_group():
    # 인풋 위젯의 하위 서브 탭들
    tab_text, tab_slider, tab_select, tab_other = st.tabs([
        "텍스트 입력", 
        "숫자 & 슬라이더", 
        "선택 위젯", 
        "날짜 & 기타"
    ])

    with tab_text:
        show_text_widgets()

    with tab_slider:
        show_slider_widgets()

    with tab_select:
        show_selection_widgets()

    with tab_other:
        show_other_widgets()

