2025-12-11T13:05:19.9074216Z Found build manifest file at '/home/site/wwwroot/oryx-manifest.toml'. Deserializing it...
2025-12-11T13:05:19.910345Z Build Operation ID: e88876d962de8be6
2025-12-11T13:05:19.9163626Z Oryx Version: 0.2.20251017.2, Commit: 482d4c55e818733ab33b9d2131f9dc485a21fd03, ReleaseTagName: 20251017.2
2025-12-11T13:05:19.9174352Z Output is compressed. Extracting it...
2025-12-11T13:05:19.9198444Z Extracting '/home/site/wwwroot/output.tar.gz' to directory '/tmp/8de38b57d490c4f'...
2025-12-11T13:05:24.0244225Z App path is set to '/tmp/8de38b57d490c4f'
2025-12-11T13:05:24.2358368Z Writing output script to '/opt/startup/startup.sh'
2025-12-11T13:05:24.5963822Z Using packages from virtual environment antenv located at /tmp/8de38b57d490c4f/antenv.
2025-12-11T13:05:24.5964277Z Updated PYTHONPATH to '/opt/startup/app_logs:/tmp/8de38b57d490c4f/antenv/lib/python3.11/site-packages'
2025-12-11T13:05:24.9543748Z [2025-12-11 13:05:24 +0000] [2121] [INFO] Starting gunicorn 21.2.0
2025-12-11T13:05:24.9549455Z [2025-12-11 13:05:24 +0000] [2121] [INFO] Listening at: http://0.0.0.0:8000 (2121)
2025-12-11T13:05:24.9549649Z [2025-12-11 13:05:24 +0000] [2121] [INFO] Using worker: uvicorn.workers.UvicornWorker
2025-12-11T13:05:24.9583847Z [2025-12-11 13:05:24 +0000] [2122] [INFO] Booting worker with pid: 2122
2025-12-11T13:05:27.3910345Z 2025-12-11 13:05:27,390 WARNING mcp.server.fastmcp.tools.tool_manager: Tool already exists: ping
2025-12-11T13:05:27.4619073Z [2025-12-11 13:05:27 +0000] [2122] [INFO] Started server process [2122]
2025-12-11T13:05:27.4619507Z [2025-12-11 13:05:27 +0000] [2122] [INFO] Waiting for application startup.
2025-12-11T13:05:27.4622814Z [2025-12-11 13:05:27 +0000] [2122] [INFO] Application startup complete.

gunicorn -k uvicorn.workers.UvicornWorker -w 1 mcp_server.main:app

PS C:\Users\ripandit> curl.exe -Method POST -Uri "https://banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net/mcp/" -Headers @{ "Content-Type" = "application/json" } -Body '{ "jsonrpc":"2.0", "id":"1", "method":"tools/list"}'
Warning: built-in manual was disabled at build-time
PS C:\Users\ripandit> curl.exe -Method POST -Uri "https://banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net/" -Headers @{ "Content-Type" = "application/json" } -Body '{ "jsonrpc":"2.0", "id":"1", "method":"tools/list"}'
Warning: built-in manual was disabled at build-time
PS C:\Users\ripandit>
