#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 12:33:27 2024

@author: andreadesogus
"""

import os
import pinecone
from pinecone import Pinecone
from pinecone.core.client.model.query_response import QueryResponse
from typing import Optional, Dict, Any, Union, List,Tuple, Callable
from AzureOpenAI import embeddings_retriever
from dynamoDB import DynamoDBHandler, KVEmbeddingsWrapper
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np



class JurixPineconeIndex:
    def __init__(self, pinecone_key:str):
        """
        Initializes the JurixPineconeIndex class by setting up the Pinecone API key, environment, and other necessary variables.
        """
        self.pinecone_key: str = pinecone_key  # Pinecone API key
        os.environ['PINECONE_API_KEY'] = self.pinecone_key
        self.user_query: str =  str()# Placeholder for user query
        self.user_query_vector: List[float] = []  # Placeholder for the vector representation of the user query
        self.pinecone_index = self._initialize_pinecone_index()  # Initializes the Pinecone index upon object creation

    def _initialize_pinecone_index(self):
        """
        Initializes the Pinecone index with the provided API key and environment.
        """
        # pinecone.init(api_key=self.pinecone_key, environment=self.environment)
        # return pinecone.Index("jurix-test-1")  # Creates a Pinecone index named 'jurix-test-1'
        pc = Pinecone(api_key=self.pinecone_key)
        pineconeIndex = pc.Index('jurix-test-v2')  
        return pineconeIndex

    def vectorized_query(self, user_query: str) -> List[float]:
        """
        Converts the user query into a vector representation using an embeddings retriever function.

        Args:
        - user_query (str): The user query to be converted.

        Returns:
        List[float]: Vector representation of the user query.
        """
        return embeddings_retriever(user_query,"")  # Retrieves vector representation using embeddings_retriever function

    def set_user_query_text(self, user_query: str) -> List[float]:
        """
        Sets the user query and its vector representation.

        Args:
        - user_query (str): The user query to be set.

        Returns:
        List[float]: Vector representation of the user query.
        """
        self.user_query = user_query  # Sets the user query
        self.user_query_vector = self.vectorized_query(user_query)  # Converts the user query into a vector
        return self.user_query_vector  # Returns the vector representation of the user query
    
    def set_user_query_float(self, user_query: List[float]) -> List[float]:
        """
        Sets the user query and its vector representation.

        Args:
        - user_query (List[float]): The user query to be set.

        Returns:
        List[float]: Vector representation of the user query.
        """
        self.user_query_vector = user_query  # Sets the user query
        return self.user_query_vector  # Returns the vector representation of the user query
    
    
    def query(self, filters: Optional[Dict[str, Union[Union[str, Dict[str, Union[str, int]]], Union[str, int, Dict[str, Union[str, int]]]]]] = None, topK: int = 10) -> QueryResponse:
        """
        Queries the Pinecone index with the user query vector to retrieve results.

        Args:
        - filters (Optional[Dict[str, Dict[str, Any]]]): Optional filters for the query.
        - top_k (int): Number of top results to retrieve.

        Returns:
        Pinecone Query Response.
        """
        if not self.user_query_vector:
            raise ValueError("User query vector is not initialized. Please set a user query.")

        # Define query parameters
        query_params: Dict[str, Union[str, int, List[float]]] = {
            'vector': self.user_query_vector,
            'top_k': topK,
            'include_values': False,
            'include_metadata': True
        }

        # Include additional filters if provided
        if filters:
            query_params['filter'] = filters

        # Query the Pinecone index to retrieve results
        results: QueryResponse = self.pinecone_index.query(**query_params)
        return results  # Returns the list of query results


    
class SearchResultsHandler:
    def __init__(self, pineconeResults: List[dict]):
        self.res: List[dict] = pineconeResults
        
        # Dictionary to store search results
        self.result_dict: Dict[str, dict] = {}
        # Dictionary to store text scores
        self.text_scores_dict: Dict[str, float] = {}
        
    def computeTextScores(self) -> Dict[str, float]:
        self.text_scores_dict = {}  # Initialize score for the query
        for r in self.res:
            # Update text scores
            self.text_scores_dict.update({r.id: r.score})
        return self.text_scores_dict
        


    def handle_search_results(self) -> Dict[str, dict]:
        """
        Handles search results and associated texts.

        Args:
        - res (List[dict]): List of search results.

        Returns:
        Dict[str, dict]: A dictionary containing the result dictionary.
        """
        self.result_dict.clear()
        for r in self.res:        
            # Extract metadata for each result
            metadata_dict = {}
            for key, value in r.metadata.items():
                metadata_dict[key] = value
            self.result_dict[r.id] = metadata_dict

        return self.result_dict


class EmbeddingsHandler:
    def retrieve_embeddings(self, ddb: DynamoDBHandler, result_dict: Dict[str, dict], categories=None):
        if categories is None:
            categories = ['category', 'summary']
        
        embeddings_dict = {category: {} for category in categories}
        
        for key in result_dict:
            response = ddb.get_item(key)
            if 'Item' in response:
                kv_wrapper = KVEmbeddingsWrapper(response['Item'])
                for category in categories:
                    category_emb = getattr(kv_wrapper, category, None)
                    if category_emb is not None:
                        embeddings_dict[category][key] = category_emb
        
        return embeddings_dict
        
    def calculate_embeddings(self, result_dict, categories, embeddings_retriever):
        """
        Calculates embeddings based on search results.

        Args:
        - result_dict: Dictionary containing search results. 
        - categories (List[str]): Categories to calculate embeddings for. 
        - embeddings_retriever: Function to retrieve embeddings.

        Returns:
        Dict[str, Dict[str, Any]]: Dictionary containing embeddings for each category.
        """
        embeddings_dict = {}
        for category in categories:
            category_embs = {}
            for key, value in result_dict.items():
                if category in value:
                    # Calculate embeddings for each text in the category
                    category_emb = embeddings_retriever(value[category],"")
                    category_embs[key] = category_emb
            embeddings_dict[category] = category_embs

        return embeddings_dict


class CorrelationDataProcessor:
    def calculate_correlation_lists(self, query_emb: str, embeddings_dict: Dict[str, Dict[str, Any]]) -> Dict[str, List[float]]:
        """
        Calculates correlation lists based on embeddings.

        Args:
        - query_emb (str): Query embeddings.
        - embeddings_dict (Dict[str, Dict[str, Any]]): Dictionary containing embeddings for each category.

        Returns:
        Dict[str, List[float]]: Dictionary containing correlation lists for each category.
        """
        correlation_dict = {}
        for category, embs in embeddings_dict.items():
            embs_list = [query_emb] + list(embs.values())
            corr_list = cosine_similarity(embs_list, embs_list)[0]
            correlation_dict[category] = corr_list
            list_results = list(embs.keys())

        return correlation_dict, list_results

    def create_dataframe(self, correlation_results: Dict[str, List[float]], text_scores_dict: Dict[str, Any], list_results: list) -> pd.DataFrame:
        """
        Creates a DataFrame based on correlation results and text scores.

        Args:
        - correlation_results (Dict[str, List[float]]): Dictionary containing correlation lists for each category.
        - text_scores_dict (Dict[str, Any]): Dictionary containing text scores.

        Returns:
        pd.DataFrame: DataFrame with correlation results and text scores.
        """
        df_data = {}
        for category, corr_list in correlation_results.items():
            df_data[category] = list(corr_list)

        text_scores_dict_ = {k: v for k, v in text_scores_dict.items() if k in list_results}
        df_data['text_score'] = [1] + list(text_scores_dict_.values())
        df = pd.DataFrame(df_data, index=['query'] + list(text_scores_dict_.keys()))
        df['average'] = df.mean(axis=1)



        # Calculate weighted average
        #weights = {category: (1 / len(df.columns)) for category in df.columns}#{category: 1 / len(df.columns) if len(df.columns) != 0 else 0 for category in df.columns}

        df['average_weighted'] = df['text_score']*0.5 + df[[col for col in df.columns if col not in ['text_score','average']]].mean(axis=1)*0.5 #df.apply(lambda row: sum(row[category] * weights[category] for category in weights.keys()), axis=1)

        
        return df


class OptimizedSearchProcessor:
    def __init__(self, pineconeResults: List[dict], ):
        # Initialize components of the search process
        #self.search_handler = SearchResultsHandler(pineconeResults)
        #self.embeddings_dict = embeddings_dict
        self.correlation_processor = CorrelationDataProcessor()
        

    def process_search_results(self, query_emb: List[int], result_dict_: dict, text_scores_dict: dict, embeddings_dict: dict, reranking: bool, embeddings_retriever: Callable = embeddings_retriever) -> pd.DataFrame:
        """
        Process optimized search results.

        Args:
        - query_emb (List[int]): Query embeddings.
        - categories_to_handle (List[str]): Categories to handle.
        - res (List[dict]): List of search results.
        - embeddings_retriever (Callable[[str], Any]): Function to retrieve embeddings.

        Returns:
        pd.DataFrame: DataFrame with processed search results.
        """
        # result_dict = self.search_handler.handle_search_results()
        # text_scores_dict = self.search_handler.computeTextScores()
        #embeddings_dict = self.embeddings_handler.retrieve_embeddings(ddb, result_dict, categories_to_handle) #self.embeddings_handler.calculate_embeddings(result_dict, categories_to_handle, embeddings_retriever)
        if reranking:
            correlation_results, list_results = self.correlation_processor.calculate_correlation_lists(query_emb, embeddings_dict)
            df = self.correlation_processor.create_dataframe(correlation_results, text_scores_dict, list_results)
            result_dict = {k: v for k, v in result_dict_.items() if k in list_results}
            # Additional DataFrame processing
            df = df.iloc[1:, :]
        else:
            result_dict = result_dict_
            df = pd.DataFrame(index=list(result_dict.keys()))
            df['average_weighted'] = list(text_scores_dict.values())
        
        df['link'] = [result_dict[k]['externalId'] for k in list(result_dict.keys())]
        df['Summary'] = [result_dict[k]['summary'] for k in list(result_dict.keys())]
        df['categoria'] = [result_dict[k]['microCategory'] for k in list(result_dict.keys())]
        df['anno'] = [result_dict[k]['anno'] for k in list(result_dict.keys())]
        df['numero'] = [result_dict[k]['numero'] for k in list(result_dict.keys())]
        df['emanante'] = [result_dict[k]['emanante'] for k in list(result_dict.keys())]
        df['tipo'] = [result_dict[k]['tipo'] for k in list(result_dict.keys())]
        df['riferimenti_citati'] = [result_dict[k]['riferimenti_citati'] for k in list(result_dict.keys())]
        df['first_order'] = list(np.arange(len(df))+1)
        
        return df.sort_values(by="average_weighted", ascending=False)

    