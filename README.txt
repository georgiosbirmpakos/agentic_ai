Running the Agent : 
uvicorn nl_query_agent.main:app --reload

Running MCP : 
cd nl_query_mcp
npx -y @modelcontextprotocol/inspector python mcp_server.py