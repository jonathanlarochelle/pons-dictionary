# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings
import html.parser

# import third-party modules
import bs4

# import your own module
from pons_dictionary.rom import Rom
import pons_dictionary.parser as parser


class Entry:
    """
    All data pertaining to an Entry.

    [...]
    """

    def __init__(self, pons_api_entry: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        # Initialize attributes
        self._opendict = None
        self._roms = []

        # Parsing pons_api_entry dict
        self._opendict = pons_api_entry['opendict']

        # Parsing roms
        for rom in pons_api_entry["roms"]:
            self._roms.append(Rom(rom, acronyms_in_fields, acronyms_in_text, hints_in_text))

    @property
    def opendict(self) -> bool:
        return self._opendict

    @property
    def roms(self) -> typing.List[Rom]:
        return self._roms


class EntryWithSecondaryEntries:
    """
    All data pertaining to an Entry with secondary entries.

    [...]
    """

    def __init__(self, pons_api_entry: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        self._primary_entry = Entry(pons_api_entry["primary_entry"], acronyms_in_fields, acronyms_in_text, hints_in_text)
        self._secondary_entries = []
        for secondary_entry in pons_api_entry["secondary_entries"]:
            self._secondary_entries.append(Entry(secondary_entry, acronyms_in_fields, acronyms_in_text, hints_in_text))

    @property
    def primary_entry(self) -> Entry:
        return self._primary_entry

    @property
    def secondary_entries(self) -> typing.List[Entry]:
        return self._secondary_entries
