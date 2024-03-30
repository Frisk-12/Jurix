#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:40:28 2024

@author: andreadesogus
"""

from libraryManager import LibraryManager

class Telemetria:
    def __init__(self, session_state):
        self.state = session_state
        self.ddbs, self.ddbt = LibraryManager(self.state).loadDdbTable()
        
    def update_session(self,new_info):
        import time
        self.ddbs.update_item(self.state.username, {str(time.time()):new_info})
