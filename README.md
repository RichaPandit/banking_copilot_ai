2025-12-09T18:33:25.6218584Z [2025-12-09 18:33:25 +0000] [2123] [ERROR] Exception in worker process
2025-12-09T18:33:25.6218608Z Traceback (most recent call last):
2025-12-09T18:33:25.621865Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 608, in spawn_worker
2025-12-09T18:33:25.6218677Z     worker.init_process()
2025-12-09T18:33:25.6218709Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 135, in init_process
2025-12-09T18:33:25.6218735Z     self.load_wsgi()
2025-12-09T18:33:25.6218765Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 147, in load_wsgi
2025-12-09T18:33:25.6218792Z     self.wsgi = self.app.wsgi()
2025-12-09T18:33:25.621882Z                 ^^^^^^^^^^^^^^^
2025-12-09T18:33:25.621885Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/app/base.py", line 66, in wsgi
2025-12-09T18:33:25.6218878Z     self.callable = self.load()
2025-12-09T18:33:25.6218906Z                     ^^^^^^^^^^^
2025-12-09T18:33:25.6218943Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 57, in load
2025-12-09T18:33:25.6218979Z     return self.load_wsgiapp()
2025-12-09T18:33:25.6219006Z            ^^^^^^^^^^^^^^^^^^^
2025-12-09T18:33:25.6219038Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 47, in load_wsgiapp
2025-12-09T18:33:25.6219066Z     return util.import_app(self.app_uri)
2025-12-09T18:33:25.6219094Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T18:33:25.6219126Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/util.py", line 370, in import_app
2025-12-09T18:33:25.6219153Z     mod = importlib.import_module(module)
2025-12-09T18:33:25.6219181Z           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T18:33:25.621921Z   File "/opt/python/3.11.14/lib/python3.11/importlib/__init__.py", line 126, in import_module
2025-12-09T18:33:25.6219242Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-12-09T18:33:25.6219283Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T18:33:25.6219312Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-09T18:33:25.6219344Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-09T18:33:25.6219374Z   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2025-12-09T18:33:25.6219402Z   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2025-12-09T18:33:25.6219561Z   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2025-12-09T18:33:25.6219595Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2025-12-09T18:33:25.6219623Z   File "/tmp/8de37501e8eb6b4/mcp_server/main.py", line 15, in <module>
2025-12-09T18:33:25.6219649Z     from mcp.server.fastmcp import MCPServer
2025-12-09T18:33:25.6219682Z ImportError: cannot import name 'MCPServer' from 'mcp.server.fastmcp' (/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/__init__.py)
2025-12-09T18:33:25.6219722Z [2025-12-09 18:33:25 +0000] [2125] [INFO] Worker exiting (pid: 2125)
2025-12-09T18:33:25.6265491Z [2025-12-09 18:33:25 +0000] [2123] [INFO] Worker exiting (pid: 2123)
2025-12-09T18:33:25.6265583Z [2025-12-09 18:33:25 +0000] [2124] [INFO] Worker exiting (pid: 2124)
2025-12-09T18:33:26.3241754Z [2025-12-09 18:33:26 +0000] [2121] [ERROR] Worker (pid:2125) exited with code 3
2025-12-09T18:33:26.3255034Z [2025-12-09 18:33:26 +0000] [2121] [ERROR] Worker (pid:2122) exited with code 3
2025-12-09T18:33:26.326201Z [2025-12-09 18:33:26 +0000] [2121] [ERROR] Worker (pid:2123) exited with code 3
2025-12-09T18:33:26.3267626Z Traceback (most recent call last):
2025-12-09T18:33:26.3267778Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 208, in run
2025-12-09T18:33:26.3267812Z     self.sleep()
2025-12-09T18:33:26.3267869Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 359, in sleep
2025-12-09T18:33:26.3270764Z     ready = select.select([self.PIPE[0]], [], [], 1.0)
2025-12-09T18:33:26.3270838Z             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T18:33:26.3270871Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 241, in handle_chld
2025-12-09T18:33:26.3270898Z     self.reap_workers()
2025-12-09T18:33:26.3270929Z   File "/tmp/8de37501e8eb6b4/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 529, in reap_workers
