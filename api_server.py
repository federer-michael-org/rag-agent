import os
import asyncio
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from agent import RagAgent

app = FastAPI(title="AWS Agent API")

# セッションごとの会話履歴を管理
session_store: dict = {}

# RagAgentはアプリ起動時に1つだけ生成
rag_agent = RagAgent()


# ── リクエスト/レスポンスのスキーマ ──────────────────────────
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str


# ── エンドポイント（1つ） ─────────────────────────────────────
@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    authorization: Optional[str] = Header(None),  # Authorization ヘッダー
):
    # セッションの会話履歴を取得（なければ新規作成）
    if request.session_id not in session_store:
        session_store[request.session_id] = []

    messages = session_store[request.session_id]

    # ユーザーメッセージを履歴に追加
    messages.append({
        "role": "user",
        "content": [{"text": request.message}]
    })

    # Agentを呼び出して返答を収集（ストリーミングなし）
    reply_text = ""
    assistant_message = None
    try:
        async for message in rag_agent.stream(messages):
            if message.get("role") == "assistant":
                for content in message.get("content", []):
                    if "text" in content:
                        reply_text += content["text"]
                assistant_message = message  # 最後のassistantメッセージだけ記録

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 最終的なassistantメッセージだけ履歴に追加（toolUse/toolResultは除外）
    if assistant_message:
        messages.append(assistant_message)

    # 更新した履歴を保存
    session_store[request.session_id] = messages

    return ChatResponse(reply=reply_text, session_id=request.session_id)