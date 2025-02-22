# MCP Blockchain Query Server

[Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that provides tools for querying Bitcoin blockchain data using the Blockchain.com [Data API](https://www.blockchain.com/explorer/api/blockchain_api) and [Query API](https://www.blockchain.com/explorer/api/q).

## Features

- Supports both stdio and SSE transports
- Available [tools](https://modelcontextprotocol.io/docs/concepts/tools):
    - Get block by hash
    - Get transaction by hash
    - Get address by hash
    - Get block count
    - Get difficulty
    - Get address balance
    - Get hash rate
    - Get average transaction size
    - Get total bitcoins
    - Get probability of finding a block
    - Get 24-hour market price
    - Get block interval
    - Get block reward
    - Get next retarget
    - Get latest hash
    - Get unconfirmed count
    - Get 24-hour transaction count

## Installation

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running

Run in stdio mode (default):

    $ python main.py

Run in SSE mode:

    $ python main.py --transport sse --port 8000

CLI Arguments:

- `--port`: Port number for SSE transport (default: 8000)
- `--transport`: Transport type (stdio or sse, default: stdio)
