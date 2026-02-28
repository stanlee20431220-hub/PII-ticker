import streamlit as st
import yfinance as yf
from datetime import datetime
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="PII Premium Ticker", layout="wide")

# 2. 영문 이름과 한글 이름을 튜플로 매핑
ticker_map = {
    "USDKRW=X": ("USD/KRW", "미국달러/원"),
    "^TNX": ("US 10Y", "미국채 10년"),
    "GC=F": ("GOLD", "국제 금"),
    "CL=F": ("WTI", "WTI 유가"),
    "DX-Y.NYB": ("DXY", "달러인덱스"),
    "BTC-USD": ("BTC", "비트코인"),
    "ETH-USD": ("ETH", "이더리움"),
    "XRP-USD": ("XRP", "리플"),
    "^DJI": ("DJI", "다우존스"),
    "^IXIC": ("IXIC", "나스닥"),
    "^GSPC": ("S&P500", "S&P 500"),
    "^KS11": ("KOSPI", "코스피"),
    "^KQ11": ("KOSDAQ", "코스닥")
}

ticker_html = ""

for ticker, (eng_name, kor_name) in ticker_map.items():
    try:
        data = yf.Ticker(ticker).fast_info
        price = data['last_price']
        change_pct = ((price - data['previous_close']) / data['previous_close']) * 100
        
        status_class = "up" if change_pct >= 0 else "down"
        sign = "▲" if change_pct >= 0 else "▼"
        
        # HTML 텍스트 조립 (영문 아래 한글 추가)
        ticker_html += f"""
        <div class="ticker-card">
            <div class="symbol-info">
                <span class="symbol-name">{eng_name}</span>
                <span class="symbol-ko">{kor_name}</span>
            </div>
            <span class="current-price">{price:,.2f}</span>
            <span class="price-change {status_class}">{sign} {abs(change_pct):.2f}%</span>
        </div>
        """
    except:
        continue

# 3. 완벽하게 격리된 HTML/CSS/JS 코드 생성
full_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 0;
        background-color: #0e1117;
        font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, sans-serif;
    }}
    .ticker-container {{
        width: 100%;
        overflow: hidden;
        background-color: #131722; 
        padding: 12px 0;
        border-top: 1px solid #2a2e39;
        border-bottom: 1px solid #2a2e39;
    }}
    .ticker-track {{
        display: flex;
        white-space: nowrap;
        width: max-content;
        animation: scroll 45s linear infinite;
    }}
    /* 마우스 호버 시 일시 정지 */
    .ticker-container:hover .ticker-track {{
        animation-play-state: paused;
        cursor: pointer;
    }}
    .ticker-card {{
        display: inline-flex;
        align-items: center;
        padding: 0 35px;
        border-right: 1px solid #2a2e39;
    }}
    /* 종목 이름 래퍼 (영문/한글 세로 배치) */
    .symbol-info {{
        display: flex;
        flex-direction: column;
        margin-right: 15px;
        justify-content: center;
    }}
    .symbol-name {{
        font-weight: 800;
        font-size: 1.0rem;
        color: #ffffff;
        line-height: 1.2;
    }}
    .symbol-ko {{
        font-weight: 500;
        font-size: 0.75rem;
        color: #8b92a5; /* 한글은 은은한 회색으로 처리 */
        line-height: 1.2;
        margin-top: 3px;
    }}
    .current-price {{
        font-weight: 700;
        font-size: 1.1rem;
        color: #d1d4dc;
        margin-right: 12px;
    }}
    .price-change {{
        font-weight: 600;
        font-size: 1.0rem;
    }}
    /* 한국 시장 표준 색상 명확하게 적용 (!important 추가) */
    .up {{ color: #ff4b4b !important; }}    /* 상승: 뚜렷한 빨간색 */
    .down {{ color: #3b82f6 !important; }}  /* 하락: 뚜렷한 파란색 */
    
    @keyframes scroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
</style>
</head>
<body>
    <div class="ticker-container">
        <div class="ticker-track">
            {ticker_html} {ticker_html}
        </div>
    </div>
</body>
</html>
"""

# 4. 위아래 글씨가 잘리지 않도록 높이를 75로 설정
components.html(full_html, height=75)

# 업데이트 시간 표시
st.caption(f"Last Synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
