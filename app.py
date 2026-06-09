import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
import calendar

# ── 페이지 설정 ───────────────────────────────────────────────────
st.set_page_config(
    page_title="한솔 다골프 회원권 관리",
    page_icon="⛳",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }

.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    border: 1px solid #e8ecf0;
    height: 100%;
}
.kpi-title { font-size: 13px; font-weight: 600; color: #64748b; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.kpi-main { font-size: 32px; font-weight: 700; color: #1e293b; line-height: 1; margin-bottom: 4px; }
.kpi-sub { font-size: 13px; color: #94a3b8; margin-bottom: 12px; }
.progress-bar-bg { background: #f1f5f9; border-radius: 6px; height: 8px; overflow: hidden; margin-bottom: 6px; }
.progress-bar-fill { height: 8px; border-radius: 6px; transition: width 0.4s; }
.progress-blue { background: #3b82f6; }
.progress-orange { background: #f59e0b; }
.progress-red { background: #ef4444; }
.kpi-row { display: flex; justify-content: space-between; font-size: 12px; color: #94a3b8; }

.badge {
    display: inline-block; padding: 2px 8px; border-radius: 10px;
    font-size: 11px; font-weight: 600;
}
.badge-blue { background: #dbeafe; color: #1d4ed8; }
.badge-purple { background: #ede9fe; color: #6d28d9; }
.badge-gray { background: #f1f5f9; color: #64748b; }
.badge-green { background: #dcfce7; color: #16a34a; }
.badge-orange { background: #fff7ed; color: #c2410c; }
.badge-red { background: #fee2e2; color: #dc2626; }

.section-title { font-size: 15px; font-weight: 700; color: #1e293b; margin: 16px 0 8px 0; }

.cal-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
.cal-header { text-align: center; font-size: 12px; font-weight: 600; color: #64748b; padding: 4px; }
.cal-day { background: #f8fafc; border-radius: 8px; padding: 6px 4px; min-height: 56px; font-size: 12px; }
.cal-day-num { font-weight: 600; color: #374151; margin-bottom: 2px; }
.cal-today .cal-day-num { color: #2563eb; }
.cal-weekend { background: #fefce8; }
.cal-other { opacity: 0.3; }
.cal-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin: 1px; }
.dot-used { background: #94a3b8; }
.dot-confirmed { background: #3b82f6; }
.dot-pending { background: #a855f7; }
.dot-event { background: #f59e0b; }
</style>
""", unsafe_allow_html=True)

# ── 초기 데이터 ───────────────────────────────────────────────────
BOOKINGS_INIT = [
    {"id": 1,  "date": "2026-06-14", "executive": "-", "type": "event",   "status": "confirmed", "credit": 2},
    {"id": 2,  "date": "2026-06-21", "executive": "김명산", "type": "general", "status": "pending",   "credit": 2},
    {"id": 3,  "date": "2026-06-06", "executive": "김태수", "type": "general", "status": "confirmed", "credit": 2},
    {"id": 4,  "date": "2026-06-03", "executive": "곽상효", "type": "general", "status": "used",      "credit": 1},
    {"id": 5,  "date": "2026-05-24", "executive": "-",    "type": "event",   "status": "used",      "credit": 2},
    {"id": 6,  "date": "2026-05-24", "executive": "김명산", "type": "general", "status": "used",      "credit": 2},
    {"id": 7,  "date": "2026-05-16", "executive": "김명산", "type": "general", "status": "used",      "credit": 2},
    {"id": 8,  "date": "2026-05-09", "executive": "곽상효", "type": "general", "status": "used",      "credit": 2},
    {"id": 9,  "date": "2026-05-05", "executive": "-",    "type": "event",   "status": "used",      "credit": 2},
    {"id": 10, "date": "2026-04-28", "executive": "-",    "type": "event",   "status": "used",      "credit": 2},
    {"id": 11, "date": "2026-04-25", "executive": "-",    "type": "event",   "status": "used",      "credit": 2},
    {"id": 12, "date": "2026-04-17", "executive": "김명산", "type": "general", "status": "used",      "credit": 1},
    {"id": 13, "date": "2026-04-11", "executive": "정용혁", "type": "general", "status": "used",      "credit": 2},
    {"id": 14, "date": "2026-04-05", "executive": "곽상효", "type": "general", "status": "used",      "credit": 2},
    {"id": 15, "date": "2026-04-04", "executive": "-",    "type": "event",   "status": "used",      "credit": 2},
    {"id": 16, "date": "2026-04-04", "executive": "-",    "type": "event",   "status": "used",      "credit": 2},
    {"id": 17, "date": "2026-03-29", "executive": "-",    "type": "event",   "status": "used",      "credit": 2},
    {"id": 18, "date": "2026-03-22", "executive": "정용혁", "type": "general", "status": "used",      "credit": 2},
    {"id": 19, "date": "2026-03-21", "executive": "곽상효", "type": "general", "status": "used",      "credit": 2},
    {"id": 20, "date": "2026-03-07", "executive": "김명산", "type": "general", "status": "used",      "credit": 2},
    {"id": 21, "date": "2026-03-02", "executive": "김태수", "type": "general", "status": "used",      "credit": 1},
    {"id": 22, "date": "2026-02-21", "executive": "곽상효", "type": "general", "status": "used",      "credit": 2},
    {"id": 23, "date": "2026-02-14", "executive": "정용혁", "type": "general", "status": "used",      "credit": 2},
]

HIST25_INIT = [
    {"date": "2025-12-21", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-12-06", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-11-29", "executive": "-",    "type": "event",   "status": "used", "credit": 2},
    {"date": "2025-11-23", "executive": "김태수", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-11-01", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-10-19", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-10-11", "executive": "이해성", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-10-10", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-10-02", "executive": "김태수", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-09-27", "executive": "이해성", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-09-14", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-09-07", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-08-31", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-08-09", "executive": "김태수", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-08-02", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-07-19", "executive": "-",    "type": "event",   "status": "used", "credit": 2},
    {"date": "2025-07-19", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-07-13", "executive": "김태수", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-07-12", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-06-21", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-06-14", "executive": "곽상효", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-06-13", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-06-05", "executive": "김태수", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-05-25", "executive": "이상훈", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-05-23", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-05-17", "executive": "김태수", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-05-10", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-04-20", "executive": "김태수", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-04-13", "executive": "이해성", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-04-12", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-03-23", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-03-15", "executive": "이해성", "type": "general", "status": "used", "credit": 2},
    {"date": "2025-03-01", "executive": "정용혁", "type": "general", "status": "used", "credit": 2},
]

ANNUAL_TOTAL = 80

# ── 세션 상태 초기화 ───────────────────────────────────────────────
if "bookings" not in st.session_state:
    st.session_state.bookings = [dict(b) for b in BOOKINGS_INIT]
if "executives" not in st.session_state:
    st.session_state.executives = ["곽상효", "김명산", "정용혁", "김태수", "이해성", "이상훈"]
if "next_id" not in st.session_state:
    st.session_state.next_id = 24

# ── 헬퍼 함수 ─────────────────────────────────────────────────────
def is_weekend(d: date) -> bool:
    return d.weekday() >= 5  # 토=5, 일=6

def calc_credit(d: date, btype: str) -> int:
    if btype == "event":
        return 2
    return 2 if is_weekend(d) else 1

def get_df() -> pd.DataFrame:
    df = pd.DataFrame(st.session_state.bookings)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

def status_badge(status: str) -> str:
    mapping = {
        "used":      ('<span class="badge badge-gray">사용완료</span>', "사용완료"),
        "confirmed": ('<span class="badge badge-blue">예약확정</span>', "예약확정"),
        "pending":   ('<span class="badge badge-purple">미확정</span>',  "미확정"),
        "hope":      ('<span class="badge badge-gray">희망</span>',      "희망"),
    }
    return mapping.get(status, (status, status))

def type_label(t: str) -> str:
    return "이벤트" if t == "event" else "일반"

# ── KPI 계산 ───────────────────────────────────────────────────────
def compute_kpi():
    df = get_df()
    today = date.today()

    annual_used = int(df["credit"].sum())
    annual_pct = annual_used / ANNUAL_TOTAL * 100

    def month_stats(y, m):
        mdf = df[(df["date"].apply(lambda d: d.year == y and d.month == m))]
        weekday_cnt = int(mdf[(mdf["type"] == "general") & (~mdf["date"].apply(is_weekend))].shape[0])
        weekend_cnt = int(mdf[(mdf["type"] == "general") & (mdf["date"].apply(is_weekend))].shape[0])
        sat_cnt = int(mdf[mdf["date"].apply(lambda d: d.weekday() == 5)].shape[0])
        event_cnt = int(mdf[mdf["type"] == "event"].shape[0])
        return weekday_cnt, weekend_cnt, sat_cnt, event_cnt

    this_wd, this_we, this_sat, this_ev = month_stats(today.year, today.month)
    nm = today.replace(day=1) + timedelta(days=32)
    next_wd, next_we, next_sat, next_ev = month_stats(nm.year, nm.month)

    return {
        "annual_used": annual_used,
        "annual_pct": annual_pct,
        "this": {"wd": this_wd, "we": this_we, "sat": this_sat, "ev": this_ev,
                 "y": today.year, "m": today.month},
        "next": {"wd": next_wd, "we": next_we, "sat": next_sat, "ev": next_ev,
                 "y": nm.year, "m": nm.month},
    }

# ── 헤더 ──────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex; align-items:center; gap:12px; margin-bottom:24px;">
  <div style="font-size:28px;">⛳</div>
  <div>
    <div style="font-size:22px; font-weight:800; color:#1e293b;">한솔 다골프 회원권 관리</div>
    <div style="font-size:13px; color:#94a3b8;">골프 회원권 예약 및 크레딧 현황</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI 카드 ──────────────────────────────────────────────────────
kpi = compute_kpi()
c1, c2, c3 = st.columns(3)

with c1:
    pct = kpi["annual_pct"]
    bar_cls = "progress-red" if pct >= 90 else "progress-orange" if pct >= 70 else "progress-blue"
    remaining = ANNUAL_TOTAL - kpi["annual_used"]
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-title">연간 크레딧 ({date.today().year}년)</div>
      <div class="kpi-main">{kpi["annual_used"]} <span style="font-size:16px;color:#94a3b8;">/ {ANNUAL_TOTAL} cr</span></div>
      <div class="kpi-sub">잔여 {remaining} cr</div>
      <div class="progress-bar-bg"><div class="progress-bar-fill {bar_cls}" style="width:{min(pct,100):.1f}%"></div></div>
      <div class="kpi-row"><span>0 cr</span><span style="font-weight:600;color:#374151;">{pct:.1f}% 사용</span><span>{ANNUAL_TOTAL} cr</span></div>
    </div>
    """, unsafe_allow_html=True)

def month_card(info, label):
    we_pct = info["we"] / 3 * 100
    sat_pct = info["sat"] / 2 * 100
    we_cls = "progress-red" if info["we"] >= 3 else "progress-orange" if info["we"] >= 2 else "progress-blue"
    sat_cls = "progress-red" if info["sat"] >= 2 else "progress-blue"
    we_badge = "badge-red" if info["we"] >= 3 else "badge-orange" if info["we"] >= 2 else "badge-blue"
    we_text = "한도" if info["we"] >= 3 else "주의" if info["we"] >= 2 else "여유"
    return f"""
    <div class="kpi-card">
      <div class="kpi-title">{label} ({info["m"]}월)</div>
      <div style="margin-bottom:10px;">
        <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
          <span style="color:#64748b;">평일</span><span style="font-weight:600;">{info["wd"]}건</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px;">
          <span style="color:#64748b;">주말 <span class="badge {we_badge}" style="font-size:10px;">{we_text}</span></span>
          <span style="font-weight:600;">{info["we"]} / 3회</span>
        </div>
        <div class="progress-bar-bg"><div class="progress-bar-fill {we_cls}" style="width:{min(we_pct,100):.0f}%"></div></div>
        <div style="display:flex;justify-content:space-between;font-size:13px;margin-top:6px;margin-bottom:4px;">
          <span style="color:#64748b;">└ 토요일</span><span style="font-weight:600;">{info["sat"]} / 2회</span>
        </div>
        <div class="progress-bar-bg"><div class="progress-bar-fill {sat_cls}" style="width:{min(sat_pct,100):.0f}%"></div></div>
        <div style="display:flex;justify-content:space-between;font-size:13px;margin-top:6px;">
          <span style="color:#64748b;">이벤트</span><span style="font-weight:600;">{info["ev"]}건</span>
        </div>
      </div>
    </div>
    """

with c2:
    st.markdown(month_card(kpi["this"], "당월 현황"), unsafe_allow_html=True)
with c3:
    st.markdown(month_card(kpi["next"], "차월 현황"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 탭 ────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📅 예약 관리", "📊 임원별 통계", "📋 2025 이력"])

# ════════════════════════════════════════════════════════
# TAB 1 — 예약 관리
# ════════════════════════════════════════════════════════
with tab1:
    col_form, col_cal = st.columns([1, 1.4], gap="large")

    with col_form:
        st.markdown('<div class="section-title">예약 추가</div>', unsafe_allow_html=True)
        with st.form("add_booking", clear_on_submit=True):
            sel_date = st.date_input("날짜", value=date.today(), format="YYYY-MM-DD")
            btype = st.selectbox("구분", ["일반", "이벤트"])
            btype_val = "general" if btype == "일반" else "event"

            exec_options = st.session_state.executives
            if btype_val == "event":
                executive = "-"
                st.info("이벤트 예약은 임원을 지정하지 않습니다.")
            else:
                executive = st.selectbox("담당 임원", exec_options)

            auto_credit = calc_credit(sel_date, btype_val)
            day_name = ["월", "화", "수", "목", "금", "토", "일"][sel_date.weekday()]
            st.info(f"선택일: {sel_date} ({day_name}) — 크레딧: **{auto_credit} cr**")

            status_opts = {"예약(확정)": "confirmed", "예약(미확정)": "pending", "희망": "hope"}
            status_label = st.selectbox("상태", list(status_opts.keys()))
            status_val = status_opts[status_label]
            if sel_date < date.today():
                status_val = "used"
                st.warning("과거 날짜는 자동으로 '사용완료' 처리됩니다.")

            submitted = st.form_submit_button("예약 추가", use_container_width=True, type="primary")
            if submitted:
                # 주말 한도 체크
                df = get_df()
                today = date.today()
                mdf = df[(df["date"].apply(lambda d: d.year == sel_date.year and d.month == sel_date.month))]
                we_cnt = int(mdf[(mdf["type"] == "general") & (mdf["date"].apply(is_weekend))].shape[0])
                sat_cnt = int(mdf[mdf["date"].apply(lambda d: d.weekday() == 5)].shape[0])

                error = None
                if btype_val == "general" and is_weekend(sel_date):
                    if we_cnt >= 3:
                        error = f"{sel_date.month}월 주말 한도(3회)를 초과합니다."
                    elif sel_date.weekday() == 5 and sat_cnt >= 2:
                        error = f"{sel_date.month}월 토요일 한도(2회)를 초과합니다."

                if error:
                    st.error(error)
                else:
                    new_booking = {
                        "id": st.session_state.next_id,
                        "date": sel_date.strftime("%Y-%m-%d"),
                        "executive": executive,
                        "type": btype_val,
                        "status": status_val,
                        "credit": auto_credit,
                    }
                    st.session_state.bookings.append(new_booking)
                    st.session_state.next_id += 1
                    st.success("예약이 추가되었습니다.")
                    st.rerun()

    with col_cal:
        st.markdown('<div class="section-title">월별 캘린더</div>', unsafe_allow_html=True)
        today = date.today()

        if "cal_year" not in st.session_state:
            st.session_state.cal_year = today.year
        if "cal_month" not in st.session_state:
            st.session_state.cal_month = today.month

        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.button("◀", key="prev_month"):
                m = st.session_state.cal_month - 1
                if m < 1:
                    m = 12
                    st.session_state.cal_year -= 1
                st.session_state.cal_month = m
                st.rerun()
        with nav2:
            st.markdown(f"<div style='text-align:center;font-weight:700;font-size:16px;padding:6px 0'>{st.session_state.cal_year}년 {st.session_state.cal_month}월</div>", unsafe_allow_html=True)
        with nav3:
            if st.button("▶", key="next_month"):
                m = st.session_state.cal_month + 1
                if m > 12:
                    m = 1
                    st.session_state.cal_year += 1
                st.session_state.cal_month = m
                st.rerun()

        cy, cm = st.session_state.cal_year, st.session_state.cal_month
        df = get_df()
        month_bookings = df[(df["date"].apply(lambda d: d.year == cy and d.month == cm))]

        cal_matrix = calendar.monthcalendar(cy, cm)
        days_header = ["월", "화", "수", "목", "금", "토", "일"]

        header_html = "".join(f'<div class="cal-header" style="color:{"#ef4444" if i>=5 else "#64748b"}">{d}</div>' for i, d in enumerate(days_header))

        cells_html = ""
        for week in cal_matrix:
            for i, day in enumerate(week):
                if day == 0:
                    cells_html += '<div class="cal-day cal-other"></div>'
                    continue
                d = date(cy, cm, day)
                is_we = i >= 5
                is_tod = d == today
                cls = "cal-day"
                if is_we:
                    cls += " cal-weekend"
                if is_tod:
                    cls += " cal-today"

                day_bks = month_bookings[month_bookings["date"] == d]
                dots = ""
                for _, row in day_bks.iterrows():
                    dot_cls = "dot-event" if row["type"] == "event" else f"dot-{row['status']}"
                    exec_name = row["executive"]
                    dots += f'<span class="cal-dot {dot_cls}" title="{exec_name}"></span>'

                cells_html += f'<div class="{cls}"><div class="cal-day-num">{day}</div>{dots}</div>'

        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:16px;border:1px solid #e8ecf0;">
          <div class="cal-grid">{header_html}</div>
          <div class="cal-grid" style="margin-top:4px;">{cells_html}</div>
          <div style="margin-top:12px;display:flex;gap:12px;flex-wrap:wrap;font-size:12px;color:#64748b;">
            <span><span class="cal-dot dot-confirmed"></span> 예약확정</span>
            <span><span class="cal-dot dot-pending"></span> 미확정</span>
            <span><span class="cal-dot dot-used"></span> 사용완료</span>
            <span><span class="cal-dot dot-event"></span> 이벤트</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 예약 목록
    st.markdown('<div class="section-title">예약 목록</div>', unsafe_allow_html=True)
    df = get_df().sort_values("date", ascending=False)

    show_past = st.checkbox("과거 사용 이력 포함", value=False)
    today = date.today()
    if not show_past:
        display_df = df[df["date"] >= today]
    else:
        display_df = df

    if display_df.empty:
        st.info("표시할 예약이 없습니다.")
    else:
        for _, row in display_df.iterrows():
            d = row["date"]
            day_name = ["월", "화", "수", "목", "금", "토", "일"][d.weekday()]
            is_we_day = d.weekday() >= 5
            badge_html, badge_text = status_badge(row["status"])
            exec_disp = row["executive"] if row["executive"] != "-" else "—"

            cols = st.columns([2, 1.5, 1, 1.5, 0.8, 1, 1])
            with cols[0]:
                color = "#ef4444" if is_we_day else "#374151"
                st.markdown(f'<span style="font-weight:600;color:{color}">{d.strftime("%Y-%m-%d")} ({day_name})</span>', unsafe_allow_html=True)
            with cols[1]:
                st.markdown(exec_disp)
            with cols[2]:
                st.markdown(type_label(row["type"]))
            with cols[3]:
                st.markdown(badge_html, unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f'<span style="font-weight:700;color:#2563eb">{row["credit"]}cr</span>', unsafe_allow_html=True)
            with cols[5]:
                if row["status"] in ("pending", "hope"):
                    if st.button("확정", key=f"confirm_{row['id']}", use_container_width=True):
                        for b in st.session_state.bookings:
                            if b["id"] == row["id"]:
                                b["status"] = "confirmed"
                                break
                        st.rerun()
            with cols[6]:
                if st.button("삭제", key=f"del_{row['id']}", use_container_width=True):
                    st.session_state.bookings = [b for b in st.session_state.bookings if b["id"] != row["id"]]
                    st.rerun()

# ════════════════════════════════════════════════════════
# TAB 2 — 임원별 통계
# ════════════════════════════════════════════════════════
with tab2:
    df = get_df()
    executives = st.session_state.executives

    st.markdown('<div class="section-title">임원별 사용 현황</div>', unsafe_allow_html=True)

    # 임원별 집계
    rows = []
    for exec_name in executives:
        edf = df[(df["executive"] == exec_name) & (df["type"] == "general")]
        wd = int(edf[~edf["date"].apply(is_weekend)].shape[0])
        we = int(edf[edf["date"].apply(is_weekend)].shape[0])
        total_cr = int(edf["credit"].sum())
        rows.append({"임원": exec_name, "평일": wd, "주말": we, "합계 (cr)": total_cr})

    # 이벤트 행
    edf_ev = df[df["type"] == "event"]
    ev_count = int(edf_ev.shape[0])
    ev_cr = int(edf_ev["credit"].sum())
    rows.append({"임원": "이벤트 합계", "평일": "-", "주말": ev_count, "합계 (cr)": ev_cr})

    stat_df = pd.DataFrame(rows)
    max_cr = max([r["합계 (cr)"] for r in rows if isinstance(r["합계 (cr)"], int)] or [1])

    header_cols = st.columns([2, 1, 1, 1.5, 3])
    for h, c in zip(["임원", "평일", "주말", "합계(cr)", "크레딧 비율"], header_cols):
        c.markdown(f'<span style="font-size:12px;font-weight:600;color:#64748b">{h}</span>', unsafe_allow_html=True)
    st.divider()

    for row in rows:
        cols = st.columns([2, 1, 1, 1.5, 3])
        is_event_row = row["임원"] == "이벤트 합계"
        name_style = "color:#f59e0b;font-weight:600" if is_event_row else "font-weight:600"
        cols[0].markdown(f'<span style="{name_style}">{row["임원"]}</span>', unsafe_allow_html=True)
        cols[1].markdown(str(row["평일"]))
        cols[2].markdown(str(row["주말"]))
        cols[3].markdown(f'<span style="font-weight:700;color:#2563eb">{row["합계 (cr)"]} cr</span>', unsafe_allow_html=True)
        if isinstance(row["합계 (cr)"], int) and max_cr > 0:
            cols[4].progress(row["합계 (cr)"] / max_cr)

    st.markdown("<br>", unsafe_allow_html=True)

    # 월별 크레딧 피벗
    st.markdown('<div class="section-title">월별 크레딧 현황 (2026)</div>', unsafe_allow_html=True)
    df26 = df[df["date"].apply(lambda d: d.year == 2026)]
    df26 = df26.copy()
    df26["month"] = df26["date"].apply(lambda d: d.month)
    df26["month_label"] = df26["month"].apply(lambda m: f"{m}월")

    pivot = df26[df26["type"] == "general"].groupby(["executive", "month_label"])["credit"].sum().unstack(fill_value=0)
    month_cols = [f"{m}월" for m in range(1, 13)]
    for mc in month_cols:
        if mc not in pivot.columns:
            pivot[mc] = 0
    pivot = pivot[month_cols]

    if not pivot.empty:
        st.dataframe(pivot, use_container_width=True)
    else:
        st.info("2026년 데이터가 없습니다.")

    st.markdown("<br>", unsafe_allow_html=True)

    # 월별 주말 사용 현황
    st.markdown('<div class="section-title">월별 주말 사용 현황 (2026)</div>', unsafe_allow_html=True)
    we_rows = []
    for m in range(1, 13):
        mdf = df26[df26["month"] == m]
        we = int(mdf[(mdf["type"] == "general") & (mdf["date"].apply(is_weekend))].shape[0])
        sat = int(mdf[mdf["date"].apply(lambda d: d.weekday() == 5)].shape[0])
        sun = int(mdf[mdf["date"].apply(lambda d: d.weekday() == 6)].shape[0])

        we_badge = "🔴 한도" if we >= 3 else "🟡 주의" if we >= 2 else "🟢 여유"
        sat_badge = "🔴 한도" if sat >= 2 else "🟢 여유"

        we_rows.append({
            "월": f"{m}월",
            "주말 합계": f"{we}/3 {we_badge}",
            "토요일": f"{sat}/2 {sat_badge}",
            "일요일": str(sun),
        })

    st.dataframe(pd.DataFrame(we_rows).set_index("월"), use_container_width=True)

# ════════════════════════════════════════════════════════
# TAB 3 — 2025 이력
# ════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">2025년 이용 이력</div>', unsafe_allow_html=True)

    hist_df = pd.DataFrame(HIST25_INIT)
    hist_df["date"] = pd.to_datetime(hist_df["date"]).dt.date
    hist_df = hist_df.sort_values("date", ascending=False)

    display = hist_df.copy()
    display["날짜"] = display["date"].apply(
        lambda d: f"{d.strftime('%Y-%m-%d')} ({['월','화','수','목','금','토','일'][d.weekday()]})"
    )
    display["담당임원"] = display["executive"].apply(lambda x: "—" if x == "-" else x)
    display["구분"] = display["type"].apply(type_label)
    display["크레딧"] = display["credit"].apply(lambda c: f"{c} cr")

    st.dataframe(
        display[["날짜", "담당임원", "구분", "크레딧"]].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
        height=700,
    )
    st.caption(f"총 {len(hist_df)}건 | 합계 {int(hist_df['credit'].sum())} cr")

# ── 관리자 패널 ────────────────────────────────────────────────────
with st.expander("⚙️ 관리자 패널 — 임원 관리"):
    st.markdown("**현재 임원 목록**")

    to_delete = None
    for i, name in enumerate(st.session_state.executives):
        c1, c2 = st.columns([3, 1])
        c1.text(name)
        if c2.button("삭제", key=f"rm_exec_{i}"):
            to_delete = i

    if to_delete is not None:
        removed = st.session_state.executives.pop(to_delete)
        st.success(f"'{removed}' 삭제됨")
        st.rerun()

    st.markdown("**임원 추가**")
    with st.form("add_exec"):
        new_name = st.text_input("임원 이름")
        if st.form_submit_button("추가"):
            if not new_name.strip():
                st.error("이름을 입력하세요.")
            elif new_name.strip() in st.session_state.executives:
                st.error("이미 존재하는 임원입니다.")
            else:
                st.session_state.executives.append(new_name.strip())
                st.success(f"'{new_name.strip()}' 추가됨")
                st.rerun()
