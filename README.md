2025-12-09T13:09:43.0907454Z 2025-12-09 13:09:43,073 INFO banking-mcp: RESP GET /robots933456.txt | status=404
2025-12-09T13:10:42.6081541Z 2025-12-09 13:10:42,607 INFO banking-mcp: REQ POST / | x-agent-key=None x_agent_key=None
2025-12-09T13:10:42.6119403Z 2025-12-09 13:10:42,611 INFO banking-mcp: RAW BODY: {'jsonrpc': '2.0', 'id': '1', 'method': 'initialize', 'params': {'capabilities': {}, 'clientInfo': {'agentName': 'Credit Risk Copilot', 'appId': '9f5ec673-1dfa-4337-8438-b5b4c76b8a08', 'cdsBotId': '7139856d-d4d1-f011-8544-6045bd067b2f', 'channelId': 'pva-studio', 'name': 'mcs', 'version': '1.0.0'}, 'protocolVersion': '2024-11-05', 'sessionContext': {}}}
2025-12-09T13:10:42.6119679Z 2025-12-09 13:10:42,611 INFO banking-mcp: MCP REQ: id=1 method=initialize
2025-12-09T13:10:42.6125967Z 2025-12-09 13:10:42,612 INFO banking-mcp: DEBUG INITIALIZE RESPONSE: {
2025-12-09T13:10:42.6126139Z   "protocolVersion": "2024-11-05",
2025-12-09T13:10:42.6126176Z   "capabilities": {
2025-12-09T13:10:42.6126208Z     "tools": {
2025-12-09T13:10:42.6126236Z       "listChanged": true
2025-12-09T13:10:42.6126292Z     },
2025-12-09T13:10:42.6126322Z     "resources": {
2025-12-09T13:10:42.6126351Z       "listChanged": true
2025-12-09T13:10:42.6126381Z     }
2025-12-09T13:10:42.6126412Z   },
2025-12-09T13:10:42.612644Z   "serverInfo": {
2025-12-09T13:10:42.6126469Z     "name": "BankingMCP",
2025-12-09T13:10:42.6126498Z     "version": "1.0.0"
2025-12-09T13:10:42.6126524Z   }
2025-12-09T13:10:42.6126549Z }
2025-12-09T13:10:42.6126577Z 2025-12-09 13:10:42,612 INFO banking-mcp: RESP POST / | status=200
2025-12-09T13:10:42.8867899Z 2025-12-09 13:10:42,886 INFO banking-mcp: REQ POST / | x-agent-key=None x_agent_key=None
2025-12-09T13:10:42.8878934Z 2025-12-09 13:10:42,887 INFO banking-mcp: RAW BODY: {'jsonrpc': '2.0', 'method': 'notifications/initialized'}
2025-12-09T13:10:42.8879112Z 2025-12-09 13:10:42,887 INFO banking-mcp: MCP REQ: id=None method=notifications/initialized
2025-12-09T13:10:42.8879158Z 2025-12-09 13:10:42,887 INFO banking-mcp: Ignoring notification: notifications/initialized
2025-12-09T13:10:42.8879191Z 2025-12-09 13:10:42,887 INFO banking-mcp: RESP POST / | status=204
