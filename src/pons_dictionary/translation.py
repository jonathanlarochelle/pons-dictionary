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

    def __init__(self, pons_translation_obj: dict):
        # Initialize attributes
        self._raw = pons_translation_obj
        self._opendict = None
        self._source = None
        self._target = None

        # Parsing pons_translation_obj
        bool_map = {"true": True, "false": False}
        if "opendict" in pons_translation_obj:
            self._opendict = bool_map[pons_translation_obj['opendict']]

        if "source" in pons_translation_obj:
            self._source = TranslationEntry(pons_translation_obj['source'])

        if "target" in pons_translation_obj:
            self._target = TranslationEntry(pons_translation_obj['target'])

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
