Running the Agent : 
uvicorn nl_query_agent.main:app --reload

Running MCP Inspector : 
cd nl_query_mcp
npx -y @modelcontextprotocol/inspector python mcp_server.py

Exposing the MCP Server:
npx mcp-proxy --port 3000 python mcp_server.py
