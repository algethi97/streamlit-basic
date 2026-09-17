import streamlit as st

def render_theme_switcher():
    """
    사이드바 상단에 원클릭 해수면(☀️) ↔ 심해 어비스(🌌) 테마 전환 버튼을 배치합니다.
    """
    if "theme_mode" not in st.session_state:
        st.session_state.theme_mode = "light"

    st.sidebar.markdown("### 🌊 해양 테마 제어")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("☀️ 해수면", use_container_width=True, key="theme_btn_light"):
            if st.session_state.theme_mode != "light":
                st.session_state.theme_mode = "light"
                st.rerun()
    with col2:
        if st.button("🌌 심해 어비스", use_container_width=True, key="theme_btn_dark"):
            if st.session_state.theme_mode != "dark":
                st.session_state.theme_mode = "dark"
                st.rerun()

    mode_label = "☀️ 맑은 해수면 (부상 완료)" if st.session_state.theme_mode == "light" else "🌌 칠흑의 심해 어비스 (잠수 완료)"
    st.sidebar.caption(f"현재 위치: **{mode_label}**")
    st.sidebar.markdown("---")


def apply_theme():
    """
    사이드바 버튼 원클릭으로 화면 전체(배경, 사이드바, 말풍선, 하단 입력창, 버튼, 캡션)가
    해수면(☀️ 청량 에메랄드) ↔ 심해 어비스(🌌 칠흑의 어둠 및 네온 발광)로 확실하게 전환됩니다.
    - 하단 채팅 입력창([data-testid="stBottom"])의 시커먼 박스는 완벽 투명화됩니다.
    - 화면 전환 시 터지는 느낌 없이, 즉시 화면 곳곳에서 빠르게 솟아오르는 20개의 자연스러운 기포 파티클 적용.
    """
    # 1. 사이드바 스위치 렌더링
    render_theme_switcher()

    is_dark = (st.session_state.get("theme_mode", "light") == "dark")

    if is_dark:
        # 🌌 [심해 어비스 모드] 스타일 세팅
        bg_gradient = """linear-gradient(
            180deg,
            #072738 0%,    /* 상단: 깊은 해역의 암흑 */
            #041a29 35%,
            #02101c 70%,
            #00050f 100%   /* 바닥: 칠흑의 심해 어비스 */
        )"""
        main_text_color = "#e0f7fa"
        caption_color = "#80deea"          # 어두운 심해에서 또렷하게 읽히는 아쿠아 민트
        title_color = "#e0f7fa"
        title_shadow = "0 0 16px rgba(0, 229, 255, 0.7)"
        
        sidebar_bg = "rgba(2, 10, 24, 0.9)"
        sidebar_border = "rgba(0, 229, 255, 0.3)"
        
        msg_bg = "rgba(4, 18, 38, 0.9)"
        msg_border = "rgba(0, 229, 255, 0.35)"
        msg_shadow = "0 0 22px rgba(0, 229, 255, 0.25)"
        
        input_bg = "rgba(4, 18, 38, 0.85)"
        input_border = "rgba(0, 229, 255, 0.5)"
        input_shadow = "0 0 25px rgba(0, 229, 255, 0.3)"

        # 버튼 가독성 (심해 모드: 네온 시안 테두리 + 선명한 아쿠아 화이트 글씨)
        btn_bg = "rgba(6, 26, 50, 0.85)"
        btn_text = "#e0f7fa"
        btn_border = "rgba(0, 229, 255, 0.5)"
        btn_shadow = "0 0 14px rgba(0, 229, 255, 0.2)"

        # 심해 기포 발광 (네온 시안 빛)
        bubble_glow = "rgba(0, 229, 255, 0.65)"
        bubble_core = "rgba(0, 229, 255, 0.45)"
    else:
        # ☀️ [해수면 모드] 스타일 세팅
        bg_gradient = """linear-gradient(
            180deg,
            #d4f5f9 0%,    /* 상단: 맑은날 해수면 투과 햇살 */
            #94e6ee 35%,
            #40c8d8 70%,
            #1596b6 100%   /* 바닥: 청량한 에메랄드 블루 */
        )"""
        main_text_color = "#003049"
        caption_color = "#006d77"          # 밝은 수면에서 선명한 딥 청록색
        title_color = "#004d61"
        title_shadow = "0 2px 8px rgba(0, 150, 180, 0.2)"
        
        sidebar_bg = "rgba(240, 253, 255, 0.75)"
        sidebar_border = "rgba(128, 222, 234, 0.4)"
        
        msg_bg = "rgba(255, 255, 255, 0.88)"
        msg_border = "rgba(128, 222, 234, 0.6)"
        msg_shadow = "0 6px 20px rgba(0, 150, 180, 0.12)"
        
        input_bg = "rgba(255, 255, 255, 0.75)"
        input_border = "rgba(128, 222, 234, 0.6)"
        input_shadow = "0 8px 30px rgba(0, 150, 180, 0.15)"

        # 버튼 가독성 (해수면 모드: 화이트 글래스 + 깊은 네이비 글씨)
        btn_bg = "rgba(255, 255, 255, 0.85)"
        btn_text = "#003049"
        btn_border = "rgba(128, 222, 234, 0.6)"
        btn_shadow = "0 4px 12px rgba(0, 150, 180, 0.12)"

        # 해수면 기포 발광 (맑은 청록빛 햇살)
        bubble_glow = "rgba(0, 150, 180, 0.35)"
        bubble_core = "rgba(128, 222, 234, 0.4)"

    css_code = f"""
    <style>
    /* ==========================================================================
       1. 전체 해양 배경 (뷰포트 고정 및 부드러운 전환)
       ========================================================================== */
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    section[data-testid="stMain"] {{
        background: {bg_gradient} !important;
        background-attachment: fixed !important;
        transition: background 2.0s ease, color 1.5s ease !important;
        color: {main_text_color} !important;
    }}

    /* 2. 스트림릿 상단 헤더 투명화 */
    [data-testid="stHeader"] {{
        background-color: transparent !important;
    }}

    /* ==========================================================================
       3. 🌊 하단 채팅 입력창 영역 투명화 (시커먼 직사각형 박스 완벽 제거)
       ========================================================================== */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottom"] > div > div,
    [data-testid="stBottomBlockContainer"] {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* 하단 입력창(Chat Input): 글래스모피즘 캡슐 */
    [data-testid="stChatInput"] {{
        background: {input_bg} !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1.5px solid {input_border} !important;
        border-radius: 28px !important;
        box-shadow: {input_shadow} !important;
        transition: background 1.5s ease, border-color 1.5s ease, box-shadow 1.5s ease !important;
    }}

    [data-testid="stChatInput"] textarea {{
        color: {main_text_color} !important;
    }}

    /* 4. 사이드바 글래스모피즘 */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-right: 1px solid {sidebar_border} !important;
        transition: background-color 1.5s ease, border-color 1.5s ease !important;
    }}

    /* 5. 버튼 스타일링 (모드별 선명한 가독성 보장) */
    .stButton > button {{
        background: {btn_bg} !important;
        color: {btn_text} !important;
        border: 1.5px solid {btn_border} !important;
        box-shadow: {btn_shadow} !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}

    .stButton > button:hover {{
        filter: brightness(1.15) !important;
        transform: translateY(-1px) !important;
    }}

    /* 6. 캡션(Caption) 가독성 극대화 */
    .stCaption,
    .stCaption p,
    [data-testid="stCaptionContainer"],
    small {{
        color: {caption_color} !important;
        font-weight: 500 !important;
        transition: color 1.5s ease !important;
    }}

    /* 7. 채팅 말풍선 글래스모피즘 */
    .stChatMessage {{
        background-color: {msg_bg} !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid {msg_border} !important;
        border-radius: 16px !important;
        box-shadow: {msg_shadow} !important;
        color: {main_text_color} !important;
        transition: background-color 1.5s ease, 
                    border-color 1.5s ease, 
                    box-shadow 1.5s ease, 
                    color 1.5s ease !important;
        margin-bottom: 0.85rem !important;
    }}

    /* 본문 텍스트 기본 가독성 */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] span,
    [data-testid="stAppViewContainer"] label {{
        color: {main_text_color} !important;
        transition: color 1.5s ease !important;
    }}

    /* 타이틀 */
    h1 {{
        color: {title_color} !important;
        text-shadow: {title_shadow} !important;
        transition: color 1.5s ease, text-shadow 1.5s ease !important;
    }}

    /* ==========================================================================
       8. 🫧 빠르고 유려하게 피어오르는 S자 곡선 기포 (Bubbles) 애니메이션
       - 음수 딜레이(negative delay)로 화면 전환 즉시 이미 올라가고 있는 상태로 렌더링
       - bottom: -50px 화면 밖 출발로 초기 뭉침/터짐 현상 완전 제거
       - 3.5s ~ 6.8s의 경쾌하고 빠른 속도감 부여
       ========================================================================== */
    @keyframes riseSwayLeft {{
        0% {{
            transform: translateY(0) translateX(0) scale(0.6);
            opacity: 0;
        }}
        12% {{
            opacity: 0.85;
        }}
        50% {{
            transform: translateY(-55vh) translateX(-24px) scale(0.9);
            opacity: 0.9;
        }}
        85% {{
            opacity: 0.8;
            transform: translateY(-95vh) translateX(18px) scale(1.1);
        }}
        100% {{
            transform: translateY(-115vh) translateX(-10px) scale(1.15);
            opacity: 0;
        }}
    }}

    @keyframes riseSwayRight {{
        0% {{
            transform: translateY(0) translateX(0) scale(0.6);
            opacity: 0;
        }}
        12% {{
            opacity: 0.85;
        }}
        50% {{
            transform: translateY(-55vh) translateX(24px) scale(0.9);
            opacity: 0.9;
        }}
        85% {{
            opacity: 0.8;
            transform: translateY(-95vh) translateX(-18px) scale(1.1);
        }}
        100% {{
            transform: translateY(-115vh) translateX(10px) scale(1.15);
            opacity: 0;
        }}
    }}

    .ocean-bubble {{
        position: fixed;
        bottom: -50px; /* 화면 밖 아래에서 부드럽게 출발 (초기 깜빡임/터짐 원천 제거) */
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.95), {bubble_core} 60%, rgba(255, 255, 255, 0.15));
        box-shadow: inset 0 0 6px rgba(255, 255, 255, 0.85), 0 0 12px {bubble_glow};
        pointer-events: none;
        z-index: 9999;
    }}

    /* 음수 딜레이로 화면 전환 즉시 화면 전역에서 빠르게 상승 중인 상태로 연출 */
    .b1  {{ left: 5%;  width: 14px; height: 14px; animation: riseSwayLeft  4.8s infinite linear -1.2s; }}
    .b2  {{ left: 10%; width: 22px; height: 22px; animation: riseSwayRight 5.8s infinite linear -3.4s; }}
    .b3  {{ left: 16%; width: 8px;  height: 8px;  animation: riseSwayLeft  3.8s infinite linear -0.5s; }}
    .b4  {{ left: 21%; width: 30px; height: 30px; animation: riseSwayRight 6.5s infinite linear -4.1s; }}
    .b5  {{ left: 27%; width: 16px; height: 16px; animation: riseSwayLeft  4.5s infinite linear -2.0s; }}
    .b6  {{ left: 33%; width: 10px; height: 10px; animation: riseSwayRight 4.0s infinite linear -1.7s; }}
    .b7  {{ left: 39%; width: 26px; height: 26px; animation: riseSwayLeft  6.0s infinite linear -3.8s; }}
    .b8  {{ left: 45%; width: 7px;  height: 7px;  animation: riseSwayRight 3.5s infinite linear -0.9s; }}
    .b9  {{ left: 51%; width: 32px; height: 32px; animation: riseSwayLeft  6.8s infinite linear -5.0s; }}
    .b10 {{ left: 56%; width: 12px; height: 12px; animation: riseSwayRight 4.2s infinite linear -2.3s; }}
    .b11 {{ left: 62%; width: 20px; height: 20px; animation: riseSwayLeft  5.2s infinite linear -1.5s; }}
    .b12 {{ left: 68%; width: 9px;  height: 9px;  animation: riseSwayRight 3.6s infinite linear -2.8s; }}
    .b13 {{ left: 73%; width: 28px; height: 28px; animation: riseSwayLeft  6.2s infinite linear -4.5s; }}
    .b14 {{ left: 78%; width: 15px; height: 15px; animation: riseSwayRight 4.6s infinite linear -0.3s; }}
    .b15 {{ left: 83%; width: 24px; height: 24px; animation: riseSwayLeft  5.5s infinite linear -3.1s; }}
    .b16 {{ left: 88%; width: 11px; height: 11px; animation: riseSwayRight 4.1s infinite linear -1.9s; }}
    .b17 {{ left: 93%; width: 18px; height: 18px; animation: riseSwayLeft  5.0s infinite linear -3.7s; }}
    .b18 {{ left: 97%; width: 28px; height: 28px; animation: riseSwayRight 6.6s infinite linear -2.2s; }}
    .b19 {{ left: 13%; width: 12px; height: 12px; animation: riseSwayRight 4.3s infinite linear -0.8s; }}
    .b20 {{ left: 65%; width: 19px; height: 19px; animation: riseSwayLeft  5.1s infinite linear -4.0s; }}
    </style>

    <!-- 배경 부유 기포 20개 -->
    <div class="ocean-bubble b1"></div>
    <div class="ocean-bubble b2"></div>
    <div class="ocean-bubble b3"></div>
    <div class="ocean-bubble b4"></div>
    <div class="ocean-bubble b5"></div>
    <div class="ocean-bubble b6"></div>
    <div class="ocean-bubble b7"></div>
    <div class="ocean-bubble b8"></div>
    <div class="ocean-bubble b9"></div>
    <div class="ocean-bubble b10"></div>
    <div class="ocean-bubble b11"></div>
    <div class="ocean-bubble b12"></div>
    <div class="ocean-bubble b13"></div>
    <div class="ocean-bubble b14"></div>
    <div class="ocean-bubble b15"></div>
    <div class="ocean-bubble b16"></div>
    <div class="ocean-bubble b17"></div>
    <div class="ocean-bubble b18"></div>
    <div class="ocean-bubble b19"></div>
    <div class="ocean-bubble b20"></div>
    """
    st.html(css_code)
