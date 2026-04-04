"""
Page 2: Org chart & Appointment management
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta
from utils import run_query, run_write, DB, SCHEMA, get_departments, get_positions

st.title("組織図・発令管理")

tab1, tab2, tab3 = st.tabs(["組織図", "発令履歴", "発令登録"])

# ── Tab 1: Org chart ──────────────────────────────────────────────────────────
with tab1:
    hc_df = run_query(f"""
        SELECT
            d.DEPARTMENT_ID, d.DEPARTMENT_NAME, d.PARENT_ID, d.DEPT_LEVEL,
            COUNT(e.EMPLOYEE_ID) AS HEADCOUNT
        FROM {DB}.{SCHEMA}.DEPARTMENTS d
        LEFT JOIN {DB}.{SCHEMA}.EMPLOYEES e
            ON d.DEPARTMENT_ID = e.DEPARTMENT_ID AND e.IS_ACTIVE = TRUE
        GROUP BY d.DEPARTMENT_ID, d.DEPARTMENT_NAME, d.PARENT_ID, d.DEPT_LEVEL
    """)

    if not hc_df.empty:
        # Add a root node
        root_row = pd.DataFrame([{
            "DEPARTMENT_ID": "ROOT",
            "DEPARTMENT_NAME": "Demo Financial Corp",
            "PARENT_ID": "",
            "DEPT_LEVEL": 0,
            "HEADCOUNT": int(hc_df["HEADCOUNT"].sum()),
        }])
        plot_df = pd.concat([root_row, hc_df], ignore_index=True)
        plot_df["PARENT_ID"] = plot_df["PARENT_ID"].fillna("ROOT")
        plot_df.loc[plot_df["DEPT_LEVEL"] == 1, "PARENT_ID"] = "ROOT"

        fig = go.Figure(go.Treemap(
            ids=plot_df["DEPARTMENT_ID"],
            labels=plot_df.apply(
                lambda r: f'{r["DEPARTMENT_NAME"]}<br>{r["HEADCOUNT"]}名', axis=1
            ),
            parents=plot_df["PARENT_ID"],
            values=plot_df["HEADCOUNT"],
            branchvalues="total",
            marker=dict(colorscale="Blues", showscale=False),
            textinfo="label",
        ))
        fig.update_layout(
            height=520,
            margin=dict(l=0, r=0, t=20, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Headcount table
    st.markdown('<div class="section-header">部門別人員サマリー</div>', unsafe_allow_html=True)
    summary_df = run_query(f"""
        SELECT
            d.DEPARTMENT_NAME AS 部門名,
            d.DEPT_LEVEL AS レベル,
            COUNT(e.EMPLOYEE_ID) AS 人員数,
            SUM(CASE WHEN e.GENDER='男性' THEN 1 ELSE 0 END) AS 男性,
            SUM(CASE WHEN e.GENDER='女性' THEN 1 ELSE 0 END) AS 女性,
            ROUND(AVG(e.PERFORMANCE_SCORE),2) AS 平均評価,
            ROUND(AVG(e.ENGAGEMENT_SCORE),1) AS 平均ENG
        FROM {DB}.{SCHEMA}.DEPARTMENTS d
        LEFT JOIN {DB}.{SCHEMA}.EMPLOYEES e
            ON d.DEPARTMENT_ID = e.DEPARTMENT_ID AND e.IS_ACTIVE = TRUE
        GROUP BY d.DEPARTMENT_ID, d.DEPARTMENT_NAME, d.DEPT_LEVEL
        ORDER BY d.DEPT_LEVEL, 人員数 DESC
    """)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)


# ── Tab 2: Appointment history ─────────────────────────────────────────────────
with tab2:
    st.markdown("**絞り込みフィルタ**")
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        date_from = st.date_input("開始日", value=date.today() - timedelta(days=180))
        date_to   = st.date_input("終了日", value=date.today())
    with fc2:
        apt_types = st.multiselect(
            "発令種別",
            ["採用","異動","昇格","降格","出向","転籍","退職"],
            default=["異動","昇格"],
        )
    with fc3:
        dept_df = get_departments()
        dept_opts = dept_df["DEPARTMENT_NAME"].tolist()
        sel_depts = st.multiselect("部門（新所属）", dept_opts)

    type_filter = ""
    if apt_types:
        type_list = "','".join(apt_types)
        type_filter = f"AND a.APPOINTMENT_TYPE IN ('{type_list}')"

    dept_id_filter = ""
    if sel_depts:
        ids = dept_df[dept_df["DEPARTMENT_NAME"].isin(sel_depts)]["DEPARTMENT_ID"].tolist()
        did_list = "','".join(ids)
        dept_id_filter = f"AND a.TO_DEPARTMENT_ID IN ('{did_list}')"

    apt_df = run_query(f"""
        SELECT
            a.APPOINTMENT_DATE AS 発令日,
            e.EMPLOYEE_NAME    AS 氏名,
            a.APPOINTMENT_TYPE AS 発令種別,
            d1.DEPARTMENT_NAME AS 旧所属,
            d2.DEPARTMENT_NAME AS 新所属,
            p1.POSITION_NAME   AS 旧職位,
            p2.POSITION_NAME   AS 新職位,
            a.REASON           AS 理由
        FROM {DB}.{SCHEMA}.APPOINTMENTS a
        JOIN {DB}.{SCHEMA}.EMPLOYEES e    ON a.EMPLOYEE_ID = e.EMPLOYEE_ID
        LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d1 ON a.FROM_DEPARTMENT_ID = d1.DEPARTMENT_ID
        LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d2 ON a.TO_DEPARTMENT_ID   = d2.DEPARTMENT_ID
        LEFT JOIN {DB}.{SCHEMA}.POSITIONS   p1 ON a.FROM_POSITION_ID   = p1.POSITION_ID
        LEFT JOIN {DB}.{SCHEMA}.POSITIONS   p2 ON a.TO_POSITION_ID     = p2.POSITION_ID
        WHERE a.APPOINTMENT_DATE BETWEEN '{date_from}' AND '{date_to}'
        {type_filter} {dept_id_filter}
        ORDER BY a.APPOINTMENT_DATE DESC
        LIMIT 200
    """)

    st.markdown(f"**{len(apt_df)} 件** の発令が見つかりました")
    st.dataframe(apt_df, use_container_width=True, hide_index=True, height=420)


# ── Tab 3: New appointment ─────────────────────────────────────────────────────
with tab3:
    role = st.session_state.get("role", "HR_EMPLOYEE_ROLE")
    if role not in ("HR_ADMIN_ROLE", "HR_USER_ROLE"):
        st.warning("発令登録は HR管理者・HR担当者のみ利用できます。")
        st.stop()

    st.markdown('<div class="section-header">新規発令登録</div>', unsafe_allow_html=True)

    emp_list = run_query(f"""
        SELECT EMPLOYEE_ID, EMPLOYEE_NAME FROM {DB}.{SCHEMA}.EMPLOYEES
        WHERE IS_ACTIVE = TRUE ORDER BY EMPLOYEE_NAME
    """)
    emp_opts = {row["EMPLOYEE_NAME"]: row["EMPLOYEE_ID"]
                for _, row in emp_list.iterrows()}

    fc1, fc2 = st.columns(2)
    with fc1:
        sel_name  = st.selectbox("対象社員", list(emp_opts.keys()))
        apt_type  = st.selectbox("発令種別", ["採用","異動","昇格","降格","出向","転籍","退職"])
        apt_date  = st.date_input("発令日", value=date.today())
    with fc2:
        dept_df2  = get_departments()
        dept_map  = {r["DEPARTMENT_NAME"]: r["DEPARTMENT_ID"]
                     for _, r in dept_df2.iterrows()}
        pos_df    = get_positions()
        pos_map   = {r["POSITION_NAME"]: r["POSITION_ID"]
                     for _, r in pos_df.iterrows()}
        to_dept   = st.selectbox("異動先部門", list(dept_map.keys()))
        to_pos    = st.selectbox("発令後職位", list(pos_map.keys()))

    reason = st.text_area("発令理由", height=80)

    if st.button("発令を登録する", type="primary"):
        if not reason.strip():
            st.error("発令理由を入力してください。")
        else:
            import uuid
            apt_id = "APT" + uuid.uuid4().hex[:10].upper()
            emp_id = emp_opts[sel_name]
            to_did = dept_map[to_dept]
            to_pid = pos_map[to_pos]
            run_write(f"""
                INSERT INTO {DB}.{SCHEMA}.APPOINTMENTS
                (APPOINTMENT_ID, EMPLOYEE_ID, APPOINTMENT_DATE, APPOINTMENT_TYPE,
                 TO_DEPARTMENT_ID, TO_POSITION_ID, REASON, EFFECTIVE_DATE)
                VALUES ('{apt_id}', '{emp_id}', '{apt_date}', '{apt_type}',
                        '{to_did}', '{to_pid}', $${reason}$$, '{apt_date}')
            """)
            st.success(f"発令を登録しました: {sel_name} → {apt_type} ({to_dept})")
            st.cache_data.clear()
