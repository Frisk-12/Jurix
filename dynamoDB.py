#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 11:32:47 2024

@author: andreadesogus
"""


import boto3
from typing import Optional, List, Union, Dict


class DynamoDBHandler():
    def __init__(self, aws_access_key_id:str, aws_secret_access_key:str, region_name:str, partition_key: Optional[str] = 'doc_id'):
        self.aws_access_key_id: str = aws_access_key_id
        self.aws_secret_access_key: str = aws_secret_access_key
        self.region_name:str = region_name
        self.partition_key:str = partition_key
        self.dynamodb = self.dynamodbSession()
        self.table = self.useTable
        
    def dynamodbSession(self):
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

        # Ritorna l'oggetto DynamoDB dalla sessione
        return session.resource('dynamodb')
        
    def createTable(self, table_name: str, capacity_units: int = 5):
        # Create the DynamoDB table.
        table = self.dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': self.partition_key,
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': self.partition_key,
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': capacity_units,
                'WriteCapacityUnits': capacity_units
            }
        )
        
        table.wait_until_exists()
        return table
    
    def useTable(self, table_name: str): #dynamodb.Table(name='metaEmb-1')
        try:
            self.table = self.dynamodb.Table(table_name)
            return self.table
        except Exception as e:
             print(f"""An error occurred when calling the table named {table_name}. Verify the name is correct.""")
             
    def scanTable(self):
        response = self.table.scan(
                                   
                                )
        return response
             
    def insert_BatchItem(self, textDict: Dict[str,Dict[str,str]]):
        #try:
        with self.table.batch_writer() as batch:
            for i in list(textDict.keys()):
                batch.put_item(
                    Item=textDict[i]
                    )
        # except Exception as e:
        #     print(f"""An error occurred when inserting values to KV Store.""")
            
    def insert_item(self, textDict: Dict[str,dict]):
        try:
            response = self.table.put_item(
                            Item=textDict
                        )
        except Exception as e:
            print(f"""An error occurred when inserting values to KV Store.""")

    
    def get_item(self, partition_value:str): #dict
        try:
            response = self.table.get_item(
                Key={
                    self.partition_key: partition_value,
                }
            )
            return response
        except Exception as e:
            print(f"""An error occurred when retrieving values from KV Store. Be sure to provide a right '{self.partition_key}' value.""")
        
        
    def get_batchItems(self, partition_values:List[str]):
        batch_keys = {
            self.table.name: {
                'Keys': [
                    {
                    self.partition_key: i
                    } for i in partition_values]
                }
            }
        
        response = self.dynamodb.batch_get_item(RequestItems=batch_keys)
        return response['Responses'][self.table.name]
    
    def update_item(self,partition_value:str, new_attributes:dict):
        
        # Costruisci l'espressione di aggiornamento per aggiungere gli attributi
        update_expression = 'SET '
        expression_attribute_values = {}
        expression_attribute_names = {}
        # Aggiungi ciascun nuovo attributo all'espressione di aggiornamento e ai valori dell'espressione
        for i, (attribute_name, attribute_value) in enumerate(new_attributes.items()):
            update_expression += f'#attr{i} = :val{i}, '
            expression_attribute_values[f':val{i}'] = attribute_value
            expression_attribute_names[f'#attr{i}'] = attribute_name
        
        # Rimuovi l'ultima virgola e lo spazio dall'espressione di aggiornamento
        update_expression = update_expression[:-2]
        
        response = self.table.update_item(
                            Key={
                                'username': partition_value,
                            },
                            UpdateExpression=update_expression,
                            ExpressionAttributeValues=expression_attribute_values,
                            ExpressionAttributeNames=expression_attribute_names
                        )
        
    def delete_item(self, partition_value:str):
        self.table.delete_item(
                Key={
                    self.partition_key: partition_value,
            }
)
    def delete_table(self):
        self.table.delete()

class KVEmbeddingsWrapper:
    def __init__(self, response: Dict[str, Union[str, List[str]]]):
        self.doc_id: str = response['doc_id']
        self.category: List[float] = [float(i) for i in response['microCategory']]
        self.summary: List[float] = [float(i) for i in response['summary']]
            
