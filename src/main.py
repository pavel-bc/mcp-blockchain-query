import anyio
import click
import httpx
import mcp.types as types
from mcp.server.lowlevel import Server
from typing import List, Union

BASE_URL = "https://blockchain.info"


async def fetch_blockchain_data(endpoint: str, params: dict = None) -> Union[dict, str]:
    headers = {
        "User-Agent": "MCP Blockchain Server (github.com/modelcontextprotocol/python-sdk)"
    }
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
        url = f"{BASE_URL}/{endpoint}"
        response = await client.get(url, params=params)
        response.raise_for_status()
        # Simple Query API returns plain text, while raw endpoints return JSON
        if endpoint.startswith("q/"):
            return response.text
        return response.json()


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    app = Server("mcp-blockchain-query")

    @app.call_tool()
    async def blockchain_tool(
        name: str, arguments: dict
    ) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
        if name == "get_block":
            if "block_hash" not in arguments:
                raise ValueError("Missing required argument 'block_hash'")
            data = await fetch_blockchain_data(f"rawblock/{arguments['block_hash']}")
            return [types.TextContent(type="text", text=str(data))]

        elif name == "get_transaction":
            if "tx_hash" not in arguments:
                raise ValueError("Missing required argument 'tx_hash'")
            data = await fetch_blockchain_data(f"rawtx/{arguments['tx_hash']}")
            return [types.TextContent(type="text", text=str(data))]

        elif name == "get_address":
            if "address" not in arguments:
                raise ValueError("Missing required argument 'address'")
            params = {"limit": arguments.get("limit", 50)}
            data = await fetch_blockchain_data(
                f"rawaddr/{arguments['address']}", params
            )
            return [types.TextContent(type="text", text=str(data))]

        elif name == "get_difficulty":
            data = await fetch_blockchain_data("q/getdifficulty")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_block_count":
            data = await fetch_blockchain_data("q/getblockcount")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_address_balance":
            if "address" not in arguments:
                raise ValueError("Missing required argument 'address'")
            params = {"confirmations": arguments.get("confirmations", 0)}
            data = await fetch_blockchain_data(
                f"q/addressbalance/{arguments['address']}", params
            )
            return [types.TextContent(type="text", text=data)]

        elif name == "get_hash_rate":
            data = await fetch_blockchain_data("q/hashrate")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_avg_tx_size":
            blocks = arguments.get("blocks", 1000)
            data = await fetch_blockchain_data(f"q/avgtxsize/{blocks}")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_total_bitcoins":
            data = await fetch_blockchain_data("q/totalbc")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_probability":
            hashrate = arguments.get("hashrate", 1)
            data = await fetch_blockchain_data(f"q/probability/{hashrate}")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_market_price":
            data = await fetch_blockchain_data("q/24hrprice")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_block_interval":
            data = await fetch_blockchain_data("q/interval")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_block_reward":
            data = await fetch_blockchain_data("q/bcperblock")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_next_retarget":
            data = await fetch_blockchain_data("q/nextretarget")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_latest_hash":
            data = await fetch_blockchain_data("q/latesthash")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_unconfirmed_count":
            data = await fetch_blockchain_data("q/unconfirmedcount")
            return [types.TextContent(type="text", text=data)]

        elif name == "get_24h_tx_count":
            data = await fetch_blockchain_data("q/24hrtransactioncount")
            return [types.TextContent(type="text", text=data)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    @app.list_tools()
    async def list_tools() -> List[types.Tool]:
        return [
            types.Tool(
                name="get_block",
                description="Fetches information about a specific block",
                inputSchema={
                    "type": "object",
                    "required": ["block_hash"],
                    "properties": {
                        "block_hash": {
                            "type": "string",
                            "description": "The block hash to query",
                        }
                    },
                },
            ),
            types.Tool(
                name="get_transaction",
                description="Fetches information about a specific transaction",
                inputSchema={
                    "type": "object",
                    "required": ["tx_hash"],
                    "properties": {
                        "tx_hash": {
                            "type": "string",
                            "description": "The transaction hash to query",
                        }
                    },
                },
            ),
            types.Tool(
                name="get_address",
                description="Fetches information about a Bitcoin address",
                inputSchema={
                    "type": "object",
                    "required": ["address"],
                    "properties": {
                        "address": {
                            "type": "string",
                            "description": "The Bitcoin address to query",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Number of transactions to return (default: 50)",
                            "default": 50,
                        },
                    },
                },
            ),
            types.Tool(
                name="get_difficulty",
                description="Returns the current Bitcoin network difficulty",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_block_count",
                description="Returns the current block height in the Bitcoin blockchain",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_address_balance",
                description="Returns the balance of a Bitcoin address in satoshis",
                inputSchema={
                    "type": "object",
                    "required": ["address"],
                    "properties": {
                        "address": {
                            "type": "string",
                            "description": "The Bitcoin address to query",
                        },
                        "confirmations": {
                            "type": "integer",
                            "description": "Minimum confirmations for included transactions (default: 0)",
                            "default": 0,
                        },
                    },
                },
            ),
            types.Tool(
                name="get_hash_rate",
                description="Returns the estimated network hash rate in GH/s",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_avg_tx_size",
                description="Returns the average transaction size over a specified number of blocks",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "blocks": {
                            "type": "integer",
                            "description": "Number of blocks to average (default: 1000)",
                            "default": 1000,
                        }
                    },
                },
            ),
            types.Tool(
                name="get_total_bitcoins",
                description="Returns the total number of bitcoins that have been mined",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_probability",
                description="Returns the probability of finding a block with the specified hashrate in GH/s",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "hashrate": {
                            "type": "number",
                            "description": "Hashrate in GH/s (default: 1)",
                            "default": 1,
                        }
                    },
                },
            ),
            types.Tool(
                name="get_market_price",
                description="Returns the 24-hour market price in USD",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_block_interval",
                description="Returns the average time between blocks in seconds",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_block_reward",
                description="Returns the current block reward in BTC",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_next_retarget",
                description="Returns the block height of the next difficulty retarget",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_latest_hash",
                description="Returns the hash of the latest block",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_unconfirmed_count",
                description="Returns the number of unconfirmed transactions in the mempool",
                inputSchema={"type": "object", "properties": {}},
            ),
            types.Tool(
                name="get_24h_tx_count",
                description="Returns the number of transactions in the last 24 hours",
                inputSchema={"type": "object", "properties": {}},
            ),
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0


# Add this if you want the file to be directly runnable
if __name__ == "__main__":
    main()
