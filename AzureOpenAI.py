#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 22:41:21 2023

@author: andreadesogus
"""


from openai import OpenAI, AzureOpenAI
from connect import APIKeys

def embeddings_retriever(text: str, client_type: str) -> list:
    """
    Retrieves embeddings for the given text using the specified OpenAI client.

    Args:
        text (str): The input text for which embeddings are to be retrieved.
        client_type (str): The type of OpenAI client to use. Possible values are "azure" or anything else for default.

    Returns:
        list: A list containing the embeddings for the input text.
    """
    ak = APIKeys()
    
    if client_type == "azure":
        api_key, api_version, azure_endpoint = ak.azure_key()
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
    else:
        api_key = ak.openai_key()
        client = OpenAI(api_key=api_key)
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-large",
            dimensions=3072
        )
    embeddings = response.data[0].embedding
    return embeddings

def response_builder(system: str, text: str, n: list, format_: str, client_type: str, stream: bool, resp_mode: str) -> tuple:
    """
    Builds a response using the specified OpenAI client and parameters.

    Args:
        system (str): The system message to include in the conversation.
        text (str): The user's input text.
        n (list): A list containing the maximum tokens allowed.
        format_ (str): The format of the response. Possible values are "json" or anything else for default.
        client_type (str): The type of OpenAI client to use. Possible values are "azure" or anything else for default.
        stream (bool): A boolean indicating whether to stream the response.
        resp_mode (str): The mode of the response. Possible values are "text" or anything else for default.

    Returns:
        tuple: A tuple containing the response message and the total tokens used.
    """
    ak = APIKeys()
    if client_type == "azure":
        api_key, api_version, azure_endpoint = ak.azure_key()
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint,
        )
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": text}
        ]
        if format_ == "json":
            completion = client.chat.completions.create(
                model="gpt-35-turbo-1106",
                temperature=0,
                response_format={"type": "json_object"},
                max_tokens=4096,
                messages=messages
            )
        else:
            completion = client.chat.completions.create(
                model="gpt-35-turbo-16k",
                temperature=0,
                max_tokens=16000 - n[0],
                messages=messages
            )
    else:
        api_key = ak.openai_key()
        client = OpenAI(api_key=api_key)
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": text}
        ]
        if format_ == "json":
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={"type": "json_object"},
                messages=messages
            )
        else:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",#"gpt-4-0125-preview",#
                messages=messages,
                stream=stream,
                max_tokens=3000
            )

    if resp_mode == "text":
        return completion.choices[0].message.content, completion.usage.total_tokens
    else:
        return completion
