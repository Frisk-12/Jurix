#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 19:44:23 2024

@author: andreadesogus
"""

from typing import Dict, List
import streamlit as st
import time

class Work:
    def __init__(self, session_state: Dict) -> None:
        """
        Initialize the Work class.

        Parameters:
        - session_state (dict): The session state dictionary.
        """
        self.state = session_state
        # Initialize DDB table
        self.ddbs, self.ddbt = libraryManager.load_ddb_table()

    def streamOpenAI_funct(self, system: str, question: str) -> str:
        """
        Call Azure OpenAI to generate a response based on the given system and question.

        Parameters:
        - system (str): The system description.
        - question (str): The user's question.

        Returns:
        - str: The response from Azure OpenAI.
        """
        delay_time = 0.01  # faster
        answer = ''
        start_time = time.time()
        # Call Azure OpenAI API for response
        response = response_builder(system, question, 5000, "", "", True, "")
        return response

    def multiSelect(self) -> List[str]:
        """
        Display a multiselect widget to choose documents to work on.

        Returns:
        - list: The selected document titles.
        """
        # Display multiselect widget
        choice = st.multiselect("On which document would you like to work?", [list(k.values())[0] for k in self.state.results])
        return choice

    def streamOpenAI(self) -> None:
        """
        Stream document content and user's question to Azure OpenAI and display the response.
        """
        def get_key_from_value(choices: List[Dict[str, str]], value: str) -> str:
            """
            Get the key corresponding to a given value in a list of dictionaries.

            Parameters:
            - choices (list): List of dictionaries.
            - value (str): The value to search for.

            Returns:
            - str: The key corresponding to the value.
            """
            for c in choices:
                for key, val in c.items():
                    if val == value:
                        return key
            return None
        
        # Get text content of selected documents
        texts = [self.ddbt.get_item(get_key_from_value(self.state.results, i)) for i in self.state.choice]
        for t in texts:
            with st.container(border=True):
                # Define system description for Azure OpenAI
                system = "You are a legal AI and you must always provide an answer to clarifications or doubts regarding legal documents that users provide. If possible, also take this request into account when responding: " + self.state.query + "###\n\n Here is the text to base the response on:\n "
                # Generate response from Azure OpenAI
                response = self.streamOpenAI_funct(system=system+"Title: "+t['Item']['doc_id']+"\n"+t['Item']['contentText'] + "\n\n",
                                     question=self.state.query)
                full_resp = ""
                with st.empty():
                    for event in response: 
                        time.sleep(0.01)
                        if str(event.choices[0].delta.content) and str(event.choices[0].delta.content) != "None":
                            full_resp+=str(event.choices[0].delta.content)
                            st.markdown(f"{t['Item']['doc_id']}\n\n" + full_resp)

    def doWork(self) -> None:
        """
        Perform work based on user's selected documents and question.
        """
        if "results" in self.state:
            # Get user's selected documents
            self.state.choice = self.multiSelect()
            # Stream documents to Azure OpenAI and display responses
            self.streamOpenAI()
