import streamlit as st
import yfinance as yf
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="PII Premium Ticker", layout="wide")

# 2. 고급스러운 트레이딩뷰 스타일 CSS (마우스 호버 멈춤 포함)
st.markdown("""
    <style>
    /* 전체 배경 설정 */
    .stApp { background-color: #0e1117; }
    
    /* 전광판 메인 컨테이너 */
    .ticker-container {
        width: 100%;
        overflow: hidden;
        background-color: #131722; 
        padding: 12px 0;
        border-top: 1px solid #2a2e39;
        border-bottom: 1px solid #2a2e39;
        font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, sans-serif;
    }

    /* 흐르는 트랙 */
    .ticker-track {
        display: flex;
        white-space: nowrap;
        width: max-content;
        animation: scroll 45s linear infinite;
    }

    /* 마우스 호버 시 애니메이션 일시 정지 */
    .ticker-container:hover .ticker-track {
        animation-play-state: paused;
        cursor: pointer;
    }

    /* 개별 지표 카드 디자인 */
    .ticker-card {
        display: inline-flex;
        align-items: center;
        padding: 0 35px;
        border-right: 1px solid #2a2e39;
    }

    .symbol-name {
        font-weight: 800;
        font-size: 1.1rem;
        color: #ffffff;
        margin-right: 10px;
    }

    .current-price {
        font-weight: 700;
        font-size: 1.1rem;
        color: #d1d4dc;
        margin-right: 8px;
    }

    .price-change {
        font-weight: 600;
        font-size: 1rem;
    }

    /* 트레이딩뷰 스타일 색상 */
    .up { color: #089981 !important; }
    .down { color: #f23645 !important; }

    /* 애니메이션 정의 */
    @keyframes scroll {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 수집 리스트
ticker_map = {
    "USDKRW=X": "USD/KRW", "^TNX": "US 10Y", "GC=F": "GOLD",
    "CL=F": "WTI", "DX-Y.NYB": "DXY", "BTC-USD": "BTC",
    "ETH-USD": "ETH", "XRP-USD": "XRP", "^DJI": "DJI", 
    "^IXIC": "IXIC", "^GSPC": "S&P500", "^KS11": "KOSPI", "^KQ11": "KOSDAQ"
}

ticker_html = ""

for ticker, display_name in ticker_map.items():
    try:
        data = yf.Ticker(ticker).fast_info
        price = data['last_price']
        change_pct = ((price - data['previous_close']) / data['previous_close']) * 100
        
        status_class = "up" if change_pct >= 0 else "down"
        sign = "▲" if change_pct >= 0 else "▼"
        
        ticker_html += f"""
        <div class="ticker-card">
            <span class="symbol-name">{display_name}</span>
            <span class="current-price">{price:,.2f}</span>
            <span class="price-change {status_class}">{sign} {abs(change_pct):.2f}%</span>
        </div>
        """
    except:
        continue

# 4. 무한 루프를 위해 내용을 두 번 반복하여 출력
st.markdown(f"""
    <div class="ticker-container">
        <div class="ticker-track">
            {ticker_html} {ticker_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.caption(f"Last Synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
