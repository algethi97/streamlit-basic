import streamlit as st
import pandas as pd

def show_data_elements():
    tab_df, tab_editor, tab_metric_json = st.tabs([
        "데이터프레임 & 테이블",
        "데이터 편집기",
        "메트릭 & JSON"
    ])

    # 샘플 데이터 생성
    data = {
        "이름": ["홍길동", "이순신", "강감찬"],
        "나이": [25, 45, 38],
        "직업": ["개발자", "장군", "장군"],
        "점수": [95.5, 88.0, 92.3]
    }
    df = pd.DataFrame(data)

    # 1. 데이터프레임 & 정적 테이블
    with tab_df:
        st.subheader("1. st.dataframe (대화형 데이터프레임)")
        st.write("컬럼별 정렬, 크기 조절, 검색이 가능한 인터랙티브 표입니다.")
        st.dataframe(df)

        st.divider()

        st.subheader("2. st.table (정적 테이블)")
        st.write("스크롤이나 상호작용 없이 전체 데이터가 한눈에 펼쳐지는 표입니다.")
        st.table(df)

    # 2. 데이터 편집기 (st.data_editor)
    with tab_editor:
        st.subheader("3. st.data_editor (셀 값 직접 수정 가능한 테이블)")
        st.write("표 내부의 셀을 더블클릭하여 값을 직접 수정해보세요:")
        edited_df = st.data_editor(df)
        st.write("현재 수정된 데이터:")
        st.dataframe(edited_df)

    # 3. 메트릭 & JSON
    with tab_metric_json:
        st.subheader("4. st.metric (주요 지표 카드)")
        col1, col2, col3 = st.columns(3)
        col1.metric("총 매출", "₩ 1,250만", "+12%")
        col2.metric("방문자 수", "3,400명", "-5%")
        col3.metric("전환율", "4.8%", "+0.6%")

        st.divider()

        st.subheader("5. st.json (JSON 뷰어)")
        sample_json = {
            "service": "Streamlit App",
            "version": "1.64.0",
            "settings": {
                "theme": "dark",
                "notifications": True
            },
            "tags": ["python", "dashboard", "fast"]
        }
        st.json(sample_json)

