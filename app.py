import streamlit as st
import yfinance as yf
from datetime import datetime
import streamlit.components.v1 as components
import altair as alt # 차트를 그리기 위한 내장 라이브러리

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

# 3. 상단 흐르는 티커 전광판 HTML
full_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0; padding: 0; background-color: #0e1117;
        font-family: -apple-system, sans-serif;
    }}
    .ticker-container {{
        width: 100%; overflow: hidden; background-color: #131722; 
        padding: 12px 0; border-top: 1px solid #2a2e39; border-bottom: 1px solid #2a2e39;
    }}
    .ticker-track {{
        display: flex; white-space: nowrap; width: max-content;
        animation: scroll 45s linear infinite;
    }}
    .ticker-container:hover .ticker-track {{
        animation-play-state: paused; cursor: pointer;
    }}
    .ticker-card {{
        display: inline-flex; align-items: center; padding: 0 35px; border-right: 1px solid #2a2e39;
    }}
    .symbol-info {{
        display: flex; flex-direction: column; margin-right: 15px; justify-content: center;
    }}
    .symbol-name {{ font-weight: 800; font-size: 1.0rem; color: #ffffff; line-height: 1.2; }}
    .symbol-ko {{ font-weight: 500; font-size: 0.75rem; color: #8b92a5; line-height: 1.2; margin-top: 3px; }}
    .current-price {{ font-weight: 700; font-size: 1.1rem; color: #d1d4dc; margin-right: 12px; }}
    .price-change {{ font-weight: 600; font-size: 1.0rem; }}
    .up {{ color: #ff4b4b !important; }}
    .down {{ color: #3b82f6 !important; }}
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

components.html(full_html, height=75)
st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📊 주요 지표 및 관심 종목 차트")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📊 주요 지표 및 관심 종목 차트")

# 4. 차트 데이터를 가져오는 함수 (1개월치 데이터 로드)
@st.cache_data(ttl=600)
def get_chart_data():
    targets = {
        "코스피": "^KS11", "코스닥": "^KQ11", "환율(달러/원)": "USDKRW=X",
        "미국 국채 10년": "^TNX", "국제금": "GC=F", 
        "삼성전자": "005930.KS", "SK하이닉스": "000660.KS"
    }
    hist_data = {}
    for name, tk in targets.items():
        try:
            df = yf.Ticker(tk).history(period="1mo")
            if not df.empty and len(df) > 1:
                hist_data[name] = df
        except:
            continue
    return hist_data

chart_data = get_chart_data()

# 5. 4열 그리드 레이아웃으로 차트 카드 배치
cols = st.columns(4)

for idx, (name, df) in enumerate(chart_data.items()):
    col = cols[idx % 4]
    
    with col:
        # Streamlit의 Card 형태 컨테이너 사용
        with st.container(border=True):
            curr_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            diff = curr_price - prev_price
            pct = (diff / prev_price) * 100
            
            # 종목별 소수점 포맷팅
            if name in ["삼성전자", "SK하이닉스"]:
                p_str, d_str = f"{curr_price:,.0f}", f"{diff:,.0f}"
            elif name == "미국 국채 10년":
                p_str, d_str = f"{curr_price:.4f}", f"{diff:.4f}"
            else:
                p_str, d_str = f"{curr_price:,.2f}", f"{diff:,.2f}"
                
            color_hex = "#ff4b4b" if diff >= 0 else "#3b82f6"
            sign = "▲" if diff >= 0 else "▼"
            
            # 글씨 겹침/잘림 해결을 위해 간격(margin) 최적화
            st.markdown(f"""
            <div>
                <div style="color: #8b92a5; font-size: 14px; font-weight: 600;">{name}</div>
                <div style="color: #d1d4dc; font-size: 24px; font-weight: bold; margin: 4px 0;">{p_str}</div>
                <div style="color: {color_hex}; font-size: 15px; font-weight: 600; margin-bottom: 8px;">{sign} {abs(diff):.2f} ({pct:+.2f}%)</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 데이터프레임 인덱스(날짜) 초기화 및 차트 영역 설정
            chart_df = df.reset_index()
            chart_df = chart_df.rename(columns={chart_df.columns[0]: 'Date'})
            
            # 💡 핵심 수정: Y축이 0부터 시작하지 않고 데이터 범위에 딱 맞게(zero=False) 설정
            base_chart = alt.Chart(chart_df).encode(
                x=alt.X('Date:T', axis=None), # X축 숨김
                y=alt.Y('Close:Q', scale=alt.Scale(zero=False), axis=None), # Y축 숨김 및 범위 자동 조절
                tooltip=['Date:T', 'Close:Q']
            ).properties(height=80) # 차트 높이를 80으로 줄여 카드 안에 쏙 들어가게 조절
            
            # 선 차트 생성
            line = base_chart.mark_line(color=color_hex, strokeWidth=2)
            
            # 하단 그라데이션 면적 추가 (트레이딩뷰 스타일)
            area = base_chart.mark_area(
                line={'color': 'transparent'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color=color_hex, offset=0), 
                           alt.GradientStop(color='rgba(0,0,0,0)', offset=1)],
                    x1=1, x2=1, y1=1, y2=0
                )
            )
            
            # 차트를 화면에 렌더링
            st.altair_chart(area + line, use_container_width=True)
