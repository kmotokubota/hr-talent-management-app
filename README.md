# TalentHub - HR タレントマネジメント

**Streamlit in Snowflake** で構築した人事タレントマネジメントシステムです。**Snowflake Cortex AI** による自然言語人材検索を搭載しています。

## 機能一覧

| ページ | 機能概要 |
|--------|----------|
| ダッシュボード | KPIサマリー・お知らせ・直近の発令情報 |
| 組織図・発令管理 | 組織ツリー(Treemap)・発令履歴・新規発令登録 |
| 従業員プロフィール | 個人プロフィール・スキル・資格・評価スコア |
| 人材サーチ | 12以上のフィルタ条件による多条件検索 |
| 人材リスト | リスト保存・管理・フィルタ条件による自動更新 |
| AI人材検索 | Cortex Search + AI_COMPLETE による自然言語人材マッチング |

## 技術スタック

- **Snowflake** — データウェアハウス、Streamlit in Snowflake（コンテナランタイム）、Cortex AI
- **Streamlit** — UIフレームワーク
- **Snowflake Cortex AI** — `AI_COMPLETE`（LLMスコアリング）/ Cortex Search Service（ベクトル検索）
- **Plotly** — インタラクティブチャート（Treemap・レーダー・ゲージ・棒グラフ）
- **Pandas** — データ操作

## プロジェクト構成

```
streamlit_app/
├── app.py                  # メインエントリーポイント・サイドバーナビゲーション
├── utils.py                # セッション管理・クエリ実行・ヘルパー関数
├── styles.css              # カスタムCSS
├── pyproject.toml          # Python依存パッケージ（コンテナランタイム用）
└── pages/
    ├── 1_dashboard.py      # ダッシュボード
    ├── 2_org_chart.py      # 組織図・発令管理
    ├── 3_profile.py        # 従業員プロフィール
    ├── 4_search.py         # 多条件人材サーチ
    ├── 5_talent_list.py    # 人材リスト管理
    └── 6_ai_search.py      # AI自然言語人材検索

sql/
├── 00_setup.sql            # DB・スキーマ・WH・コンピュートプール・EAI・ロール作成
├── 01_create_tables.sql    # テーブル定義
├── 02_generate_data.sql    # テストデータ生成（従業員1,000名）
├── 03_create_views.sql     # ビュー作成（V_EMPLOYEE_FULL, V_DEPT_HEADCOUNT）
└── 04_cortex_search.sql    # Cortex Search Service 作成
```

## セットアップ手順

### 1. Snowflake インフラ構築

SQLファイルを順番に実行します：

```sql
-- ACCOUNTADMIN で接続
USE ROLE ACCOUNTADMIN;

-- 以下の順番で実行：
-- sql/00_setup.sql      → HR_WH, HR_TALENT_DB, HRスキーマ, コンピュートプール, EAI, ロール
-- sql/01_create_tables.sql → 全テーブル作成
-- sql/02_generate_data.sql → デモデータ投入（従業員約1,000名 + 関連データ）
-- sql/03_create_views.sql  → V_EMPLOYEE_FULL, V_DEPT_HEADCOUNT ビュー作成
-- sql/04_cortex_search.sql → EMPLOYEE_SEARCH_SOURCE テーブル + EMPLOYEE_SEARCH_SERVICE 作成
```

### 2. Streamlit アプリのデプロイ（コンテナランタイム）

```sql
USE ROLE ACCOUNTADMIN;
USE DATABASE HR_TALENT_DB;
USE SCHEMA HR;
USE WAREHOUSE HR_WH;

-- ステージにファイルをアップロード（Snowsight / SnowSQL / snow CLI）
PUT file://streamlit_app/app.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/utils.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/styles.css @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pyproject.toml @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/1_dashboard.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/2_org_chart.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/3_profile.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/4_search.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/5_talent_list.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;
PUT file://streamlit_app/pages/6_ai_search.py @HR_TALENT_DB.HR.HR_STAGE/streamlit_app/pages/ OVERWRITE=TRUE AUTO_COMPRESS=FALSE;

-- コンテナランタイムで Streamlit アプリを作成
CREATE OR REPLACE STREAMLIT HR_TALENT_DB.HR.HR_TALENT_APP
  FROM '@HR_TALENT_DB.HR.HR_STAGE/streamlit_app'
  MAIN_FILE = 'app.py'
  RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
  COMPUTE_POOL = HR_COMPUTE_POOL
  EXTERNAL_ACCESS_INTEGRATIONS = (HR_PYPI_ACCESS_INTEGRATION)
  QUERY_WAREHOUSE = HR_WH
  TITLE = 'TalentHub - HR Portal'
  COMMENT = 'HR Talent Management System - Demo Financial Corp';

-- ライブバージョンをプッシュ（オーナー以外のユーザーがアクセスするために必要）
ALTER STREAMLIT HR_TALENT_DB.HR.HR_TALENT_APP ADD LIVE VERSION FROM LAST;
```

### 3. アプリへのアクセス

デプロイ後、**Snowsight → Projects → Streamlit → HR_TALENT_APP** から開きます。

> コンピュートプールは初回アクセス時に自動でリジュームされます。コンテナのビルドに数分かかる場合があります。

## データ概要

| テーブル | 件数 | 説明 |
|----------|------|------|
| DEPARTMENTS | 25 | 組織階層（本部7 + 部門18） |
| POSITIONS | 8 | 職位（一般職 → 本部長） |
| SKILLS | 40 | 4カテゴリのスキル |
| EMPLOYEES | ~1,000 | 従業員マスタ |
| EMPLOYEE_SKILLS | ~4,500 | 従業員-スキル紐付け |
| EMPLOYEE_CERTIFICATIONS | ~500 | 資格情報 |
| APPOINTMENTS | ~2,000 | 発令履歴 |
| ANNOUNCEMENTS | 10 | お知らせ |
| TALENT_LISTS | 3 | サンプル人材リスト |

## 注意事項

- 全てのデータはデモ用のダミーデータです。従業員名・メールアドレス・組織構成は架空のものです。
- AI機能を利用するには、Snowflake アカウントで Cortex AI が有効になっている必要があります。
- アプリは Snowflake のコンテナランタイム (SPCS) 上で動作します。コンピュートプールと PyPI 外部アクセス統合は `00_setup.sql` で自動作成されます。
