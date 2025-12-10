2025-12-10T17:35:28.6617933Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 2442, in handle_invalid_for_json_schema
2025-12-10T17:35:28.6618041Z     raise PydanticInvalidForJsonSchema(f'Cannot generate a JsonSchema for {error_info}')
2025-12-10T17:35:28.6618078Z pydantic.errors.PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'pandas.core.frame.DataFrame'>)
2025-12-10T17:35:28.661818Z
2025-12-10T17:35:28.6618212Z For further information visit https://errors.pydantic.dev/2.12/u/invalid-for-json-schema
2025-12-10T17:35:28.6670116Z [2025-12-10 17:35:28 +0000] [2125] [INFO] Worker exiting (pid: 2125)
2025-12-10T17:35:28.7022579Z [2025-12-10 17:35:28 +0000] [2122] [ERROR] Exception in worker process
2025-12-10T17:35:28.7022807Z Traceback (most recent call last):
2025-12-10T17:35:28.7022844Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 609, in spawn_worker
2025-12-10T17:35:28.702287Z     worker.init_process()
2025-12-10T17:35:28.7022899Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 134, in init_process
2025-12-10T17:35:28.7023033Z     self.load_wsgi()
2025-12-10T17:35:28.7023065Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 146, in load_wsgi
2025-12-10T17:35:28.7023236Z     self.wsgi = self.app.wsgi()
2025-12-10T17:35:28.7023263Z                 ^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7023292Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
2025-12-10T17:35:28.7023316Z     self.callable = self.load()
2025-12-10T17:35:28.7023341Z                     ^^^^^^^^^^^
2025-12-10T17:35:28.7023369Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
2025-12-10T17:35:28.7023394Z     return self.load_wsgiapp()
2025-12-10T17:35:28.7023418Z            ^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7023446Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
2025-12-10T17:35:28.7023473Z     return util.import_app(self.app_uri)
2025-12-10T17:35:28.7023598Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7023628Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
2025-12-10T17:35:28.7023652Z     mod = importlib.import_module(module)
2025-12-10T17:35:28.7023677Z           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7023705Z   File "/opt/python/3.11.14/lib/python3.11/importlib/__init__.py", line 126, in import_module
2025-12-10T17:35:28.7023731Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-12-10T17:35:28.7023759Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7023784Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-10T17:35:28.702381Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-10T17:35:28.7023836Z   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2025-12-10T17:35:28.7023861Z   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2025-12-10T17:35:28.7023956Z   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2025-12-10T17:35:28.7023984Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2025-12-10T17:35:28.7024009Z   File "/tmp/8de38115ab235c9/mcp_server/main.py", line 107, in <module>
2025-12-10T17:35:28.7024036Z     mcp_adapter.add_tool(generate_report_internal)
2025-12-10T17:35:28.7024063Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/server.py", line 422, in add_tool
2025-12-10T17:35:28.7024087Z     self._tool_manager.add_tool(
2025-12-10T17:35:28.7024116Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/tools/tool_manager.py", line 57, in add_tool
2025-12-10T17:35:28.702414Z     tool = Tool.from_function(
2025-12-10T17:35:28.7024166Z            ^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7024195Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/tools/base.py", line 76, in from_function
2025-12-10T17:35:28.7024289Z     parameters = func_arg_metadata.arg_model.model_json_schema(by_alias=True)
2025-12-10T17:35:28.7024318Z                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7024347Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/main.py", line 576, in model_json_schema
2025-12-10T17:35:28.7024371Z     return model_json_schema(
2025-12-10T17:35:28.7024394Z            ^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7024421Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 2548, in model_json_schema
2025-12-10T17:35:28.7024448Z     return schema_generator_instance.generate(cls.__pydantic_core_schema__, mode=mode)
2025-12-10T17:35:28.7024475Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7024503Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 415, in generate
2025-12-10T17:35:28.702453Z     json_schema: JsonSchemaValue = self.generate_inner(schema)
2025-12-10T17:35:28.7024615Z                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7024647Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.7024671Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7024696Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7024726Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7024751Z     return self.handler(core_schema)
2025-12-10T17:35:28.7024776Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7024805Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 556, in new_handler_func
2025-12-10T17:35:28.7024831Z     json_schema = js_modify_function(schema_or_field, current_handler)
2025-12-10T17:35:28.7024858Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7025304Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/main.py", line 852, in __get_pydantic_json_schema__
2025-12-10T17:35:28.7025343Z     return handler(core_schema)
2025-12-10T17:35:28.7025371Z            ^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7025401Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7025425Z     return self.handler(core_schema)
2025-12-10T17:35:28.702545Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7025479Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7025505Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7025531Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7025559Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1604, in model_schema
2025-12-10T17:35:28.7025631Z     json_schema = self.generate_inner(schema['schema'])
2025-12-10T17:35:28.7025659Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7025686Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.7025713Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7025738Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7025767Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7025791Z     return self.handler(core_schema)
2025-12-10T17:35:28.7025815Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7025842Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7025868Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7025893Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7026134Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1717, in model_fields_schema
2025-12-10T17:35:28.7026163Z     json_schema = self._named_required_fields_schema(named_required_fields)
2025-12-10T17:35:28.7026189Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.702622Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1508, in _named_required_fields_schema
2025-12-10T17:35:28.7026246Z     field_json_schema = self.generate_inner(field).copy()
2025-12-10T17:35:28.7026272Z                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.70263Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.7026327Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7026354Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7026383Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7026522Z     return self.handler(core_schema)
2025-12-10T17:35:28.7026548Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7026576Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7026601Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7026625Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7026653Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1576, in model_field_schema
2025-12-10T17:35:28.7026677Z     return self.generate_inner(schema['schema'])
2025-12-10T17:35:28.7026701Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7026728Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.7026752Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7026838Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7026871Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7026896Z     return self.handler(core_schema)
2025-12-10T17:35:28.7026919Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7026946Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7026974Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7026999Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7027027Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 921, in is_instance_schema
2025-12-10T17:35:28.7027054Z     return self.handle_invalid_for_json_schema(schema, f'core_schema.IsInstanceSchema ({schema["cls"]})')
2025-12-10T17:35:28.7027082Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7027172Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 2442, in handle_invalid_for_json_schema
2025-12-10T17:35:28.7027282Z     raise PydanticInvalidForJsonSchema(f'Cannot generate a JsonSchema for {error_info}')
2025-12-10T17:35:28.7027315Z pydantic.errors.PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'pandas.core.frame.DataFrame'>)
2025-12-10T17:35:28.7027339Z
2025-12-10T17:35:28.7027366Z For further information visit https://errors.pydantic.dev/2.12/u/invalid-for-json-schema
2025-12-10T17:35:28.7128228Z [2025-12-10 17:35:28 +0000] [2122] [INFO] Worker exiting (pid: 2122)
2025-12-10T17:35:28.721645Z [2025-12-10 17:35:28 +0000] [2124] [ERROR] Exception in worker process
2025-12-10T17:35:28.7216614Z Traceback (most recent call last):
2025-12-10T17:35:28.7216651Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/arbiter.py", line 609, in spawn_worker
2025-12-10T17:35:28.7216779Z     worker.init_process()
2025-12-10T17:35:28.7216811Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 134, in init_process
2025-12-10T17:35:28.7216835Z     self.load_wsgi()
2025-12-10T17:35:28.7216862Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/workers/base.py", line 146, in load_wsgi
2025-12-10T17:35:28.7216886Z     self.wsgi = self.app.wsgi()
2025-12-10T17:35:28.7216909Z                 ^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7217045Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/app/base.py", line 67, in wsgi
2025-12-10T17:35:28.7217069Z     self.callable = self.load()
2025-12-10T17:35:28.7217092Z                     ^^^^^^^^^^^
2025-12-10T17:35:28.721712Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
2025-12-10T17:35:28.7217143Z     return self.load_wsgiapp()
2025-12-10T17:35:28.721724Z            ^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7217269Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
2025-12-10T17:35:28.7217293Z     return util.import_app(self.app_uri)
2025-12-10T17:35:28.7217317Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7217343Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/gunicorn/util.py", line 371, in import_app
2025-12-10T17:35:28.7217367Z     mod = importlib.import_module(module)
2025-12-10T17:35:28.7217395Z           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7217423Z   File "/opt/python/3.11.14/lib/python3.11/importlib/__init__.py", line 126, in import_module
2025-12-10T17:35:28.7217448Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-12-10T17:35:28.7217473Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7217561Z   File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
2025-12-10T17:35:28.7217589Z   File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
2025-12-10T17:35:28.7217614Z   File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
2025-12-10T17:35:28.7217639Z   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
2025-12-10T17:35:28.7217664Z   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
2025-12-10T17:35:28.721769Z   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
2025-12-10T17:35:28.7217716Z   File "/tmp/8de38115ab235c9/mcp_server/main.py", line 107, in <module>
2025-12-10T17:35:28.7217741Z     mcp_adapter.add_tool(generate_report_internal)
2025-12-10T17:35:28.7217768Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/server.py", line 422, in add_tool
2025-12-10T17:35:28.7217793Z     self._tool_manager.add_tool(
2025-12-10T17:35:28.721782Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/tools/tool_manager.py", line 57, in add_tool
2025-12-10T17:35:28.7217887Z     tool = Tool.from_function(
2025-12-10T17:35:28.7217912Z            ^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7217939Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/mcp/server/fastmcp/tools/base.py", line 76, in from_function
2025-12-10T17:35:28.7217964Z     parameters = func_arg_metadata.arg_model.model_json_schema(by_alias=True)
2025-12-10T17:35:28.7217989Z                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7218018Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/main.py", line 576, in model_json_schema
2025-12-10T17:35:28.7218041Z     return model_json_schema(
2025-12-10T17:35:28.7218063Z            ^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.721809Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 2548, in model_json_schema
2025-12-10T17:35:28.721812Z     return schema_generator_instance.generate(cls.__pydantic_core_schema__, mode=mode)
2025-12-10T17:35:28.7218369Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7218398Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 415, in generate
2025-12-10T17:35:28.7218424Z     json_schema: JsonSchemaValue = self.generate_inner(schema)
2025-12-10T17:35:28.7218448Z                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7218475Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.7218499Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7218522Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7218549Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7218574Z     return self.handler(core_schema)
2025-12-10T17:35:28.7218598Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7218715Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 556, in new_handler_func
2025-12-10T17:35:28.7218742Z     json_schema = js_modify_function(schema_or_field, current_handler)
2025-12-10T17:35:28.7218766Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7218909Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/main.py", line 852, in __get_pydantic_json_schema__
2025-12-10T17:35:28.7218936Z     return handler(core_schema)
2025-12-10T17:35:28.7218961Z            ^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7218989Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7219012Z     return self.handler(core_schema)
2025-12-10T17:35:28.7219035Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219062Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7219155Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7219181Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219209Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1604, in model_schema
2025-12-10T17:35:28.7219234Z     json_schema = self.generate_inner(schema['schema'])
2025-12-10T17:35:28.7219258Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219287Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.7219311Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7219335Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219363Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7219386Z     return self.handler(core_schema)
2025-12-10T17:35:28.7219472Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.72195Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7219525Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7219549Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219575Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1717, in model_fields_schema
2025-12-10T17:35:28.7219601Z     json_schema = self._named_required_fields_schema(named_required_fields)
2025-12-10T17:35:28.7219628Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219657Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1508, in _named_required_fields_schema
2025-12-10T17:35:28.7219682Z     field_json_schema = self.generate_inner(field).copy()
2025-12-10T17:35:28.7219708Z                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219793Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.721982Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7219844Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219872Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.7219894Z     return self.handler(core_schema)
2025-12-10T17:35:28.7219916Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7219944Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7219969Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7219993Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.722002Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1576, in model_field_schema
2025-12-10T17:35:28.7220044Z     return self.generate_inner(schema['schema'])
2025-12-10T17:35:28.7220132Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7220161Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:35:28.7220184Z     json_schema = current_handler(schema)
2025-12-10T17:35:28.7220208Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7220236Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:35:28.722026Z     return self.handler(core_schema)
2025-12-10T17:35:28.7220284Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.722031Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:35:28.7220335Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:35:28.7220359Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7220444Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 921, in is_instance_schema
2025-12-10T17:35:28.7220473Z     return self.handle_invalid_for_json_schema(schema, f'core_schema.IsInstanceSchema ({schema["cls"]})')
2025-12-10T17:35:28.7220499Z            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:35:28.7220526Z   File "/tmp/8de38115ab235c9/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 2442, in handle_invalid_for_json_schema
2025-12-10T17:35:28.7220618Z     raise PydanticInvalidForJsonSchema(f'Cannot generate a JsonSchema for {error_info}')
2025-12-10T17:35:28.7220651Z pydantic.errors.PydanticInvalidForJsonSchema: Cannot generate a JsonSchema for core_schema.IsInstanceSchema (<class 'pandas.core.frame.DataFrame'>)
2025-12-10T17:35:28.7220674Z
2025-12-10T17:35:28.7220701Z For further information visit https://errors.pydantic.dev/2.12/u/invalid-for-json-schema
2025-12-10T17:35:28.7305416Z [2025-12-10 17:35:28 +0000] [2124] [INFO] Worker exiting (pid: 2124)
