import streamlit as st
import yfinance as yf
from datetime import datetime
import streamlit.components.v1 as components

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
        
        # HTML 텍스트 조립 (영문 아래 한글 추가)
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

# 3. 완벽하게 격리된 HTML/CSS/JS 코드 생성
full_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{
        margin: 0;
        padding: 0;
        background-color: #0e1117;
        font-family: -apple-system, BlinkMacSystemFont, "Trebuchet MS", Roboto, sans-serif;
    }}
    .ticker-container {{
        width: 100%;
        overflow: hidden;
        background-color: #131722; 
        padding: 12px 0;
        border-top: 1px solid #2a2e39;
        border-bottom: 1px solid #2a2e39;
    }}
    .ticker-track {{
        display: flex;
        white-space: nowrap;
        width: max-content;
        animation: scroll 45s linear infinite;
    }}
    /* 마우스 호버 시 일시 정지 */
    .ticker-container:hover .ticker-track {{
        animation-play-state: paused;
        cursor: pointer;
    }}
    .ticker-card {{
        display: inline-flex;
        align-items: center;
        padding: 0 35px;
        border-right: 1px solid #2a2e39;
    }}
    /* 종목 이름 래퍼 (영문/한글 세로 배치) */
    .symbol-info {{
        display: flex;
        flex-direction: column;
        margin-right: 15px;
        justify-content: center;
    }}
    .symbol-name {{
        font-weight: 800;
        font-size: 1.0rem;
        color: #ffffff;
        line-height: 1.2;
    }}
    .symbol-ko {{
        font-weight: 500;
        font-size: 0.75rem;
        color: #8b92a5; /* 한글은 은은한 회색으로 처리 */
        line-height: 1.2;
        margin-top: 3px;
    }}
    .current-price {{
        font-weight: 700;
        font-size: 1.1rem;
        color: #d1d4dc;
        margin-right: 12px;
    }}
    .price-change {{
        font-weight: 600;
        font-size: 1.0rem;
    }}
    /* 한국 시장 표준 색상 명확하게 적용 (!important 추가) */
    .up {{ color: #ff4b4b !important; }}    /* 상승: 뚜렷한 빨간색 */
    .down {{ color: #3b82f6 !important; }}  /* 하락: 뚜렷한 파란색 */
    
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

# 4. 위아래 글씨가 잘리지 않도록 높이를 75로 설정
components.html(full_html, height=75)

import os
import pandas as pd

# --- 여기서부터 기존 티커 코드 아래에 추가하세요 ---

st.markdown("<br><br>", unsafe_allow_html=True)
st.subheader("📔 PROJECT 2043 : 연기금 운용일지")

# 1. 데이터베이스 파일 설정 (csv로 저장하여 데이터 영구 보존)
DB_FILE = "journal_db.csv"

# 초기 데이터 로드 또는 생성
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    # 올려주신 노션 이미지와 동일한 컬럼 구성
    initial_data = pd.DataFrame({
        '날짜': ['2026-02-28'],
        '생각 (제목)': ['삼성전자와 SK하이닉스 매수 분석한다'],
        '코스피': [6244.13],
        '코스닥': [1192.78],
        '환율(달러/원)': [1445.00],
        '미국 국채 10년': [3.9490],
        '국제금': [5247.90],
        '삼성전자': [216500],
        'SK하이닉스': [1061000],
        '상세분석': ['여기에 오늘의 시황 분석 내용을 상세히 적습니다.']
    })
    initial_data.to_csv(DB_FILE, index=False)
    df = initial_data

# 2. 노션 스타일 데이터베이스 출력 (Data Editor)
st.write("요약 뷰 (더블 클릭하여 바로 수정 가능합니다)")
edited_df = st.data_editor(
    df.drop(columns=['상세분석']), # 표에서는 상세내용 숨김
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic" # 표에서 바로 행 추가/삭제 가능
)

# 표에서 수정한 내용이 있으면 CSV 파일에 자동 업데이트
if not edited_df.equals(df.drop(columns=['상세분석'])):
    df.update(edited_df)
    df.to_csv(DB_FILE, index=False)

st.divider()

# 3. 상세 시황 분석 (터치해서 들어가는 효과)
st.subheader("📝 상세 시황 분석 작성")

col1, col2 = st.columns([1, 2])

with col1:
    # 작성된 날짜 목록 불러오기
    date_list = df['날짜'].tolist()
    selected_date = st.selectbox("분석을 보거나 작성할 날짜를 선택하세요", ["새로 작성하기 ➕"] + date_list)

with col2:
    if selected_date == "새로 작성하기 ➕":
        with st.form("new_entry_form"):
            new_date = st.date_input("날짜").strftime("%Y-%m-%d")
            new_title = st.text_input("생각 (제목)")
            
            # 입력 폼 (2칸으로 나누어 깔끔하게 배치)
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                new_kospi = st.number_input("코스피", value=0.0)
                new_kosdaq = st.number_input("코스닥", value=0.0)
                new_usd = st.number_input("환율(달러/원)", value=0.0)
                new_sam = st.number_input("삼성전자", value=0)
            with f_col2:
                new_bond = st.number_input("미국 국채 10년", value=0.0)
                new_gold = st.number_input("국제금", value=0.0)
                new_hynix = st.number_input("SK하이닉스", value=0)
            
            new_detail = st.text_area("오늘의 시황 분석을 자유롭게 적어주세요", height=200)
            submit_btn = st.form_submit_button("일지 저장하기")
            
            if submit_btn:
                # 새 데이터 추가
                new_row = pd.DataFrame([{
                    '날짜': new_date, '생각 (제목)': new_title, '코스피': new_kospi, 
                    '코스닥': new_kosdaq, '환율(달러/원)': new_usd, '미국 국채 10년': new_bond,
                    '국제금': new_gold, '삼성전자': new_sam, 'SK하이닉스': new_hynix, '상세분석': new_detail
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success("저장되었습니다! 화면을 새로고침 해주세요.")
    
    else:
        # 선택한 날짜의 상세 데이터 보여주기 (터치해서 들어간 화면)
        selected_row = df[df['날짜'] == selected_date].iloc[0]
        st.info(f"**{selected_row['생각 (제목)']}**")
        
        # 상세 분석 내용 수정 기능
        updated_detail = st.text_area("시황 분석 (수정 가능)", value=selected_row['상세분석'], height=250)
        if st.button("분석 내용 업데이트"):
            df.loc[df['날짜'] == selected_date, '상세분석'] = updated_detail
            df.to_csv(DB_FILE, index=False)
            st.success("수정 완료되었습니다!")

# 업데이트 시간 표시
st.caption(f"Last Synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

