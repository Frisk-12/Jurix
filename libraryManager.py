#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 15:15:20 2024

@author: andreadesogus
"""

from extractKeyWords import KeyWordsExtractor
from pineconeIndex import JurixPineconeIndex, OptimizedSearchProcessor, EmbeddingsHandler, SearchResultsHandler
from dynamoDB import DynamoDBHandler, KVEmbeddingsWrapper
from dict_emanante import InvertEmanante
from connect import APIKeys

class LibraryManager:
    def __init__(self, session_state: dict):
        """
        Initializes the LibraryManager class.

        Args:
        - session_state (dict): The state of the session.
        """
        self.state = session_state
        
    def loadEmList(self) -> InvertEmanante:
        """
        Loads the inverted emanante dictionary.

        Returns:
        - InvertEmanante: The inverted emanante dictionary.
        """
        invEm = InvertEmanante()
        return invEm
    
    def loadKV(self) -> KeyWordsExtractor:
        """
        Loads the KeyWordsExtractor instance.

        Returns:
        - KeyWordsExtractor: The KeyWordsExtractor instance.
        """
        KWExtractor = KeyWordsExtractor()
        return KWExtractor
    
    def loadIndex(self) -> JurixPineconeIndex:
        """
        Loads the JurixPineconeIndex instance and stores it in session state.

        Returns:
        - JurixPineconeIndex: The JurixPineconeIndex instance.
        """
        ak = APIKeys()
        pineconeIndex = JurixPineconeIndex(ak.pinecone_key())
        return pineconeIndex
    
    def loadSearchProcessor(self, risultati: list) -> tuple:
        """
        Loads the necessary handlers and processors for search results.

        Args:
        - risultati (list): The search results.

        Returns:
        - tuple: A tuple containing embeddings_handler, result_handler, and search_processor.
        """
        embeddings_handler = EmbeddingsHandler()
        result_handler = SearchResultsHandler(risultati)
        search_processor = OptimizedSearchProcessor(risultati)
        return embeddings_handler, result_handler, search_processor
        
    def loadDdbTable(self) -> tuple:
        """
        Loads the DynamoDB tables.

        Returns:
        - tuple: A tuple containing ddb and ddbT.
        """
        def ddbInitializer(table_name, primary_key = 'doc_id'):
            ak = APIKeys()
            aws_access_key_id, aws_secret_access_key, region_name = ak.aws_key()
            aws_access_key_id = aws_access_key_id
            aws_secret_access_key = aws_secret_access_key    
            # Specify the AWS region
            region_name = region_name
        
            ddb = DynamoDBHandler(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name,
                partition_key = primary_key
            )
            
            ddb.useTable(table_name)
            return ddb
        
        #ddb = ddbInitializer('metaEmb-1')
        ddbT = ddbInitializer('texts')
        ddbS = ddbInitializer("UserSession", primary_key='username')
        
        return ddbS, ddbT
    
    def loadEmanenteList(self) -> InvertEmanante:
        """
        Loads the inverted emanante dictionary and stores it in session state.

        Returns:
        - InvertEmanante: The inverted emanante dictionary.
        """
        self.state['emDict'] = InvertEmanante()
        return self.state['emDict']