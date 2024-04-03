#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 00:34:00 2024

@author: andreadesogus
"""


import time
import base64
import streamlit as st
from logoDisplayer import logoDisplayer
from startSession import StartSession
from libraryManager import LibraryManager
from streamResponse import StreamResponse
from telemetria import Telemetria
from auth import Login
from search import Search
from work import Work


if __name__ == "__main__":
    #General page configuration
    st.set_page_config(layout="wide")
    st.markdown(
        """
        <style>
        body {
            background-color: #FFFFFF; /* Colore di sfondo */
            color: #31333F; /* Colore del testo */
        }
        .stApp {
            background-color: #FFFFFF; /* Colore di sfondo */
        }
        .st-bw {
            color: #31333F; /* Colore del testo */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    state = st.session_state
    img = "https://i.imgur.com/7Kfx7gv.png"
    login = Login(state,img,LibraryManager(state),Telemetria)
    #Authentication Section
    if not login.check_user_login():
        authenticated = login.authentication()
        
    if state.authenticated:
        startSession = StartSession(state, img)
        
        list_tabs, whitespace, css = startSession.tabsHandler()
        t1,t2,t3 = st.tabs([s.center(whitespace,"\u2001") for s in list_tabs])
        st.markdown(css, unsafe_allow_html=True)
        with t1:
            streamResponse  = StreamResponse(state, LibraryManager(state))
            search = Search(state, LibraryManager(state), streamResponse, Telemetria)
            res = search.doSearch()
            #st.write(state)

        #with t2:
        #    # work = Work(state)
        #    # work.doWork()
        #    a,b,c = st.columns([0.15,0.6,0.15])
        #    with b:
        #        st.info(f"🚧 Sarà presto disponibile la funzionalità rivolta ai professionisti per rispondere a domande complesse e preparare una bozza di parere. Stay tuned! 💥")
            
       # with t3:
       #     # upload = Upload(state)
       #     # upload.doUpload()
       #     a,b,c = st.columns([0.15,0.6,0.15])
       #     with b:
       #         st.info("🚧 Sarà presto disponibile la funzionalità per caricare propri documenti personali e interrogarli tenendo in considerazione anche la banca dati di Jurix. Stay tuned! 💥")

        
    
        
