-- ============================================================
-- HR Talent Management System - Table Definitions
-- ============================================================

USE WAREHOUSE HR_WH;
USE DATABASE HR_TALENT_DB;
USE SCHEMA HR;

-- ------------------------------------------------------------
-- DEPARTMENTS
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.DEPARTMENTS (
    DEPARTMENT_ID     VARCHAR(10)  PRIMARY KEY,
    DEPARTMENT_NAME   VARCHAR(100) NOT NULL,
    PARENT_ID         VARCHAR(10),
    DEPT_LEVEL        INT          DEFAULT 1,
    DIVISION_HEAD_ID  VARCHAR(10),
    CREATED_AT        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- POSITIONS
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.POSITIONS (
    POSITION_ID     VARCHAR(10)  PRIMARY KEY,
    POSITION_NAME   VARCHAR(50)  NOT NULL,
    JOB_GRADE_MIN   VARCHAR(5),
    JOB_GRADE_MAX   VARCHAR(5),
    IS_MANAGER      BOOLEAN      DEFAULT FALSE,
    SORT_ORDER      INT          DEFAULT 0
);

-- ------------------------------------------------------------
-- EMPLOYEES (master)
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.EMPLOYEES (
    EMPLOYEE_ID         VARCHAR(10)   PRIMARY KEY,
    EMPLOYEE_NAME       VARCHAR(50)   NOT NULL,
    EMPLOYEE_NAME_KANA  VARCHAR(50),
    GENDER              VARCHAR(5),
    DATE_OF_BIRTH       DATE,
    AGE                 INT,
    HIRE_DATE           DATE,
    TENURE_YEARS        FLOAT,
    DEPARTMENT_ID       VARCHAR(10),
    POSITION_ID         VARCHAR(10),
    JOB_GRADE           VARCHAR(5),
    EMPLOYEE_TYPE       VARCHAR(20)   DEFAULT '正社員',
    LOCATION            VARCHAR(30),
    EMAIL               VARCHAR(100),
    PHONE               VARCHAR(20),
    MANAGER_ID          VARCHAR(10),
    ANNUAL_SALARY       INT,
    PERFORMANCE_SCORE   FLOAT,
    ENGAGEMENT_SCORE    FLOAT,
    PROFILE_SUMMARY     TEXT,
    IS_ACTIVE           BOOLEAN       DEFAULT TRUE,
    CREATED_AT          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT          TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- APPOINTMENTS (history)
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.APPOINTMENTS (
    APPOINTMENT_ID     VARCHAR(15)  PRIMARY KEY,
    EMPLOYEE_ID        VARCHAR(10),
    APPOINTMENT_DATE   DATE,
    APPOINTMENT_TYPE   VARCHAR(30),  -- 採用/異動/昇格/降格/出向/転籍/退職
    FROM_DEPARTMENT_ID VARCHAR(10),
    TO_DEPARTMENT_ID   VARCHAR(10),
    FROM_POSITION_ID   VARCHAR(10),
    TO_POSITION_ID     VARCHAR(10),
    FROM_JOB_GRADE     VARCHAR(5),
    TO_JOB_GRADE       VARCHAR(5),
    REASON             TEXT,
    EFFECTIVE_DATE     DATE,
    CREATED_AT         TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- SKILLS (master)
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.SKILLS (
    SKILL_ID        VARCHAR(10)  PRIMARY KEY,
    SKILL_NAME      VARCHAR(100) NOT NULL,
    SKILL_CATEGORY  VARCHAR(50),   -- ITスキル/金融スキル/プロジェクト管理/コンプライアンス
    SORT_ORDER      INT          DEFAULT 0
);

-- ------------------------------------------------------------
-- EMPLOYEE_SKILLS (link)
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.EMPLOYEE_SKILLS (
    EMPLOYEE_ID   VARCHAR(10),
    SKILL_ID      VARCHAR(10),
    SKILL_LEVEL   INT           DEFAULT 3,   -- 1=初級 2=中級 3=上級 4=エキスパート
    ACQUIRED_DATE DATE,
    PRIMARY KEY (EMPLOYEE_ID, SKILL_ID)
);

-- ------------------------------------------------------------
-- EMPLOYEE_CERTIFICATIONS
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.EMPLOYEE_CERTIFICATIONS (
    CERTIFICATION_ID    VARCHAR(15)  PRIMARY KEY,
    EMPLOYEE_ID         VARCHAR(10),
    CERTIFICATION_NAME  VARCHAR(100),
    ISSUER              VARCHAR(100),
    ACQUIRED_DATE       DATE,
    EXPIRY_DATE         DATE
);

-- ------------------------------------------------------------
-- TALENT_LISTS
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.TALENT_LISTS (
    LIST_ID          VARCHAR(15)  PRIMARY KEY,
    LIST_NAME        VARCHAR(100),
    DESCRIPTION      TEXT,
    FILTER_CONFIG    VARIANT,    -- JSON filter conditions
    CREATED_BY       VARCHAR(50),
    CREATED_AT       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT       TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
    IS_AUTO_REFRESH  BOOLEAN     DEFAULT TRUE
);

-- ------------------------------------------------------------
-- TALENT_LIST_MEMBERS
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.TALENT_LIST_MEMBERS (
    LIST_ID      VARCHAR(15),
    EMPLOYEE_ID  VARCHAR(10),
    ADDED_AT     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    ADDED_BY     VARCHAR(50),
    PRIMARY KEY (LIST_ID, EMPLOYEE_ID)
);

-- ------------------------------------------------------------
-- ANNOUNCEMENTS
-- ------------------------------------------------------------
CREATE OR REPLACE TABLE HR.ANNOUNCEMENTS (
    ANNOUNCEMENT_ID  VARCHAR(15)  PRIMARY KEY,
    TITLE            VARCHAR(200),
    CONTENT          TEXT,
    CATEGORY         VARCHAR(30),  -- 発令/制度変更/人事お知らせ/研修/全社連絡
    IMPORTANCE       VARCHAR(5),   -- 高/中/低
    TARGET_AUDIENCE  VARCHAR(50),
    AUTHOR           VARCHAR(50),
    PUBLISH_DATE     DATE,
    IS_PINNED        BOOLEAN      DEFAULT FALSE,
    CREATED_AT       TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Post-creation grants
GRANT SELECT ON ALL TABLES IN SCHEMA HR_TALENT_DB.HR TO ROLE HR_USER_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA HR_TALENT_DB.HR TO ROLE HR_MANAGER_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA HR_TALENT_DB.HR TO ROLE HR_EMPLOYEE_ROLE;
GRANT INSERT, UPDATE ON TABLE HR_TALENT_DB.HR.APPOINTMENTS TO ROLE HR_USER_ROLE;
GRANT INSERT, UPDATE, DELETE ON TABLE HR_TALENT_DB.HR.TALENT_LISTS TO ROLE HR_USER_ROLE;
GRANT INSERT, DELETE ON TABLE HR_TALENT_DB.HR.TALENT_LIST_MEMBERS TO ROLE HR_USER_ROLE;

SELECT 'Tables created successfully' AS STATUS;
