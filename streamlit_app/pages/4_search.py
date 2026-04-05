"""
Page 4: Advanced Search - multi-condition employee filter
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from utils import (
    run_query, DB, SCHEMA,
    get_departments, get_positions, get_skills,
    grade_badge,
)

st.title("人材サーチ")
st.markdown("複数条件を組み合わせて人材を検索し、リストへ保存できます。")

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 検索フィルタ")

    name_q = st.text_input("氏名（部分一致）", "")

    dept_df = get_departments()
    dept_map = {r["DEPARTMENT_NAME"]: r["DEPARTMENT_ID"]
                for _, r in dept_df.iterrows()}
    sel_depts = st.multiselect("部門", list(dept_map.keys()))

    pos_df = get_positions()
    pos_map = {r["POSITION_NAME"]: r["POSITION_ID"]
               for _, r in pos_df.iterrows()}
    sel_positions = st.multiselect("職位", list(pos_map.keys()))

    grade_options = ["G1","G2","G3","G4","G5","G6","G7","G8"]
    grade_range = st.select_slider(
        "職位等級",
        options=grade_options,
        value=("G1", "G8"),
    )

    age_range = st.slider("年齢範囲", 22, 65, (22, 65))
    tenure_range = st.slider("勤続年数", 0, 30, (0, 30))

    gender = st.radio("性別", ["全員","男性","女性"], horizontal=True)

    sel_emp_types = st.multiselect(
        "雇用形態", ["正社員","契約社員","派遣社員"], default=["正社員"]
    )

    locations = ["東京","大阪","名古屋","福岡","札幌"]
    sel_locations = st.multiselect("勤務地", locations)

    skill_df = get_skills()
    skill_map = {r["SKILL_NAME"]: r["SKILL_ID"]
                 for _, r in skill_df.iterrows()}
    sel_skills = st.multiselect("スキル", list(skill_map.keys()))
    if sel_skills:
        skill_logic = st.radio("スキルマッチング", ["OR（いずれか）","AND（すべて）"])
    else:
        skill_logic = "OR（いずれか）"

    perf_range = st.slider("評価スコア", 1.0, 5.0, (1.0, 5.0), step=0.1)
    eng_range  = st.slider("エンゲージメントスコア", 0, 100, (0, 100))

    search_btn = st.button("検索する", type="primary", use_container_width=True)

# ── Build dynamic SQL ─────────────────────────────────────────────────────────
def build_query(
    name_q, sel_depts, dept_map, sel_positions, pos_map,
    grade_range, age_range, tenure_range, gender,
    sel_emp_types, sel_locations, sel_skills, skill_map, skill_logic,
    perf_range, eng_range,
) -> str:
    conditions = ["e.IS_ACTIVE = TRUE"]

    if name_q.strip():
        safe_name = name_q.strip().replace("'", "''")
        conditions.append(f"e.EMPLOYEE_NAME LIKE '%{safe_name}%'")

    if sel_depts:
        ids = "','".join(dept_map[d] for d in sel_depts)
        conditions.append(f"e.DEPARTMENT_ID IN ('{ids}')")

    if sel_positions:
        ids = "','".join(pos_map[p] for p in sel_positions)
        conditions.append(f"e.POSITION_ID IN ('{ids}')")

    # Grade range using index
    g_opts = ["G1","G2","G3","G4","G5","G6","G7","G8"]
    g_low  = grade_range[0]
    g_high = grade_range[1]
    g_in   = "','".join(g for g in g_opts
                         if g_opts.index(g) >= g_opts.index(g_low)
                         and g_opts.index(g) <= g_opts.index(g_high))
    if g_in != "','".join(g_opts):
        conditions.append(f"e.JOB_GRADE IN ('{g_in}')")

    conditions.append(f"e.AGE BETWEEN {age_range[0]} AND {age_range[1]}")
    conditions.append(f"e.TENURE_YEARS BETWEEN {tenure_range[0]} AND {tenure_range[1]}")

    if gender != "全員":
        conditions.append(f"e.GENDER = '{gender}'")

    if sel_emp_types:
        ids = "','".join(sel_emp_types)
        conditions.append(f"e.EMPLOYEE_TYPE IN ('{ids}')")

    if sel_locations:
        ids = "','".join(sel_locations)
        conditions.append(f"e.LOCATION IN ('{ids}')")

    if sel_skills:
        skill_ids = [skill_map[s] for s in sel_skills]
        if "AND" in skill_logic:
            for sid in skill_ids:
                conditions.append(
                    f"EXISTS (SELECT 1 FROM {DB}.{SCHEMA}.EMPLOYEE_SKILLS es "
                    f"WHERE es.EMPLOYEE_ID = e.EMPLOYEE_ID AND es.SKILL_ID = '{sid}')"
                )
        else:
            ids_str = "','".join(skill_ids)
            conditions.append(
                f"EXISTS (SELECT 1 FROM {DB}.{SCHEMA}.EMPLOYEE_SKILLS es "
                f"WHERE es.EMPLOYEE_ID = e.EMPLOYEE_ID AND es.SKILL_ID IN ('{ids_str}'))"
            )

    conditions.append(f"e.PERFORMANCE_SCORE BETWEEN {perf_range[0]} AND {perf_range[1]}")
    conditions.append(f"e.ENGAGEMENT_SCORE BETWEEN {eng_range[0]} AND {eng_range[1]}")

    where = " AND ".join(conditions)
    return f"""
        SELECT
            e.EMPLOYEE_ID   AS ID,
            e.EMPLOYEE_NAME AS "氏名",
            d.DEPARTMENT_NAME AS "部門",
            p.POSITION_NAME   AS "職位",
            e.JOB_GRADE       AS "グレード",
            e.GENDER          AS "性別",
            e.AGE             AS "年齢",
            e.TENURE_YEARS    AS "勤続年数",
            e.LOCATION        AS "勤務地",
            e.EMPLOYEE_TYPE   AS "雇用形態",
            e.PERFORMANCE_SCORE AS "評価",
            e.ENGAGEMENT_SCORE  AS ENG,
            v.SKILLS_TEXT       AS "スキル"
        FROM {DB}.{SCHEMA}.EMPLOYEES e
        LEFT JOIN {DB}.{SCHEMA}.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
        LEFT JOIN {DB}.{SCHEMA}.POSITIONS   p ON e.POSITION_ID   = p.POSITION_ID
        LEFT JOIN {DB}.{SCHEMA}.V_EMPLOYEE_FULL v ON e.EMPLOYEE_ID = v.EMPLOYEE_ID
        WHERE {where}
        ORDER BY e.DEPARTMENT_ID, e.JOB_GRADE DESC
        LIMIT 500
    """


# ── Run search ─────────────────────────────────────────────────────────────────
if search_btn or st.session_state.get("search_results") is not None:
    if search_btn:
        sql = build_query(
            name_q, sel_depts, dept_map, sel_positions, pos_map,
            grade_range, age_range, tenure_range, gender,
            sel_emp_types, sel_locations, sel_skills, skill_map, skill_logic,
            perf_range, eng_range,
        )
        results = run_query(sql)
        st.session_state["search_results"] = results
        st.session_state["last_search_sql"] = sql
    else:
        results = st.session_state["search_results"]

    # Display results
    if results is None or results.empty:
        st.warning("条件に一致する従業員が見つかりませんでした。")
    else:
        hit_count = len(results)
        rc1, rc2, rc3 = st.columns([2, 1, 1])
        with rc1:
            st.markdown(
                f'<span style="font-size:16px;font-weight:700;color:#2563eb">'
                f'{hit_count:,} 名</span> がヒットしました',
                unsafe_allow_html=True,
            )
        with rc2:
            csv_data = results.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "CSVエクスポート",
                csv_data,
                file_name="talent_search_results.csv",
                mime="text/csv",
            )
        with rc3:
            if st.button("リストに保存", type="secondary"):
                st.session_state["pending_list_save"] = results["ID"].tolist()
                st.info("ページ「人材リスト」に移動して保存してください。")

        st.dataframe(results, use_container_width=True, hide_index=True, height=500)

        # Per-employee profile link buttons
        st.markdown('<div class="section-header">プロフィールを見る</div>', unsafe_allow_html=True)
        btn_cols = st.columns(5)
        for i, (_, row) in enumerate(results.head(20).iterrows()):
            with btn_cols[i % 5]:
                label = f'{row["氏名"]} ({row["ID"]})'
                if st.button(label, key=f"go_profile_{row['ID']}"):
                    st.session_state["selected_employee_id"] = row["ID"]
                    st.switch_page("pages/3_profile.py")
else:
    st.info("左のフィルタを設定して「検索する」ボタンを押してください。")
