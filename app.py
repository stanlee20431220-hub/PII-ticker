import streamlit as st
import yfinance as yf
from datetime import datetime
import streamlit.components.v1 as components
import altair as alt
import pandas as pd
import plotly.express as px

# ==========================================
# 1. 페이지 및 기본 설정
# ==========================================
st.set_page_config(page_title="PII Premium Ticker", layout="wide")

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

# ==========================================
# 2. 상단 흐르는 티커 전광판
# ==========================================
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

full_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; padding: 0; background-color: #0e1117; font-family: -apple-system, sans-serif; }}
    .ticker-container {{ width: 100%; overflow: hidden; background-color: #131722; padding: 12px 0; border-top: 1px solid #2a2e39; border-bottom: 1px solid #2a2e39; }}
    .ticker-track {{ display: flex; white-space: nowrap; width: max-content; animation: scroll 45s linear infinite; }}
    .ticker-container:hover .ticker-track {{ animation-play-state: paused; cursor: pointer; }}
    .ticker-card {{ display: inline-flex; align-items: center; padding: 0 35px; border-right: 1px solid #2a2e39; }}
    .symbol-info {{ display: flex; flex-direction: column; margin-right: 15px; justify-content: center; }}
    .symbol-name {{ font-weight: 800; font-size: 1.0rem; color: #ffffff; line-height: 1.2; }}
    .symbol-ko {{ font-weight: 500; font-size: 0.75rem; color: #8b92a5; line-height: 1.2; margin-top: 3px; }}
    .current-price {{ font-weight: 700; font-size: 1.1rem; color: #d1d4dc; margin-right: 12px; }}
    .price-change {{ font-weight: 600; font-size: 1.0rem; }}
    .up {{ color: #ff4b4b !important; }}
    .down {{ color: #3b82f6 !important; }}
    @keyframes scroll {{ 0% {{ transform: translateX(0); }} 100% {{ transform: translateX(-50%); }} }}
</style>
</head>
<body>
    <div class="ticker-container">
        <div class="ticker-track">{ticker_html} {ticker_html}</div>
    </div>
</body>
</html>
"""

components.html(full_html, height=75)
st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ==========================================
# 3. 주요 지표 스파크라인 차트 (일직선 오류 해결)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("📊 주요 지표 및 관심 종목 차트")

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
cols = st.columns(4)

for idx, (name, df) in enumerate(chart_data.items()):
    col = cols[idx % 4]
    with col:
        with st.container(border=True):
            curr_price = float(df['Close'].iloc[-1])
            prev_price = float(df['Close'].iloc[-2])
            diff = curr_price - prev_price
            pct = (diff / prev_price) * 100
            
            if name in ["삼성전자", "SK하이닉스"]:
                p_str, d_str = f"{curr_price:,.0f}", f"{diff:,.0f}"
            elif name == "미국 국채 10년":
                p_str, d_str = f"{curr_price:.4f}", f"{diff:.4f}"
            else:
                p_str, d_str = f"{curr_price:,.2f}", f"{diff:,.2f}"
                
            color_hex = "#ff4b4b" if diff >= 0 else "#3b82f6"
            sign = "▲" if diff >= 0 else "▼"
            
            st.markdown(f"""
            <div>
                <div style="color: #8b92a5; font-size: 14px; font-weight: 600;">{name}</div>
                <div style="color: #d1d4dc; font-size: 24px; font-weight: bold; margin: 4px 0;">{p_str}</div>
                <div style="color: {color_hex}; font-size: 15px; font-weight: 600; margin-bottom: 8px;">{sign} {abs(diff):.2f} ({pct:+.2f}%)</div>
            </div>
            """, unsafe_allow_html=True)
            
            chart_df = df.reset_index()
            chart_df = chart_df.rename(columns={chart_df.columns[0]: 'Date'})
            
            # 💡 [핵심 수정] 0이 아닌 차트의 최저점을 바닥(bottom_val)으로 강제 고정
            min_val = float(chart_df['Close'].min())
            max_val = float(chart_df['Close'].max())
            margin = (max_val - min_val) * 0.1 if max_val != min_val else 1
            bottom_val = min_val - margin
            
            base_chart = alt.Chart(chart_df).encode(
                x=alt.X('Date:T', axis=None), 
                y=alt.Y('Close:Q', scale=alt.Scale(domain=[bottom_val, max_val + margin]), axis=None), 
                tooltip=['Date:T', 'Close:Q']
            ).properties(height=80) 
            
            line = base_chart.mark_line(color=color_hex, strokeWidth=2)
            
            # area 차트가 0이 아닌 bottom_val(최저점)까지만 칠해지도록 y2 값 추가
            area = base_chart.mark_area(
                line={'color': 'transparent'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color=color_hex, offset=0), 
                           alt.GradientStop(color='rgba(0,0,0,0)', offset=1)],
                    x1=1, x2=1, y1=1, y2=0
                )
            ).encode(
                y2=alt.datum(bottom_val)
            )
            st.altair_chart(area + line, use_container_width=True)

# ==========================================
# 4. 국내 주요 섹터 히트맵 (파이썬 Plotly 버전)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🗺️ 국내 주요 섹터 히트맵 (Market Heatmap)")

@st.cache_data(ttl=600)
def get_heatmap_data():
    portfolio = {
        "반도체": {"삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "한미반도체": "042700.KS"},
        "배터리/화학": {"LG에너지솔루션": "373220.KS", "POSCO홀딩스": "005490.KS", "LG화학": "051910.KS"},
        "IT/플랫폼": {"NAVER": "035420.KS", "카카오": "035720.KS"},
        "자동차": {"현대차": "005380.KS", "기아": "000270.KS"},
        "바이오": {"삼성바이오로직스": "207940.KS", "셀트리온": "068270.KS"},
        "금융": {"KB금융": "105560.KS", "신한지주": "055550.KS"}
    }

    data = []
    for sector, stocks in portfolio.items():
        for name, ticker in stocks.items():
            try:
                info = yf.Ticker(ticker).fast_info
                mcap = info['market_cap']
                price = info['last_price']
                prev = info['previous_close']
                pct_change = ((price - prev) / prev) * 100

                data.append({
                    "섹터": sector,
                    "종목명": name,
                    "시가총액": mcap,
                    "등락률": pct_change,
                    "텍스트표시": f"<b>{name}</b><br>{pct_change:+.2f}%"
                })
            except:
                continue
    return pd.DataFrame(data)

with st.spinner("히트맵 데이터를 불러오는 중입니다..."):
    heatmap_df = get_heatmap_data()

if not heatmap_df.empty:
    fig = px.treemap(
        heatmap_df,
        path=[px.Constant("한국 주요증시"), '섹터', '종목명'], 
        values='시가총액', 
        color='등락률',   
        color_continuous_scale=[[0, '#3b82f6'], [0.5, '#131722'], [1, '#ff4b4b']], 
        color_continuous_midpoint=0,
        custom_data=['텍스트표시']
    )

    fig.update_traces(
        texttemplate="%{customdata[0]}",
        textposition="middle center",
        textfont=dict(color="white", size=16),
        marker=dict(line=dict(color='#0e1117', width=2)) 
    )
    
    fig.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)
