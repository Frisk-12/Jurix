#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 12:34:24 2024

@author: andreadesogus
"""

import streamlit as st

class logoDisplayer:
    def __init__(self, logo):
        self.logo = logo
    
    def displayLogo(self):
        hide_img_fs = '''
            <style>
            button[title="View fullscreen"]{
                visibility: hidden;}
            </style>
            '''
            
        st.markdown(hide_img_fs, unsafe_allow_html=True)
        return st.image(self.logo)
