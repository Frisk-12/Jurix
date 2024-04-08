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
    state = st.session_state
    state.primaryColor = "#324356"
    state.backgroundColor = "#FFFFFF"
    state.secondaryBackgroundColor = "#EFEFEF"
    state.textColor = "#31333F"
    state.font = "serif"
    st.config.set_option("theme.primaryColor", state.primaryColor)
    st.config.set_option("theme.backgroundColor", state.backgroundColor)
    st.config.set_option(
        "theme.secondaryBackgroundColor", state.secondaryBackgroundColor
    )
    st.config.set_option("theme.textColor", state.textColor)
    st.config.set_option("theme.font", state.font)

    img = "https://i.imgur.com/7Kfx7gv.png"
    login = Login(state,img,LibraryManager(state),Telemetria)
    #Authentication Section
    if not login.check_user_login():
        authenticated = login.authentication()
        
    if state.authenticated:
        startSession = StartSession(state, img)
        
        list_tabs, whitespace, css = startSession.tabsHandler()
        st.info("Scopri il potenziale della nostra esclusiva demo gratuita! Esplora un ricco dataset di prassi e giurisprudenza tributaria aggiornato fino a novembre 2023.")

        #t1,t2,t3 = st.tabs([s.center(whitespace,"\u2001") for s in list_tabs])
        #st.markdown(css, unsafe_allow_html=True)
        #t1 = st.tabs(["Ricerca"])
        #with t1:
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

        
    
        
