"""
Page 6: AI Talent Search - natural language employee matching
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import re
from utils import run_query, DB, SCHEMA, avatar_html

st.title("AI人材検索")
st.markdown(
    "自然言語で求める人材像を入力すると、Snowflake Cortex AI がマッチする候補者を提案します。"
)

# ── Input form ────────────────────────────────────────────────────────────────
query_text = st.text_area(
    "求める人材像・仕事内容を自由に入力してください",
    placeholder=(
        "例: Pythonとクラウドインフラに強く、5年以上の経験を持つリーダー候補。"
        "データ分析経験があれば尚可。"
    ),
    height=120,
)

model_options = {
    "claude-sonnet-4-6": "Claude Sonnet 4.6 (最新・高精度)",
    "claude-4-sonnet":   "Claude 4 Sonnet (高精度)",
    "openai-gpt-5.2":    "GPT-5.2 (最新・汎用)",
    "openai-gpt-4.1":    "GPT-4.1 (高速・汎用)",
}
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    sel_model = st.selectbox(
        "AIモデル",
        list(model_options.keys()),
        format_func=lambda x: model_options[x],
    )
with col2:
    top_n = st.number_input("候補者数", min_value=5, max_value=20, value=10)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("検索", type="primary", use_container_width=True)


# ── AI search logic ───────────────────────────────────────────────────────────
def search_with_cortex(query: str, limit: int = 20) -> list:
    """Use Cortex Search Service via SQL SEARCH_PREVIEW."""
    safe_q = query.replace("\\", "\\\\").replace("'", "\\'")
    try:
        result = run_query(f"""
            SELECT PARSE_JSON(
              SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{DB}.{SCHEMA}.EMPLOYEE_SEARCH_SERVICE',
                '{{"query": "{safe_q}", "columns": ["EMPLOYEE_ID","EMPLOYEE_NAME","DEPARTMENT_NAME","POSITION_NAME","JOB_GRADE","SKILLS_TEXT","PROFILE_SUMMARY","PERFORMANCE_SCORE","ENGAGEMENT_SCORE","AGE","TENURE_YEARS"], "limit": {limit}}}'
              )
            ) AS RESULT
        """)
        if result.empty:
            return []
        parsed = json.loads(result["RESULT"].iloc[0])
        return parsed.get("results", [])
    except Exception:
        # Fallback: keyword search
        safe_q2 = query[:100].replace("'", "''")
        fallback = run_query(f"""
            SELECT
                e.EMPLOYEE_ID, e.EMPLOYEE_NAME, d.DEPARTMENT_NAME,
                p.POSITION_NAME, e.JOB_GRADE, e.PROFILE_SUMMARY,
                v.SKILLS_TEXT, e.PERFORMANCE_SCORE, e.ENGAGEMENT_SCORE,
                e.AGE, e.TENURE_YEARS
            FROM {DB}.{SCHEMA}.EMPLOYEES e
            JOIN {DB}.{SCHEMA}.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
            JOIN {DB}.{SCHEMA}.POSITIONS p ON e.POSITION_ID = p.POSITION_ID
            LEFT JOIN {DB}.{SCHEMA}.V_EMPLOYEE_FULL v ON e.EMPLOYEE_ID = v.EMPLOYEE_ID
            WHERE e.IS_ACTIVE = TRUE
              AND (e.PROFILE_SUMMARY ILIKE '%{safe_q2[:30]}%' OR v.SKILLS_TEXT ILIKE '%{safe_q2[:30]}%')
            ORDER BY e.PERFORMANCE_SCORE DESC
            LIMIT {limit}
        """)
        return fallback.to_dict("records")


def score_candidate(candidate: dict, query: str, model: str) -> dict:
    """Use AI_COMPLETE to score and explain candidate match."""
    name     = candidate.get("EMPLOYEE_NAME", "")
    dept     = candidate.get("DEPARTMENT_NAME", "")
    pos      = candidate.get("POSITION_NAME", "")
    grade    = candidate.get("JOB_GRADE", "")
    skills   = candidate.get("SKILLS_TEXT", "")
    profile  = (candidate.get("PROFILE_SUMMARY", "") or "")[:300]

    prompt = f"""あなたは優秀な人材コンサルタントです。
求める人材像: {query}
候補者情報:
- 氏名: {name}
- 所属: {dept} / {pos} ({grade})
- スキル: {skills}
- プロフィール: {profile}

この候補者が求める人材像にどの程度マッチするか、100点満点でスコアをつけ、
マッチする理由を2〜3文で簡潔に述べてください。
出力形式（他の文章は一切不要）:
スコア: XX
理由: ..."""

    safe_prompt = prompt.replace("\\", "\\\\").replace("'", "\\'")
    try:
        result = run_query(f"""
            SELECT SNOWFLAKE.CORTEX.COMPLETE(
                '{model}',
                '{safe_prompt}'
            ) AS AI_RESULT
        """)
        raw = result["AI_RESULT"].iloc[0] if not result.empty else ""
        # Parse score and reason
        score_match  = re.search(r"スコア[：:]\s*(\d+)", raw)
        reason_match = re.search(r"理由[：:]\s*(.+?)(?:\n|$)", raw, re.DOTALL)
        score  = int(score_match.group(1))  if score_match  else 50
        reason = reason_match.group(1).strip() if reason_match else raw[:200]
        return {**candidate, "AI_SCORE": score, "AI_REASON": reason}
    except Exception as ex:
        return {**candidate, "AI_SCORE": 50, "AI_REASON": f"AI評価エラー: {ex}"}


# ── Run search ─────────────────────────────────────────────────────────────────
if search_btn:
    if not query_text.strip():
        st.error("検索クエリを入力してください。")
        st.stop()

    with st.spinner("Cortex Search で候補者を検索中..."):
        candidates = search_with_cortex(query_text.strip(), limit=top_n + 5)

    if not candidates:
        st.warning("条件に一致する候補者が見つかりませんでした。")
        st.stop()

    st.markdown(f"**{len(candidates)} 名** の候補者が見つかりました。AI評価を生成中...")
    progress = st.progress(0)
    scored = []
    for i, c in enumerate(candidates[:top_n]):
        progress.progress((i + 1) / top_n)
        scored.append(score_candidate(c, query_text.strip(), sel_model))
    progress.empty()

    # Sort by AI score descending
    scored.sort(key=lambda x: x.get("AI_SCORE", 0), reverse=True)
    # Persist results so profile buttons survive reruns
    st.session_state["ai_search_scored"] = scored

# ── Display results (from current search or previous session state) ───────────
scored = st.session_state.get("ai_search_scored")
if scored:
    st.markdown(
        f'<div style="font-size:18px;font-weight:700;color:#1e293b;margin-bottom:16px">'
        f'AIマッチング結果 TOP {len(scored)}</div>',
        unsafe_allow_html=True,
    )

    for rank, cand in enumerate(scored, 1):
        emp_id   = cand.get("EMPLOYEE_ID", "")
        name     = cand.get("EMPLOYEE_NAME", "")
        dept     = cand.get("DEPARTMENT_NAME", "")
        pos      = cand.get("POSITION_NAME", "")
        grade    = cand.get("JOB_GRADE", "")
        skills   = cand.get("SKILLS_TEXT", "")
        ai_score = int(cand.get("AI_SCORE", 50))
        ai_reason = cand.get("AI_REASON", "")
        perf = float(cand.get("PERFORMANCE_SCORE") or 3.0)

        score_color = (
            "#059669" if ai_score >= 80 else
            "#2563eb" if ai_score >= 60 else
            "#f59e0b" if ai_score >= 40 else "#ef4444"
        )

        with st.container():
            st.markdown(
                f'<div style="background:white;border-radius:8px;padding:16px;'
                f'margin-bottom:12px;border:1px solid #e2e8f0;'
                f'border-left:4px solid {score_color}">'
                f'<div style="display:flex;align-items:center;gap:16px">'
                f'{avatar_html(name, size=48)}'
                f'<div style="flex:1">'
                f'<div style="font-weight:700;font-size:15px">{rank}. {name}</div>'
                f'<div style="font-size:13px;color:#64748b">'
                f'{dept} / {pos} ({grade})</div>'
                f'<div style="font-size:12px;color:#94a3b8;margin-top:2px">'
                f'スキル: {skills[:80]}...</div>'
                f'</div>'
                f'<div style="text-align:center;min-width:80px">'
                f'<div style="font-size:32px;font-weight:800;color:{score_color}">'
                f'{ai_score}</div>'
                f'<div style="font-size:11px;color:#94a3b8">AIマッチ</div>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            with st.expander("AI推薦コメント・詳細を見る"):
                st.markdown(
                    f'<div style="background:#f0f9ff;border-radius:6px;padding:12px;'
                    f'font-size:14px;color:#1e293b;line-height:1.7">'
                    f'<strong>推薦理由:</strong><br>{ai_reason}</div>',
                    unsafe_allow_html=True,
                )
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("評価スコア", f"{perf} / 5.0")
                with col_b:
                    eng = float(cand.get("ENGAGEMENT_SCORE") or 50)
                    st.metric("エンゲージメント", f"{eng:.0f} / 100")

            if st.button(
                "📋 プロフィールを見る",
                key=f"profile_link_{emp_id}_{rank}",
                type="secondary",
            ):
                st.session_state["selected_employee_id"] = emp_id
                st.switch_page("pages/3_profile.py")
