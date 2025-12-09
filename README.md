2025-12-09T20:03:53.0161044Z [2025-12-09 20:03:53 +0000] [2123] [ERROR] Exception in worker process
2025-12-09T20:03:53.0161477Z Traceback (most recent call last):
2025-12-09T20:03:53.0161515Z   File "/tmp/8de375d0d25997c/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 609, in spawn_worker
2025-12-09T20:03:53.0161542Z     worker.init_process()
2025-12-09T20:03:53.016157Z   File "/tmp/8de375d0d25997c/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 134, in init_process
2025-12-09T20:03:53.0161594Z     self.load_wsgi()
2025-12-09T20:03:53.0161623Z   File "/tmp/8de375d0d25997c/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 146, in load_wsgi
2025-12-09T20:03:53.0161647Z     self.wsgi = self.app.wsgi()
2025-12-09T20:03:53.0161671Z                 ^^^^^^^^^^^^^^^
2025-12-09T20:03:53.0161698Z   File "/tmp/8de375d0d25997c/antenv/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
2025-12-09T20:03:53.0161723Z     self.callable = self.load()
2025-12-09T20:03:53.0161761Z                     ^^^^^^^^^^^
2025-12-09T20:03:53.0161791Z   File "/tmp/8de375d0d25997c/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
2025-12-09T20:03:53.0161816Z     return self.load_wsgiapp()
2025-12-09T20:03:53.016184Z            ^^^^^^^^^^^^^^^^^^^
2025-12-09T20:03:53.0161868Z   File "/tmp/8de375d0d25997c/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
2025-12-09T20:03:53.0161894Z     return util.import_app(self.app_uri)
2025-12-09T20:03:53.0161935Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T20:03:53.0161963Z   File "/tmp/8de375d0d25997c/antenv/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
2025-12-09T20:03:53.0161987Z     mod = importlib.import_module(module)
2025-12-09T20:03:53.016201Z           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T20:03:53.0162045Z   File "/opt/python/3.11.14/lib/python3.11/importlib/__init__.py", line 126, in import_module
2025-12-09T20:03:53.0162071Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-12-09T20:03:53.0162099Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T20:03:53.0162124Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-09T20:03:53.0162149Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-09T20:03:53.0162175Z   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2025-12-09T20:03:53.0162201Z   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2025-12-09T20:03:53.0162227Z   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2025-12-09T20:03:53.0162253Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2025-12-09T20:03:53.0162281Z   File "/tmp/8de375d0d25997c/mcp_server/main.py", line 65, in <module>
2025-12-09T20:03:53.0162308Z     app.mount("/mcp/", mcp_adapter.asgi)
2025-12-09T20:03:53.0162343Z                        ^^^^^^^^^^^^^^^^
2025-12-09T20:03:53.0162377Z AttributeError: 'FastMCP' object has no attribute 'asgi'
2025-12-09T20:03:53.0188727Z [2025-12-09 20:03:53 +0000] [2123] [INFO] Worker exiting (pid: 2123)
