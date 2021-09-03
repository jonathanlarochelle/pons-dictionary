# -*- coding: utf-8 -*-

# import built-in module
import typing
import warnings

# import third-party modules
import requests

# import your own module
from pons_dictionary.entry import Entry, EntryWithSecondaryEntries, Translation
from pons_dictionary.exceptions_warnings import PonsApiRequestError, BadDictionaryError


class PonsDictionary:
    """
    Represents a PonsDictionary

    Params:
    - from_language: language of word to translate (two-letter codes as per ISO 639-1)
    - to_language: translation language  (two-letter codes as per ISO 639-1)
    - api_key:
    - fuzzy_matching: see Pons API documentation
    - references: see Pons API documentation
    """

    # TODO: Should we allow user to set output_language?

    valid_dictionaries = ['deel', 'deen', 'defr', 'dees', 'deru', 'depl', 'deit', 'dept', 'detr', 'dela', 'desl',
                           'enes', 'enfr', 'enpl', 'ensl', 'espl', 'frpl', 'itpl', 'plru', 'essl', 'frsl', 'itsl',
                           'enit', 'enpt', 'enru', 'espt', 'esfr', 'delb', 'dezh', 'enzh', 'eszh', 'frzh', 'denl',
                           'arde', 'defa', 'defi', 'dehr', 'deja', 'dero', 'desk', 'esit', 'frit', 'bgde', 'bgen',
                           'dade', 'csde', 'dehu', 'deno', 'desv', 'kfzdeen', 'wmeddeen', 'wgeodeen', 'winddeen',
                           'deis', 'desr', 'ensr', 'dede', 'dedx']
    tested_dictionaries = ['deen', 'defr', 'enfr', 'dede']

    def __init__(self, from_language: str, to_language: str, api_key: str, fuzzy_matching: bool = False, references: bool = True):
        self._from_language = from_language
        self._to_language = to_language
        self._dictionary = self._get_dictionary_code_from_language_codes(from_language, to_language)
        self._api_key = api_key
        self._fuzzy_matching = fuzzy_matching
        self._references = references

    def search(self, term) -> typing.List[typing.Union[Entry, EntryWithSecondaryEntries, Translation]]:
        url = "https://api.pons.com/v1/dictionary"
        payload = {"q": term,
                   "l": self._dictionary,
                   "in": self._from_language,
                   "fm": self._fuzzy_matching,
                   "ref": self._references,
                   'language': 'en'}
        headers = {"X-Secret": self._api_key}

        r = requests.get(url, params=payload, headers=headers)
        status_code = r.status_code

        if status_code == 200: # OK - Results found
            entries_list = []
            contents = r.json()[0]
            for hit in contents['hits']:
                if hit['type'] == 'entry':
                    entries_list.append(Entry(hit))
                elif hit['type'] == 'translation':
                    entries_list.append(Translation(hit))
                elif hit['type'] == 'entry_with_secondary_entries':
                    entries_list.append(EntryWithSecondaryEntries(hit))
            return entries_list
        elif status_code == 204: # NO CONTENT - No results found
            return []
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

    def _get_dictionary_code_from_language_codes(self, from_code: str, to_code: str) -> str:
        codes_list = [from_code, to_code]
        codes_list.sort()
        dictionary_code = codes_list[0] + codes_list[1]

        if dictionary_code in self.valid_dictionaries:
            if dictionary_code not in self.tested_dictionaries:
                warnings.warn(f"Dictionary {dictionary_code} is valid, but has not been tested within PonsDictionary. "
                              f"Use at your own risk. Tested dictionaries are {self.tested_dictionaries}", UserWarning)
            return dictionary_code
        else:
            raise BadDictionaryError(f"Dictionary {dictionary_code} is not supported by the PONS API. Valid "
                                     f"dictionnaries are listed in PonsDictionary.valid_dictionaries")

    @property
    def from_language(self) -> str:
        return self._from_language

    @property
    def to_language(self) -> str:
        return self._to_language

    @property
    def dictionary(self) -> str:
        return self._dictionary

    @property
    def fuzzy_matching(self) -> str:
        return self._fuzzy_matching

    @property
    def references(self) -> str:
        return self._references
