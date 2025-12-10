2025-12-10T14:51:48.3152556Z Traceback (most recent call last):
2025-12-10T14:51:48.3152598Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 609, in spawn_worker
2025-12-10T14:51:48.3152632Z     worker.init_process()
2025-12-10T14:51:48.315267Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 134, in init_process
2025-12-10T14:51:48.3152704Z     self.load_wsgi()
2025-12-10T14:51:48.3152757Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 146, in load_wsgi
2025-12-10T14:51:48.3152789Z     self.wsgi = self.app.wsgi()
2025-12-10T14:51:48.3152818Z                 ^^^^^^^^^^^^^^^
2025-12-10T14:51:48.3152852Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
2025-12-10T14:51:48.3153005Z     self.callable = self.load()
2025-12-10T14:51:48.3153036Z                     ^^^^^^^^^^^
2025-12-10T14:51:48.3153083Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
2025-12-10T14:51:48.3153115Z     return self.load_wsgiapp()
2025-12-10T14:51:48.3153145Z            ^^^^^^^^^^^^^^^^^^^
2025-12-10T14:51:48.315318Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
2025-12-10T14:51:48.3153213Z     return util.import_app(self.app_uri)
2025-12-10T14:51:48.3153244Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T14:51:48.3153278Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
2025-12-10T14:51:48.3153321Z     mod = importlib.import_module(module)
2025-12-10T14:51:48.3153353Z           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T14:51:48.3153386Z   File "/opt/python/3.11.14/lib/python3.11/importlib/__init__.py", line 126, in import_module
2025-12-10T14:51:48.3153418Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-12-10T14:51:48.3153447Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T14:51:48.315348Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-10T14:51:48.3153521Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-10T14:51:48.3153553Z   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2025-12-10T14:51:48.3153585Z   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2025-12-10T14:51:48.3153618Z   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2025-12-10T14:51:48.315365Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2025-12-10T14:51:48.3153685Z   File "/tmp/8de37fb7f2f6c1c/mcp_server/main.py", line 78, in <module>
2025-12-10T14:51:48.3153727Z     mcp_adapter.add_tool("ping", ping)
2025-12-10T14:51:48.3153762Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/server.py", line 422, in add_tool
2025-12-10T14:51:48.3153792Z     self._tool_manager.add_tool(
2025-12-10T14:51:48.3153827Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/tools/tool_manager.py", line 57, in add_tool
2025-12-10T14:51:48.3153859Z     tool = Tool.from_function(
2025-12-10T14:51:48.3153888Z            ^^^^^^^^^^^^^^^^^^^
2025-12-10T14:51:48.3153933Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/tools/base.py", line 60, in from_function
2025-12-10T14:51:48.3153963Z     validate_and_warn_tool_name(func_name)
2025-12-10T14:51:48.3153996Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/mcp/shared/tool_name_validation.py", line 127, in validate_and_warn_tool_name
2025-12-10T14:51:48.3154027Z     result = validate_tool_name(name)
2025-12-10T14:51:48.3154056Z              ^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T14:51:48.315409Z   File "/tmp/8de37fb7f2f6c1c/antenv/lib/python3.11/site-packages/mcp/shared/tool_name_validation.py", line 59, in validate_tool_name
2025-12-10T14:51:48.3154133Z     if len(name) > 128:
2025-12-10T14:51:48.3154163Z        ^^^^^^^^^
2025-12-10T14:51:48.3154194Z TypeError: object of type 'function' has no len()
