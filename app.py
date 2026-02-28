import streamlit as st
import yfinance as yf
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="PII TradingView Ticker", layout="wide")

# 2. 세련된 트레이딩뷰 스타일 CSS
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .tv-ticker-wrap {
        width: 100%; overflow: hidden; background-color: #131722; 
        padding: 15px 0; border-bottom: 2px solid #2a2e39;
        font-family: -apple-system, sans-serif;
    }
    .tv-ticker {
        display: inline-block; white-space: nowrap;
        animation: ticker-move 40s linear infinite;
    }
    .tv-ticker__item {
        display: inline-block; padding: 0 50px;
        font-size: 1.2rem; border-right: 1px solid #2a2e39;
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
        price, prev = data['last_price'], data['previous_close']
        change_pct = ((price - prev) / prev) * 100
        color = "price-up" if change_pct >= 0 else "price-down"
        ticker_items_html += f'<div class="tv-ticker__item"><span class="tv-ticker__name">{name}</span><span class="tv-ticker__price">{price:,.2f}</span> <span class="{color}">{change_pct:+.2f}%</span></div>'
    except: continue

# 4. 화면 출력 (반드시 unsafe_allow_html=True 포함)
st.markdown(f'<div class="tv-ticker-wrap"><div class="tv-ticker">{ticker_items_html} {ticker_items_html}</div></div>', unsafe_allow_html=True)
st.caption(f"Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
