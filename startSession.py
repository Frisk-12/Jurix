#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 12:36:02 2024

@author: andreadesogus
"""

from logoDisplayer import logoDisplayer
import streamlit as st

class StartSession:
    def __init__(self, session_state: str, img: str):
        """
        Initializes the StartSession class.

        Args:
        - session_state (str): The state of the session.
        - img (str): Path to the image file for the logo.
        """
        self.state = session_state
        self.logo = logoDisplayer(img)

    def tabsHandler(self) -> tuple:
        """
        Handles the tabs for the session.

        Returns:
        - tuple: A tuple containing list_tabs, whitespace, and css.
        """
        empty = st.empty()
        cl, cc, cr = st.columns(3)
        
        with cc:
            self.logo.displayLogo()
            st.write("---")
            st.empty()
        
        list_tabs = ["🔍 **Ricerca**", "🛠️ **Elabora**", "📂 **Gestisci**"]
        whitespace = 32
        
        ## Fills and centers each tab label with em-spaces
        css = '''
        <style>
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                font-size: 1.1rem;
            }
        </style>
        '''

        # st.markdown(css, unsafe_allow_html=True)  # Uncomment if needed
        
        return list_tabs, whitespace, css