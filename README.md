2025-12-09T18:16:22.5608663Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-12-09T18:16:22.5608688Z     raise exc
2025-12-09T18:16:22.5608723Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-12-09T18:16:22.5608753Z     await app(scope, receive, sender)
2025-12-09T18:16:22.5608788Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/routing.py", line 716, in __call__
2025-12-09T18:16:22.5608817Z     await self.middleware_stack(scope, receive, send)
2025-12-09T18:16:22.560886Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/routing.py", line 736, in app
2025-12-09T18:16:22.5608888Z     await route.handle(scope, receive, send)
2025-12-09T18:16:22.560892Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/routing.py", line 290, in handle
2025-12-09T18:16:22.5608946Z     await self.app(scope, receive, send)
2025-12-09T18:16:22.5608977Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/server.py", line 1089, in __call__
2025-12-09T18:16:22.5609203Z     await self.session_manager.handle_request(scope, receive, send)
2025-12-09T18:16:22.5609236Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/mcp/server/streamable_http_manager.py", line 143, in handle_request
2025-12-09T18:16:22.5609262Z     raise RuntimeError("Task group is not initialized. Make sure to use run().")
2025-12-09T18:16:22.5609287Z RuntimeError: Task group is not initialized. Make sure to use run().
2025-12-09T18:16:23.6832286Z [2025-12-09 18:16:23 +0000] [2122] [ERROR] Exception in ASGI application
2025-12-09T18:16:23.6832623Z Traceback (most recent call last):
2025-12-09T18:16:23.6832666Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/uvicorn/protocols/http/h11_impl.py", line 403, in run_asgi
2025-12-09T18:16:23.6832696Z     result = await app(  # type: ignore[func-returns-value]
2025-12-09T18:16:23.6832726Z              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T18:16:23.6832759Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/uvicorn/middleware/proxy_headers.py", line 60, in __call__
2025-12-09T18:16:23.6832788Z     return await self.app(scope, receive, send)
2025-12-09T18:16:23.6832815Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T18:16:23.6832846Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/fastapi/applications.py", line 1139, in __call__
2025-12-09T18:16:23.6832874Z     await super().__call__(scope, receive, send)
2025-12-09T18:16:23.6832902Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/applications.py", line 107, in __call__
2025-12-09T18:16:23.6832948Z     await self.middleware_stack(scope, receive, send)
2025-12-09T18:16:23.6832983Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 186, in __call__
2025-12-09T18:16:23.6833009Z     raise exc
2025-12-09T18:16:23.6833039Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/middleware/errors.py", line 164, in __call__
2025-12-09T18:16:23.6833068Z     await self.app(scope, receive, _send)
2025-12-09T18:16:23.6833099Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/middleware/cors.py", line 85, in __call__
2025-12-09T18:16:23.6833128Z     await self.app(scope, receive, send)
2025-12-09T18:16:23.683316Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
2025-12-09T18:16:23.6833189Z     await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
2025-12-09T18:16:23.6833219Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 53, in wrapped_app
2025-12-09T18:16:23.6833258Z     raise exc
2025-12-09T18:16:23.6833288Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
2025-12-09T18:16:23.6833316Z     await app(scope, receive, sender)
2025-12-09T18:16:23.6833346Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
2025-12-09T18:16:23.6833373Z     await self.app(scope, receive, send)
2025-12-09T18:16:23.6833406Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/routing.py", line 716, in __call__
2025-12-09T18:16:23.683436Z     await self.middleware_stack(scope, receive, send)
2025-12-09T18:16:23.6834395Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/routing.py", line 736, in app
2025-12-09T18:16:23.6834423Z     await route.handle(scope, receive, send)
2025-12-09T18:16:23.6834455Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/routing.py", line 462, in handle
2025-12-09T18:16:23.6834496Z     await self.app(scope, receive, send)
2025-12-09T18:16:23.6834527Z   File "/tmp/8de374eb5f0898d/antenv/lib/python3.11/site-packages/starlette/applications.py", line 107, in __call__
2025-12-09T18:16:23.6834553Z     await self.middleware_stack(scope, receive, send)
