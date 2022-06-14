#!/usr/bin/env python
# -*-coding:utf-8 -*

# site packages
import pandas as pd
import requests
import bs4
import unicodedata


class ReversoDictionary:
    
    def __init__(self, base_url=None, hdr=None, lang_dict=None, all_lang=None):
        """
        Create an instance of object to interact with the Reverso dictionary online and retrieve translations/defitions
        programmatically, and parse them to have them in a more structured format
        
        Important: when dealing with text, understanding encoding is paramount:
        http://sametmax.com/lencoding-en-python-une-bonne-fois-pour-toute/
        https://stackoverflow.com/questions/51710082/what-does-unicodedata-normalize-do-in-python
        https://stackoverflow.com/questions/10993612/python-removing-xa0-from-string
        
        Attributes:
            base_url (str): placeholder with link that can be changed depending on translation wanted
            hdr (dict): user agent to be used when making requests to url
            lang_dict (dict): used to normalize names of languages to what's accepted by website
            all_lang (set): all variations accepted as input 
        """
        # default values
        if base_url is None:
            base_url = 'http://dictionary.reverso.net/{lang1}-{lang2}/'
        if hdr is None:
            hdr = {'User-Agent': 'Mozilla/5.0'}
        if lang_dict is None:
            lang_dict = {'fra': 'francais', 'fr': 'francais',
                         'it': 'italien', 'ita': 'italien',
                         'def': 'definition',
                         'esp': 'espagnol', 'es': 'espagnol', 'spa': 'espagnol',
                         'eng': 'anglais', 'ang': 'anglais',
                         'por': 'portugais', 'port': 'portugais'}
        if all_lang is None:
            all_lang = list(set(lang_dict.values()) | set(lang_dict.keys()))
        # store in attributes
        self.base_url = base_url
        self.hdr = hdr
        self.lang_dict = lang_dict
        self.all_lang = all_lang

    @staticmethod
    def _parse_html_elements(html_elems, lang1, lang2, verbose=False, ffill=False):
        """
        Method to parse html elements and organise them in a structured fashion.
        Look at tag elements in sequence and find ways to understand whether content 
        relate to original language, target language or context/category by looking for
        hints in attributes like 'direction', 'id', 'style' or 'title'
        
        Args:
            html_elems (bs4.element.ResultSet): list containing html elements
            lang1 (str): language to translate from
            lang2 (str): language to translate to
            verbose (bool, optional): whether to show debugging prints
            ffill (bool, optional): whether to forward fill lang1
        
        Returns:
            (pd.DataFrame): frame with content organized
        """
        # initiate parameters
        df = pd.DataFrame(columns=[lang1, 'contexte', 'cat', lang2])
        idx = 0
        is_defined_orig_word = False
        # loop through bs4 tags
        for elem in html_elems:
            # skip empty lines
            content = elem.getText().strip().replace('\n', '').replace('\r', '')
            if content == '':
                continue
            if verbose:
                print("\n")
                print(elem.getText())
                print(elem.attrs)
                print(idx)
            # catch examples
            if content[0] == '→':
                df.loc[idx, 'cat'] = 'e.g.'
                df.loc[idx, lang1] = content
                if verbose:
                    print('idx +1 example')
                idx += 1
                continue
            # catch expressions
            if 'id' in elem.attrs:
                if elem['id'] == "ctl00_cC_ucResEM_lblEntry":
                    df.loc[idx, lang1] = content
                    if verbose:
                        print('writing orig word based on id')
                    is_defined_orig_word = True
                    continue
                elif elem['id'] == "ctl00_cC_ucResEM_lblTranslation":
                    df.loc[idx, 'cat'] = 'exp.'
                    df.loc[idx, lang2] = content
                    if verbose:
                        print('idx +1 expression')
                    is_defined_orig_word = False
                    idx += 1
                    continue
            # deal with them in cycles afterwards
            # assume it goes from source language to target language
            if 'direction' in elem.attrs:
                # first element, target language or not
                if 'target' not in elem['direction']:
                    # then color used, if any
                    if 'style' in elem.attrs:
                        # green means it's context
                        if elem['style'] == 'color:#008000;':
                            df.loc[idx, 'contexte'] = content
                            if verbose:
                                print('assigned to context based on style')
                            continue
                        # light grey is context too
                        if elem['style'] == 'color:#808080;':
                            df.loc[idx, 'contexte'] = content
                            if verbose:
                                print('assigned to context based on style')
                            continue
                        # blue it's the word in original language
                        elif elem['style'] == 'color:#0000ff;': 
                            if not is_defined_orig_word:
                                df.loc[idx, lang1] = content
                                is_defined_orig_word = True
                                if verbose:
                                    print('writing orig word based on style')
                                continue
                            if verbose:
                                print('skipped orig word based on style')
                            continue
                        # red for category
                        elif elem['style'] == 'color:#B50000;':
                            df.loc[idx, 'cat'] = content
                            if verbose:
                                print('assigned to category based on style')
                            continue
                        # white on black background for numbers
                        elif elem['style'] == 'color:#ffffff;':
                            if verbose:
                                print('skipped based on style')
                            continue
                    # title if color not there, if there is a title it's a category, unless... it's context
                    if 'title' not in elem.attrs:
                        if not is_defined_orig_word:
                            df.loc[idx, lang1] = content
                            is_defined_orig_word = True
                            if verbose:
                                print('writing orig word based on title')
                        continue
                    else:
                        # catch context - contains square bracket
                        if "[" in content:
                            df.loc[idx, 'contexte'] = content
                            if verbose:
                                print('assigned to context based on title + contains [')
                            continue
                        df.loc[idx, 'cat'] = content
                        if verbose:
                            print('assigned to category based on title')
                        continue
                else:
                    # skipping terminaisons
                    if elem['direction'] == 'targettargettargettargettargettarget':
                        if verbose:
                            print('skipping terminaison based on direction')
                        continue
                    df.loc[idx, lang2] = content
                    if verbose:
                        print('idx +1 target in direction')
                    is_defined_orig_word = False
                    idx += 1
                    
        if ffill:
            df[lang1] = df[lang1].ffill()
        return df.fillna('')
    
    def get_translation_or_definition(self, mot, lang1, lang2, target=False):
        """
        Method to translate word, by querying url for that word, after doing some normalization. It first 
        set up the operation to be performed. if 'definition' is used as a second parameter it goes and fetch
        the definition (not available in all languages from website) 
        
        Args:
            mot (str): word to translate/define
            lang1 (str): language to translate from
            lang2 (str): language to translate to
            target (bool, optional): whether to see only content in target language in content-df
        
        Returns:
            word_url (str): URL queried, for debugging purposes
            box0_elems_norm (str): raw html in str format for main translate box
            box1_elems_norm (str): raw html in str format for second translate box
            content_df (pd.DataFrame): frame with content organized for all page
        """
        # first set up translation type
        # initial checks
        assert all([lang.lower() in self.all_lang for lang in [lang1, lang2]]), \
            "languages must be in {}, {} and {} were passed".format(self.all_lang, lang1, lang2)
        # replace entries to something accepted by website
        if lang1.lower() in self.lang_dict.keys():
            lang1 = self.lang_dict[lang1.lower()]
        if lang2.lower() in self.lang_dict.keys():
            lang2 = self.lang_dict[lang2.lower()]
        # normalized languages
        # modify url accordingly
        url = self.base_url.format(lang1=lang1, lang2=lang2)
        # some normalization, lower case, stripping, replacing spaces with '+'
        mot = mot.lower().strip().replace(" ", "+")
        # make request to website
        word_url = url + mot
        res = requests.get(word_url, headers=self.hdr)
        res.raise_for_status()
        # parse resquest response
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        # remove items I don't want to see - like logos
        element = soup.find("div", id="dicoCopyright")
        if element:
            element.decompose()
        elements = soup.find_all("div", {"class": "dicoCopyr"})
        if elements:
            for element in elements:
                element.decompose()
        elements = soup.find_all("div", {"class": "logocorner"})
        if elements:
            for element in elements:
                element.decompose()
        elements = soup.find_all("img", {"class": "collins_logo_right"})
        if elements:
            for element in elements:
                element.decompose()
        # look for specific tags
        # 'direction' for everything related to translation
        # 'direction' and something with 'target' for everything related to translation in the target language
        if target:
            html_elems = soup.select('span[direction^="target"]')
        else:
            html_elems = soup.select('span[direction]')
        # structure html elements into a frame
        content_df = self._parse_html_elements(html_elems, lang1, lang2, verbose=False, ffill=False)
        # selecting only translate boxes I am interested in for raw html
        translate_box0_elems = soup.find_all("div", {"class": "translate_box0"})
        translate_box1_elems = soup.find_all("div", {"id": "translate_box1"})
        # do some normalization to get a nice html, removing list characters like squared brackets and commas
        # also take care of encoding normalization
        box0_elems_norm = str(translate_box0_elems).replace("[", "").replace("]", "").replace(",", "")
        box0_elems_norm = unicodedata.normalize('NFKD', box0_elems_norm)
        box1_elems_norm = str(translate_box1_elems).replace("[", "").replace("]", "").replace(",", "")
        box1_elems_norm = unicodedata.normalize('NFKD', box1_elems_norm)
        return word_url, box0_elems_norm, box1_elems_norm, content_df


if __name__ == "__main__":
    app = ReversoDictionary()
    input_word = 'croquant'
    lang_from = 'fr'
    lang_to = 'def'
    w_url, box0_elms_norm, box1_elms_norm, table_df = app.get_translation_or_definition(input_word, lang_from, lang_to)
