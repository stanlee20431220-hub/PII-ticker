import streamlit as st
import yfinance as yf
from datetime import datetime

# 1. 페이지 설정 (메뉴 숨기기 및 넓게 쓰기)
st.set_page_config(page_title="PII TradingView Ticker", layout="wide")

# 2. 세련된 트레이딩뷰 스타일 CSS
st.markdown("""
    <style>
    /* 메인 배경 및 레이아웃 */
    .stApp { background-color: #0e1117; }
    
    .tv-ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #131722; 
        padding: 15px 0;
        border-bottom: 2px solid #2a2e39;
        font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, sans-serif;
    }
    
    .tv-ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker-move 40s linear infinite;
    }
    
    .tv-ticker__item {
        display: inline-block;
        padding: 0 50px;
        font-size: 1.2rem;
        border-right: 1px solid #2a2e39;
    }
    
    .tv-ticker__name { font-weight: 700; color: #ffffff; margin-right: 10px; }
    .tv-ticker__price { font-weight: 700; color: #d1d4dc; }
    .price-up { color: #00897b !important; }
    .price-down { color: #ef5350 !important; }
    
    @keyframes ticker-move {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 수집
tickers = {
    "USDKRW=X": "USD/KRW", "^TNX": "US 10YR", "GC=F": "GOLD",
    "CL=F": "WTI", "DX-Y.NYB": "DXY", "BTC-USD": "BTC",
    "ETH-USD": "ETH", "^DJI": "DJI", "^IXIC": "IXIC", 
    "^GSPC": "SPX500", "^KS11": "KOSPI", "^KQ11": "KOSDAQ"
}

ticker_items_html = ""

for ticker, name in tickers.items():
    try:
        data = yf.Ticker(ticker).fast_info
        price = data['last_price']
        change_pct = ((price - data['previous_close']) / data['previous_close']) * 100
        color_class = "price-up" if change_pct >= 0 else "price-down"
        sign = "+" if change_pct >= 0 else ""
        
        ticker_items_html += f"""
        <div class="tv-ticker__item">
            <span class="tv-ticker__name">{name}</span>
            <span class="tv-ticker__price">{price:,.2f}</span>
            <span class="tv-ticker__change {color_class}">{sign}{change_pct:.2f}%</span>
        </div>
        """
    except:
        continue

# 4. HTML 출력 (반드시 아래 형식을 유지하세요)
st.markdown(f"""
    <div class="tv-ticker-wrap">
        <div class="tv-ticker">
            {ticker_items_html} {ticker_items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
