# TalentHub - HR Talent Management

A human resources talent management system built with **Streamlit in Snowflake**, featuring AI-powered talent search using **Snowflake Cortex**.

## Features

| Page | Description |
|------|-------------|
| Dashboard | KPI summary, announcements, recent appointments |
| Org Chart & Appointments | Organization tree visualization, appointment history, new appointment registration |
| Employee Profile | Individual profiles, skills, certifications, evaluation scores |
| Advanced Search | Multi-condition employee search with 12+ filters |
| Talent Lists | Save and auto-refresh named employee lists |
| AI Talent Search | Natural language search powered by Cortex Search + AI_COMPLETE |

## Tech Stack

- **Snowflake** — Data warehouse, Streamlit in Snowflake hosting, Cortex AI
- **Streamlit** — UI framework
- **Snowflake Cortex AI** — `AI_COMPLETE` / Cortex Search Service
- **Plotly** — Interactive charts (treemap, radar, gauge, bar)
- **Pandas** — Data manipulation

## Project Structure

```
streamlit_app/
├── app.py                  # Main entry point & sidebar navigation
├── utils.py                # Shared session, queries, helpers
├── styles.css              # Custom CSS
└── pages/
    ├── 1_dashboard.py      # Dashboard
    ├── 2_org_chart.py      # Org chart & appointment management
    ├── 3_profile.py        # Employee profile
    ├── 4_search.py         # Advanced multi-condition search
    ├── 5_talent_list.py    # Talent list management
    └── 6_ai_search.py      # AI natural language talent search

sql/
├── 00_setup.sql            # DB, schema, warehouse, roles
├── 01_create_tables.sql    # Table definitions
├── 02_generate_data.sql    # Test data (1,000 employees)
├── 03_create_views.sql     # Views (V_EMPLOYEE_FULL, V_DEPT_HEADCOUNT)
└── 04_cortex_search.sql    # Cortex Search Service
```

## Setup Instructions

### 1. Snowflake Infrastructure

Run SQL files in order:

```sql
-- Connect as ACCOUNTADMIN
USE ROLE ACCOUNTADMIN;

-- Run in sequence:
-- sql/00_setup.sql      → creates HR_WH, HR_TALENT_DB, HR schema, roles
-- sql/01_create_tables.sql → creates all tables
-- sql/02_generate_data.sql → inserts ~1,000 employees + related data
-- sql/03_create_views.sql  → creates V_EMPLOYEE_FULL, V_DEPT_HEADCOUNT
-- sql/04_cortex_search.sql → creates EMPLOYEE_SEARCH_SERVICE
```

### 2. Deploy Streamlit in Snowflake

```sql
USE ROLE ACCOUNTADMIN;
USE DATABASE HR_TALENT_DB;
USE SCHEMA HR;
USE WAREHOUSE HR_WH;

-- Upload files to stage (use Snowsight or SnowSQL)
PUT file://streamlit_app/app.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/utils.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/styles.css @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/1_dashboard.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/2_org_chart.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/3_profile.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/4_search.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/5_talent_list.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/6_ai_search.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;

-- Create Streamlit app
CREATE OR REPLACE STREAMLIT HR_TALENT_DB.HR.HR_TALENT_APP
  ROOT_LOCATION = '@HR_TALENT_DB.HR.HR_STAGE/streamlit_app'
  MAIN_FILE = 'app.py'
  QUERY_WAREHOUSE = 'HR_WH'
  TITLE = 'TalentHub - HR Portal';
```

### 3. Access the App

After deployment, navigate to **Snowsight → Streamlit → HR_TALENT_APP**.

## Data Overview

| Table | Rows | Description |
|-------|------|-------------|
| DEPARTMENTS | 25 | Organization hierarchy (2 levels) |
| POSITIONS | 8 | Job positions (一般職 → 本部長) |
| SKILLS | 40 | Skills across 4 categories |
| EMPLOYEES | ~1,000 | Employee master data |
| EMPLOYEE_SKILLS | ~4,500 | Employee-skill links |
| EMPLOYEE_CERTIFICATIONS | ~500 | Certification records |
| APPOINTMENTS | ~2,000 | Appointment history |
| ANNOUNCEMENTS | 10 | Company announcements |
| TALENT_LISTS | 3 | Sample saved talent lists |

## Notes

- This project uses generic demo data. All employee names, emails, and organizational structures are fictional.
- AI features require Cortex AI to be enabled on the Snowflake account.
- The `COMPUTE_WH` resource monitor may need to be checked if queries fail; use `HR_WH` instead.
