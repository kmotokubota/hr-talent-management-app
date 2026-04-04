"""
Page 1: Dashboard - KPI summary, announcements, recent appointments
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import run_query, DB, SCHEMA, importance_dot

st.title("ダッシュボード")
st.markdown('<div class="section-header">社内情報の見える化</div>', unsafe_allow_html=True)

# ── KPI Row ──────────────────────────────────────────────────────────────────
kpi_df = run_query(f"""
    SELECT
        COUNT(*)                       AS TOTAL_EMP,
        ROUND(AVG(PERFORMANCE_SCORE),2) AS AVG_PERF,
        ROUND(AVG(ENGAGEMENT_SCORE),1)  AS AVG_ENG
    FROM {DB}.{SCHEMA}.EMPLOYEES
    WHERE IS_ACTIVE = TRUE
""")

appt_df = run_query(f"""
    SELECT COUNT(*) AS MONTHLY_APT
    FROM {DB}.{SCHEMA}.APPOINTMENTS
    WHERE APPOINTMENT_DATE >= DATEADD('day', -30, CURRENT_DATE())
""")

total_emp   = int(kpi_df["TOTAL_EMP"].iloc[0])
avg_perf    = float(kpi_df["AVG_PERF"].iloc[0])
avg_eng     = float(kpi_df["AVG_ENG"].iloc[0])
monthly_apt = int(appt_df["MONTHLY_APT"].iloc[0])

c1, c2, c3, c4 = st.columns(4)
for col, label, value, delta in [
    (c1, "総従業員数",       f"{total_emp:,} 名", None),
    (c2, "今月の発令件数",   f"{monthly_apt} 件", None),
    (c3, "平均評価スコア",   f"{avg_perf}",        "/ 5.0"),
    (c4, "平均エンゲージメント", f"{avg_eng}",     "/ 100"),
]:
    with col:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">{label}</div>'
            f'<div class="value">{value}</div>'
            f'<div class="delta">{delta or ""}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row ───────────────────────────────────────────────────────────────
col_chart, col_gender = st.columns([2, 1])

with col_chart:
    st.markdown('<div class="section-header">本部別人員構成</div>', unsafe_allow_html=True)
    dept_df = run_query(f"""
        SELECT
            d.DEPARTMENT_NAME,
            SUM(CASE WHEN e.GENDER = '男性' THEN 1 ELSE 0 END) AS MALE,
            SUM(CASE WHEN e.GENDER = '女性' THEN 1 ELSE 0 END) AS FEMALE,
            COUNT(*) AS TOTAL
        FROM {DB}.{SCHEMA}.EMPLOYEES e
        JOIN {DB}.{SCHEMA}.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
        WHERE e.IS_ACTIVE = TRUE AND d.DEPT_LEVEL = 2
        GROUP BY d.DEPARTMENT_NAME
        ORDER BY TOTAL DESC
        LIMIT 15
    """)
    if not dept_df.empty:
        fig = go.Figure()
        fig.add_bar(
            y=dept_df["DEPARTMENT_NAME"], x=dept_df["MALE"],
            name="男性", orientation="h", marker_color="#2563eb",
        )
        fig.add_bar(
            y=dept_df["DEPARTMENT_NAME"], x=dept_df["FEMALE"],
            name="女性", orientation="h", marker_color="#ec4899",
        )
        fig.update_layout(
            barmode="stack", height=420,
            margin=dict(l=0, r=0, t=20, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig, use_container_width=True)

with col_gender:
    st.markdown('<div class="section-header">男女比</div>', unsafe_allow_html=True)
    gen_df = run_query(f"""
        SELECT GENDER, COUNT(*) AS CNT
        FROM {DB}.{SCHEMA}.EMPLOYEES
        WHERE IS_ACTIVE = TRUE
        GROUP BY GENDER
    """)
    if not gen_df.empty:
        fig2 = px.pie(
            gen_df, values="CNT", names="GENDER",
            color_discrete_sequence=["#2563eb", "#ec4899"],
            hole=0.4,
        )
        fig2.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=0),
                           showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-header">雇用形態</div>', unsafe_allow_html=True)
    emp_type_df = run_query(f"""
        SELECT EMPLOYEE_TYPE, COUNT(*) AS CNT
        FROM {DB}.{SCHEMA}.EMPLOYEES WHERE IS_ACTIVE = TRUE
        GROUP BY EMPLOYEE_TYPE ORDER BY CNT DESC
    """)
    if not emp_type_df.empty:
        fig3 = px.pie(
            emp_type_df, values="CNT", names="EMPLOYEE_TYPE",
            color_discrete_sequence=["#2563eb","#7c3aed","#94a3b8"],
            hole=0.4,
        )
        fig3.update_layout(height=200, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig3, use_container_width=True)

# ── Announcements ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">お知らせ</div>', unsafe_allow_html=True)

cat_options = ["すべて", "発令", "制度変更", "人事お知らせ", "研修", "全社連絡"]
selected_cat = st.selectbox("カテゴリフィルタ", cat_options, label_visibility="collapsed")
cat_filter = "" if selected_cat == "すべて" else f"AND CATEGORY = '{selected_cat}'"

ann_df = run_query(f"""
    SELECT ANNOUNCEMENT_ID, TITLE, CONTENT, CATEGORY, IMPORTANCE,
           AUTHOR, PUBLISH_DATE, IS_PINNED
    FROM {DB}.{SCHEMA}.ANNOUNCEMENTS
    WHERE 1=1 {cat_filter}
    ORDER BY IS_PINNED DESC, PUBLISH_DATE DESC
    LIMIT 10
""")

for _, row in ann_df.iterrows():
    pinned_cls = "pinned" if row["IS_PINNED"] else ""
    imp_cls    = "high"   if row["IMPORTANCE"] == "高" else ""
    card_cls   = f"announcement-card {pinned_cls} {imp_cls}".strip()
    pin_icon   = "📌 " if row["IS_PINNED"] else ""
    imp_html   = importance_dot(row["IMPORTANCE"])
    st.markdown(
        f'<div class="{card_cls}">'
        f'<strong>{pin_icon}{row["TITLE"]}</strong>'
        f'&nbsp;&nbsp;{imp_html}'
        f'<div style="font-size:12px;color:#64748b;margin-top:4px">'
        f'{row["CATEGORY"]} | {row["AUTHOR"]} | {row["PUBLISH_DATE"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    with st.expander("詳細を見る", expanded=False):
        st.write(row["CONTENT"])

# ── Recent appointments ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">直近の発令情報（30日）</div>',
            unsafe_allow_html=True)

recent_df = run_query(f"""
    SELECT
        a.APPOINTMENT_DATE,
        e.EMPLOYEE_NAME,
        a.APPOINTMENT_TYPE,
        d1.DEPARTMENT_NAME AS FROM_DEPT,
        d2.DEPARTMENT_NAME AS TO_DEPT,
        p1.POSITION_NAME   AS FROM_POS,
        p2.POSITION_NAME   AS TO_POS
    FROM {DB}.{SCHEMA}.APPOINTMENTS a
    JOIN {DB}.{SCHEMA}.EMPLOYEES   e  ON a.EMPLOYEE_ID        = e.EMPLOYEE_ID
    LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d1 ON a.FROM_DEPARTMENT_ID = d1.DEPARTMENT_ID
    LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d2 ON a.TO_DEPARTMENT_ID   = d2.DEPARTMENT_ID
    LEFT JOIN {DB}.{SCHEMA}.POSITIONS   p1 ON a.FROM_POSITION_ID   = p1.POSITION_ID
    LEFT JOIN {DB}.{SCHEMA}.POSITIONS   p2 ON a.TO_POSITION_ID     = p2.POSITION_ID
    WHERE a.APPOINTMENT_DATE >= DATEADD('day', -30, CURRENT_DATE())
    ORDER BY a.APPOINTMENT_DATE DESC
    LIMIT 50
""")

if recent_df.empty:
    st.info("直近30日間の発令はありません。")
else:
    st.dataframe(
        recent_df.rename(columns={
            "APPOINTMENT_DATE": "発令日",
            "EMPLOYEE_NAME": "氏名",
            "APPOINTMENT_TYPE": "発令種別",
            "FROM_DEPT": "旧所属",
            "TO_DEPT": "新所属",
            "FROM_POS": "旧職位",
            "TO_POS": "新職位",
        }),
        use_container_width=True,
        hide_index=True,
    )
