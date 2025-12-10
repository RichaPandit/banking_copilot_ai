2025-12-10T17:05:26.852111Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:05:26.8521137Z     json_schema = current_handler(schema)
2025-12-10T17:05:26.8521168Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8521226Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:05:26.8521258Z     return self.handler(core_schema)
2025-12-10T17:05:26.8521285Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8521317Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 556, in new_handler_func
2025-12-10T17:05:26.8521349Z     json_schema = js_modify_function(schema_or_field, current_handler)
2025-12-10T17:05:26.8521377Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8521592Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/main.py", line 852, in __get_pydantic_json_schema__
2025-12-10T17:05:26.852163Z     return handler(core_schema)
2025-12-10T17:05:26.8521658Z            ^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8521693Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:05:26.8521737Z     return self.handler(core_schema)
2025-12-10T17:05:26.8521766Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8521799Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:05:26.8521831Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:05:26.8521862Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8521892Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1604, in model_schema
2025-12-10T17:05:26.8521922Z     json_schema = self.generate_inner(schema['schema'])
2025-12-10T17:05:26.852195Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8521981Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:05:26.8522009Z     json_schema = current_handler(schema)
2025-12-10T17:05:26.8522037Z                   ^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8522078Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/_internal/_schema_generation_shared.py", line 37, in __call__
2025-12-10T17:05:26.8522107Z     return self.handler(core_schema)
2025-12-10T17:05:26.8522143Z            ^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8522174Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 511, in handler_func
2025-12-10T17:05:26.8522202Z     json_schema = generate_for_schema_type(schema_or_field)
2025-12-10T17:05:26.852223Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8522263Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1717, in model_fields_schema
2025-12-10T17:05:26.8522293Z     json_schema = self._named_required_fields_schema(named_required_fields)
2025-12-10T17:05:26.8522322Z                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8522355Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 1508, in _named_required_fields_schema
2025-12-10T17:05:26.8522399Z     field_json_schema = self.generate_inner(field).copy()
2025-12-10T17:05:26.8522429Z                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-12-10T17:05:26.8522461Z   File "/tmp/8de380c64c9c336/antenv/lib/python3.11/site-packages/pydantic/json_schema.py", line 578, in generate_inner
2025-12-10T17:05:26.852249Z     json_schema = current_handler(schema)
2025-12-10T17:05:26.8522517Z                   ^^^^^^^^^^^^^^^^^^^^^^^
