import streamlit as st
import time

def show_status_elements():
    tab_alerts, tab_progress, tab_effects = st.tabs([
        "알림 메시지 박스",
        "진행률 & 상태 표시",
        "토스트 & 축하 효과"
    ])

    # 1. 알림 메시지 박스
    with tab_alerts:
        st.subheader("상태별 안내 메시지 박스")
        st.success("st.success: 작업이 성공적으로 완료되었습니다!")
        st.info("st.info: 유용한 참고 정보입니다.")
        st.warning("st.warning: 주의가 필요한 경고 메시지입니다.")
        st.error("st.error: 오류가 발생했습니다.")

    # 2. 진행률 & 상태 표시
    with tab_progress:
        st.subheader("1. st.progress (진행률 바)")
        st.progress(70, text="진행률: 70%")

        st.divider()

        st.subheader("2. st.spinner (로딩 스피너)")
        if st.button("스피너 테스트 실행 (1초)"):
            with st.spinner("작업 처리 중..."):
                time.sleep(1)
            st.success("처리 완료!")

        st.divider()

        st.subheader("3. st.status (단계별 상태 컨테이너)")
        if st.button("단계별 상태 테스트 실행"):
            with st.status("데이터 처리 중...", expanded=True) as status:
                st.write("1단계: 데이터 불러오는 중...")
                time.sleep(0.5)
                st.write("2단계: 데이터 변환 중...")
                time.sleep(0.5)
                status.update(label="모든 작업 완료!", state="complete", expanded=False)

    # 3. 토스트 & 축하 효과
    with tab_effects:
        st.subheader("1. st.toast (우측 하단 토스트 팝업)")
        if st.button("토스트 알림 띄우기"):
            st.toast("새로운 알림이 도착했습니다! 🔔")

        st.divider()

        st.subheader("2. 애니메이션 효과")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("풍선 날리기 (st.balloons)"):
                st.balloons()
        with col2:
            if st.button("눈 내리기 (st.snow)"):
                st.snow()

