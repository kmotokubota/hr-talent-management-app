-- ============================================================
-- HR Talent Management System - Cortex Search Service
-- ============================================================

USE WAREHOUSE HR_WH;
USE DATABASE HR_TALENT_DB;
USE SCHEMA HR;

-- Create Cortex Search Service on employee profile summaries
-- This enables natural language AI talent search
CREATE OR REPLACE CORTEX SEARCH SERVICE HR.EMPLOYEE_SEARCH_SERVICE
  ON PROFILE_SUMMARY
  ATTRIBUTES EMPLOYEE_ID, EMPLOYEE_NAME, DEPARTMENT_NAME, POSITION_NAME,
             JOB_GRADE, SKILLS_TEXT, CERTIFICATIONS_TEXT, GENDER,
             LOCATION, EMPLOYEE_TYPE, PERFORMANCE_SCORE, ENGAGEMENT_SCORE,
             AGE, TENURE_YEARS
  WAREHOUSE = HR_WH
  TARGET_LAG = '1 hour'
  COMMENT = 'AI-powered employee talent search service'
  AS (
    SELECT
      e.EMPLOYEE_ID,
      e.EMPLOYEE_NAME,
      d.DEPARTMENT_NAME,
      p.POSITION_NAME,
      e.JOB_GRADE,
      e.GENDER,
      e.LOCATION,
      e.EMPLOYEE_TYPE,
      e.AGE,
      e.TENURE_YEARS,
      e.PERFORMANCE_SCORE,
      e.ENGAGEMENT_SCORE,
      e.PROFILE_SUMMARY,
      COALESCE(
        (SELECT LISTAGG(s.SKILL_NAME, ', ') WITHIN GROUP (ORDER BY s.SKILL_NAME)
         FROM HR.EMPLOYEE_SKILLS es JOIN HR.SKILLS s ON es.SKILL_ID = s.SKILL_ID
         WHERE es.EMPLOYEE_ID = e.EMPLOYEE_ID),
        ''
      ) AS SKILLS_TEXT,
      COALESCE(
        (SELECT LISTAGG(c.CERTIFICATION_NAME, ', ') WITHIN GROUP (ORDER BY c.CERTIFICATION_NAME)
         FROM HR.EMPLOYEE_CERTIFICATIONS c
         WHERE c.EMPLOYEE_ID = e.EMPLOYEE_ID),
        ''
      ) AS CERTIFICATIONS_TEXT
    FROM HR.EMPLOYEES e
    JOIN HR.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
    JOIN HR.POSITIONS p ON e.POSITION_ID = p.POSITION_ID
    WHERE e.IS_ACTIVE = TRUE
  );

SELECT 'Cortex Search Service created' AS STATUS;
