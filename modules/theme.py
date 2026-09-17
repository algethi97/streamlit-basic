import streamlit as st

def apply_theme():
    """
    Streamlit 자체 라이트/다크 모드(Settings -> Theme) 및 OS 테마와 100% 연동되는
    순수 CSS 해수면 ↔ 심해 수직 잠수/부상 애니메이션을 주입합니다.
    """
    css_code = """
    <style>
    /* ==========================================================================
       1. 거대한 400% 수직 해양 배경 (기본: ☀️ 해수면 모드 / 0%)
       ========================================================================== */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(
            180deg,
            #d4f5f9 0%,    /* [0%] 맑은날 해수면 바로 아래 (태양광 투과) */
            #94e6ee 10%,
            #40c8d8 22%,   /* [얕은 바다] 청량한 에메랄드 블루 */
            #1596b6 38%,
            #0b6a8d 52%,   /* [중층 해역] 깊어지는 청록빛 */
            #044265 68%,
            #032545 80%,   /* [어둠의 경계] 짙은 미드나이트 블루 */
            #021226 90%,
            #00050f 100%   /* [100%] 칠흑의 심해 어비스 */
        ) !important;
        background-size: 100% 400% !important;
        background-position: 50% 0% !important; /* 기본: 해수면 */
        transition: background-position 2.5s cubic-bezier(0.22, 1, 0.36, 1),
                    color 2.0s ease,
                    background-color 2.0s ease !important;
        color: #042c38 !important;
    }

    /* 2. 스트림릿 상단 헤더 투명화 */
    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 3. 사이드바 (기본: 해수면 모드) */
    [data-testid="stSidebar"] {
        background-color: rgba(240, 253, 255, 0.65) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-right: 1px solid rgba(128, 222, 234, 0.35) !important;
        transition: background-color 2.0s ease, border-color 2.0s ease !important;
    }

    /* 4. 채팅 말풍선 (기본: 해수면 모드 - 화이트/아쿠아 글래스모피즘) */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.82) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(128, 222, 234, 0.6) !important;
        border-radius: 16px !important;
        box-shadow: 0 6px 20px rgba(0, 150, 180, 0.12) !important;
        color: #042c38 !important;
        transition: background-color 2.0s ease, 
                    border-color 2.0s ease, 
                    box-shadow 2.0s ease, 
                    color 2.0s ease !important;
        margin-bottom: 0.85rem !important;
    }

    /* 기본 타이틀 (해수면 햇살 음영) */
    h1 {
        color: #004d61 !important;
        text-shadow: 0 2px 8px rgba(0, 150, 180, 0.15) !important;
        transition: color 2.0s ease, text-shadow 2.0s ease !important;
    }

    /* ==========================================================================
       5. 🌌 다크 모드 감지 시: 2.5초간 심해(100%)로 수직 하강 잠수!
       (브라우저/OS 다크모드 및 Streamlit Settings -> Theme 'Dark' 완벽 대응)
       ========================================================================== */
    @media (prefers-color-scheme: dark) {
        [data-testid="stAppViewContainer"] {
            background-position: 50% 100% !important; /* 심해로 잠수! */
            color: #e0f7fa !important;
        }

        [data-testid="stSidebar"] {
            background-color: rgba(2, 10, 24, 0.75) !important;
            border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
        }

        .stChatMessage {
            background-color: rgba(4, 18, 38, 0.82) !important;
            border: 1px solid rgba(0, 229, 255, 0.35) !important;
            box-shadow: 0 0 22px rgba(0, 229, 255, 0.2) !important;
            color: #e0f7fa !important;
        }

        h1 {
            color: #e0f7fa !important;
            text-shadow: 0 0 16px rgba(0, 229, 255, 0.5) !important;
        }
    }

    /* Streamlit DOM data-theme="dark" 속성 지원 */
    [data-theme="dark"] [data-testid="stAppViewContainer"],
    body[data-theme="dark"] [data-testid="stAppViewContainer"],
    .dark [data-testid="stAppViewContainer"] {
        background-position: 50% 100% !important;
        color: #e0f7fa !important;
    }

    [data-theme="dark"] [data-testid="stSidebar"],
    body[data-theme="dark"] [data-testid="stSidebar"] {
        background-color: rgba(2, 10, 24, 0.75) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.2) !important;
    }

    [data-theme="dark"] .stChatMessage,
    body[data-theme="dark"] .stChatMessage {
        background-color: rgba(4, 18, 38, 0.82) !important;
        border: 1px solid rgba(0, 229, 255, 0.35) !important;
        box-shadow: 0 0 22px rgba(0, 229, 255, 0.2) !important;
        color: #e0f7fa !important;
    }

    [data-theme="dark"] h1,
    body[data-theme="dark"] h1 {
        color: #e0f7fa !important;
        text-shadow: 0 0 16px rgba(0, 229, 255, 0.5) !important;
    }

    /* ==========================================================================
       6. 부유하는 바닷속 기포(Bubbles) 파티클 애니메이션
       ========================================================================== */
    @keyframes riseBubble {
        0% {
            transform: translateY(105vh) translateX(0) scale(0.5);
            opacity: 0;
        }
        15% {
            opacity: 0.7;
        }
        80% {
            opacity: 0.85;
        }
        100% {
            transform: translateY(-10vh) translateX(35px) scale(1.15);
            opacity: 0;
        }
    }

    .ocean-bubble {
        position: fixed;
        bottom: 0;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.9), rgba(0, 229, 255, 0.45) 60%, rgba(255, 255, 255, 0.1));
        box-shadow: inset 0 0 6px rgba(255, 255, 255, 0.8), 0 0 10px rgba(0, 229, 255, 0.3);
        pointer-events: none;
        z-index: 9999;
    }

    .b1 { left: 10%; width: 14px; height: 14px; animation: riseBubble 7s infinite linear; }
    .b2 { left: 25%; width: 22px; height: 22px; animation: riseBubble 9s infinite 1.5s linear; }
    .b3 { left: 45%; width: 10px; height: 10px; animation: riseBubble 6s infinite 3s linear; }
    .b4 { left: 65%; width: 26px; height: 26px; animation: riseBubble 11s infinite 0.5s linear; }
    .b5 { left: 80%; width: 16px; height: 16px; animation: riseBubble 8s infinite 2.2s linear; }
    .b6 { left: 92%; width: 12px; height: 12px; animation: riseBubble 7.5s infinite 4s linear; }
    </style>

    <!-- 배경 부유 기포 요소들 -->
    <div class="ocean-bubble b1"></div>
    <div class="ocean-bubble b2"></div>
    <div class="ocean-bubble b3"></div>
    <div class="ocean-bubble b4"></div>
    <div class="ocean-bubble b5"></div>
    <div class="ocean-bubble b6"></div>
    """
    st.html(css_code)
