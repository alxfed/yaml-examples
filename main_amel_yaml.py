# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from ruamel.yaml import YAML


def test_read_yaml(file_name):
    with open(file_name, "r") as stream:
        try:
            data = YAML().load(stream)
        except Exception as exc:
            print(exc)
    return data


def test_write_yaml(file_name, data):
    with open(file_name, "w") as stream:
        try:
            YAML().dump(data, stream)
        except Exception as exc:
            print(exc)


if __name__ == "__main__":
    """ ruamel.yaml allows for the round-trip use of comments in a YAML file."""
    file_name = "standard_messages.yaml"
    data = test_read_yaml(file_name)
    file_name = "write_test_" + file_name
    test_write_yaml(file_name, data)
    print('Done!')
