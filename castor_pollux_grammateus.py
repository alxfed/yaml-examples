# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from yaml import safe_load as yl
from grammateus import Grammateus
from castor_pollux import rest as cp

location = '/home/alxfed/Gramms/'


def main():
    recorder = Grammateus(location)
    kwargs = """  # this is a string in YAML format
      model:        gemini-2.5-pro-exp-03-25
      mime_type:    text/plain
      modalities:
        - TEXT
      max_tokens:   12768
      n: 2
      stop_sequences:
        - STOP
        - "\nTitle"
      temperature:  0.5
      top_k:        10
      top_p:        0.5
      thinking:     0  # thinking tokens budget. 24576
    """

    instruction = 'You are an eloquent assistant.'

    text_to_continue = 'Were there any coups after that?'

    machine_text = cp.continuation(
        text=text_to_continue,
        instruction=instruction,
        recorder=recorder,
        **yl(kwargs)
    )

    return machine_text


if __name__ == "__main__":
    result = main()
    ...
