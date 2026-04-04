"""
Page 3: Employee Profile
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import plotly.graph_objects as go
from utils import (
    run_query, DB, SCHEMA, grade_badge, skill_badge,
    avatar_html, tenure_label, perf_color,
)

st.title("従業員プロフィール")

# ── Employee search ───────────────────────────────────────────────────────────
emp_list = run_query(f"""
    SELECT EMPLOYEE_ID, EMPLOYEE_NAME, DEPARTMENT_ID
    FROM {DB}.{SCHEMA}.EMPLOYEES
    WHERE IS_ACTIVE = TRUE
    ORDER BY EMPLOYEE_NAME
""")
emp_opts = {f"{r['EMPLOYEE_NAME']} ({r['EMPLOYEE_ID']})": r["EMPLOYEE_ID"]
            for _, r in emp_list.iterrows()}

# Accept pre-selection from other pages
default_key = None
pre = st.session_state.get("selected_employee_id")
if pre:
    for k, v in emp_opts.items():
        if v == pre:
            default_key = k
            break

sel_label = st.selectbox(
    "従業員を選択 / 検索",
    list(emp_opts.keys()),
    index=list(emp_opts.keys()).index(default_key) if default_key else 0,
)
emp_id = emp_opts[sel_label]

# ── Load employee data ────────────────────────────────────────────────────────
emp = run_query(f"""
    SELECT v.*, d.PARENT_ID,
           dp.DEPARTMENT_NAME AS DIVISION_NAME
    FROM {DB}.{SCHEMA}.V_EMPLOYEE_FULL v
    LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d ON v.DEPARTMENT_ID = d.DEPARTMENT_ID
    LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS dp ON d.PARENT_ID = dp.DEPARTMENT_ID
    WHERE v.EMPLOYEE_ID = '{emp_id}'
""")

if emp.empty:
    st.error("従業員データが見つかりません。")
    st.stop()

e = emp.iloc[0]

# ── Profile header ─────────────────────────────────────────────────────────────
col_av, col_info = st.columns([1, 4])
with col_av:
    st.markdown(avatar_html(e["EMPLOYEE_NAME"], size=80), unsafe_allow_html=True)

with col_info:
    st.markdown(
        f'<div style="margin-left:8px">'
        f'<div style="font-size:24px;font-weight:700;color:#1e293b">{e["EMPLOYEE_NAME"]}</div>'
        f'<div style="color:#64748b;font-size:14px">{e["EMPLOYEE_ID"]}</div>'
        f'<div style="margin-top:6px;font-size:14px">'
        f'{e.get("DIVISION_NAME","") or ""} &gt; {e["DEPARTMENT_NAME"]} &nbsp;|&nbsp; '
        f'{e["POSITION_NAME"]} &nbsp;'
        f'{grade_badge(e["JOB_GRADE"])}'
        f'</div>'
        f'<div style="color:#64748b;font-size:13px;margin-top:4px">'
        f'勤務地: {e["LOCATION"]} &nbsp;|&nbsp; '
        f'入社: {e["HIRE_DATE"]} &nbsp;|&nbsp; '
        f'勤続: {tenure_label(e["TENURE_YEARS"])}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
t1, t2, t3, t4 = st.tabs(["基本情報", "スキル・資格", "発令履歴", "評価スコア"])

# Tab 1: Basic info
with t1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**連絡先・基本情報**")
        info_rows = [
            ("メールアドレス", e["EMAIL"]),
            ("電話番号",       e["PHONE"]),
            ("雇用形態",       e["EMPLOYEE_TYPE"]),
            ("性別",           e["GENDER"]),
            ("生年月日",       str(e["DATE_OF_BIRTH"])),
            ("年齢",           f'{e["AGE"]} 歳'),
            ("上長",           e.get("MANAGER_NAME") or "-"),
        ]
        for label, val in info_rows:
            st.markdown(
                f'<div style="display:flex;gap:12px;padding:6px 0;border-bottom:1px solid #f1f5f9">'
                f'<span style="color:#64748b;width:120px;flex-shrink:0">{label}</span>'
                f'<span style="font-weight:500">{val}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
    with c2:
        st.markdown("**プロフィールサマリー**")
        st.markdown(
            f'<div style="background:#f8fafc;border-radius:8px;padding:16px;'
            f'font-size:14px;line-height:1.7;color:#374151">'
            f'{e.get("PROFILE_SUMMARY","")}</div>',
            unsafe_allow_html=True,
        )

# Tab 2: Skills & certifications
with t2:
    skills_df = run_query(f"""
        SELECT s.SKILL_NAME, s.SKILL_CATEGORY, es.SKILL_LEVEL, es.ACQUIRED_DATE
        FROM {DB}.{SCHEMA}.EMPLOYEE_SKILLS es
        JOIN {DB}.{SCHEMA}.SKILLS s ON es.SKILL_ID = s.SKILL_ID
        WHERE es.EMPLOYEE_ID = '{emp_id}'
        ORDER BY s.SKILL_CATEGORY, s.SKILL_NAME
    """)
    cert_df = run_query(f"""
        SELECT CERTIFICATION_NAME, ISSUER, ACQUIRED_DATE, EXPIRY_DATE
        FROM {DB}.{SCHEMA}.EMPLOYEE_CERTIFICATIONS
        WHERE EMPLOYEE_ID = '{emp_id}'
        ORDER BY ACQUIRED_DATE DESC
    """)

    sc1, sc2 = st.columns([3, 2])
    with sc1:
        st.markdown("**スキルタグ**")
        if skills_df.empty:
            st.info("スキル情報がありません。")
        else:
            badges = " ".join(
                skill_badge(row["SKILL_NAME"], row["SKILL_CATEGORY"])
                for _, row in skills_df.iterrows()
            )
            st.markdown(badges, unsafe_allow_html=True)

            # Radar chart
            st.markdown("<br>**スキルレベル**", unsafe_allow_html=True)
            cats = ["ITスキル","金融スキル","プロジェクト管理","コンプライアンス"]
            scores = []
            for cat in cats:
                cat_skills = skills_df[skills_df["SKILL_CATEGORY"] == cat]
                scores.append(
                    round(cat_skills["SKILL_LEVEL"].mean(), 1)
                    if not cat_skills.empty else 0
                )
            fig = go.Figure(go.Scatterpolar(
                r=scores + [scores[0]],
                theta=cats + [cats[0]],
                fill="toself",
                line_color="#2563eb",
                fillcolor="rgba(37,99,235,0.15)",
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 4])),
                height=280, margin=dict(l=20, r=20, t=20, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

    with sc2:
        st.markdown("**資格一覧**")
        if cert_df.empty:
            st.info("資格情報がありません。")
        else:
            for _, row in cert_df.iterrows():
                exp_str = str(row["EXPIRY_DATE"]) if row["EXPIRY_DATE"] else "期限なし"
                st.markdown(
                    f'<div style="background:#f8fafc;border-radius:6px;padding:10px;'
                    f'margin-bottom:8px;border-left:3px solid #2563eb">'
                    f'<div style="font-weight:600;font-size:13px">{row["CERTIFICATION_NAME"]}</div>'
                    f'<div style="font-size:12px;color:#64748b">{row["ISSUER"]}</div>'
                    f'<div style="font-size:12px;color:#64748b">'
                    f'取得: {row["ACQUIRED_DATE"]} &nbsp;|&nbsp; 有効期限: {exp_str}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

# Tab 3: Appointment history
with t3:
    apt_df = run_query(f"""
        SELECT
            a.APPOINTMENT_DATE, a.APPOINTMENT_TYPE,
            d1.DEPARTMENT_NAME AS FROM_DEPT,
            d2.DEPARTMENT_NAME AS TO_DEPT,
            p1.POSITION_NAME   AS FROM_POS,
            p2.POSITION_NAME   AS TO_POS,
            a.FROM_JOB_GRADE, a.TO_JOB_GRADE,
            a.REASON
        FROM {DB}.{SCHEMA}.APPOINTMENTS a
        LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d1 ON a.FROM_DEPARTMENT_ID = d1.DEPARTMENT_ID
        LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d2 ON a.TO_DEPARTMENT_ID   = d2.DEPARTMENT_ID
        LEFT JOIN {DB}.{SCHEMA}.POSITIONS   p1 ON a.FROM_POSITION_ID   = p1.POSITION_ID
        LEFT JOIN {DB}.{SCHEMA}.POSITIONS   p2 ON a.TO_POSITION_ID     = p2.POSITION_ID
        WHERE a.EMPLOYEE_ID = '{emp_id}'
        ORDER BY a.APPOINTMENT_DATE DESC
    """)

    if apt_df.empty:
        st.info("発令履歴がありません。")
    else:
        for _, row in apt_df.iterrows():
            from_info = f"{row['FROM_DEPT'] or '-'} / {row['FROM_POS'] or '-'}"
            to_info   = f"{row['TO_DEPT'] or '-'} / {row['TO_POS'] or '-'}"
            st.markdown(
                f'<div class="timeline-item">'
                f'<div style="font-weight:600">{row["APPOINTMENT_DATE"]} — {row["APPOINTMENT_TYPE"]}</div>'
                f'<div style="font-size:13px;color:#475569">'
                f'<b>変更前:</b> {from_info} ({row.get("FROM_JOB_GRADE") or "-"})'
                f' &rarr; <b>変更後:</b> {to_info} ({row.get("TO_JOB_GRADE") or "-"})'
                f'</div>'
                f'<div style="font-size:12px;color:#94a3b8">{row.get("REASON","")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

# Tab 4: Evaluation scores
with t4:
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("**評価スコア**")
        perf = float(e["PERFORMANCE_SCORE"] or 0)
        pcolor = perf_color(perf)
        st.markdown(
            f'<div style="text-align:center;padding:30px">'
            f'<div style="font-size:60px;font-weight:800;color:{pcolor}">{perf}</div>'
            f'<div style="font-size:14px;color:#64748b">/ 5.0 スケール</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=perf,
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 5], "tickvals": [1,2,3,4,5]},
                "bar": {"color": pcolor},
                "steps": [
                    {"range": [0, 2], "color": "#fee2e2"},
                    {"range": [2, 3], "color": "#fef3c7"},
                    {"range": [3, 4], "color": "#dbeafe"},
                    {"range": [4, 5], "color": "#d1fae5"},
                ],
                "threshold": {"line": {"color": "#1e293b", "width": 3}, "value": 3.3},
            },
        ))
        fig.update_layout(height=220, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with sc2:
        st.markdown("**エンゲージメントスコア**")
        eng = float(e["ENGAGEMENT_SCORE"] or 0)
        st.markdown(
            f'<div style="text-align:center;padding:30px">'
            f'<div style="font-size:60px;font-weight:800;color:#2563eb">{eng:.0f}</div>'
            f'<div style="font-size:14px;color:#64748b">/ 100 スケール</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=eng,
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0,  40], "color": "#fee2e2"},
                    {"range": [40, 60], "color": "#fef3c7"},
                    {"range": [60, 80], "color": "#dbeafe"},
                    {"range": [80,100], "color": "#d1fae5"},
                ],
            },
        ))
        fig2.update_layout(height=220, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)
