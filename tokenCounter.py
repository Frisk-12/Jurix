#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 22:34:22 2023

@author: andreadesogus
"""
import tiktoken
from typing import Union, List

#NUMBER OF TOKENS
def num_tokens_from_input(data: Union[str, List[str]]) -> List[int]:
    """Returns the number of tokens for a text string or a list of strings."""
    encoding = tiktoken.get_encoding("cl100k_base")
    
    if isinstance(data, str):
        num_tokens = len(encoding.encode(data))
        return [num_tokens]
    elif isinstance(data, list):
        num_tokens_list = [len(encoding.encode(text)) for text in data]
        return num_tokens_list
    else:
        raise ValueError("Input must be a string or a list of strings")