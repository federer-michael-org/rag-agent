# rag-agent

AWS MCP Server および AWS Bedrock Knowledge Base を活用した AI Agent アプリです。

## 必要な環境

- Python 3.13 以上
- [uv](https://docs.astral.sh/uv/getting-started/installation/) または pip
- AWS アカウント（Bedrock へのアクセス権限が必要）

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/federermichael55/rag-agent.git
cd rag-agent
```

### 2. 依存パッケージをインストール

uv を使う場合（推奨）：
```bash
uv sync
```

pip を使う場合：
```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定

`.env` ファイルをプロジェクトルートに作成し、AWS 認証情報を設定します：

```bash
cp .env.example .env
```

`.env` を編集：
```
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_SESSION_TOKEN=your_session_token
```

> `AWS_SESSION_TOKEN` は一時認証情報（AWS SSO や STS）を使う場合に必要です。

### 4. アプリを起動

Streamlit UI を起動する場合：
```bash
uv run streamlit run app.py
```

Knowledge Base 版を使う場合：
```bash
uv run streamlit run app_with_kb.py
```

API サーバーを起動する場合：
```bash
uv run python api_server.py
```
