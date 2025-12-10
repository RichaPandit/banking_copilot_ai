2025-12-10T12:35:02.0327556Z 2025-12-10 12:35:02,032 INFO banking-mcp: ROUTE MOUNTED: /docs
2025-12-10T12:35:02.0327594Z 2025-12-10 12:35:02,032 INFO banking-mcp: ROUTE MOUNTED: /docs/oauth2-redirect
2025-12-10T12:35:02.032818Z 2025-12-10 12:35:02,032 INFO banking-mcp: ROUTE MOUNTED: /redoc
2025-12-10T12:35:02.0338838Z 2025-12-10 12:35:02,032 INFO banking-mcp: ROUTE MOUNTED: /health
2025-12-10T12:35:02.0339074Z 2025-12-10 12:35:02,033 INFO banking-mcp: ROUTE MOUNTED: /
2025-12-10T12:35:02.033995Z 2025-12-10 12:35:02,033 INFO banking-mcp: ROUTE MOUNTED: /mcp
2025-12-10T12:35:02.0430875Z [2025-12-10 12:35:02 +0000] [2125] [ERROR] Exception in worker process
2025-12-10T12:35:02.0431107Z Traceback (most recent call last):
2025-12-10T12:35:02.0431174Z   File "/tmp/8de376089fcdb58/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 609, in spawn_worker
2025-12-10T12:35:02.0431202Z     worker.init_process()
2025-12-10T12:35:02.0431235Z   File "/tmp/8de376089fcdb58/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 134, in init_process
2025-12-10T12:35:02.0431263Z     self.load_wsgi()
2025-12-10T12:35:02.0431292Z   File "/tmp/8de376089fcdb58/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 146, in load_wsgi
2025-12-10T12:35:02.0431319Z     self.wsgi = self.app.wsgi()
2025-12-10T12:35:02.0431346Z                 ^^^^^^^^^^^^^^^
2025-12-10T12:35:02.0431375Z   File "/tmp/8de376089fcdb58/antenv/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
2025-12-10T12:35:02.0431402Z     self.callable = self.load()
2025-12-10T12:35:02.0431428Z                     ^^^^^^^^^^^
2025-12-10T12:35:02.0431463Z   File "/tmp/8de376089fcdb58/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
2025-12-10T12:35:02.0431503Z     return self.load_wsgiapp()
2025-12-10T12:35:02.0431533Z            ^^^^^^^^^^^^^^^^^^^
2025-12-10T12:35:02.0431566Z   File "/tmp/8de376089fcdb58/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
2025-12-10T12:35:02.0431595Z     return util.import_app(self.app_uri)
2025-12-10T12:35:02.0431623Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T12:35:02.0431654Z   File "/tmp/8de376089fcdb58/antenv/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
2025-12-10T12:35:02.0431684Z     mod = importlib.import_module(module)
2025-12-10T12:35:02.0431711Z           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T12:35:02.0431743Z   File "/opt/python/3.11.14/lib/python3.11/importlib/__init__.py", line 126, in import_module
2025-12-10T12:35:02.0431772Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-12-10T12:35:02.0431812Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T12:35:02.0431842Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-10T12:35:02.043187Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-10T12:35:02.0431901Z   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2025-12-10T12:35:02.0431931Z   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2025-12-10T12:35:02.0431961Z   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2025-12-10T12:35:02.043199Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2025-12-10T12:35:02.043202Z   File "/tmp/8de376089fcdb58/mcp_server/main.py", line 79, in <module>
2025-12-10T12:35:02.0432048Z     @mcp_server.tool()
2025-12-10T12:35:02.0432076Z      ^^^^^^^^^^^^^^^
2025-12-10T12:35:02.0432107Z AttributeError: 'Server' object has no attribute 'tool'
