#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 19:42:19 2024

@author: andreadesogus
"""

from libraryManager import LibraryManager
from AzureOpenAI import embeddings_retriever, response_builder
import streamlit as st
import time


class StreamResponse:
    def __init__(self, session_state: dict, library_manager: LibraryManager):
        """
        Initializes the StreamResponse class.

        Args:
        - session_state (dict): The state of the session.
        - library_manager (LibraryManager): An instance of LibraryManager.
        """
        self.state = session_state
        # Load DynamoDB tables using the LibraryManager instance
        self.ddb, self.ddbt = library_manager.loadDdbTable()

    def streamOpenAI_funct(self, system: str, question: str) -> list:
        """
        Performs OpenAI inference.

        Args:
        - system (str): The system information.
        - question (str): The question to be answered.

        Returns:
        - list: A list of response events.
        """
        
        from AzureOpenAI import embeddings_retriever, response_builder
        # Set a delay time for faster response
        delay_time = 0.01
        answer = ''
        start_time = time.time()
        # Call responseBuilder function from AzureOpenAI module
        response = response_builder(system, question, 5000, "", "", True, "")
        return response
    
    def streamOpenAI(self, doc_id: str, system: str, question: str) -> None:
        """
        Streams the OpenAI response.

        Args:
        - doc_id (str): The document ID.
        - system (str): The system information.
        - question (str): The question to be answered.

        Returns:
        - None
        """
        
        # Retrieve text data from DynamoDB based on the document ID
        text = self.ddbt.get_item(doc_id)
            
        with st.container(border=False):
            # Perform OpenAI inference
            response = self.streamOpenAI_funct(system=system + "Titolo: " + text['Item']['doc_id'] + "\n" + text['Item']['contentText'] + "\n\n",
                                               question=question)
            full_resp = ""
            with st.empty():
                # Iterate through response events
                for event in response: 
                    time.sleep(0.01)
                    # Check if content exists in the response event
                    if str(event.choices[0].delta.content) and str(event.choices[0].delta.content) != "None":
                        full_resp += str(event.choices[0].delta.content)
                        # Display the document ID and the full response
                        st.markdown(f"Jurix risponde:\n\n" + full_resp)
                        #st.markdown(f"{text['Item']['doc_id']}\n\n" + full_resp)
