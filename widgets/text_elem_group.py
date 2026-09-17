import streamlit as st

def show_text_elements():
    tab_headings, tab_markdown, tab_code = st.tabs([
        "제목 및 서식",
        "마크다운 & 배지",
        "코드 & 수식"
    ])

    # 1. 제목 및 서식
    with tab_headings:
        st.title("st.title: 대제목")
        st.header("st.header: 섹션 헤더")
        st.subheader("st.subheader: 하위 서브헤더")
        st.caption("st.caption: 주석이나 작은 설명 문구")
        st.divider()
        st.write("st.divider()로 위아래를 구분선으로 나눌 수 있습니다.")

    # 2. 마크다운 & 배지
    with tab_markdown:
        st.subheader("st.markdown 예제")
        st.markdown("**굵은 글씨**, *기울임*, ~~취소선~~")
        st.markdown(":red[빨간색 텍스트], :blue[파란색 텍스트], :green[초록색 텍스트]")
        st.markdown("[Streamlit 공식 홈페이지](https://streamlit.io)")

        st.divider()

        st.subheader("st.badge 예제")
        st.badge("신규 기능", icon=":material/new_releases:")
        st.badge("안정 버전", icon=":material/verified:")

    # 3. 코드 & 수식
    with tab_code:
        st.subheader("st.code (문법 강조 코드 블록)")
        code_example = """def hello():
    print("Hello, Streamlit!")
hello()"""
        st.code(code_example, language="python")

        st.divider()

        st.subheader("st.latex (수식 렌더링)")
        st.latex(r"E = mc^2")
        st.latex(r"a^2 + b^2 = c^2")

        st.divider()

        st.subheader("st.text (고정폭 서식 없는 텍스트)")
        st.text("이것은 서식이 없는 순수 텍스트(Fixed-width text)입니다.")

