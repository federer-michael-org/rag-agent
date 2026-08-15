# rag-agent

AWS MCP Server 及び AWS Bedrock Knowledge Base を活用した AI Agent アプリです。
AWS Bedrock Knowledge Base は AWS Bedrock の RAG を構築する必要があるため、これを利用しない形でも実行可能です。

AWS MCP Serverだけを利用した Agent アプリ
- app.py 及び agent.py

AWS MCP Server 及び AWS Bedrock Knowledge Base を活用した Agent アプリ
- app_with_kb.py 及び agent_with_kb.py

## 必要な環境

- Python 3.13 以上
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 
- AWS アカウント（Bedrock へのアクセス権限が必要）

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/federermichael55/rag-agent.git
cd rag-agent
```

### 2. 依存パッケージをインストール

uv を利用：
```bash
uv sync
```
pyenv+venv+pip でも可能ですが、こちらでは割愛

### 3. 環境変数を設定

AWS 認証情報を環境変数に設定します：

ターミナルで以下を実行：

```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_SESSION_TOKEN=your_session_token
```

> `AWS_SESSION_TOKEN` は一時認証情報（AWS SSO や STS）を使う場合に必要です。

### 4. アプリを起動

AWS MCP Server だけを利用する Agent を起動する場合：
```bash
uv run streamlit run app.py
```

起動後、チャット欄に以下を入力して動作を確認してください：
```
AWSでMCPサーバをホスティングする方法を教えて
```
以下のような表示が出ればOK：
![説明テキスト](images/app.png)

AWS MCP Server 及び AWS Bedrock Knowledge Base を活用した Agent を起動する場合：
```bash
uv run streamlit run app_with_kb.py
```

起動後、チャット欄に以下を入力して動作を確認してください：
```
システム設計書を参考に、構築したストレージシステムのS3のライフサイクルルールってどうなっているか教えて
```
> 事前準備として、AWS Bedrock Knowledge Base でのRAGを構築する必要があります（別途ガイド提供します）
以下のような表示が出ればOK：
![説明テキスト](images/app_with_kb.png)

API サーバーを起動する場合：
```bash
uv run uvicorn api_server_with_kb:app --host 0.0.0.0 --port 8000
```
