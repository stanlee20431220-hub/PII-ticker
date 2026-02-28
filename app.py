import streamlit as st
import yfinance as yf
from datetime import datetime
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="PII Premium Ticker", layout="wide")

# 2. 데이터 수집 리스트
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
        
        # HTML 텍스트 조립
        ticker_html += f"""
        <div class="ticker-card">
            <span class="symbol-name">{display_name}</span>
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
        background-color: #0e1117; /* Streamlit 다크모드 배경색 */
        font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, sans-serif;
    }}
    .ticker-container {{
        width: 100%;
        overflow: hidden;
        background-color: #131722; 
        padding: 10px 0;
        border-top: 1px solid #2a2e39;
        border-bottom: 1px solid #2a2e39;
    }}
    .ticker-track {{
        display: flex;
        white-space: nowrap;
        width: max-content;
        animation: scroll 40s linear infinite;
    }}
    /* 마우스 호버 시 일시 정지 */
    .ticker-container:hover .ticker-track {{
        animation-play-state: paused;
        cursor: pointer;
    }}
    .ticker-card {{
        display: inline-flex;
        align-items: center;
        padding: 0 30px;
        border-right: 1px solid #2a2e39;
    }}
    .symbol-name {{
        font-weight: 800;
        font-size: 1.0rem;
        color: #ffffff;
        margin-right: 10px;
    }}
    .current-price {{
        font-weight: 700;
        font-size: 1.0rem;
        color: #d1d4dc;
        margin-right: 8px;
    }}
    .price-change {{
        font-weight: 600;
        font-size: 0.95rem;
    }}
    .up {{ color: #089981; }}
    .down {{ color: #f23645; }}
    
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

# 4. components.html을 사용하여 화면에 렌더링 (높이를 60px로 고정하여 깔끔하게 출력)
components.html(full_html, height=60)

# 업데이트 시간 표시
st.caption(f"Last Synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
