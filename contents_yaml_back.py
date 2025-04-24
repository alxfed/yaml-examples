# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from yaml import safe_load as yl
from yaml import safe_dump as yd

contents = [
    {'parts': [{'text': 'what is it?'}], 'role': 'user'},
    {'parts': [{'text': 'this is a...'}], 'role': 'model'}
]

records = [
    {'role': 'Human','text': 'what is it?'},
    {'role': 'machine', 'text': 'this is a...'}
]

yaml_contents = yd(contents)
yaml_records = yd(records)
...
