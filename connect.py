#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:51:14 2024

@author: andreadesogus
"""
    
import json

class APIKeys:
    def __init__(self, config_file='/Users/andreadesogus/Desktop/jurix/production/config.json'):
        self.config_file = config_file

    def load_keys(self):
        with open(self.config_file) as f:
            config = json.load(f)
        return config

    def pinecone_key(self):
        keys = self.load_keys()
        return keys['pinecone_key']

    def aws_key(self):
        keys = self.load_keys()
        return keys['aws_access_key_id'], keys['aws_secret_access_key'], keys['region_name']

    def azure_key(self):
        keys = self.load_keys()
        return keys['azure_api_key'], keys['azure_api_version'], keys['azure_endpoint']

    def openai_key(self):
        keys = self.load_keys()
        return keys['openai_api_key']

