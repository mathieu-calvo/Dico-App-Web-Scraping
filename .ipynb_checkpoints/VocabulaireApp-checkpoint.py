#!/usr/bin/env python
# -*-coding:utf-8 -*

# standard packages
import imp
import time
import asyncio

# site packages
import pandas as pd
import ipywidgets as widgets
from IPython.display import HTML, display

# project modules
import ReversoDictionary as reverso
imp.reload(reverso)

#TODO: interface to start storing those words with associated htmls for definitions/translations
#TODO: interface to brush up, with ability to choose exercise type and then select based on some logic (when last seen, how often seen, how good I fare on it, importance of word etc...). Ability to rate myself perhaps, i.e. see the word, think of definition/translation, see result and rate myself on how close I was from truth, and maybe a star for importance


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback()

    def start(self):
        self._task = asyncio.ensure_future(self._job())

    def cancel(self):
        self._task.cancel()


def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        timer = None
        def debounced(*args, **kwargs):
            nonlocal timer
            def call_it():
                fn(*args, **kwargs)
            if timer is not None:
                timer.cancel()
            timer = Timer(wait, call_it)
            timer.start()
        return debounced
    return decorator


class VocabulaireApp:
    
    def __init__(self):
        """
        Create an instance of object to have a nice GUI to interact with the Reverso dictionary online, add selected definitions and translations 
        to our virtual notebooks so it grows with things we want to learn and remember 
                
        Attributes:
            dico (ReversoDictionary): object to interact with the website and retrieve translations/definitions in various formats
            all_lang (set): all variations accepted as input 
            lang_from (str): language to define/translate
            lang_to (str): target language or definition
        """
        self.dico = reverso.ReversoDictionary()
        self.all_lang = ['francais', 'italien', 'anglais', 'espagnol'] 
        # default params
        self.lang_from = 'francais'
        self.lang_to = 'definition'
        self.dico.set_up_translation_type(self.lang_from, self.lang_to)
        self._build_gui()
    
    def _build_gui(self):
        """
        Method to create GUI to interact with
        
        Attributes:
            gui (widgets.VBox): containing all elements
        """
        # define widgets
        self.from_dd = widgets.Dropdown(options=self.all_lang, \
                                        description='from:', \
                                        value=self.lang_from)
        self.to_dd = widgets.Dropdown(options=self.all_lang + ['definition'], \
                                      description='to:', \
                                      value=self.lang_to)
        self.search_box = widgets.Textarea(placeholder='Type something here...')
        self.html_out = widgets.Output(layout={'border': '1px solid black'})
            
        # event-driven functions
        def on_from_dropdown_change(change):
            """ Method to change translation type and attributes based on user selection """
            self.dico.set_up_translation_type(change['new'], self.lang_to)
            self.lang_from = change['new']
            self._display_translate_or_define()
            
        def on_to_dropdown_change(change):
            """ Method to change translation type and attributes based on user selection """
            self.dico.set_up_translation_type(self.lang_from, change['new'])
            self.lang_to = change['new']
            self._display_translate_or_define()
        
        @debounce(0.5)  # minimum half a second before next change
        def on_search_box_change(change):
            """ Method to make a query for word typed in by user,  """
            self._display_translate_or_define()
            
        # event-driven triggers
        self.from_dd.observe(on_from_dropdown_change, names='value')
        self.to_dd.observe(on_to_dropdown_change, names='value')
        self.search_box.observe(on_search_box_change, names='value')
        
        # putting everything together
        self.gui = widgets.VBox([self.from_dd, self.to_dd, self.search_box, self.html_out])
    
    def _display_translate_or_define(self):
        """ fetch definition/translation and display it to the user """
        time.sleep(1)
        word = self.search_box.value
        self.html_out.clear_output()
        if word != '':
            with self.html_out:
                word_url, html_display, html_elems, content_df = self.dico.translate_or_define(word)
                display(html_display)
                display(content_df)
                    
    def show_gui(self):
        """
        Method to display GUI to user
        """
        return self.gui
