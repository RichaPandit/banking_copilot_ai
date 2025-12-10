C:\Users\ripandit>curl -v -X POST "https://banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net/mcp/" -H "Content-Type: application/json" -H "Accept: application/json" -H "x-agent-key: agent-007" --data-binary "{ \"jsonrpc\":\"2.0\", \"id\":\"2\", \"method\":\"tools/list\" }"
Note: Unnecessary use of -X or --request, POST is already inferred.
* Host banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net:443 was resolved.
* IPv6: (none)
* IPv4: 51.104.28.84
*   Trying 51.104.28.84:443...
* schannel: disabled automatic use of client certificate
* ALPN: curl offers http/1.1
* ALPN: server accepted http/1.1
* Established connection to banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net (51.104.28.84 port 443) from 192.168.1.161 port 62500
* using HTTP/1.x
> POST /mcp/ HTTP/1.1
> Host: banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net
> User-Agent: curl/8.16.0
> Content-Type: application/json
> Accept: application/json
> x-agent-key: agent-007
> Content-Length: 52
>
* upload completely sent off: 52 bytes
* schannel: remote party requests renegotiation
* schannel: renegotiating SSL/TLS connection
* schannel: SSL/TLS connection renegotiated
< HTTP/1.1 404 Not Found
< Content-Length: 9
< Content-Type: text/plain; charset=utf-8
< Date: Wed, 10 Dec 2025 19:46:50 GMT
< Server: uvicorn
<
Not Found* Connection #0 to host banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net:443 left intact
