PS C:\Users\ripandit> curl.exe -sS -L -X POST "https://banking-ai-mcp-hpg8e8d7dxe0hkf0.uksouth-01.azurewebsites.net/" --header "Content-Type: application/json" --data "{ ""jsonrpc"":""2.0"", ""id"":""1"", ""method"":""initialize""}"
Traceback (most recent call last):
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
    await self.app(scope, receive, send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/routing.py", line 716, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/routing.py", line 736, in app
    await route.handle(scope, receive, send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/routing.py", line 290, in handle
    await self.app(scope, receive, send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/fastapi/routing.py", line 120, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
    raise exc
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/fastapi/routing.py", line 106, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/fastapi/routing.py", line 430, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/8de38b9dd883b2b/antenv/lib/python3.11/site-packages/fastapi/routing.py", line 316, in run_endpoint_function
    return await dependant.call(**values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/8de38b9dd883b2b/mcp_server/main.py", line 74, in root_jsonrpc
    return await mcp_adapter.run_streamable_http_async(body, headers)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: FastMCP.run_streamable_http_async() takes 1 positional argument but 3 were given
