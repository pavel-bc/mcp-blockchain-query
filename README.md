# MCP Blockchain Query Server

[Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that provides tools for querying Bitcoin blockchain data using the [Blockchain.com](https://www.blockchain.com) [Data API](https://www.blockchain.com/explorer/api/blockchain_api) and [Query API](https://www.blockchain.com/explorer/api/q).

## Features

- Supports both stdio and SSE transports
- Available [tools](https://modelcontextprotocol.io/docs/concepts/tools):
    - Retrieve block information by hash
    - Retrieve transaction details by hash
    - Retrieve address information including transaction history
    - Get address balance
    - Get network hash rate
    - Get average transaction size

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
