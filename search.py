#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 19:42:59 2024

@author: andreadesogus
"""

from typing import Dict, Any
import streamlit as st
import time

class Search:
    def __init__(self, session_state: Dict, libraryManager: Any, streamResponse: Any, Telemetria: Any) -> None:
        """
        Initialize the Search class.

        Parameters:
        - session_state (dict): The session state dictionary.
        - libraryManager (any): The library manager object.
        - stremResponse (any): The stream response object.
        """
        # Initialize session state, library manager, and stream response
        self.state = session_state
        self.lm = libraryManager
        self.invEm = libraryManager.loadEmList()
        self.kw = libraryManager.loadKV()
        self.index = libraryManager.loadIndex()
        self.ddbs, self.ddbt = libraryManager.loadDdbTable()
        self.stream = streamResponse
        self.telem = Telemetria(self.state)

    def filter_out(self, cat, tipo, start_date, entryStartDate, end_date, entryEndDate, text_filters, emanante):
        """
        Generate filters based on user input.

        Parameters:
        - cat (list): List of categories.
        - tipo (list): List of types.
        - start_date (int): Start year.
        - entryStartDate (int): Entry start year.
        - end_date (int): End year.
        - entryEndDate (int): Entry end year.
        - text_filters (str): Text filters.
        - emanante (list): List of emitters.

        Returns:
        - dict: Filter dictionary.
        """
        filters = {}
        if cat:
            # Add category filter
            if len(cat) == 1:
                filters.update({'categoria': {"$eq": cat[0].lower()}})
            else:
                f = []
                for i in cat:
                    f.append({"categoria": {"$eq": i.lower()}})
                filters.update({"$or": f})
        if tipo:
            # Add type filter
            if len(tipo) == 1:
                filters.update({'tipo': {"$eq": tipo[0].lower()}})
            else:
                f = []
                for i in tipo:
                    f.append({"tipo": {"$eq": i.lower()}})
                filters.update({"$or": f})
        if (start_date > entryStartDate) or (end_date < entryEndDate):
            # Add date range filter
            filters.update({"$and": [{"anno": {"$gte": start_date}}, {"anno": {"$lte": end_date}}]})
        if text_filters:
            # Add text filter
            if len(text_filters.split(",")) == 1:
                filters.update({'keywords': {"$in": self.kw.process_text(text_filters.strip().lower())}})
            elif len(text_filters.split(",")) > 1:
                f = []
                for i in text_filters.split(","):
                    f.append({"keywords": {"$in": self.kw.process_text(i.strip().lower())}})
                filters.update({"$and": f})
        return filters
        
    def searchFilters(self):
        """
        Display search filters form and return selected filters.

        Returns:
        - dict: Selected filters.
        """
        with st.form("form", border=True):
            # Display search filters form
            st.markdown(f"<h1 style='text-align: left; font-size: 16px;'><b>Inserisci filtri:</b></h1>", unsafe_allow_html=True)
            st.write("   ")
            st.write("   ")
            category = st.multiselect(label="Dove vuoi cercare?", options=["Giurisprudenza", "Prassi"], placeholder="Seleziona un'opzione:")
            st.write("---")
            
            entryStartDate = 1980
            entryEndDate = 2023
            start_date, end_date = st.select_slider(
                'Seleziona il periodo temporale:',
                options=[i for i in range(1980, 2024)],
                value=(entryStartDate, entryEndDate),
            )
            st.write("---")
            
            text_filters = st.text_area(label="Cerca nel testo:", placeholder='Digita le parole chiave separate da una virgola. Esmepio: IFRS 2, IVA')
            st.write("---")
            
            tipo = st.multiselect(label="Tipo:", options=['Circolare', 'Conclusione', 'Decisione', 'Decreto', 'Delibera', 'Deliberazione', 'Direttiva', 'Interpello', 'Lettera', 'Lodo', 'Nota', 'Ordinanza', 'Parere', 'Ricorso', 'Risoluzione', 'Sentenza'], placeholder="Seleziona una o più opzioni:")
            st.write("---")
            
            emanante = st.multiselect(label="Emanante:", options=self.invEm.emananti_list(), placeholder="Seleziona una o più opzioni:")
            st.write("---")
            
            if st.form_submit_button("Filtra!"):
                # Return selected filters
                filters = self.filter_out(category, tipo, start_date, entryStartDate, end_date, entryEndDate, text_filters, emanante)
                self.state['searchFilters'] = filters
                self.telem.update_session({"SearchFilters":filters})
                return filters

    def doSearch(self):
        """
        Perform search based on user input.
        """
        s = time.time()
        t1, t2 = st.columns([0.25, 0.75])
        with t1:
            filters = self.searchFilters()
        with t2:
            search_icon = "🔍"
            container = st.container(border=True)
            query = container.text_input(label="Cerca:", placeholder=f"{search_icon} Cerca qui")
            if query:
                self.telem.update_session({"query":query})
                self.state.query = query
                query_embs = self.index.set_user_query_text(query)
                
                if 'searchFilters' in self.state:
                    # Perform search with filters
                    results = self.index.query(filters=self.state['searchFilters'], topK=10)['matches']
                else:
                    # Perform search without filters
                    results = self.index.query(filters={}, topK=10)['matches']
                if results:
                    self.state.results = [{k.id: f"{k.metadata['tipo'].capitalize()} {k.metadata['numero']}/{round(k.metadata['anno'])} - {self.invEm.key2value(k.metadata['emanante'])}"} for k in results]
                    t = time.time() - s
                    st.markdown(
                        f"<div style='display: flex; justify-content: space-between; align-items: center;'><h1 style='text-align: left; font-size: 16px;'><b>Results: {len(results)}</b></h1>"
                        f"<p style='text-align: right; font-size: 10px;'>Calcolato in {round(t, 2)} secondi.</p></div>",
                        unsafe_allow_html=True
                    )
                    for i, result in enumerate(results):
                        with st.expander(f"""{i+1} - **{result.metadata['tipo'].capitalize()} {result.metadata['numero']}/{round(result.metadata['anno'])}** - {self.invEm.key2value(result.metadata['emanante'])}"""):
                            tab1, tab4 = st.tabs(["📝 **Sintesi**", "🪄 **Chiedi**" ]) #tab3 =  "🏛️ **Similar**", , tab2 =  "📌 **Citazioni**"
                            with tab1:
                                st.markdown(f"**Categoria:** {result.metadata['macroCategory']} - {result.metadata['microCategory']}", unsafe_allow_html=True)
                                st.markdown(f":open_book: Visualizza il documento originale [qui](%s) :paperclip:" % result.metadata['externalId'])
                                st.markdown(f"**Sintesi:** {result.metadata['summary']}", unsafe_allow_html=True)   
                            # with tab2:
                            #     riferimenti_citati = result.metadata['riferimenti_citati']
                            #     for j in riferimenti_citati:
                            #         st.text(f"- {j.capitalize()};")
                            # with tab3:
                            #     st.write("")  # Placeholder for similar documents
                            with tab4:
                                subtabs = st.columns([0.9,0.1])
                                with subtabs[0]:
                                    question = st.text_input("Chiedi a Jurix qualsiasi cosa:", key="Q_"+result.id, placeholder=f"Scrivi qui")
                                with subtabs[1]:
                                    st.write("")
                                    st.write("")

                                    c = st.button("Vai", key="Qc_"+result.id, )
                                del self.state["Q_"+result.id]
                                del self.state["Qc_"+result.id]
                                if c:
                                    system   = f"""Immagina di essere un consulente specializzato in diritto tributario. Immagina che puoi usufruire di un database composto da svariate sentenze, ordinanze, interpelli e documenti legali relativi al ramo tributario. 

Un utente ha una domanda da porti e sulla base del contenuto di uno dei testi presenti nel database tu hai l'opportunità di aiutare l'utente rispondendo alla sua domanda.

Hai molta esperienza in casi concreti e sei in grado di compiere ragionamenti basati su vari step, in modo deduttivo. Sai inoltre compiere ragionamento induttivo, partendo da una fattispecie non perfettamente allineata alla domanda dell'utente per formulare comunque una risposta logica e attinente.

Qualora il testo a tua disposizione non abbia affinità con la domanda dell'utente, rispondi cortesemente affermando che la risposta non si trova nel documento consultato.
In alternativa, fornisci innanzitutto una risposta diretta e concisa rispetto alla domanda dell'utente, e se questo non fosse possibile, fornisci una prima parte di risposta con le informazioni presenti nel testo e una seconda parte di risposta formulando un ragionamento logico che vada a impattare la domanda dell'utente. 

E' importante che rimani breve e conciso, con un massimo di 200 parole e che ti attieni al testo fornito.

Ecco il testo: """
                                    self.stream.streamOpenAI(doc_id = result.id, system = system, question = question)
                                    st.write("---")  # Add a horizontal line between results
                                    self.telem.update_session({"AskJurix":question})
