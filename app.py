import streamlit as st
import yfinance as yf
from datetime import datetime

# 1. 페이지 설정 (전체 폭 사용 및 메뉴 숨기기)
st.set_page_config(page_title="PII Ticker Tape", layout="wide")

# 2. CSS를 이용한 흐르는 애니메이션 정의
st.markdown("""
    <style>
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #0e1117; 
        padding: 10px 0;
        border-bottom: 1px solid #31333f;
    }
    .ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker 30s linear infinite;
    }
    .ticker__item {
        display: inline-block;
        padding: 0 30px;
        font-size: 1.2rem;
        color: white;
    }
    .price-up { color: #ff4b4b; }
    .price-down { color: #0068c9; }
    
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 수집 함수
tickers = {
    "USDKRW=X": "USD/KRW", "^TNX": "미국채10년", "GC=F": "금",
    "CL=F": "WTI유가", "DX-Y.NYB": "달러인덱스", "BTC-USD": "BTC",
    "ETH-USD": "ETH", "^DJI": "다우존스", "^IXIC": "나스닥", 
    "^GSPC": "S&P500", "^KS11": "코스피", "^KQ11": "코스닥"
}

ticker_items_html = ""

for ticker, name in tickers.items():
    try:
        data = yf.Ticker(ticker).fast_info
        price = data['last_price']
        change_pct = ((price - data['previous_close']) / data['previous_close']) * 100
        color_class = "price-up" if change_pct >= 0 else "price-down"
        sign = "+" if change_pct >= 0 else ""
        
        # 각 아이템을 HTML 문자열로 생성
        ticker_items_html += f'<div class="ticker__item"><b>{name}</b> {price:,.2f} <span class="{color_class}">{sign}{change_pct:.2f}%</span></div>'
    except:
        continue

# 4. 화면에 흐르는 전광판 출력
st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            {ticker_items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 하단에 기존 그리드 방식도 유지하고 싶다면 아래 주석을 해제하세요.
# st.write("---")
# (이전의 st.columns 코드를 여기에 넣을 수 있습니다)
