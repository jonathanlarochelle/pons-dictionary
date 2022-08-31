# -*- coding: utf-8 -*-

# import built-in module
import typing
import warnings

# import third-party modules
import requests

# import your own module
from .entry import Entry, EntryWithSecondaryEntries, Translation
from .exceptions_warnings import *


class PonsDictionary:
    """
    Represents a PonsDictionary

    Params:
    - api_key: secret API key
    - dictionary: takes precedence over from_language and to_language, should be part of VALID_DICTIONARIES.
    - from_language: [optional] language of word to translate (two-letter codes as per ISO 639-1)
    - fuzzy_matching: [optional] see Pons API documentation
    - references: [optional] see Pons API documentation
    - output_language: [optional] language of output (two-letter codes as per ISO 639-1)
    """

    VALID_DICTIONARIES = ['deel', 'deen', 'defr', 'dees', 'deru', 'depl', 'deit', 'dept', 'detr', 'dela', 'desl',
                           'enes', 'enfr', 'enpl', 'ensl', 'espl', 'frpl', 'itpl', 'plru', 'essl', 'frsl', 'itsl',
                           'enit', 'enpt', 'enru', 'espt', 'esfr', 'delb', 'dezh', 'enzh', 'eszh', 'frzh', 'denl',
                           'arde', 'defa', 'defi', 'dehr', 'deja', 'dero', 'desk', 'esit', 'frit', 'bgde', 'bgen',
                           'dade', 'csde', 'dehu', 'deno', 'desv', 'kfzdeen', 'wmeddeen', 'wgeodeen', 'winddeen',
                           'deis', 'desr', 'ensr', 'dede', 'dedx']
    TESTED_DICTIONARIES = ['deen', 'defr', 'enfr', 'dede']
    VALID_LANGUAGES = ['de', 'el', 'en', 'es', 'fr', 'it', 'pl', 'pt', 'ru', 'sl', 'tr', 'zh']

    def __init__(self, api_key: str, dictionary: str, from_language: str = None, fuzzy_matching: bool = False,
                 references: bool = True, output_language: str = "en"):
        self._api_key = api_key
        self.dictionary = dictionary
        self.from_language = from_language
        self._fuzzy_matching = fuzzy_matching
        self._references = references
        self.output_language = output_language

    def search(self, term: str) -> typing.List[typing.Union[Entry, EntryWithSecondaryEntries, Translation]]:
        """
        Search for "term" in the dictionary.
        Returns a list of hits, which are one of the following classes: Entry, Translation, EntryWithSecondaryEntries
        """
        url = "https://api.pons.com/v1/dictionary"
        payload = {"q": term,
                   "l": self._dictionary}
        headers = {"X-Secret": self._api_key}

        if self.from_language is not None:
            payload["in"] = self.from_language
        if self.fuzzy_matching is not None:
            payload["fm"] = self.fuzzy_matching
        if self.references is not None:
            payload["ref"] = self.references
        if self.output_language is not None:
            payload["language"] = self.output_language

        r = requests.get(url, params=payload, headers=headers)
        status_code = r.status_code

        entries_list = list()

        if status_code == 200: # OK - Results found
            contents = r.json()[0]
            for hit in contents['hits']:
                if hit['type'] == 'entry':
                    entries_list.append(Entry(hit))
                elif hit['type'] == 'translation':
                    entries_list.append(Translation(hit))
                elif hit['type'] == 'entry_with_secondary_entries':
                    entries_list.append(EntryWithSecondaryEntries(hit))
        elif status_code == 204: # NO CONTENT - No results found
            pass
        elif status_code == 404: # NOT FOUND - Dictionary does not exist
            raise PonsApiRequestError(f"PONS API request returned code 404 (NOT FOUND) - The dictionary {self.dictionary} does not "
                                      f"exist.")
        elif status_code == 403: # NOT AUTHORIZED - Bad api-key, access to dictionary is not allowed
            raise PonsApiRequestError(f"PONS API returned code 403 (NOT AUTHORIZED) - The supplied credentials could "
                                      f"not be verified or the access to dictionary {self.dictionary} is not allowed.")
        elif status_code == 500: # INTERNAL SERVER ERROR
            raise PonsApiRequestError(f"PONS API returned code 500 (INTERNAL SERVER ERROR) - An internal error has "
                                      f"occurred, please try again later.")
        elif status_code == 503: # SERVICE UNAVAILABLE - Daily limit has been reached
            raise PonsApiRequestError(f"PONS API returned code 503 (SERVICE UNAVAILABLE) - The daily limit has been "
                                      f"reached. Please try again tomorrow.")

        return entries_list

    @property
    def dictionary(self) -> str:
        return self._dictionary

    @dictionary.setter
    def dictionary(self, d):
        if d in self.VALID_DICTIONARIES:
            if d not in self.TESTED_DICTIONARIES:
                warnings.warn(f"Dictionary {d} is valid, but has not been tested within PonsDictionary. "
                              f"Use at your own risk. Tested dictionaries are {self.TESTED_DICTIONARIES}", UserWarning)
            self._dictionary = d
        else:
            raise UnsupportedDictionaryError(f"Dictionary {d} is not supported by the PONS API. Valid "
                                             f"dictionnaries are {self.VALID_DICTIONARIES}.")

    @property
    def from_language(self) -> str:
        return self._from_language

    @from_language.setter
    def from_language(self, language: str):
        """ language should be in the format of a two-letter codes as per ISO 639-1 """
        if language is None:
            self._from_language = None
        elif language in self.dictionary:
            self._from_language = language
        else:
            raise UnsupportedLanguageError(f"Language {language} is not part of "
                                           f"the selected dictionary {self.dictionary}.")

    @property
    def fuzzy_matching(self) -> str:
        return self._fuzzy_matching

    @property
    def references(self) -> str:
        return self._references

    @property
    def output_language(self) -> str:
        return self._output_language

    @output_language.setter
    def output_language(self, language):
        """ language should be in the format of a two-letter codes as per ISO 639-1 """
        if language in self.VALID_LANGUAGES:
            self._output_language = language
        else:
            raise UnsupportedLanguageError(f"Language {language} is not supported by the PONS API as a source language."
                                           f"Valid languages are {self.VALID_LANGUAGES}.")
