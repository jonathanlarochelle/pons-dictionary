# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings

# import third-party modules

# import your own module
from pons_dictionary.translation_entry import TranslationEntry


class Translation:
    """
    A Translation is comprised of a source (original expression) and a target (translated expression).
    """

    def __init__(self, pons_api_translation_dict: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        # Initialize attributes
        self._raw = pons_api_translation_dict
        self._opendict = None
        self._source = None
        self._target = None

        # Parsing pons_translation_obj
        if "opendict" in pons_api_translation_dict:
            self._opendict = pons_api_translation_dict['opendict']

        if "source" in pons_api_translation_dict:
            self._source = TranslationEntry(pons_api_translation_dict['source'], acronyms_in_fields, acronyms_in_text,
                                            hints_in_text)

        if "target" in pons_api_translation_dict:
            self._target = TranslationEntry(pons_api_translation_dict['target'], acronyms_in_fields, acronyms_in_text,
                                            hints_in_text)

    @property
    def raw(self) -> dict:
        return self._raw

    @property
    def opendict(self) -> bool:
        return self._opendict

    @property
    def source(self) -> TranslationEntry:
        return self._source

    @property
    def target(self) -> TranslationEntry:
        return self._target
