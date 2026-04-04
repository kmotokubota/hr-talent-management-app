"""
HR Talent Management - Main Entry Point
Demo Financial Corp
"""
import streamlit as st
import os

st.set_page_config(
    page_title="TalentHub | HR Portal",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load and inject CSS
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state defaults
if "role" not in st.session_state:
    st.session_state["role"] = "HR_ADMIN_ROLE"
if "search_results" not in st.session_state:
    st.session_state["search_results"] = None
if "pending_list_save" not in st.session_state:
    st.session_state["pending_list_save"] = None
if "selected_employee_id" not in st.session_state:
    st.session_state["selected_employee_id"] = None

# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 20px 0; border-bottom: 1px solid #334155; margin-bottom: 16px;">
            <div class="app-title">TalentHub</div>
            <div class="app-subtitle">Demo Financial Corp | HR Portal</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link("app.py", label="ホーム")
    st.page_link("pages/1_dashboard.py",    label="ダッシュボード")
    st.page_link("pages/2_org_chart.py",    label="組織図・発令管理")
    st.page_link("pages/3_profile.py",      label="従業員プロフィール")
    st.page_link("pages/4_search.py",       label="人材サーチ")
    st.page_link("pages/5_talent_list.py",  label="人材リスト")
    st.page_link("pages/6_ai_search.py",    label="AI人材検索")

    st.markdown("<hr style='border-color:#334155;margin:20px 0 12px'>", unsafe_allow_html=True)

    role_labels = {
        "HR_ADMIN_ROLE":    "HR管理者",
        "HR_USER_ROLE":     "HR担当者",
        "HR_MANAGER_ROLE":  "管理職",
        "HR_EMPLOYEE_ROLE": "一般社員",
    }
    selected_role = st.selectbox(
        "ロール切替（デモ用）",
        list(role_labels.keys()),
        format_func=lambda x: role_labels[x],
        index=0,
    )
    st.session_state["role"] = selected_role

    badge_colors = {
        "HR_ADMIN_ROLE":    "#2563eb",
        "HR_USER_ROLE":     "#7c3aed",
        "HR_MANAGER_ROLE":  "#059669",
        "HR_EMPLOYEE_ROLE": "#64748b",
    }
    bc = badge_colors[selected_role]
    lbl = role_labels[selected_role]
    st.markdown(
        f'<div style="margin-top:8px">'
        f'<span style="background:{bc};color:white;padding:4px 10px;border-radius:4px;font-size:12px;font-weight:600">'
        f'{lbl}</span></div>',
        unsafe_allow_html=True,
    )

# ─── Home page content ───────────────────────────────────────────────────────

st.title("HR Talent Management Portal")

st.markdown("""
Demo Financial Corp の HR タレントマネジメントシステムへようこそ。

左側のナビゲーションから各機能にアクセスしてください。

| ページ | 機能概要 |
|---|---|
| **ダッシュボード** | KPIサマリー・お知らせ・直近発令 |
| **組織図・発令管理** | 組織ツリー・発令履歴・新規発令登録 |
| **従業員プロフィール** | 個人プロフィール・スキル・評価 |
| **人材サーチ** | 多条件フィルタによる人材リストアップ |
| **人材リスト** | リスト保存・管理・自動更新 |
| **AI人材検索** | 自然言語でのAI人材マッチング |
""")
