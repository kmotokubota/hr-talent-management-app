"""
Page 5: Talent List management
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import uuid
from utils import run_query, run_write, DB, SCHEMA, get_departments, get_positions, get_skills

st.title("人材リスト管理")

tab1, tab2 = st.tabs(["リスト一覧", "新規リスト作成"])

# ── Tab 1: List overview ──────────────────────────────────────────────────────
with tab1:
    lists_df = run_query(f"""
        SELECT
            tl.LIST_ID, tl.LIST_NAME, tl.DESCRIPTION,
            tl.CREATED_BY, tl.CREATED_AT, tl.UPDATED_AT,
            tl.IS_AUTO_REFRESH,
            COUNT(tlm.EMPLOYEE_ID) AS MEMBER_COUNT
        FROM {DB}.{SCHEMA}.TALENT_LISTS tl
        LEFT JOIN {DB}.{SCHEMA}.TALENT_LIST_MEMBERS tlm USING (LIST_ID)
        GROUP BY tl.LIST_ID, tl.LIST_NAME, tl.DESCRIPTION,
                 tl.CREATED_BY, tl.CREATED_AT, tl.UPDATED_AT, tl.IS_AUTO_REFRESH
        ORDER BY tl.UPDATED_AT DESC
    """)

    if lists_df.empty:
        st.info("保存されたリストがありません。「新規リスト作成」タブからリストを作成してください。")
    else:
        for _, row in lists_df.iterrows():
            with st.expander(
                f"📋 {row['LIST_NAME']}  —  {row['MEMBER_COUNT']} 名  "
                f"| {'自動更新' if row['IS_AUTO_REFRESH'] else '手動'}",
                expanded=False,
            ):
                ci1, ci2 = st.columns([3, 1])
                with ci1:
                    st.markdown(f"**説明**: {row['DESCRIPTION'] or '-'}")
                    st.markdown(
                        f"作成者: {row['CREATED_BY']} &nbsp;|&nbsp; "
                        f"最終更新: {str(row['UPDATED_AT'])[:16]}"
                    )
                with ci2:
                    # Refresh
                    if st.button("最新データに更新", key=f"refresh_{row['LIST_ID']}"):
                        try:
                            filter_cfg = run_query(f"""
                                SELECT FILTER_CONFIG FROM {DB}.{SCHEMA}.TALENT_LISTS
                                WHERE LIST_ID = '{row["LIST_ID"]}'
                            """)
                            cfg = json.loads(filter_cfg["FILTER_CONFIG"].iloc[0])

                            # Build refresh conditions
                            conds = ["e.IS_ACTIVE = TRUE"]
                            if cfg.get("departments"):
                                dids = "','".join(cfg["departments"])
                                conds.append(f"e.DEPARTMENT_ID IN ('{dids}')")
                            if cfg.get("skills"):
                                sids = "','".join(cfg["skills"])
                                conds.append(
                                    f"EXISTS (SELECT 1 FROM {DB}.{SCHEMA}.EMPLOYEE_SKILLS es "
                                    f"WHERE es.EMPLOYEE_ID = e.EMPLOYEE_ID AND es.SKILL_ID IN ('{sids}'))"
                                )
                            if cfg.get("performance_min"):
                                conds.append(f"e.PERFORMANCE_SCORE >= {cfg['performance_min']}")
                            if cfg.get("engagement_max"):
                                conds.append(f"e.ENGAGEMENT_SCORE <= {cfg['engagement_max']}")
                            if cfg.get("tenure_max"):
                                conds.append(f"e.TENURE_YEARS <= {cfg['tenure_max']}")
                            if cfg.get("job_grades"):
                                gds = "','".join(cfg["job_grades"])
                                conds.append(f"e.JOB_GRADE IN ('{gds}')")

                            where = " AND ".join(conds)
                            run_write(f"""
                                DELETE FROM {DB}.{SCHEMA}.TALENT_LIST_MEMBERS
                                WHERE LIST_ID = '{row["LIST_ID"]}'
                            """)
                            run_write(f"""
                                INSERT INTO {DB}.{SCHEMA}.TALENT_LIST_MEMBERS
                                (LIST_ID, EMPLOYEE_ID, ADDED_AT, ADDED_BY)
                                SELECT '{row["LIST_ID"]}', e.EMPLOYEE_ID,
                                       CURRENT_TIMESTAMP, 'system'
                                FROM {DB}.{SCHEMA}.EMPLOYEES e
                                WHERE {where}
                                LIMIT 200
                            """)
                            run_write(f"""
                                UPDATE {DB}.{SCHEMA}.TALENT_LISTS
                                SET UPDATED_AT = CURRENT_TIMESTAMP
                                WHERE LIST_ID = '{row["LIST_ID"]}'
                            """)
                            st.success("リストを更新しました。")
                            st.cache_data.clear()
                        except Exception as ex:
                            st.error(f"更新エラー: {ex}")

                # Members table
                members = run_query(f"""
                    SELECT
                        e.EMPLOYEE_ID AS ID, e.EMPLOYEE_NAME AS "氏名",
                        d.DEPARTMENT_NAME AS "部門", p.POSITION_NAME AS "職位",
                        e.JOB_GRADE AS "グレード", e.PERFORMANCE_SCORE AS "評価",
                        e.ENGAGEMENT_SCORE AS ENG
                    FROM {DB}.{SCHEMA}.TALENT_LIST_MEMBERS tlm
                    JOIN {DB}.{SCHEMA}.EMPLOYEES e USING (EMPLOYEE_ID)
                    JOIN {DB}.{SCHEMA}.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
                    JOIN {DB}.{SCHEMA}.POSITIONS p ON e.POSITION_ID = p.POSITION_ID
                    WHERE tlm.LIST_ID = '{row["LIST_ID"]}'
                    ORDER BY e.DEPARTMENT_ID, e.JOB_GRADE DESC
                """)

                if not members.empty:
                    dc1, dc2 = st.columns([3, 1])
                    with dc1:
                        st.dataframe(members, use_container_width=True, hide_index=True)
                    with dc2:
                        csv = members.to_csv(index=False).encode("utf-8-sig")
                        st.download_button(
                            "CSVダウンロード",
                            csv,
                            file_name=f"{row['LIST_NAME']}.csv",
                            mime="text/csv",
                            key=f"csv_{row['LIST_ID']}",
                        )
                        if st.button(
                            "リストを削除",
                            key=f"del_{row['LIST_ID']}",
                            type="secondary",
                        ):
                            if st.session_state.get(f"confirm_del_{row['LIST_ID']}"):
                                run_write(f"""
                                    DELETE FROM {DB}.{SCHEMA}.TALENT_LIST_MEMBERS
                                    WHERE LIST_ID = '{row["LIST_ID"]}'
                                """)
                                run_write(f"""
                                    DELETE FROM {DB}.{SCHEMA}.TALENT_LISTS
                                    WHERE LIST_ID = '{row["LIST_ID"]}'
                                """)
                                st.cache_data.clear()
                                st.success("削除しました。")
                            else:
                                st.session_state[f"confirm_del_{row['LIST_ID']}"] = True
                                st.warning("もう一度押すと削除されます。")


# ── Tab 2: Create new list ─────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">新規リスト作成</div>', unsafe_allow_html=True)

    # Pre-populate from search page
    pending = st.session_state.get("pending_list_save")
    if pending:
        st.info(f"人材サーチから {len(pending)} 名のリストを保存できます。")

    list_name = st.text_input("リスト名 *", placeholder="例: AI人材候補2026")
    list_desc = st.text_area("説明", placeholder="リストの目的や選定基準など", height=80)

    st.markdown("**フィルタ条件を保存（オプション - 自動更新用）**")
    fc1, fc2 = st.columns(2)

    with fc1:
        dept_df = get_departments()
        dept_map = {r["DEPARTMENT_NAME"]: r["DEPARTMENT_ID"]
                    for _, r in dept_df.iterrows()}
        sel_depts = st.multiselect("対象部門", list(dept_map.keys()), key="new_list_dept")

        grade_opts = ["G1","G2","G3","G4","G5","G6","G7","G8"]
        sel_grades = st.multiselect("対象グレード", grade_opts, key="new_list_grade")

        perf_min = st.slider("評価スコア下限", 1.0, 5.0, 1.0, 0.1, key="new_list_perf")

    with fc2:
        skill_df = get_skills()
        skill_map = {r["SKILL_NAME"]: r["SKILL_ID"]
                     for _, r in skill_df.iterrows()}
        sel_skills = st.multiselect("スキル条件", list(skill_map.keys()), key="new_list_skill")

        eng_max = st.slider("エンゲージメント上限", 0, 100, 100, key="new_list_eng")
        tenure_max = st.slider("勤続年数上限", 0, 30, 30, key="new_list_tenure")

    is_auto = st.checkbox("自動更新を有効にする", value=True)

    if st.button("リストを保存する", type="primary"):
        if not list_name.strip():
            st.error("リスト名を入力してください。")
        else:
            list_id = "LST" + uuid.uuid4().hex[:6].upper()
            filter_cfg: dict = {}
            if sel_depts:
                filter_cfg["departments"] = [dept_map[d] for d in sel_depts]
            if sel_grades:
                filter_cfg["job_grades"] = sel_grades
            if perf_min > 1.0:
                filter_cfg["performance_min"] = perf_min
            if sel_skills:
                filter_cfg["skills"] = [skill_map[s] for s in sel_skills]
            if eng_max < 100:
                filter_cfg["engagement_max"] = eng_max
            if tenure_max < 30:
                filter_cfg["tenure_max"] = tenure_max

            cfg_json = json.dumps(filter_cfg, ensure_ascii=False).replace("'", "\\'")
            run_write(f"""
                INSERT INTO {DB}.{SCHEMA}.TALENT_LISTS
                (LIST_ID, LIST_NAME, DESCRIPTION, FILTER_CONFIG,
                 CREATED_BY, IS_AUTO_REFRESH)
                SELECT '{list_id}', '{list_name.replace("'","''")}',
                       '{list_desc.replace("'","''")}',
                       PARSE_JSON('{cfg_json}'),
                       'user', {is_auto}
            """)

            # Add members
            if pending:
                # From search page
                emp_ids = "','".join(pending)
                run_write(f"""
                    INSERT INTO {DB}.{SCHEMA}.TALENT_LIST_MEMBERS
                    (LIST_ID, EMPLOYEE_ID, ADDED_BY)
                    SELECT '{list_id}', EMPLOYEE_ID, 'user'
                    FROM {DB}.{SCHEMA}.EMPLOYEES
                    WHERE EMPLOYEE_ID IN ('{emp_ids}') AND IS_ACTIVE = TRUE
                """)
                st.session_state["pending_list_save"] = None
            elif filter_cfg:
                # Auto-populate from filter
                conds = ["e.IS_ACTIVE = TRUE"]
                if filter_cfg.get("departments"):
                    dids = "','".join(filter_cfg["departments"])
                    conds.append(f"e.DEPARTMENT_ID IN ('{dids}')")
                if filter_cfg.get("skills"):
                    sids = "','".join(filter_cfg["skills"])
                    conds.append(
                        f"EXISTS (SELECT 1 FROM {DB}.{SCHEMA}.EMPLOYEE_SKILLS es "
                        f"WHERE es.EMPLOYEE_ID = e.EMPLOYEE_ID AND es.SKILL_ID IN ('{sids}'))"
                    )
                if filter_cfg.get("performance_min"):
                    conds.append(f"e.PERFORMANCE_SCORE >= {filter_cfg['performance_min']}")
                where = " AND ".join(conds)
                run_write(f"""
                    INSERT INTO {DB}.{SCHEMA}.TALENT_LIST_MEMBERS
                    (LIST_ID, EMPLOYEE_ID, ADDED_BY)
                    SELECT '{list_id}', e.EMPLOYEE_ID, 'user'
                    FROM {DB}.{SCHEMA}.EMPLOYEES e
                    WHERE {where}
                    LIMIT 200
                """)

            st.success(f"リスト「{list_name}」を保存しました（ID: {list_id}）。")
            st.cache_data.clear()
