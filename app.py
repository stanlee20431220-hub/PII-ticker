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

# ==========================================
# 3. 주요 지표 스파크라인 차트
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
            
            area = base_chart.mark_area(
                line={'color': 'transparent'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color=color_hex, offset=0), 
                           alt.GradientStop(color='rgba(0,0,0,0)', offset=1)],
                    x1=1, x2=1, y1=1, y2=0
                )
            ).encode(y2=alt.datum(bottom_val))
            
            st.altair_chart(area + line, use_container_width=True)

# ==========================================
# 4. 하이브리드 시장 히트맵 (미국: TV / 한국: Custom)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🗺️ 시장 히트맵 (Market Heatmap)")

tab1, tab2 = st.tabs(["🇺🇸 S&P 500 (미국)", "🇰🇷 국내 주요 섹터 (한국)"])

with tab1:
    # 🇺🇸 미국 시장은 완벽한 트레이딩뷰 위젯 사용
    sp500_html = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
      {
        "exchanges": [],
        "dataSource": "SPX500",
        "grouping": "sector",
        "blockSize": "market_cap_basic",
        "blockColor": "change",
        "locale": "kr",
        "symbolUrl": "",
        "colorTheme": "dark",
        "hasTopBar": true,
        "isTransparent": true,
        "width": "100%",
        "height": "600"
      }
      </script>
    </div>
    """
    components.html(sp500_html, height=600)

with tab2:
    # 🇰🇷 한국 시장: 네이버 금융 시가총액 TOP 10 섹터 기준 빽빽한 커스텀 구성
    @st.cache_data(ttl=600)
    def get_korea_dense_heatmap():
        # 네이버 금융 TOP 10 섹터와 각 섹터별 대표 우량주 매핑
        portfolio = {
            "반도체와반도체장비": {"삼성전자": "005930.KS", "SK하이닉스": "000660.KS", "한미반도체": "042700.KS", "리노공업": "058470.KQ"},
            "제약": {"삼성바이오로직스": "207940.KS", "셀트리온": "068270.KS", "유한양행": "000100.KS", "한미약품": "128940.KS"},
            "자동차": {"현대차": "005380.KS", "기아": "000270.KS", "현대모비스": "012330.KS"},
            "복합기업": {"삼성물산": "028260.KS", "SK": "034730.KS", "LG": "003550.KS", "CJ": "001040.KS"},
            "은행": {"KB금융": "105560.KS", "신한지주": "055550.KS", "하나금융지주": "086790.KS", "우리금융지주": "316140.KS"},
            "조선": {"HD한국조선해양": "009540.KS", "삼성중공업": "010140.KS", "한화오션": "042660.KS", "HD현대중공업": "329180.KS"},
            "전기제품": {"LG에너지솔루션": "373220.KS", "삼성SDI": "006400.KS", "에코프로비엠": "247540.KQ", "엘앤에프": "066970.KS"},
            "우주항공과국방": {"한화에어로스페이스": "012450.KS", "한국항공우주": "047810.KS", "LIG넥스원": "079550.KS", "현대로템": "064350.KS"},
            "기계": {"두산에너빌리티": "034020.KS", "HD현대일렉트릭": "267260.KS", "LS ELECTRIC": "010120.KS"},
            "증권": {"미래에셋증권": "006800.KS", "한국금융지주": "071050.KS", "NH투자증권": "005940.KS", "삼성증권": "016360.KS"}
        }
        data = []
        for sector, stocks in portfolio.items():
            for name, ticker in stocks.items():
                try:
                    info = yf.Ticker(ticker).fast_info
                    mcap = info['market_cap']
                    price = info['last_price']
                    prev = info['previous_close']
                    pct = ((price - prev) / prev) * 100
                    data.append({
                        "섹터": sector, "종목명": name, "시가총액": mcap, "등락률": pct,
                        "텍스트표시": f"<b>{name}</b><br>{pct:+.2f}%"
                    })
                except:
                    continue
        return pd.DataFrame(data)

    with st.spinner("한국 시장 데이터를 불러오는 중입니다... (약 10초 소요)"):
        heatmap_df = get_korea_dense_heatmap()

    if not heatmap_df.empty:
        fig = px.treemap(
            heatmap_df,
            path=[px.Constant("한국 TOP 10 섹터"), '섹터', '종목명'], 
            values='시가총액', 
            color='등락률',   
            color_continuous_scale=[[0, '#3b82f6'], [0.5, '#131722'], [1, '#ff4b4b']], # 파랑-검정-빨강
            color_continuous_midpoint=0,
            custom_data=['텍스트표시']
        )
        
        # 디자인 튜닝: 테두리를 얇게 하고 여백을 없애 빽빽하게 만듦
        fig.update_traces(
            texttemplate="%{customdata[0]}",
            textposition="middle center",
            textfont=dict(color="white", size=13),
            marker=dict(line=dict(color='#0e1117', width=1)),
            hovertemplate="<b>%{label}</b><br>등락률: %{color:+.2f}%<br>시가총액: %{value:,.0f}<extra></embed>"
        )
        
        fig.update_layout(
            margin=dict(t=30, l=0, r=0, b=0), # 상단 여백만 살짝 남김
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            height=650,
            coloraxis_showscale=False # 컬러바 숨김
        )
        st.plotly_chart(fig, use_container_width=True)
