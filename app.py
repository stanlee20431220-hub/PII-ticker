import streamlit as st
import yfinance as yf
import pandas as pd

# 페이지 설정 (전체 폭 사용)
st.set_page_config(page_title="시장 지표 대시보드", layout="wide")

st.title("📊 실시간 글로벌 시장 지표")

# 가져올 지표 설정 (티커: 이름)
tickers = {
    "USDKRW=X": "미국달러/원 환율",
    "^TNX": "미국채 10년물",
    "GC=F": "국제 금(Gold)",
    "CL=F": "WTI 유가",
    "DX-Y.NYB": "달러 인덱스",
    "BTC-USD": "비트코인",
    "ETH-USD": "이더리움",
    "XRP-USD": "리플",
    "^DJI": "다우존스",
    "^IXIC": "나스닥",
    "^GSPC": "S&P 500",
    "^KS11": "코스피",
    "^KQ11": "코스닥"
}

def get_market_data(ticker_dict):
    data_list = []
    for ticker, name in ticker_dict.items():
        try:
            # 실시간 데이터 가져오기
            ytick = yf.Ticker(ticker)
            info = ytick.fast_info
            
            current_price = info['last_price']
            prev_close = info['previous_close']
            change = current_price - prev_close
            pct_change = (change / prev_close) * 100
            
            data_list.append({
                "지표명": name,
                "현재가": current_price,
                "변동": change,
                "변동률": pct_change
            })
        except:
            continue
    return data_list

# 데이터 로드
with st.spinner('데이터를 불러오는 중...'):
    market_data = get_market_data(tickers)

# 화면 레이아웃 구성 (한 줄에 4개씩 배치)
cols = st.columns(4)

for idx, item in enumerate(market_data):
    with cols[idx % 4]:
        # 상승/하락에 따른 색상 및 기호 설정
        delta_str = f"{item['변동']:.2f} ({item['변동률']:.2f}%)"
        
        st.metric(
            label=item['지표명'], 
            value=f"{item['현재가']:,.2f}", 
            delta=delta_str
        )

# 하단 업데이트 시간 표시
from datetime import datetime
st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 자동 새로고침 버튼
if st.button('시세 새로고침'):
    st.rerun()