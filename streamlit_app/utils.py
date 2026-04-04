"""
HR Talent Management - Shared utilities and session management.
"""
import streamlit as st
import pandas as pd
from typing import Optional


DB = "HR_TALENT_DB"
SCHEMA = "HR"
WH = "HR_WH"


def get_session():
    """Return Snowpark session (container runtime via st.connection, local fallback)."""
    try:
        return st.connection("snowflake").session()
    except Exception:
        from snowflake.snowpark import Session
        conn = st.secrets.get("snowflake", {})
        return Session.builder.configs(dict(conn)).create()


@st.cache_data(ttl=300, show_spinner=False)
def run_query(sql: str) -> pd.DataFrame:
    """Execute SQL and return a pandas DataFrame (cached 5 min)."""
    session = get_session()
    return session.sql(sql).to_pandas()


def run_write(sql: str) -> None:
    """Execute a DML statement (not cached)."""
    session = get_session()
    session.sql(sql).collect()


# ---------------------------------------------------------------------------
# Common lookups (cached)
# ---------------------------------------------------------------------------

@st.cache_data(ttl=600, show_spinner=False)
def get_departments():
    return run_query(f"""
        SELECT DEPARTMENT_ID, DEPARTMENT_NAME, PARENT_ID, DEPT_LEVEL
        FROM {DB}.{SCHEMA}.DEPARTMENTS
        ORDER BY DEPT_LEVEL, DEPARTMENT_NAME
    """)


@st.cache_data(ttl=600, show_spinner=False)
def get_positions():
    return run_query(f"""
        SELECT POSITION_ID, POSITION_NAME, IS_MANAGER, SORT_ORDER
        FROM {DB}.{SCHEMA}.POSITIONS
        ORDER BY SORT_ORDER
    """)


@st.cache_data(ttl=600, show_spinner=False)
def get_skills():
    return run_query(f"""
        SELECT SKILL_ID, SKILL_NAME, SKILL_CATEGORY
        FROM {DB}.{SCHEMA}.SKILLS
        ORDER BY SKILL_CATEGORY, SKILL_NAME
    """)


@st.cache_data(ttl=300, show_spinner=False)
def get_employee_list():
    """Lightweight employee list for search/select widgets."""
    return run_query(f"""
        SELECT EMPLOYEE_ID, EMPLOYEE_NAME, DEPARTMENT_ID
        FROM {DB}.{SCHEMA}.EMPLOYEES
        WHERE IS_ACTIVE = TRUE
        ORDER BY EMPLOYEE_NAME
    """)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

GRADE_COLORS = {
    "G1": "#94a3b8", "G2": "#64748b", "G3": "#3b82f6",
    "G4": "#2563eb", "G5": "#7c3aed", "G6": "#db2777",
    "G7": "#dc2626", "G8": "#991b1b",
}

SKILL_CAT_COLORS = {
    "ITスキル":       "#dbeafe",
    "金融スキル":     "#d1fae5",
    "プロジェクト管理": "#fef3c7",
    "コンプライアンス": "#fee2e2",
}

IMPORTANCE_COLORS = {
    "高": "#ef4444",
    "中": "#f59e0b",
    "低": "#10b981",
}


def grade_badge(grade: str) -> str:
    color = GRADE_COLORS.get(grade, "#94a3b8")
    return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:600">{grade}</span>'


def skill_badge(name: str, category: str) -> str:
    bg = SKILL_CAT_COLORS.get(category, "#f3f4f6")
    return (
        f'<span style="background:{bg};padding:3px 8px;border-radius:12px;'
        f'font-size:12px;margin:2px;display:inline-block">{name}</span>'
    )


def importance_dot(importance: str) -> str:
    color = IMPORTANCE_COLORS.get(importance, "#9ca3af")
    return f'<span style="color:{color};font-weight:700">{importance}</span>'


def tenure_label(years: float) -> str:
    if years is None:
        return "-"
    y = int(years)
    m = int((years - y) * 12)
    if y == 0:
        return f"{m}ヶ月"
    return f"{y}年{m}ヶ月" if m > 0 else f"{y}年"


def avatar_html(name: str, size: int = 60) -> str:
    initial = name[0] if name else "?"
    colors = ["#2563eb", "#7c3aed", "#db2777", "#dc2626", "#059669", "#d97706"]
    color = colors[ord(initial) % len(colors)]
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;'
        f'background:{color};color:white;display:flex;align-items:center;'
        f'justify-content:center;font-size:{size//2}px;font-weight:700;'
        f'flex-shrink:0">{initial}</div>'
    )


def perf_color(score: float) -> str:
    if score is None:
        return "#9ca3af"
    if score >= 4.0:
        return "#059669"
    if score >= 3.0:
        return "#2563eb"
    if score >= 2.0:
        return "#f59e0b"
    return "#dc2626"
