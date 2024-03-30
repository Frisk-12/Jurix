#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:25:52 2023

@author: andreadesogus
"""

from functions.pineconeIndex import JurixPineconeIndex

def pineconeQuery(user_query,n):
    jurix_index = JurixPineconeIndex()
    
    # Impostazione della query dell'utente e calcolo del vettore della query
    jurix_index.set_user_query(user_query)
    
    # Esempio di esecuzione di una query usando l'istanza appena creata
    tipo_query = "interpello" #['circolare','interpello','risoluzione']
    numero_risultati = n
    
    res = jurix_index.query(tipo_query, numero_risultati)
    return res
