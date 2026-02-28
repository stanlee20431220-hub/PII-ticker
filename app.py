import streamlit as st
import yfinance as yf
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="PII Continuous Ticker", layout="wide")

# 2. CSS 개선: 무한 루프를 위해 애니메이션 최적화
st.markdown("""
    <style>
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #0e1117; 
        padding: 12px 0;
        border-bottom: 2px solid #31333f;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        padding-right: 100%; /* 초기 위치 설정 */
        animation: ticker-move 40s linear infinite; /* 속도 조절 가능 */
    }
    .ticker__item {
        display: inline-block;
        padding: 0 40px; /* 지표 간 간격 */
        font-size: 1.1rem;
        color: white;
    }
    .price-up { color: #ff4b4b; font-weight: bold; }
    .price-down { color: #0068c9; font-weight: bold; }
    
    @keyframes ticker-move {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 수집
tickers = {
    "USDKRW=X": "USD/KRW", "^TNX": "미국채10년", "GC=F": "금",
    "CL=F": "WTI유가", "DX-Y.NYB": "달러인덱스", "BTC-USD": "BTC",
    "ETH-USD": "ETH", "XRP-USD": "리플", "^DJI": "다우존스", 
    "^IXIC": "나스닥", "^GSPC": "S&P500", "^KS11": "코스피", "^KQ11": "코스닥"
}

ticker_items_html = ""

# 데이터 가져오기 및 HTML 구성
for ticker, name in tickers.items():
    try:
        data = yf.Ticker(ticker).fast_info
        price = data['last_price']
        change_pct = ((price - data['previous_close']) / data['previous_close']) * 100
        color_class = "price-up" if change_pct >= 0 else "price-down"
        sign = "+" if change_pct >= 0 else ""
        
        ticker_items_html += f'<div class="ticker__item">{name} {price:,.2f} <span class="{color_class}">{sign}{change_pct:.2f}%</span></div>'
    except:
        continue

# 4. 화면 출력 (동일한 내용을 두 번 반복하여 공백 제거)
st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            {ticker_items_html} {ticker_items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
