import streamlit as st
import yfinance as yf
from datetime import datetime

# 1. 페이지 설정 (전체 폭 사용 및 다크 모드)
st.set_page_config(page_title="PII TradingView Ticker", layout="wide")

# 2. 트레이딩뷰 스타일 CSS 정의 (디자인 핵심)
st.markdown("""
    <style>
    /* 전체 전광판 컨테이너 */
    .tv-ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: #131722; /* 다크 블루 배경색 */
        padding: 15px 0;
        border-bottom: 2px solid #2a2e39; /* 테두리색 */
        font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, Ubuntu, sans-serif;
    }
    /* 흐르는 텍스트 컨테이너 */
    .tv-ticker {
        display: inline-block;
        white-space: nowrap;
        animation: ticker-move 35s linear infinite;
        will-change: transform;
    }
    /* 각 티커 아이템 스타일 */
    .tv-ticker__item {
        display: inline-block;
        padding: 0 45px; /* 지표 간 간격 */
        font-size: 1.2rem;
        color: #d1d4dc; /* 텍스트색 */
        border-right: 1px solid #2a2e39; /* 아이템 간 분리선 */
    }
    .tv-ticker__name {
        font-weight: 700;
        margin-right: 12px;
        color: white;
    }
    .tv-ticker__price {
        font-weight: bold;
    }
    .tv-ticker__change {
        margin-left: 10px;
        font-size: 1.0rem;
    }
    /* 상승/하락 색상 (트레이딩뷰 테마) */
    .price-up { color: #00897b; }
    .price-down { color: #ef5350; }
    
    /* 애니메이션 설정 */
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
    "ETH-USD": "ETH", "XRP-USD": "XRP", "^DJI": "DJI", 
    "^IXIC": "IXIC", "^GSPC": "SPX500", "^KS11": "KOSPI", "^KQ11": "KOSDAQ"
}

ticker_items_html = ""

# 데이터 가져오기 및 HTML 구성
for ticker, name in tickers.items():
    try:
        data = yf.Ticker(ticker).fast_info
        price = data['last_price']
        prev_close = data['previous_close']
        change_pct = ((price - prev_close) / prev_close) * 100
        
        # 상승/하락에 따른 색상 및 기호 설정
        color_class = "price-up" if change_pct >= 0 else "price-down"
        sign = "+" if change_pct >= 0 else ""
        
        # 각 지표 HTML 아이템 생성
        ticker_items_html += f"""
        <div class="tv-ticker__item">
            <span class="tv-ticker__name">{name}</span>
            <span class="tv-ticker__price {color_class}">{price:,.2f}</span>
            <span class="tv-ticker__change {color_class}">{sign}{change_pct:.2f}%</span>
        </div>
        """
    except:
        continue

# 4. 화면 출력 (동일한 내용을 두 번 반복하여 무한 루프 구현)
st.markdown(f"""
    <div class="tv-ticker-wrap">
        <div class="tv-ticker">
            {ticker_items_html} {ticker_items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 하단 업데이트 시간
st.caption(f"Final Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
