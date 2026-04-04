-- ============================================================
-- HR Talent Management System - Test Data Generation (~1,000)
-- ============================================================
USE WAREHOUSE HR_WH;
USE DATABASE HR_TALENT_DB;
USE SCHEMA HR;

-- ============================================================
-- 1. DEPARTMENTS (25 departments)
-- ============================================================
INSERT INTO HR.DEPARTMENTS VALUES
-- Level 1 (本部 / Division)
('D001','経営企画本部',     NULL, 1, NULL, CURRENT_TIMESTAMP),
('D002','テクノロジー本部', NULL, 1, NULL, CURRENT_TIMESTAMP),
('D003','リテールバンキング本部', NULL, 1, NULL, CURRENT_TIMESTAMP),
('D004','リスク管理本部',   NULL, 1, NULL, CURRENT_TIMESTAMP),
('D005','コンプライアンス本部', NULL, 1, NULL, CURRENT_TIMESTAMP),
('D006','人事本部',         NULL, 1, NULL, CURRENT_TIMESTAMP),
('D007','財務・経理本部',   NULL, 1, NULL, CURRENT_TIMESTAMP),
-- Level 2 under D002
('D010','システム開発部',         'D002', 2, NULL, CURRENT_TIMESTAMP),
('D011','インフラ基盤部',         'D002', 2, NULL, CURRENT_TIMESTAMP),
('D012','データ&AI推進部',        'D002', 2, NULL, CURRENT_TIMESTAMP),
('D013','サイバーセキュリティ部', 'D002', 2, NULL, CURRENT_TIMESTAMP),
-- Level 2 under D003
('D020','個人ローン部',           'D003', 2, NULL, CURRENT_TIMESTAMP),
('D021','預金・決済サービス部',   'D003', 2, NULL, CURRENT_TIMESTAMP),
('D022','カード・ポイント事業部', 'D003', 2, NULL, CURRENT_TIMESTAMP),
-- Level 2 under D004
('D030','信用リスク管理部',       'D004', 2, NULL, CURRENT_TIMESTAMP),
('D031','市場リスク管理部',       'D004', 2, NULL, CURRENT_TIMESTAMP),
('D032','オペレーショナルリスク部','D004', 2, NULL, CURRENT_TIMESTAMP),
-- Level 2 under D005
('D040','コンプライアンス推進部', 'D005', 2, NULL, CURRENT_TIMESTAMP),
('D041','法務・規制対応部',       'D005', 2, NULL, CURRENT_TIMESTAMP),
-- Level 2 under D006
('D050','採用・人材開発部',       'D006', 2, NULL, CURRENT_TIMESTAMP),
('D051','人事企画部',             'D006', 2, NULL, CURRENT_TIMESTAMP),
-- Level 2 under D007
('D060','財務企画部',             'D007', 2, NULL, CURRENT_TIMESTAMP),
('D061','経理・決算部',           'D007', 2, NULL, CURRENT_TIMESTAMP),
-- Level 2 under D001
('D070','経営企画部',             'D001', 2, NULL, CURRENT_TIMESTAMP),
('D071','IR・広報部',             'D001', 2, NULL, CURRENT_TIMESTAMP);

-- ============================================================
-- 2. POSITIONS (8 levels)
-- ============================================================
INSERT INTO HR.POSITIONS VALUES
('P001','一般職',    'G1','G3', FALSE, 1),
('P002','主任',      'G3','G4', FALSE, 2),
('P003','係長',      'G4','G5', FALSE, 3),
('P004','課長代理',  'G4','G5', FALSE, 4),
('P005','課長',      'G5','G6', TRUE,  5),
('P006','部長代理',  'G5','G6', TRUE,  6),
('P007','部長',      'G7','G7', TRUE,  7),
('P008','本部長',    'G8','G8', TRUE,  8);

-- ============================================================
-- 3. SKILLS (40 skills across 4 categories)
-- ============================================================
INSERT INTO HR.SKILLS VALUES
-- ITスキル
('SK001','Java',              'ITスキル', 1),
('SK002','Python',            'ITスキル', 2),
('SK003','SQL',               'ITスキル', 3),
('SK004','AWS',               'ITスキル', 4),
('SK005','Azure',             'ITスキル', 5),
('SK006','Snowflake',         'ITスキル', 6),
('SK007','React/TypeScript',  'ITスキル', 7),
('SK008','Kubernetes',        'ITスキル', 8),
('SK009','機械学習',          'ITスキル', 9),
('SK010','データ分析',        'ITスキル',10),
-- 金融スキル
('SK011','証券外務員一種',    '金融スキル', 1),
('SK012','FP2級',             '金融スキル', 2),
('SK013','TOEIC 700以上',     '金融スキル', 3),
('SK014','日商簿記2級',       '金融スキル', 4),
('SK015','銀行業務検定',      '金融スキル', 5),
('SK016','宅地建物取引士',    '金融スキル', 6),
('SK017','ローン審査',        '金融スキル', 7),
('SK018','財務分析',          '金融スキル', 8),
('SK019','リスク管理',        '金融スキル', 9),
('SK020','Basel III',         '金融スキル',10),
-- プロジェクト管理
('SK021','PMP',               'プロジェクト管理', 1),
('SK022','PMBOK',             'プロジェクト管理', 2),
('SK023','アジャイル/スクラム','プロジェクト管理',3),
('SK024','JIRA',              'プロジェクト管理', 4),
('SK025','ウォーターフォール', 'プロジェクト管理',5),
-- コンプライアンス
('SK026','マネロン防止',      'コンプライアンス', 1),
('SK027','個人情報保護',      'コンプライアンス', 2),
('SK028','内部監査',          'コンプライアンス', 3),
('SK029','金融規制対応',      'コンプライアンス', 4),
('SK030','情報セキュリティ',  'コンプライアンス', 5),
-- Additional skills
('SK031','統計解析',          'ITスキル',11),
('SK032','BI/Tableau',        'ITスキル',12),
('SK033','CISSP',             'コンプライアンス', 6),
('SK034','内部統制',          'コンプライアンス', 7),
('SK035','MBA',               '金融スキル',11),
('SK036','事業戦略',          '金融スキル',12),
('SK037','M&A',               '金融スキル',13),
('SK038','営業',              '金融スキル',14),
('SK039','カスタマーサクセス','金融スキル',15),
('SK040','採用・HR',          'プロジェクト管理',6);

-- ============================================================
-- 4. EMPLOYEES (1,000 rows via GENERATOR)
-- ============================================================
INSERT INTO HR.EMPLOYEES (
    EMPLOYEE_ID, EMPLOYEE_NAME, EMPLOYEE_NAME_KANA,
    GENDER, DATE_OF_BIRTH, AGE, HIRE_DATE, TENURE_YEARS,
    DEPARTMENT_ID, POSITION_ID, JOB_GRADE, EMPLOYEE_TYPE,
    LOCATION, EMAIL, PHONE, ANNUAL_SALARY,
    PERFORMANCE_SCORE, ENGAGEMENT_SCORE, PROFILE_SUMMARY,
    IS_ACTIVE
)
WITH gen AS (
    SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS rn
    FROM TABLE(GENERATOR(ROWCOUNT => 1000))
),
hashed AS (
    SELECT
        rn,
        MOD(ABS(HASH(rn * 97)),  50) AS h_surname,
        MOD(ABS(HASH(rn * 103)), 2)  AS h_gender,   -- 0=male 1=female
        MOD(ABS(HASH(rn * 107)), 30) AS h_fname,
        MOD(ABS(HASH(rn * 109)), 100) AS h_dept,
        MOD(ABS(HASH(rn * 113)), 100) AS h_pos,
        MOD(ABS(HASH(rn * 127)), 5)  AS h_loc,
        MOD(ABS(HASH(rn * 131)), 10) AS h_type,
        MOD(ABS(HASH(rn * 137)), 35) AS h_age_offset,
        MOD(ABS(HASH(rn * 139)), 25) AS h_tenure,
        MOD(ABS(HASH(rn * 149)), 100) AS h_perf,
        MOD(ABS(HASH(rn * 151)), 80)  AS h_eng
    FROM gen
),
with_name AS (
    SELECT
        rn,
        h_surname, h_gender, h_fname, h_dept, h_pos,
        h_loc, h_type, h_age_offset, h_tenure, h_perf, h_eng,
        CASE h_surname
            WHEN 0  THEN '佐藤' WHEN 1  THEN '鈴木' WHEN 2  THEN '高橋'
            WHEN 3  THEN '田中' WHEN 4  THEN '伊藤' WHEN 5  THEN '渡辺'
            WHEN 6  THEN '山本' WHEN 7  THEN '中村' WHEN 8  THEN '小林'
            WHEN 9  THEN '加藤' WHEN 10 THEN '吉田' WHEN 11 THEN '山田'
            WHEN 12 THEN '佐々木' WHEN 13 THEN '山口' WHEN 14 THEN '松本'
            WHEN 15 THEN '井上' WHEN 16 THEN '木村' WHEN 17 THEN '林'
            WHEN 18 THEN '斎藤' WHEN 19 THEN '清水' WHEN 20 THEN '山崎'
            WHEN 21 THEN '中島' WHEN 22 THEN '池田' WHEN 23 THEN '阿部'
            WHEN 24 THEN '橋本' WHEN 25 THEN '森'   WHEN 26 THEN '石川'
            WHEN 27 THEN '前田' WHEN 28 THEN '藤田' WHEN 29 THEN '岡田'
            WHEN 30 THEN '後藤' WHEN 31 THEN '小川' WHEN 32 THEN '村上'
            WHEN 33 THEN '長谷川' WHEN 34 THEN '近藤' WHEN 35 THEN '石井'
            WHEN 36 THEN '藤原' WHEN 37 THEN '坂本' WHEN 38 THEN '青木'
            WHEN 39 THEN '遠藤' WHEN 40 THEN '西村' WHEN 41 THEN '岡本'
            WHEN 42 THEN '豊田' WHEN 43 THEN '中野' WHEN 44 THEN '原'
            WHEN 45 THEN '島田' WHEN 46 THEN '内田' WHEN 47 THEN '樋口'
            WHEN 48 THEN '江口' ELSE '浜田'
        END AS surname,
        CASE
            WHEN h_gender = 0 THEN
                CASE h_fname
                    WHEN 0  THEN '健'    WHEN 1  THEN '翔太'  WHEN 2  THEN '拓哉'
                    WHEN 3  THEN '健太'  WHEN 4  THEN '雄介'  WHEN 5  THEN '直樹'
                    WHEN 6  THEN '俊介'  WHEN 7  THEN '和也'  WHEN 8  THEN '大輔'
                    WHEN 9  THEN '浩二'  WHEN 10 THEN '智也'  WHEN 11 THEN '隆'
                    WHEN 12 THEN '孝之'  WHEN 13 THEN '誠'    WHEN 14 THEN '博'
                    WHEN 15 THEN '哲也'  WHEN 16 THEN '康弘'  WHEN 17 THEN '祐介'
                    WHEN 18 THEN '亮'    WHEN 19 THEN '淳'    WHEN 20 THEN '純一'
                    WHEN 21 THEN '正'    WHEN 22 THEN '明'    WHEN 23 THEN '剛'
                    WHEN 24 THEN '潤'    WHEN 25 THEN '賢一'  WHEN 26 THEN '克也'
                    WHEN 27 THEN '智'    WHEN 28 THEN '勇'    ELSE '浩'
                END
            ELSE
                CASE h_fname
                    WHEN 0  THEN '恵子'  WHEN 1  THEN '明美'  WHEN 2  THEN '幸子'
                    WHEN 3  THEN '千春'  WHEN 4  THEN '美咲'  WHEN 5  THEN '奈緒'
                    WHEN 6  THEN '亜希子' WHEN 7  THEN '麻衣' WHEN 8  THEN '沙織'
                    WHEN 9  THEN '香'    WHEN 10 THEN '美穂'  WHEN 11 THEN '友美'
                    WHEN 12 THEN '由美'  WHEN 13 THEN '愛'    WHEN 14 THEN '理恵'
                    WHEN 15 THEN '祐子'  WHEN 16 THEN '直美'  WHEN 17 THEN '裕子'
                    WHEN 18 THEN '有美'  WHEN 19 THEN '紗也'  WHEN 20 THEN '彩子'
                    WHEN 21 THEN '里奈'  WHEN 22 THEN '結衣'  WHEN 23 THEN '桃子'
                    WHEN 24 THEN '来夢'  WHEN 25 THEN '遥'    WHEN 26 THEN '涼子'
                    WHEN 27 THEN '早紀'  WHEN 28 THEN '絵里'  ELSE '舞'
                END
        END AS firstname,
        CASE h_dept
            WHEN 0 THEN 'D010' WHEN 1 THEN 'D010' WHEN 2 THEN 'D010'
            WHEN 3 THEN 'D010' WHEN 4 THEN 'D010' WHEN 5 THEN 'D010'
            WHEN 6 THEN 'D010' WHEN 7 THEN 'D010' WHEN 8 THEN 'D010'
            WHEN 9 THEN 'D010' WHEN 10 THEN 'D010' WHEN 11 THEN 'D010'
            WHEN 12 THEN 'D010' WHEN 13 THEN 'D010' WHEN 14 THEN 'D010'
            WHEN 15 THEN 'D011' WHEN 16 THEN 'D011' WHEN 17 THEN 'D011'
            WHEN 18 THEN 'D011' WHEN 19 THEN 'D011' WHEN 20 THEN 'D011'
            WHEN 21 THEN 'D011' WHEN 22 THEN 'D012' WHEN 23 THEN 'D012'
            WHEN 24 THEN 'D012' WHEN 25 THEN 'D012' WHEN 26 THEN 'D012'
            WHEN 27 THEN 'D012' WHEN 28 THEN 'D012' WHEN 29 THEN 'D013'
            WHEN 30 THEN 'D013' WHEN 31 THEN 'D013' WHEN 32 THEN 'D013'
            WHEN 33 THEN 'D013' WHEN 34 THEN 'D013' WHEN 35 THEN 'D013'
            WHEN 36 THEN 'D013' WHEN 37 THEN 'D020' WHEN 38 THEN 'D020'
            WHEN 39 THEN 'D020' WHEN 40 THEN 'D020' WHEN 41 THEN 'D020'
            WHEN 42 THEN 'D020' WHEN 43 THEN 'D020' WHEN 44 THEN 'D020'
            WHEN 45 THEN 'D021' WHEN 46 THEN 'D021' WHEN 47 THEN 'D021'
            WHEN 48 THEN 'D021' WHEN 49 THEN 'D021' WHEN 50 THEN 'D021'
            WHEN 51 THEN 'D021' WHEN 52 THEN 'D021' WHEN 53 THEN 'D022'
            WHEN 54 THEN 'D022' WHEN 55 THEN 'D022' WHEN 56 THEN 'D022'
            WHEN 57 THEN 'D022' WHEN 58 THEN 'D022' WHEN 59 THEN 'D022'
            WHEN 60 THEN 'D030' WHEN 61 THEN 'D030' WHEN 62 THEN 'D030'
            WHEN 63 THEN 'D030' WHEN 64 THEN 'D030' WHEN 65 THEN 'D031'
            WHEN 66 THEN 'D031' WHEN 67 THEN 'D031' WHEN 68 THEN 'D031'
            WHEN 69 THEN 'D032' WHEN 70 THEN 'D032' WHEN 71 THEN 'D032'
            WHEN 72 THEN 'D040' WHEN 73 THEN 'D040' WHEN 74 THEN 'D040'
            WHEN 75 THEN 'D040' WHEN 76 THEN 'D040' WHEN 77 THEN 'D041'
            WHEN 78 THEN 'D041' WHEN 79 THEN 'D041' WHEN 80 THEN 'D041'
            WHEN 81 THEN 'D050' WHEN 82 THEN 'D050' WHEN 83 THEN 'D050'
            WHEN 84 THEN 'D050' WHEN 85 THEN 'D051' WHEN 86 THEN 'D051'
            WHEN 87 THEN 'D051' WHEN 88 THEN 'D060' WHEN 89 THEN 'D060'
            WHEN 90 THEN 'D061' WHEN 91 THEN 'D061' WHEN 92 THEN 'D070'
            WHEN 93 THEN 'D070' WHEN 94 THEN 'D071' WHEN 95 THEN 'D071'
            WHEN 96 THEN 'D001' WHEN 97 THEN 'D002' WHEN 98 THEN 'D003'
            ELSE 'D006'
        END AS dept_id,
        CASE
            WHEN h_pos BETWEEN 0  AND 44 THEN 'P001'
            WHEN h_pos BETWEEN 45 AND 59 THEN 'P002'
            WHEN h_pos BETWEEN 60 AND 71 THEN 'P003'
            WHEN h_pos BETWEEN 72 AND 79 THEN 'P004'
            WHEN h_pos BETWEEN 80 AND 89 THEN 'P005'
            WHEN h_pos BETWEEN 90 AND 94 THEN 'P006'
            WHEN h_pos BETWEEN 95 AND 98 THEN 'P007'
            ELSE 'P008'
        END AS pos_id
    FROM hashed
),
final AS (
    SELECT
        rn,
        'EMP' || LPAD(rn::VARCHAR, 4, '0') AS employee_id,
        surname || ' ' || firstname           AS employee_name,
        (CASE h_gender WHEN 0 THEN '男性' ELSE '女性' END) AS gender,
        dept_id, pos_id,
        CASE pos_id
            WHEN 'P001' THEN CASE WHEN MOD(h_fname,3)=0 THEN 'G1' WHEN MOD(h_fname,3)=1 THEN 'G2' ELSE 'G3' END
            WHEN 'P002' THEN CASE WHEN MOD(h_fname,2)=0 THEN 'G3' ELSE 'G4' END
            WHEN 'P003' THEN 'G4'
            WHEN 'P004' THEN CASE WHEN MOD(h_fname,2)=0 THEN 'G4' ELSE 'G5' END
            WHEN 'P005' THEN CASE WHEN MOD(h_fname,2)=0 THEN 'G5' ELSE 'G6' END
            WHEN 'P006' THEN CASE WHEN MOD(h_fname,2)=0 THEN 'G5' ELSE 'G6' END
            WHEN 'P007' THEN 'G7'
            ELSE 'G8'
        END AS job_grade,
        CASE
            WHEN h_type <= 1 THEN '派遣社員'
            WHEN h_type <= 3 THEN '契約社員'
            ELSE '正社員'
        END AS emp_type,
        CASE h_loc
            WHEN 0 THEN '東京'
            WHEN 1 THEN '東京'
            WHEN 2 THEN '東京'
            WHEN 3 THEN '大阪'
            ELSE '名古屋'
        END AS location,
        -- Age: biased toward 28-50 with mode around 38
        GREATEST(22, LEAST(60,
            24 + h_age_offset + MOD(ABS(HASH(rn*163)), 10)
        )) AS age,
        -- Tenure: 0.5 to 25 years, biased toward lower end
        ROUND(
            CASE
                WHEN h_tenure BETWEEN 0  AND 9  THEN h_tenure * 0.5 + 0.5
                WHEN h_tenure BETWEEN 10 AND 19 THEN (h_tenure - 10) + 5
                ELSE (h_tenure - 20) * 2 + 15
            END
        , 1) AS tenure_years,
        -- Performance: roughly normal around 3.3
        ROUND(GREATEST(1.0, LEAST(5.0,
            3.3 + (h_perf - 50) * 0.014
        )), 1) AS perf_score,
        -- Engagement: 35-100
        GREATEST(35, LEAST(100, 50 + h_eng)) AS eng_score,
        -- Annual salary by grade (万円)
        CASE pos_id
            WHEN 'P001' THEN 350 + h_age_offset * 5
            WHEN 'P002' THEN 480 + h_age_offset * 5
            WHEN 'P003' THEN 560 + h_age_offset * 6
            WHEN 'P004' THEN 650 + h_age_offset * 7
            WHEN 'P005' THEN 800 + h_age_offset * 8
            WHEN 'P006' THEN 950 + h_age_offset * 9
            WHEN 'P007' THEN 1150 + h_age_offset * 10
            ELSE              1400 + h_age_offset * 10
        END AS annual_salary
    FROM with_name
)
SELECT
    employee_id,
    employee_name,
    employee_name AS employee_name_kana,  -- simplified kana
    gender,
    DATEADD('year', -age, DATEADD('month', MOD(ABS(HASH(rn)), 12), '2026-01-01')) AS date_of_birth,
    age,
    DATEADD('year', -tenure_years::INT,
        DATEADD('month', MOD(ABS(HASH(rn*7)), 12), '2026-01-01')) AS hire_date,
    tenure_years,
    dept_id,
    pos_id,
    job_grade,
    emp_type,
    location,
    LOWER(REPLACE(employee_name, ' ', '.')) || '@demo-financial.co.jp' AS email,
    '03-' || LPAD(MOD(ABS(HASH(rn*17)), 9000) + 1000, 4, '0') || '-'
         || LPAD(MOD(ABS(HASH(rn*19)), 9000) + 1000, 4, '0') AS phone,
    annual_salary,
    perf_score,
    eng_score,
    -- Profile summary (template-based)
    employee_name || 'は、Demo Financial Corp の' ||
    CASE pos_id
        WHEN 'P001' THEN '一般職' WHEN 'P002' THEN '主任' WHEN 'P003' THEN '係長'
        WHEN 'P004' THEN '課長代理' WHEN 'P005' THEN '課長'
        WHEN 'P006' THEN '部長代理' WHEN 'P007' THEN '部長' ELSE '本部長'
    END || 'として勤務しています。' ||
    '(' || job_grade || '/ ' || location || ')。' ||
    '入社後' || tenure_years::INT || '年の経験を持ち、' ||
    CASE MOD(ABS(HASH(rn*23)), 5)
        WHEN 0 THEN 'システム開発・クラウド基盤の設計・運用を中心に活躍。'
        WHEN 1 THEN 'データ分析・AI活用推進プロジェクトをリード。'
        WHEN 2 THEN '営業・顧客対応および商品企画を担当。'
        WHEN 3 THEN 'リスク管理・コンプライアンス対応に従事。'
        ELSE 'HR・組織開発・採用戦略の立案・実行を担当。'
    END ||
    CASE WHEN perf_score >= 4.0 THEN '高い評価スコアを継続的に維持し、組織への貢献度が高い。'
         WHEN perf_score >= 3.0 THEN '安定したパフォーマンスでチームに貢献している。'
         ELSE '成長の余地があり、育成計画を策定中。'
    END AS profile_summary,
    TRUE AS is_active
FROM final;

-- ============================================================
-- 5. EMPLOYEE_SKILLS
-- Assign 3-8 skills per employee based on department
-- ============================================================
INSERT INTO HR.EMPLOYEE_SKILLS (EMPLOYEE_ID, SKILL_ID, SKILL_LEVEL, ACQUIRED_DATE)
WITH emp_base AS (
    SELECT
        EMPLOYEE_ID, DEPARTMENT_ID, POSITION_ID, rn
    FROM (
        SELECT EMPLOYEE_ID, DEPARTMENT_ID, POSITION_ID,
               ROW_NUMBER() OVER (ORDER BY EMPLOYEE_ID) AS rn
        FROM HR.EMPLOYEES WHERE IS_ACTIVE = TRUE
    )
),
skill_assignments AS (
    -- Primary skills based on department
    SELECT e.EMPLOYEE_ID,
        CASE
            WHEN e.DEPARTMENT_ID IN ('D010','D011','D012','D013','D002') THEN
                CASE MOD(ABS(HASH(e.rn * 200 + skill_n.n)), 10)
                    WHEN 0 THEN 'SK001' WHEN 1 THEN 'SK002' WHEN 2 THEN 'SK003'
                    WHEN 3 THEN 'SK004' WHEN 4 THEN 'SK005' WHEN 5 THEN 'SK006'
                    WHEN 6 THEN 'SK007' WHEN 7 THEN 'SK008' WHEN 8 THEN 'SK009'
                    ELSE 'SK010'
                END
            WHEN e.DEPARTMENT_ID IN ('D020','D021','D022','D003') THEN
                CASE MOD(ABS(HASH(e.rn * 200 + skill_n.n)), 9)
                    WHEN 0 THEN 'SK011' WHEN 1 THEN 'SK012' WHEN 2 THEN 'SK014'
                    WHEN 3 THEN 'SK015' WHEN 4 THEN 'SK017' WHEN 5 THEN 'SK038'
                    WHEN 6 THEN 'SK039' WHEN 7 THEN 'SK013' ELSE 'SK003'
                END
            WHEN e.DEPARTMENT_ID IN ('D030','D031','D032','D004') THEN
                CASE MOD(ABS(HASH(e.rn * 200 + skill_n.n)), 7)
                    WHEN 0 THEN 'SK019' WHEN 1 THEN 'SK020' WHEN 2 THEN 'SK018'
                    WHEN 3 THEN 'SK031' WHEN 4 THEN 'SK014' WHEN 5 THEN 'SK013'
                    ELSE 'SK010'
                END
            WHEN e.DEPARTMENT_ID IN ('D040','D041','D005') THEN
                CASE MOD(ABS(HASH(e.rn * 200 + skill_n.n)), 6)
                    WHEN 0 THEN 'SK026' WHEN 1 THEN 'SK027' WHEN 2 THEN 'SK028'
                    WHEN 3 THEN 'SK029' WHEN 4 THEN 'SK034' ELSE 'SK033'
                END
            WHEN e.DEPARTMENT_ID IN ('D050','D051','D006') THEN
                CASE MOD(ABS(HASH(e.rn * 200 + skill_n.n)), 5)
                    WHEN 0 THEN 'SK040' WHEN 1 THEN 'SK022' WHEN 2 THEN 'SK027'
                    WHEN 3 THEN 'SK023' ELSE 'SK013'
                END
            WHEN e.DEPARTMENT_ID IN ('D060','D061','D007') THEN
                CASE MOD(ABS(HASH(e.rn * 200 + skill_n.n)), 5)
                    WHEN 0 THEN 'SK018' WHEN 1 THEN 'SK014' WHEN 2 THEN 'SK036'
                    WHEN 3 THEN 'SK031' ELSE 'SK013'
                END
            ELSE
                CASE MOD(ABS(HASH(e.rn * 200 + skill_n.n)), 7)
                    WHEN 0 THEN 'SK035' WHEN 1 THEN 'SK036' WHEN 2 THEN 'SK037'
                    WHEN 3 THEN 'SK021' WHEN 4 THEN 'SK013' WHEN 5 THEN 'SK027'
                    ELSE 'SK003'
                END
        END AS skill_id,
        LEAST(4, GREATEST(1, MOD(ABS(HASH(e.rn + skill_n.n * 17)), 4) + 1)) AS skill_level,
        DATEADD('year', -MOD(ABS(HASH(e.rn + skill_n.n)), 8), CURRENT_DATE()) AS acquired_date
    FROM emp_base e
    CROSS JOIN (
        SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL
        SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5
    ) skill_n
    WHERE skill_n.n < CASE
        WHEN MOD(ABS(HASH(e.rn)), 5) = 0 THEN 3
        WHEN MOD(ABS(HASH(e.rn)), 5) = 1 THEN 4
        WHEN MOD(ABS(HASH(e.rn)), 5) = 2 THEN 5
        WHEN MOD(ABS(HASH(e.rn)), 5) = 3 THEN 6
        ELSE 6
    END
)
SELECT DISTINCT EMPLOYEE_ID, skill_id, skill_level, acquired_date
FROM skill_assignments
WHERE skill_id IS NOT NULL;

-- ============================================================
-- 6. EMPLOYEE_CERTIFICATIONS
-- ============================================================
INSERT INTO HR.EMPLOYEE_CERTIFICATIONS
SELECT
    'CERT' || LPAD(ROW_NUMBER() OVER (ORDER BY e.EMPLOYEE_ID) ::VARCHAR, 6, '0'),
    e.EMPLOYEE_ID,
    CASE MOD(ABS(HASH(e.EMPLOYEE_ID || 'cert')), 8)
        WHEN 0 THEN '証券外務員一種'
        WHEN 1 THEN '日商簿記2級'
        WHEN 2 THEN 'AWS認定ソリューションアーキテクト'
        WHEN 3 THEN '情報処理技術者（応用情報）'
        WHEN 4 THEN 'PMP (Project Management Professional)'
        WHEN 5 THEN 'FP2級'
        WHEN 6 THEN 'TOEIC 800点以上'
        ELSE '銀行業務検定（財務）'
    END AS certification_name,
    CASE MOD(ABS(HASH(e.EMPLOYEE_ID || 'cert')), 8)
        WHEN 0 THEN '日本証券業協会'
        WHEN 1 THEN '日本商工会議所'
        WHEN 2 THEN 'Amazon Web Services'
        WHEN 3 THEN 'IPA情報処理推進機構'
        WHEN 4 THEN 'PMI'
        WHEN 5 THEN '日本FP協会'
        WHEN 6 THEN 'IIBC'
        ELSE '銀行業務検定協会'
    END AS issuer,
    DATEADD('year', -MOD(ABS(HASH(e.EMPLOYEE_ID)), 5), CURRENT_DATE()) AS acquired_date,
    CASE
        WHEN MOD(ABS(HASH(e.EMPLOYEE_ID || 'exp')), 3) = 0 THEN NULL  -- no expiry
        ELSE DATEADD('year', 3 + MOD(ABS(HASH(e.EMPLOYEE_ID || 'exp')), 3),
                     DATEADD('year', -MOD(ABS(HASH(e.EMPLOYEE_ID)), 5), CURRENT_DATE()))
    END AS expiry_date
FROM HR.EMPLOYEES e
WHERE MOD(ABS(HASH(e.EMPLOYEE_ID)), 2) = 0;  -- ~50% have certifications

-- ============================================================
-- 7. APPOINTMENTS (history - ~2 per active employee sampled)
-- ============================================================
INSERT INTO HR.APPOINTMENTS
WITH emp_data AS (
    SELECT EMPLOYEE_ID, DEPARTMENT_ID, POSITION_ID, JOB_GRADE,
           HIRE_DATE, TENURE_YEARS,
           ROW_NUMBER() OVER (ORDER BY EMPLOYEE_ID) AS rn
    FROM HR.EMPLOYEES WHERE IS_ACTIVE = TRUE
),
apt_base AS (
    -- Hiring event for all
    SELECT
        'APT' || LPAD(ROW_NUMBER() OVER (ORDER BY rn) ::VARCHAR, 7, '0') AS appointment_id,
        EMPLOYEE_ID, HIRE_DATE AS appointment_date,
        '採用' AS appointment_type,
        NULL AS from_dept, DEPARTMENT_ID AS to_dept,
        NULL AS from_pos,  POSITION_ID AS to_pos,
        NULL AS from_grade, JOB_GRADE AS to_grade,
        '新卒・中途採用' AS reason,
        HIRE_DATE AS effective_date
    FROM emp_data
    UNION ALL
    -- Transfer/promotion events for tenured employees
    SELECT
        'APT' || LPAD(1000 + ROW_NUMBER() OVER (ORDER BY rn) ::VARCHAR, 7, '0'),
        EMPLOYEE_ID,
        DATEADD('year', MOD(ABS(HASH(rn)), GREATEST(1, TENURE_YEARS::INT)),
                HIRE_DATE) AS appointment_date,
        CASE MOD(ABS(HASH(rn * 7)), 4)
            WHEN 0 THEN '異動'
            WHEN 1 THEN '昇格'
            WHEN 2 THEN '異動'
            ELSE '昇格'
        END AS appointment_type,
        CASE MOD(ABS(HASH(rn * 11)), 10)
            WHEN 0 THEN 'D010' WHEN 1 THEN 'D011' WHEN 2 THEN 'D012'
            WHEN 3 THEN 'D020' WHEN 4 THEN 'D021' WHEN 5 THEN 'D030'
            WHEN 6 THEN 'D040' WHEN 7 THEN 'D050' WHEN 8 THEN 'D060'
            ELSE 'D070'
        END AS from_dept,
        DEPARTMENT_ID AS to_dept,
        CASE MOD(ABS(HASH(rn * 13)), 3)
            WHEN 0 THEN 'P001' WHEN 1 THEN 'P002' ELSE 'P003'
        END AS from_pos,
        POSITION_ID AS to_pos,
        CASE MOD(ABS(HASH(rn * 13)), 3)
            WHEN 0 THEN 'G1' WHEN 1 THEN 'G2' ELSE 'G3'
        END AS from_grade,
        JOB_GRADE AS to_grade,
        CASE MOD(ABS(HASH(rn * 7)), 4)
            WHEN 0 THEN '組織再編に伴う異動'
            WHEN 1 THEN '定期評価による昇格'
            WHEN 2 THEN '本人希望・キャリア開発目的'
            ELSE '事業拡大に伴う増員'
        END AS reason,
        DATEADD('year', MOD(ABS(HASH(rn)), GREATEST(1, TENURE_YEARS::INT)),
                HIRE_DATE) AS effective_date
    FROM emp_data
    WHERE TENURE_YEARS >= 2
)
SELECT * FROM apt_base;

-- ============================================================
-- 8. ANNOUNCEMENTS
-- ============================================================
INSERT INTO HR.ANNOUNCEMENTS VALUES
('ANN001','2026年4月 定期人事異動のお知らせ','2026年4月1日付けで下記の通り人事異動を発令しましたのでお知らせします。詳細については人事部までお問い合わせください。','発令','高','全社員','人事部 山田 太郎','2026-04-01',TRUE, CURRENT_TIMESTAMP),
('ANN002','育児・介護休業規程の改定について','2026年4月1日より育児休業の取得促進に向けた規程改定を実施しました。対象社員は速やかにご確認ください。','制度変更','高','全社員','人事部 山田 太郎','2026-03-28',TRUE, CURRENT_TIMESTAMP),
('ANN003','2026年度 新入社員研修のご案内','2026年4月入社の新入社員研修を下記の通り実施します。メンター社員の方もご確認ください。','研修','中','全社員','採用・人材開発部','2026-03-25',FALSE, CURRENT_TIMESTAMP),
('ANN004','在宅勤務ポリシー更新（2026年版）','ハイブリッドワークポリシーを更新しました。週3日のオフィス勤務を原則とし、残り2日は在宅可とします。','制度変更','中','全社員','人事企画部','2026-03-20',FALSE, CURRENT_TIMESTAMP),
('ANN005','人事評価システム刷新のお知らせ','2026年度より評価システムをリニューアルします。評価基準・スケジュールをご確認ください。','人事お知らせ','中','全社員','人事部','2026-03-15',FALSE, CURRENT_TIMESTAMP),
('ANN006','管理職研修（リーダーシップ強化）募集','課長以上を対象とした外部コーチングプログラムの参加者を募集します。3月末締め切り。','研修','低','管理職','採用・人材開発部','2026-03-10',FALSE, CURRENT_TIMESTAMP),
('ANN007','健康診断スケジュールのご案内','2026年度の定期健康診断スケジュールを公開しました。各自ご確認の上、予約をお願いします。','全社連絡','低','全社員','総務部','2026-03-05',FALSE, CURRENT_TIMESTAMP),
('ANN008','資格取得支援制度 対象資格追加','AWS・Google Cloud資格を資格取得支援対象に追加しました。申請方法は人事ポータルをご参照ください。','制度変更','中','全社員','採用・人材開発部','2026-02-20',FALSE, CURRENT_TIMESTAMP),
('ANN009','2025年度 下期評価フィードバック完了','下期の評価フィードバックが完了しました。マイページからご確認ください。','人事お知らせ','中','全社員','人事部','2026-02-15',FALSE, CURRENT_TIMESTAMP),
('ANN010','新規プロジェクト要員募集（データ&AI部門）','データ&AI推進部の新規プロジェクトに参加するエンジニアを社内公募します。','人事お知らせ','中','全社員','データ&AI推進部','2026-02-01',FALSE, CURRENT_TIMESTAMP);

-- ============================================================
-- 9. MANAGER_ID assignment
-- ============================================================
-- Set dept-level managers (課長以上) as managers of lower-ranked employees
UPDATE HR.EMPLOYEES e
SET MANAGER_ID = (
    SELECT e2.EMPLOYEE_ID
    FROM HR.EMPLOYEES e2
    JOIN HR.POSITIONS p2 ON e2.POSITION_ID = p2.POSITION_ID
    JOIN HR.POSITIONS p1 ON e.POSITION_ID = p1.POSITION_ID
    WHERE e2.DEPARTMENT_ID = e.DEPARTMENT_ID
      AND e2.EMPLOYEE_ID <> e.EMPLOYEE_ID
      AND p2.SORT_ORDER > p1.SORT_ORDER
      AND e2.IS_ACTIVE = TRUE
    ORDER BY p2.SORT_ORDER ASC
    LIMIT 1
)
WHERE IS_ACTIVE = TRUE
  AND POSITION_ID NOT IN ('P007', 'P008');

-- ============================================================
-- 10. Sample TALENT_LISTS
-- ============================================================
INSERT INTO HR.TALENT_LISTS VALUES
('LST001','AI・データ人材リスト','Python/機械学習スキルを持つエンジニアの一覧',
 PARSE_JSON('{"departments":["D010","D011","D012"],"skills":["SK002","SK009","SK010"],"skill_logic":"OR"}'),
 'kmotokubota', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
('LST002','次期管理職候補','G5以上・評価スコア4.0以上の候補者リスト',
 PARSE_JSON('{"job_grades":["G5","G6"],"performance_min":4.0}'),
 'kmotokubota', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
('LST003','新卒3年以内 早期離職リスク','入社3年以内・エンゲージメントスコア低い層',
 PARSE_JSON('{"tenure_max":3,"engagement_max":50}'),
 'kmotokubota', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

INSERT INTO HR.TALENT_LIST_MEMBERS
SELECT 'LST001', e.EMPLOYEE_ID, CURRENT_TIMESTAMP, 'kmotokubota'
FROM HR.EMPLOYEES e
JOIN HR.EMPLOYEE_SKILLS es ON e.EMPLOYEE_ID = es.EMPLOYEE_ID
WHERE es.SKILL_ID IN ('SK002','SK009','SK010')
  AND e.IS_ACTIVE = TRUE
QUALIFY ROW_NUMBER() OVER (PARTITION BY e.EMPLOYEE_ID ORDER BY e.EMPLOYEE_ID) = 1
LIMIT 50;

INSERT INTO HR.TALENT_LIST_MEMBERS
SELECT 'LST002', e.EMPLOYEE_ID, CURRENT_TIMESTAMP, 'kmotokubota'
FROM HR.EMPLOYEES e
WHERE e.JOB_GRADE IN ('G5','G6') AND e.PERFORMANCE_SCORE >= 4.0 AND e.IS_ACTIVE = TRUE
LIMIT 50;

-- Update profile summaries to include skills
UPDATE HR.EMPLOYEES e
SET PROFILE_SUMMARY = PROFILE_SUMMARY || ' 保有スキル: ' || COALESCE((
    SELECT LISTAGG(s.SKILL_NAME, '、') WITHIN GROUP (ORDER BY s.SKILL_NAME)
    FROM HR.EMPLOYEE_SKILLS es
    JOIN HR.SKILLS s ON es.SKILL_ID = s.SKILL_ID
    WHERE es.EMPLOYEE_ID = e.EMPLOYEE_ID
), 'なし') || '。',
    UPDATED_AT = CURRENT_TIMESTAMP
WHERE IS_ACTIVE = TRUE;

SELECT 'Data generation complete' AS STATUS,
       (SELECT COUNT(*) FROM HR.EMPLOYEES) AS EMPLOYEE_COUNT,
       (SELECT COUNT(*) FROM HR.EMPLOYEE_SKILLS) AS SKILL_LINK_COUNT,
       (SELECT COUNT(*) FROM HR.APPOINTMENTS) AS APPOINTMENT_COUNT;
