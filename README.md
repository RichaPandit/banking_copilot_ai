2025-12-09T13:44:05.7406352Z 2025-12-09 13:44:05,740 INFO banking-mcp: REQ POST / | x-agent-key=None x_agent_key=None
2025-12-09T13:44:05.7453624Z 2025-12-09 13:44:05,745 INFO banking-mcp: RAW BODY: {'jsonrpc': '2.0', 'id': '1', 'method': 'initialize', 'params': {'capabilities': {}, 'clientInfo': {'agentName': 'Credit Risk Copilot', 'appId': '9f5ec673-1dfa-4337-8438-b5b4c76b8a08', 'cdsBotId': '7139856d-d4d1-f011-8544-6045bd067b2f', 'channelId': 'pva-studio', 'name': 'mcs', 'version': '1.0.0'}, 'protocolVersion': '2024-11-05', 'sessionContext': {}}}
2025-12-09T13:44:05.7457376Z 2025-12-09 13:44:05,745 INFO banking-mcp: MCP REQ: id=1 method=initialize
2025-12-09T13:44:05.7459981Z 2025-12-09 13:44:05,745 INFO banking-mcp: DEBUG INITIALIZE RESPONSE: {
2025-12-09T13:44:05.7460075Z   "protocolVersion": "2024-11-05",
2025-12-09T13:44:05.7460109Z   "capabilities": {
2025-12-09T13:44:05.7460139Z     "tools": {
2025-12-09T13:44:05.746017Z       "listChanged": true
2025-12-09T13:44:05.7460224Z     },
2025-12-09T13:44:05.7460255Z     "resources": {
2025-12-09T13:44:05.7460286Z       "listChanged": true
2025-12-09T13:44:05.7460321Z     }
2025-12-09T13:44:05.746035Z   },
2025-12-09T13:44:05.7460384Z   "serverInfo": {
2025-12-09T13:44:05.7460415Z     "name": "BankingMCP",
2025-12-09T13:44:05.7460445Z     "version": "1.0.0"
2025-12-09T13:44:05.7460473Z   }
2025-12-09T13:44:05.7460501Z }
2025-12-09T13:44:05.746673Z 2025-12-09 13:44:05,746 INFO banking-mcp: RESP POST / | status=200
2025-12-09T13:44:05.9938405Z 2025-12-09 13:44:05,993 INFO banking-mcp: REQ POST / | x-agent-key=None x_agent_key=None
2025-12-09T13:44:05.9947773Z 2025-12-09 13:44:05,994 INFO banking-mcp: RAW BODY: {'jsonrpc': '2.0', 'method': 'notifications/initialized'}
2025-12-09T13:44:05.9948034Z 2025-12-09 13:44:05,994 INFO banking-mcp: MCP REQ: id=None method=notifications/initialized
2025-12-09T13:44:05.9953296Z 2025-12-09 13:44:05,994 INFO banking-mcp: Ignoring notification: notifications/initialized
2025-12-09T13:44:05.9953473Z 2025-12-09 13:44:05,994 INFO banking-mcp: RESP POST / | status=204
