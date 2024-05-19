# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import yaml


def test_read_yaml(file_name):
    with open(file_name, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data


def test_write_yaml(file_name, data):
    with open(file_name, "w") as stream:
        try:
            yaml.dump(data, stream)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    """ If you don't need to ingest and write back comments 
    this is enough."""
    file_name = "standard_messages.yaml"  # "standard_messages.yaml"
    data = test_read_yaml(file_name)
    file_name = "write_test_" + file_name
    test_write_yaml(file_name, data)
    print('Done!')