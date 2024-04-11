#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 19:37:27 2024

@author: andreadesogus
"""

from typing import Dict, Any
from logoDisplayer import logoDisplayer
import streamlit as st

class Login:
    def __init__(self, session_state: Dict, img: str, library_manager: Any, Telemetria: Any) -> None:
        """
        Initialize the Login class.

        Parameters:
        - session_state (dict): The session state dictionary.
        - img (str): The image path for logo display.
        - library_manager (any): The library manager object for database operations.
        """
        # Initialize session state, logo display, and database manager
        self.state = session_state
        self.logo = logoDisplayer(img)
        self.ddbs, self.ddbt = library_manager.loadDdbTable()
        self.telem = Telemetria(self.state)


    def user_exists(self) -> bool:
        """
        Check if the user exists in the database.

        Returns:
        - bool: True if the user exists, False otherwise.
        """
        try:
            # Try to get user item from the database
            response = self.ddbs.get_item(self.state.username)['Item']
            return True
        except:
            # User does not exist in the database
            return False

    def check_user_login(self) -> bool:            
        """
        Check user login status.

        Returns:
        - bool: True if the user is authenticated, False otherwise.
        """        
        # Check if username exists in session state and user exists in the database
        if "username" in self.state and self.user_exists():
            # Set authentication status to True
            self.state.authenticated = True
            self.telem.update_session("StartSession")
        else:
            # Set authentication status to False
            self.state.authenticated = False
        return self.state.authenticated

    def authentication(self) -> bool:
        """
        Perform user authentication.

        Returns:
        - bool: True if the user is authenticated, False otherwise.
        """
        # Divide the screen into three columns
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            with st.container(border=False):
                # Display logo
                self.logo.displayLogo()
                # Prompt user to enter username
                self.state.username = st.text_input("Inserisci la tua username:", placeholder="Username")
                if self.state.username:
                    # Check if user exists
                    self.state.check_user = self.user_exists()
                    if self.state.check_user:
                        # Button to login
                        button_l = st.button("Entra!", use_container_width=True, key="Login", on_click=self.check_user_login)
                        if button_l:
                            return self.check_user_login()
                    else:
                        # Button to sign up
                        button_s = st.button("Registrati qui:", use_container_width=True, key="Signup")
                        if button_s:
                            # Display sign-up form
                            st.info("Registrarsi è semplice e veloce. Rispondi giusto a qualche domanda per conoscerci meglio:")
                            with st.form("registration", border=False):
                                self.state.username = st.text_input("Conferma la tua username:*", placeholder="Username")
                                st.write("---")
                                professione = st.radio("Chi sei?*", ['Professionista legale', 'Studente', 'Docente', 'Utente comune'], index=None, key="professione")
                                st.write("---")
                                #age = st.radio("A quale classe d'età appartieni?*", ['18-24', '25-34', '35-44', '45-54', '55-64', 'Over 65'], index=None, key="age")
                                #st.write("---")
                                #italian_regions = ["Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"]
                                #regione = st.selectbox("Regione di residenza:*", italian_regions, index=None, placeholder="Scegli la tua regione", key="regione")
                                #st.write("---")
                                #email = st.text_input("Scrivi il tuo indirizzo email:", placeholder="Scrivi la tua email", key="email")
                                #st.write("---")
                                source = st.radio("Come sei arrivato qui?*", ['Linkedin', 'Sito web', 'Passaporola', 'Google'], index=None, key="source")
                                st.write("---")
                                #condizioni_marketing = st.checkbox("Acconsento a ricevere comunicazioni di marketing tramite email.", key="condizioni_marketing" ,help = "Accettando, autorizzo l'invio di comunicazioni promozionali, newsletter e offerte speciali relative ai prodotti e ai servizi offerti da AnyVentures. Comprendo che posso revocare il consenso in qualsiasi momento tramite l'opzione di annullamento dell'iscrizione presente in ogni email inviata, oppure contattando il servizio clienti di AnyVentures. I miei dati personali saranno trattati in conformità alla politica sulla privacy di AnyVentures.")
                                cu = """
                                Accettando, confermo di aver letto e compreso i Termini di Utilizzo di questo servizio. Comprendo che il database del sistema è stato aggiornato l'ultima volta a novembre 2023 e che il prodotto è attualmente in fase alpha, pertanto è offerto gratuitamente. Tuttavia, mi rendo conto che in futuro potrebbe essere introdotta una conversione in un modello a pagamento, come un abbonamento.
        
                                Riconosco che l'uso di questo servizio è soggetto ai Termini di Utilizzo e alla Politica sulla Privacy di AnyVentures. Accetto di conformarmi a tali termini e di rispettare le eventuali modifiche future. Comprendo inoltre che sono responsabile dell'uso sicuro delle mie credenziali di accesso e che sono tenuto a informare immediatamente AnyVentures in caso di utilizzo non autorizzato del mio account.
                                """
                                condizioni_utilizzo = st.checkbox("Accetto le condizioni di utilizzo.*", help=cu, key="condizioni_utilizzo")
                                
                                st.write("")
                                if st.form_submit_button("Registrati!", on_click=self.user_exists):
                                    st.write("")
                                else:
                                    st.warning("Fornisci le informazioni richieste contrassegnate con asterischi (*) prima di procedere.")

                        try:    
                            if self.state.professione and self.state.condizioni_utilizzo and self.state.source:
                                new_user = {
                                    "username": self.state.username,
                                    "profile": {
                                        "professione": self.state.professione,
                                       #"age": self.state.age,
                                       #"regione": self.state.regione,
                                        "condizioni_utilizzo": self.state.condizioni_utilizzo,
                                        "source": self.state.source
                                    }
                                }
                                #if self.state.email:
                                    #new_user['profile']['email'] = self.state.email
                                #if self.state.condizioni_marketing:
                                    #new_user['profile']['condizioni_marketing'] = self.state.condizioni_marketing
                                # Insert new user into the database
                                self.ddbs.insert_item(new_user)
                                # Clear form and state variables
                                del self.state.Signup, self.state.professione, self.state["FormSubmitter:registration-Sign up!"], self.state.source, self.state.condizioni_utilizzo
                                st.info("Please reload the page!")
                        except:
                            st.write("C'è un problema")
