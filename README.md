2025-12-09T13:23:56.4030291Z 2025-12-09 13:23:56,402 INFO banking-mcp: REQ GET /robots933456.txt | x-agent-key=None x_agent_key=None
2025-12-09T13:23:56.4039146Z 2025-12-09 13:23:56,403 INFO banking-mcp: RESP GET /robots933456.txt | status=404
2025-12-09T13:24:00.5702753Z 2025-12-09 13:24:00,570 INFO banking-mcp: REQ POST / | x-agent-key=None x_agent_key=None
2025-12-09T13:24:00.5738297Z 2025-12-09 13:24:00,573 INFO banking-mcp: RAW BODY: {'jsonrpc': '2.0', 'id': '1', 'method': 'initialize', 'params': {'capabilities': {}, 'clientInfo': {'agentName': 'Credit Risk Copilot', 'appId': '9f5ec673-1dfa-4337-8438-b5b4c76b8a08', 'cdsBotId': '7139856d-d4d1-f011-8544-6045bd067b2f', 'channelId': 'pva-studio', 'name': 'mcs', 'version': '1.0.0'}, 'protocolVersion': '2024-11-05', 'sessionContext': {}}}
2025-12-09T13:24:00.5738915Z 2025-12-09 13:24:00,573 INFO banking-mcp: MCP REQ: id=1 method=initialize
2025-12-09T13:24:00.5740014Z 2025-12-09 13:24:00,573 INFO banking-mcp: DEBUG INITIALIZE RESPONSE: {
2025-12-09T13:24:00.574009Z   "protocolVersion": "2024-11-05",
2025-12-09T13:24:00.5740126Z   "capabilities": {
2025-12-09T13:24:00.5740157Z     "tools": {
2025-12-09T13:24:00.5740188Z       "listChanged": true
2025-12-09T13:24:00.5740244Z     },
2025-12-09T13:24:00.574028Z     "resources": {
2025-12-09T13:24:00.574031Z       "listChanged": true
2025-12-09T13:24:00.5740339Z     }
2025-12-09T13:24:00.574037Z   },
2025-12-09T13:24:00.57404Z   "serverInfo": {
2025-12-09T13:24:00.5740432Z     "name": "BankingMCP",
2025-12-09T13:24:00.5740464Z     "version": "1.0.0"
2025-12-09T13:24:00.5740495Z   }
2025-12-09T13:24:00.5740534Z }
2025-12-09T13:24:00.5742488Z 2025-12-09 13:24:00,574 INFO banking-mcp: RESP POST / | status=200
2025-12-09T13:24:00.8114127Z 2025-12-09 13:24:00,811 INFO banking-mcp: REQ POST / | x-agent-key=None x_agent_key=None
2025-12-09T13:24:00.81262Z 2025-12-09 13:24:00,812 INFO banking-mcp: RAW BODY: {'jsonrpc': '2.0', 'method': 'notifications/initialized'}
2025-12-09T13:24:00.8126321Z 2025-12-09 13:24:00,812 INFO banking-mcp: MCP REQ: id=None method=notifications/initialized
2025-12-09T13:24:00.8126363Z 2025-12-09 13:24:00,812 INFO banking-mcp: Ignoring notification: notifications/initialized
2025-12-09T13:24:00.8131579Z 2025-12-09 13:24:00,812 INFO banking-mcp: RESP POST / | status=204
