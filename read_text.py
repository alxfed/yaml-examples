# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import yaml

file_name = '/home/alxfed/Documents/Fairytales/sow-anne.txt'
with open(file_name, 'r', encoding='utf-8') as file:
    text = file.read()

# text = text.replace('\u2013', '-')
# replacements = {
#     '\u2013': '-',  # en dash
#     '\u2014': '--',  # em dash
#     '\u2018': "'",   # left single quote
#     '\u2019': "'",   # right single quote
#     '\u201c': '"',   # left double quote
#     '\u201d': '"'    # right double quote
# }
#
# for old, new in replacements.items():
#     text = text.replace(old, new)
instruction = 'I am Joseph Jacobs, I retell English folk tales.'
initial_text = 'Once upon a time, when pigs drank wine '
intro = dict(role='user', parts=[dict(text=initial_text)])
records = [intro]
record = dict(role='model', parts=[dict(text=text)])
records.append(record)
# continuation = 'Please continue, I am listening.'
# ending = dict(role='user', parts=[dict(text=continuation)])
# records.append(ending)

yaml_file = '/home/alxfed/Documents/Fairytales/sow-anne.yaml'
with open(yaml_file, "w") as stream:
    try:
        yaml.dump(records, stream,  default_flow_style=False, sort_keys=False)
    except yaml.YAMLError as exc:
        print(exc)

print(text)
...