#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:51:33 2024

@author: andreadesogus
"""

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
import re
from typing import List

class KeyWordsExtractor:
    def __init__(self, language: str = 'italian') -> None:
        
        '''Initializes the KeyWordsExtractor object with stop words, stemmer, and word list.'''
        
        self.stop_words = set(stopwords.words(language))
        self.stemmer = SnowballStemmer(language)
        self.words: List[str] = []

    def process_text(self, text: str) -> List[str]:
        
        '''Performs keyword extraction from the provided text.
        
        Args:
            text (str): The text to be processed for extracting keywords.
        
        Returns:
            List[str]: A list of keywords extracted from the specific text.
        '''
        
        try:
            # Remove punctuation except alphanumeric characters and spaces
            self.words = []
            text = re.sub(r'[^\w\s]', '', text)
            
            # Tokenize the text into words
            words_ = word_tokenize(text.lower())

            added_words = set()  # Store unique stemmed words
            
            for word in words_:
                if word.lower() not in self.stop_words:
                    stemmed_word = self.stemmer.stem(word)
                    if (
                        stemmed_word not in added_words
                        and stemmed_word not in {".", ",", "'", '-', '``', ':', "''", ";", "(", ")", "=", "&", "@", "§",
                                                 "!", "?", "^", '""', '"', '……', '_'}
                        and not stemmed_word.startswith(".")
                        and not stemmed_word.endswith(".")
                        and not (len(stemmed_word) == 1 and stemmed_word.isalpha())
                    ):
                        self.words.append(stemmed_word)
                        added_words.add(stemmed_word)
            return self.words

        except Exception as e:
            # In caso di errore, stampa il messaggio di errore e gestiscilo opportunamente
            print(f"An error occurred: {str(e)}")
            return "IRPEF"  # Ritorna una lista vuota se si verifica un errore
