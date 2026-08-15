import os
from mcp.client.stdio import stdio_client, StdioServerParameters
from strands import Agent
from strands.models import BedrockModel
from strands.tools.mcp.mcp_client import MCPClient
from strands.types.content import Messages
from typing import List, Dict

class RagAgent:
    def __init__(self):
        """RAGエージェントを初期化"""
        self.tools = None  # アプリ起動時に setup() で設定される

    def create_stdio_mcp_client(self, command: str, args: List[str], env: Dict) -> MCPClient:
        return MCPClient(
            lambda: stdio_client(
                StdioServerParameters(command=command, args=args, env=env)
            ),
            startup_timeout=60
        )

    def create_agent(self, tools: list):
        return Agent(
            model=BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0"),
            system_prompt="AWSに関する質問はAWS MCP Serverを用いて、システム設計情報についてはBedrock Knowledge Retrieval Base MCP Serverを用いて回答してください。その参考先も明記してください。",
            tools=tools,
            callback_handler=None,
        )

    def setup(self):
        """
        MCPクライアントをアプリ起動時に1回だけ初期化する。
        probeのたびに接続・切断を繰り返さないようにするため。
        FastAPIのlifespanから呼び出す。
        """
        self.aws_mcp_client = self.create_stdio_mcp_client(
            command="uvx",
            args=[
                "--with", "pydantic-settings",
                "mcp-proxy-for-aws@latest",
                "https://aws-mcp.us-east-1.api.aws/mcp",
                "--metadata", "AWS_REGION=us-west-2"
            ],
            env={
                "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
                "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "AWS_SESSION_TOKEN": os.getenv("AWS_SESSION_TOKEN"),
            }
        )
        self.aws_kb_mcp_client = self.create_stdio_mcp_client(
            command="uvx",
            args=["awslabs.bedrock-kb-retrieval-mcp-server@latest"],
            env={
                "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
                "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "AWS_SESSION_TOKEN": os.getenv("AWS_SESSION_TOKEN"),
                "AWS_REGION": "us-west-2",
            }
        )

        # 両クライアントを起動したままにして、ツール一覧を1回だけ取得
        self.aws_mcp_client.__enter__()
        self.aws_kb_mcp_client.__enter__()
        self.tools = self.aws_mcp_client.list_tools_sync()
        self.tools.extend(self.aws_kb_mcp_client.list_tools_sync())

    def teardown(self):
        """アプリ終了時にMCPクライアントを閉じる"""
        self.aws_mcp_client.__exit__(None, None, None)
        self.aws_kb_mcp_client.__exit__(None, None, None)

    async def stream(self, messages: Messages):
        # MCPクライアントはアプリ起動時に初期化済み。
        # probeのたびにAgentを生成してLLM推論だけ行う。
        agent = self.create_agent(tools=self.tools)
        async for event in agent.stream_async(messages):
            if "message" in event:
                yield event["message"]
