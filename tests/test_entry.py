# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pytest

# import your own module
import pons_dictionary.entry
from pons_dictionary.entry import Entry, EntryWithSecondaryEntries


class TestEntry:
    """
    Tests for Entry.
    """

    def test_opendict(self):
        api_raw = {"opendict": True,
                   "roms": []
                   }
        e = Entry(api_raw, False, False, False)
        assert e.opendict is True

    def test_roms(self, mocker):
        spy = mocker.spy(pons_dictionary.entry.Rom, "__init__")
        # 'ad', en > fr
        api_raw = {
            "type": "entry",
            "opendict": False,
            "roms": [
                {
                    "headword": "ad-lib",
                    "headword_full": "ad-lib   <span class=\"flexion\">&lt;-bb-&gt;</span>  <span class=\"phonetics\">[\u02cc\u00e6d\u02c8l\u026ab]</span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym>, <acronym title=\"intransitive verb\">intr</acronym></span>",
                    "wordclass": "intransitive or transitive verb",
                    "arabs": []
                },
                {
                    "headword": "ad-lib",
                    "headword_full": "ad-lib    <span class=\"phonetics\">[\u02cc\u00e6d\u02c8l\u026ab]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span>",
                    "wordclass": "noun",
                    "arabs": []
                }
            ]
        }
        e = Entry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)

        spy.assert_any_call(e.roms[0], api_raw["roms"][0], False, False, False)
        spy.assert_any_call(e.roms[1], api_raw["roms"][1], False, False, False)
        assert len(e.roms) == 2
        assert isinstance(e.roms[0], pons_dictionary.entry.Rom)
        assert isinstance(e.roms[1], pons_dictionary.entry.Rom)

    def test_roms_none(self):
        # Never encountered an entry without roms so far, but it is useful to consider.
        # 'ad', en > fr
        api_raw = {
            "type": "entry",
            "opendict": False,
            "roms": []
        }
        e = Entry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert e.roms == []


class TestEntryWithSecondaryEntries:
    """
    Tests for EntryWithSecondaryEntries.
    """

    def test_init(self, mocker):
        spy = mocker.spy(pons_dictionary.entry.Entry, "__init__")
        # 'ad', en > fr
        api_raw = {
                "type": "entry_with_secondary_entries",
                "primary_entry": {
                    "type": "entry",
                    "opendict": False,
                    "roms": []
                },
                "secondary_entries": [
                    {
                        "type": "entry",
                        "opendict": False,
                        "roms": []
                    }
                ]
            }
        e = EntryWithSecondaryEntries(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)

        spy.assert_any_call(e.primary_entry, api_raw["primary_entry"], False, False, False)
        spy.assert_any_call(e.secondary_entries[0], api_raw["secondary_entries"][0], False, False, False)
        assert len(e.secondary_entries) == 1
        assert isinstance(e.primary_entry, pons_dictionary.entry.Entry)
        assert isinstance(e.secondary_entries[0], pons_dictionary.entry.Entry)
