#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 15:51:14 2024

@author: andreadesogus
"""
    
mport streamlit as st

class APIKeys:
    def __init__(self):
        pass

    def load_keys(self):
        keys = {
            'pinecone_key': st.secrets["pinecone"]["pinecone_api_key"],
            'aws_access_key_id': st.secrets["aws"]["access_key_id"],
            'aws_secret_access_key': st.secrets["aws"]["secret_access_key"],
            'region_name': st.secrets["aws"]["region_name"],
            'azure_api_key': st.secrets["azure"]["azure_api_key"],
            'azure_api_version': st.secrets["azure"]["azure_api_version"],
            'azure_endpoint': st.secrets["azure"]["endpoint"],
            'openai_api_key': st.secrets["openai"]["openai_api_key"]
        }
        return keys

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
