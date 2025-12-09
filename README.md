2025-12-09T19:42:09.5989448Z
2025-12-09T19:42:09.5989904Z Error: class uri 'uvicorn.workers.UvicornWorker' invalid or not found:
2025-12-09T19:42:09.5990157Z
2025-12-09T19:42:09.5990191Z [Traceback (most recent call last):
2025-12-09T19:42:09.5990229Z   File "/opt/python/3.11.14/lib/python3.11/site-packages/gunicorn/util.py", line 110, in load_class
2025-12-09T19:42:09.5990263Z     mod = importlib.import_module('.'.join(components))
2025-12-09T19:42:09.5990294Z           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T19:42:09.5990328Z   File "/opt/python/3.11.14/lib/python3.11/importlib/__init__.py", line 126, in import_module
2025-12-09T19:42:09.5990411Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-12-09T19:42:09.5990445Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-09T19:42:09.5990477Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-09T19:42:09.5990512Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-09T19:42:09.5990546Z   File "<frozen importlib._bootstrap>", line 1126, in _find_and_load_unlocked
2025-12-09T19:42:09.6016177Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2025-12-09T19:42:09.6016248Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-09T19:42:09.6016293Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-09T19:42:09.6016336Z   File "<frozen importlib._bootstrap>", line 1140, in _find_and_load_unlocked
2025-12-09T19:42:09.6016375Z ModuleNotFoundError: No module named 'uvicorn'
2025-12-09T19:42:09.601641Z ]
2025-12-09T19:42:09.6016594Z
