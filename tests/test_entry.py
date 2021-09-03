# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pytest

# import your own module
import pons_dictionary.entry
from pons_dictionary.entry import Entry, EntryWithSecondaryEntries, Rom, Arab, Translation, TranslationEntry


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


class TestRom:
    """
    Tests for Rom.

    First set of tests is simple testing of each attribute. Second set of tests is testing the overall behavior of
    Rom for specific corner cases. If an unexpected behavior arises in normal use, the offending raw API dict can be
    copied at the end in a new specific test.
    """

    def test_raw(self):
        # 'route', fr > de
        api_raw = {
                        "headword": "grand-route",
                        "headword_full": "grand-route   <span class=\"flexion\">&lt;grands-routes&gt;</span>  <span class=\"phonetics\">[g\u0280\u0251\u0342\u0280ut]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
                        "wordclass": "noun",
                        "arabs": []
                    }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.raw == api_raw

    def test_headword(self):
        # 'route', fr > de
        api_raw = {
            "headword": "grand-route",
            "headword_full": "grand-route   <span class=\"flexion\">&lt;grands-routes&gt;</span>  <span class=\"phonetics\">[g\u0280\u0251\u0342\u0280ut]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.headword == 'grand-route'

    def test_wordclass(self):
        # 'route', fr > de
        api_raw = {
            "headword": "grand-route",
            "headword_full": "grand-route   <span class=\"flexion\">&lt;grands-routes&gt;</span>  <span class=\"phonetics\">[g\u0280\u0251\u0342\u0280ut]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.wordclass == 'noun'

    def test_wordclass_with_acronyms(self):
        # 'route', fr > de
        api_raw = {
            "headword": "grand-route",
            "headword_full": "grand-route   <span class=\"flexion\">&lt;grands-routes&gt;</span>  <span class=\"phonetics\">[g\u0280\u0251\u0342\u0280ut]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.wordclass == 'N'

    def test_wordclass_verb(self):
        # 'abbrechen', de > fr
        api_raw = {
            "headword": "ab|brechen",
            "headword_full": "<span class=\"headword_attributes\" title=\"\">ab|brechen</span>    <span class=\"info\"><acronym title=\"irregular\">irreg</acronym></span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span> <span class=\"auxiliary_verb\">+haben</span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.wordclass == 'verb'

    def test_wordclass_verb_with_acronyms(self):
        # 'abbrechen', de > fr
        api_raw = {
            "headword": "ab|brechen",
            "headword_full": "<span class=\"headword_attributes\" title=\"\">ab|brechen</span>    <span class=\"info\"><acronym title=\"irregular\">irreg</acronym></span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span> <span class=\"auxiliary_verb\">+haben</span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.wordclass == 'VB'

    def test_arabs(self, mocker):
        spy = mocker.spy(pons_dictionary.entry.Arab, "__init__")
        # 'entreprendre', fr > de
        api_raw = {
                        "headword": "entreprendre",
                        "headword_full": "entreprendre    <span class=\"phonetics\">[\u0251\u0342t\u0280\u0259p\u0280\u0251\u0342d\u0280]</span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span>",
                        "wordclass": "transitive verb",
                        "arabs": [
                            {
                                "header": "1. entreprendre <span class=\"sense\">(commencer)</span>:",
                                "translations": []
                            },
                            {
                                "header": "2. entreprendre <span class=\"style\"><acronym title=\"informal\">inf</acronym></span> <span class=\"sense\">(s&#39;efforcer de convaincre)</span>:",
                                "translations": []
                            },
                            {
                                "header": "3. entreprendre <span class=\"sense\">(courtiser)</span>:",
                                "translations": []
                            }
                        ]
                    }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)

        spy.assert_any_call(r.arabs[0], api_raw["arabs"][0], False, False, False)
        spy.assert_any_call(r.arabs[1], api_raw["arabs"][1], False, False, False)
        spy.assert_any_call(r.arabs[2], api_raw["arabs"][2], False, False, False)
        assert len(r.arabs) == 3
        assert isinstance(r.arabs[0], pons_dictionary.entry.Arab)
        assert isinstance(r.arabs[1], pons_dictionary.entry.Arab)
        assert isinstance(r.arabs[2], pons_dictionary.entry.Arab)

    def test_arabs_none(self):
        # Never encountered a case without arabs so far, but it is useful to consider.
        # 'abbrechen', de > fr
        api_raw = {
            "headword": "ab|brechen",
            "headword_full": "<span class=\"headword_attributes\" title=\"\">ab|brechen</span>    <span class=\"info\"><acronym title=\"irregular\">irreg</acronym></span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span> <span class=\"auxiliary_verb\">+haben</span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.arabs == []

    def test_alt_headword(self):
        # 'Werbung', de > fr
        api_raw = {
                        "headword": "Internetwerbung",
                        "headword_full": "Internetwerbung, <span class=\"headword\">Internet-Werbung</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
                        "wordclass": "noun",
                        "arabs": []
                    }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.alt_headword == ['Internet-Werbung', '']

    def test_alt_headword_with_spelling_rule(self):
        # 'parfum', fr > de
        api_raw = {
            "headword": "brule-parfum",
            "headword_full": "brule-parfum<span class=\"headword_spelling\"><acronym title=\"French spelling reform, 1990\">NO</acronym></span>   <span class=\"flexion\">&lt;brule-parfums&gt;</span>  <span class=\"phonetics\">[b\u0280ylpa\u0280f\u0153\u0342]</span>, <span class=\"headword\">br\u00fble-parfum<span class=\"headword_spelling\"><acronym title=\"traditional spelling\">OT</acronym></span></span> <span class=\"info\"><acronym title=\"invariable\">inv</acronym></span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.alt_headword == ["brûle-parfum", "traditional spelling"]

    def test_alt_headword_with_spelling_rule_with_acronyms(self):
        # 'parfum', fr > de
        api_raw = {
            "headword": "brule-parfum",
            "headword_full": "brule-parfum<span class=\"headword_spelling\"><acronym title=\"French spelling reform, 1990\">NO</acronym></span>   <span class=\"flexion\">&lt;brule-parfums&gt;</span>  <span class=\"phonetics\">[b\u0280ylpa\u0280f\u0153\u0342]</span>, <span class=\"headword\">br\u00fble-parfum<span class=\"headword_spelling\"><acronym title=\"traditional spelling\">OT</acronym></span></span> <span class=\"info\"><acronym title=\"invariable\">inv</acronym></span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.alt_headword == ["brûle-parfum", "OT"]

    def test_auxiliary_verb(self):
        # 'abbrechen', de > fr
        api_raw = {
            "headword": "ab|brechen",
            "headword_full": "<span class=\"headword_attributes\" title=\"\">ab|brechen</span>    <span class=\"info\"><acronym title=\"irregular\">irreg</acronym></span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span> <span class=\"auxiliary_verb\">+haben</span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.auxiliary_verb == 'haben'

    def test_flexion_de_noun(self):
        # 'Apfel', de > fr
        api_raw = {
            "headword": "Apfel",
            "headword_full": "Apfel   <span class=\"flexion\">&lt;-s, \u00c4pfel&gt;</span>  <span class=\"phonetics\">[\u02c8apf\u0259l, <span class=\"info\">Pl\u02d0</span> \u02c8\u025bpf\u0259l]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.flexion == '-s, Äpfel'

    def test_flexion_de_adjective(self):
        # 'groß', de > fr
        api_raw = {
            "headword": "gro\u00df",
            "headword_full": "gro\u00df <span class=\"flexion\">&lt;gr\u00f6\u00dfer, gr\u00f6\u00dfte&gt;</span>  <span class=\"phonetics\">[gro\u02d0s]</span> <span class=\"wordclass\"><acronym title=\"adjective\">ADJ</acronym></span>",
            "wordclass": "adjective and adverb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.flexion == 'größer, größte'

    def test_flexion_fr_noun(self):
        # 'route', fr > de
        api_raw = {
            "headword": "grand-route",
            "headword_full": "grand-route   <span class=\"flexion\">&lt;grands-routes&gt;</span>  <span class=\"phonetics\">[g\u0280\u0251\u0342\u0280ut]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.flexion == 'grands-routes'

    def test_genus(self):
        # 'route', fr > de
        api_raw = {
            "headword": "grand-route",
            "headword_full": "grand-route   <span class=\"flexion\">&lt;grands-routes&gt;</span>  <span class=\"phonetics\">[g\u0280\u0251\u0342\u0280ut]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.genus == 'feminine'

    def test_genus_with_acronyms(self):
        # 'route', fr > de
        api_raw = {
            "headword": "grand-route",
            "headword_full": "grand-route   <span class=\"flexion\">&lt;grands-routes&gt;</span>  <span class=\"phonetics\">[g\u0280\u0251\u0342\u0280ut]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.genus == 'f'

    def test_headword_attributes(self):
        # 'unternehmen', de > fr
        api_raw = {
            "headword": "unternehmen",
            "headword_full": "<span class=\"headword_attributes\" title=\"German past participle formed without ge-\">unternehmen*</span>    <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span> <span class=\"info\"><acronym title=\"irregular\">irreg</acronym></span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.headword_attributes == 'German past participle formed without ge-'
        assert r.headword == "unternehmen"

    def test_info(self):
        # 'gros', fr > de
        api_raw = {
                        "headword": "demi-gros",
                        "headword_full": "demi-gros    <span class=\"phonetics\">[d(\u0259)mig\u0280o]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span> <span class=\"info\">sans <acronym title=\"plural\">pl</acronym></span>",
                        "wordclass": "noun",
                        "arabs": []
                    }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.info == 'sans plural'

    def test_info_with_acronyms(self):
        # 'gros', fr > de
        api_raw = {
                        "headword": "demi-gros",
                        "headword_full": "demi-gros    <span class=\"phonetics\">[d(\u0259)mig\u0280o]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span> <span class=\"info\">sans <acronym title=\"plural\">pl</acronym></span>",
                        "wordclass": "noun",
                        "arabs": []
                    }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.info == 'sans pl'

    def test_modus(self):
        # 'parce que', fr > de
        api_raw = {
            "headword": "parce que",
            "headword_full": "parce que    <span class=\"phonetics\">[pa\u0280sk\u0259]</span> <span class=\"wordclass\"><acronym title=\"conjunction\">CONJ</acronym></span> <span class=\"modus\">+<acronym title=\"indicative\">ind</acronym></span>",
            "wordclass": "conjunction",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.modus == 'indicative'

    def test_modus_with_acronyms(self):
        # 'parce que', fr > de
        api_raw = {
            "headword": "parce que",
            "headword_full": "parce que    <span class=\"phonetics\">[pa\u0280sk\u0259]</span> <span class=\"wordclass\"><acronym title=\"conjunction\">CONJ</acronym></span> <span class=\"modus\">+<acronym title=\"indicative\">ind</acronym></span>",
            "wordclass": "conjunction",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.modus == 'ind'

    def test_number(self):
        # 'cut', en > fr
        api_raw = {
            "headword": "cut flowers",
            "headword_full": "cut flowers    <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"number\"><acronym title=\"plural\">pl</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.number == "plural"

    def test_number_with_acronyms(self):
        # 'cut', en > fr
        api_raw = {
            "headword": "cut flowers",
            "headword_full": "cut flowers    <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"number\"><acronym title=\"plural\">pl</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.number == "pl"

    def test_object_case(self):
        # 'nach', de > fr
        api_raw = {
                        "headword": "nach",
                        "headword_full": "nach    <span class=\"phonetics\">[na\u02d0x]</span> <span class=\"wordclass\"><acronym title=\"preposition\">PREP</acronym></span> <span class=\"object-case\">+Dat</span>",
                        "wordclass": "preposition",
                        "arabs": []
                    }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.object_case == 'Dat'

    def test_phonetics(self):
        # 'entreprendre', fr > de
        api_raw = {
            "headword": "entreprendre",
            "headword_full": "entreprendre    <span class=\"phonetics\">[\u0251\u0342t\u0280\u0259p\u0280\u0251\u0342d\u0280]</span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.phonetics == 'ɑ͂tʀəpʀɑ͂dʀ'

    def test_region(self):
        # 'apartment', en > fr
        api_raw = {
            "headword": "apartment building",
            "headword_full": "apartment building    <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span>, <span class=\"headword\">apartment house</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"region\"><acronym title=\"American English\" class=\"Am\">Am</acronym></span> <span class=\"sense\">(block of flats)</span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.region == 'American English'

    def test_region_with_acronyms(self):
        # 'apartment', en > fr
        api_raw = {
            "headword": "apartment building",
            "headword_full": "apartment building    <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span>, <span class=\"headword\">apartment house</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"region\"><acronym title=\"American English\" class=\"Am\">Am</acronym></span> <span class=\"sense\">(block of flats)</span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.region == 'Am'

    def test_sense(self):
        # 'apartment', en > fr
        api_raw = {
            "headword": "apartment building",
            "headword_full": "apartment building    <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span>, <span class=\"headword\">apartment house</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"region\"><acronym title=\"American English\" class=\"Am\">Am</acronym></span> <span class=\"sense\">(block of flats)</span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.sense == 'block of flats'

    def test_spelling_source(self):
        # 'parfum', fr > de
        api_raw = {
            "headword": "brule-parfum",
            "headword_full": "brule-parfum<span class=\"headword_spelling\"><acronym title=\"French spelling reform, 1990\">NO</acronym></span>   <span class=\"flexion\">&lt;brule-parfums&gt;</span>  <span class=\"phonetics\">[b\u0280ylpa\u0280f\u0153\u0342]</span>, <span class=\"headword\">br\u00fble-parfum<span class=\"headword_spelling\"><acronym title=\"traditional spelling\">OT</acronym></span></span> <span class=\"info\"><acronym title=\"invariable\">inv</acronym></span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.spelling_source == 'French spelling reform, 1990'

    def test_spelling_source_with_acronyms(self):
        # 'parfum', fr > de
        api_raw = {
            "headword": "brule-parfum",
            "headword_full": "brule-parfum<span class=\"headword_spelling\"><acronym title=\"French spelling reform, 1990\">NO</acronym></span>   <span class=\"flexion\">&lt;brule-parfums&gt;</span>  <span class=\"phonetics\">[b\u0280ylpa\u0280f\u0153\u0342]</span>, <span class=\"headword\">br\u00fble-parfum<span class=\"headword_spelling\"><acronym title=\"traditional spelling\">OT</acronym></span></span> <span class=\"info\"><acronym title=\"invariable\">inv</acronym></span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.spelling_source == 'NO'

    def test_style(self):
        # 'ad', en > fr
        api_raw = {
            "headword": "ad",
            "headword_full": "ad    <span class=\"phonetics\">[\u00e6d]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"style\"><acronym title=\"informal\">inf</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.style == 'informal'

    def test_style_with_acronyms(self):
        # 'ad', en > fr
        api_raw = {
            "headword": "ad",
            "headword_full": "ad    <span class=\"phonetics\">[\u00e6d]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"style\"><acronym title=\"informal\">inf</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.style == 'inf'

    def test_topic(self):
        # 'nach', de > fr
        api_raw = {
            "headword": "Bild-nach-oben-Taste",
            "headword_full": "Bild-nach-oben-Taste    <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span> <span class=\"topic\"><acronym title=\"computing\">COMPUT</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.topic == 'computing'

    def test_topic_with_acronyms(self):
        # 'nach', de > fr
        api_raw = {
            "headword": "Bild-nach-oben-Taste",
            "headword_full": "Bild-nach-oben-Taste    <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span> <span class=\"topic\"><acronym title=\"computing\">COMPUT</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.topic == 'COMPUT'

    def test_verbclass(self):
        # 'cancel', en > fr
        api_raw = {
            "headword": "cancel",
            "headword_full": "cancel   <span class=\"flexion\">&lt;-ll- [<span class=\"or\"><acronym title=\"or\">or</acronym></span> \n\t\t\t<span class=\"region\"><acronym title=\"American English\" class=\"Am\">Am</acronym></span> -l-]&gt;</span>  <span class=\"phonetics\">[\u02c8k\u00e6nsl]</span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.verbclass == 'transitive verb'

    def test_verbclass_with_acronyms(self):
        # 'cancel', en > fr
        api_raw = {
            "headword": "cancel",
            "headword_full": "cancel   <span class=\"flexion\">&lt;-ll- [<span class=\"or\"><acronym title=\"or\">or</acronym></span> \n\t\t\t<span class=\"region\"><acronym title=\"American English\" class=\"Am\">Am</acronym></span> -l-]&gt;</span>  <span class=\"phonetics\">[\u02c8k\u00e6nsl]</span> <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"transitive verb\">trans</acronym></span>",
            "wordclass": "transitive verb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert r.verbclass == 'trans'

    def test_everything_together(self):
        # 'wohnen', de > fr
        api_raw = {
            "headword": "wohnen",
            "headword_full": "wohnen    <span class=\"wordclass\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"intransitive verb\">intr</acronym></span>",
            "wordclass": "intransitive verb",
            "arabs": [
                {
                    "header": "",
                    "translations": [
                        {
                            "source": "<strong class=\"headword\">wohnen</strong>",
                            "target": "habiter"
                        },
                        {
                            "source": "<span class=\"example\">ich wohne in Dresden</span>",
                            "target": "j&#39;habite [\u00e0] Dresde"
                        },
                        {
                            "source": "<span class=\"example\">das Wohnen</span>",
                            "target": "le logement"
                        }
                    ]
                }
            ]
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.raw == api_raw
        assert r.headword == "wohnen"
        assert len(r.arabs) == 1
        assert r.wordclass == 'verb'
        assert r.verbclass == 'intransitive verb'

    def test_empty_api_dict(self):
        api_raw = {}
        with pytest.raises(KeyError):
            _ = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)

    def test_warning_for_unhandled_tags(self):
        # invented string with unhandled tag
        api_raw = {
                        "headword": "wohnen",
                        "headword_full": "wohnen    <span class=\"UNHANDLED\"><acronym title=\"verb\">VB</acronym></span> <span class=\"verbclass\"><acronym title=\"intransitive verb\">intr</acronym></span>",
                        "wordclass": "intransitive verb",
                        "arabs": []
                    }
        with pytest.warns(UserWarning):
            r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
            assert r.raw == api_raw
            assert r.headword == "wohnen"
            assert len(r.arabs) == 0
            assert r.wordclass == None
            assert r.verbclass == 'intransitive verb'

    # Corner cases
    def test_corner_case_1(self):
        # 'Apfel', de > fr
        api_raw = {
            "headword": "Apfel",
            "headword_full": "Apfel   <span class=\"flexion\">&lt;-s, \u00c4pfel&gt;</span>  <span class=\"phonetics\">[\u02c8apf\u0259l, <span class=\"info\">Pl\u02d0</span> \u02c8\u025bpf\u0259l]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"masculine\">m</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.info is None
        assert r.phonetics == 'ˈapfəl, Plː ˈɛpfəl'

    def test_corner_case_2(self):
        # 'Pomme', fr > de
        api_raw = {
            "headword": "pomm\u00e9",
            "headword_full": "pomm\u00e9<span class=\"feminine\">(e)</span>   <span class=\"phonetics\">[p\u0254me]</span> <span class=\"wordclass\"><acronym title=\"adjective\">ADJ</acronym></span>",
            "wordclass": "adjective and adverb",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.headword == "pommé(e)"

    def test_corner_case_3(self):
        # 'bière', fr > de
        api_raw = {
            "headword": "bi\u00e8re",
            "headword_full": "bi\u00e8re<sup>1</sup>    <span class=\"phonetics\">[bj\u025b\u0280]</span> <span class=\"wordclass\"><acronym title=\"noun\">N</acronym></span> <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>",
            "wordclass": "noun",
            "arabs": []
        }
        r = Rom(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert r.headword == "bière"


class TestArab:
    """
    Tests for Arab.

    First set of tests is simple testing of each attribute. Second set of tests is testing the overall behavior of
    Arab for specific corner cases. If an unexpected behavior arises in normal use, the offending raw API dict can be
    copied at the end in a new specific test.
    """

    def test_raw(self):
        # 'gros', fr > de
        api_raw = {"header": "1. gros:",
                   "translations": []
                   }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.raw == api_raw

    def test_headword(self):
        # 'gros', fr > de
        api_raw = {"header": "1. gros:",
                   "translations": []
                   }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.headword == 'gros'

    def test_type_headword(self):
        # 'gros', fr > de
        api_raw = {"header": "1. gros:",
                   "translations": []
                   }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.type == 'headword'

    def test_type_phrases(self):
        # 'cut', en > fr
        api_raw = {"header": "Phrases:",
                   "translations": []
                   }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.type == 'phrases'

    def test_translations(self, mocker):
        spy = mocker.spy(pons_dictionary.entry.Translation, "__init__")
        # 'live', en > fr
        api_raw = {
            "header": "1. live <span class=\"sense\">(living)</span>:",
            "translations": [
                {
                    "source": "<strong class=\"headword\">live</strong>",
                    "target": "vivant(e)"
                },
                {
                    "source": "<span class=\"example\">real <strong class=\"tilde\">live</strong></span>",
                    "target": "en chair et en os"
                }
            ]
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)

        spy.assert_any_call(a.translations[0], api_raw["translations"][0], False, False, False)
        spy.assert_any_call(a.translations[1], api_raw["translations"][1], False, False, False)
        assert len(a.translations) == 2
        assert isinstance(a.translations[0], pons_dictionary.entry.Translation)
        assert isinstance(a.translations[1], pons_dictionary.entry.Translation)

    def test_translations_none(self):
        # Never encountered a case without translations so far, but it is useful to consider.
        # 'cut', en > fr (adapted)
        api_raw = {"header": "Phrases:",
                   "translations": []
                   }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.translations == []

    def test_abbreviation_of(self):
        # 'ad', en > fr
        api_raw = {
            "header": "ad <span class=\"indirect_reference_ABBR\">abbreviation of advertisement</span>",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.abbreviation_of == 'advertisement'

    def test_auxiliary_verb(self):
        # 'abbrechen', de > fr
        api_raw = {
            "header": "1. abbrechen <span class=\"auxiliary_verb\">+sein</span> <span class=\"sense\">(kaputtgehen)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.auxiliary_verb == 'sein'

    def test_collocator(self):
        # 'cut', en > fr
        api_raw = {
            "header": "5. cut <span class=\"rhetoric\"><acronym title=\"figurative\">fig</acronym></span> <span class=\"collocator\">ties</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.collocator == 'ties'

    def test_info(self):
        # 'cut', en > fr
        api_raw = {
            "header": "8. cut <span class=\"info\"><acronym title=\"plural\">pl</acronym></span> <span class=\"sense\">(decrease in government spending)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.info == 'plural'

    def test_info_with_acronyms(self):
        # 'cut', en > fr
        api_raw = {
            "header": "8. cut <span class=\"info\"><acronym title=\"plural\">pl</acronym></span> <span class=\"sense\">(decrease in government spending)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert a.info == 'pl'

    def test_num_none(self):
        # 'ad', en > fr
        api_raw = {
            "header": "ad <span class=\"indirect_reference_ABBR\">abbreviation of advertisement</span>",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.num is None

    def test_num(self):
        # 'gros', fr > de
        api_raw = {"header": "1. gros:",
                   "translations": []
                   }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.num == 1

    def test_other(self):
        # 'abbrechen', de > fr
        api_raw = {
            "header": "abbrechen <span class=\"indirect_reference_OTHER\">→ Schulabbruch</span>",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.other == 'Schulabbruch'

    def test_region(self):
        # 'route', en > fr
        api_raw = {
            "header": "2. route <span class=\"region\"><acronym title=\"American English\" class=\"Am\">Am</acronym></span> <span class=\"sense\">(delivery path)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.region == 'American English'

    def test_region_with_acronyms(self):
        # 'route', en > fr
        api_raw = {
            "header": "2. route <span class=\"region\"><acronym title=\"American English\" class=\"Am\">Am</acronym></span> <span class=\"sense\">(delivery path)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert a.region == 'Am'

    def test_rhetoric(self):
        # 'gros', fr > de
        api_raw = {
            "header": "3. gros <span class=\"rhetoric\"><acronym title=\"humorous\">hum</acronym></span> <span class=\"style\"><acronym title=\"informal\">inf</acronym></span> <span class=\"sense\">(expression affective)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.rhetoric == 'humorous'

    def test_rhetoric_with_acronyms(self):
        # 'gros', fr > de
        api_raw = {
            "header": "3. gros <span class=\"rhetoric\"><acronym title=\"humorous\">hum</acronym></span> <span class=\"style\"><acronym title=\"informal\">inf</acronym></span> <span class=\"sense\">(expression affective)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert a.rhetoric == 'hum'

    def test_sense(self):
        # 'groß', de > fr
        api_raw = {
            "header": "1. gro\u00df <span class=\"sense\">(nicht klein)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.sense == 'nicht klein'

    def test_style(self):
        # 'groß', de > fr
        api_raw = {
            "header": "1. gro\u00df <span class=\"style\"><acronym title=\"informal\">inf</acronym></span> <span class=\"sense\">(besonders)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.style == 'informal'

    def test_style_with_acronyms(self):
        # 'groß', de > fr
        api_raw = {
            "header": "1. gro\u00df <span class=\"style\"><acronym title=\"informal\">inf</acronym></span> <span class=\"sense\">(besonders)</span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert a.style == 'inf'

    def test_topic(self):
        # 'abbrechen', de > fr
        api_raw = {
            "header": "5. abbrechen <span class=\"topic\"><acronym title=\"computing\">COMPUT</acronym></span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.topic == 'computing'

    def test_topic_with_acronyms(self):
        # 'abbrechen', de > fr
        api_raw = {
            "header": "5. abbrechen <span class=\"topic\"><acronym title=\"computing\">COMPUT</acronym></span>:",
            "translations": []
        }
        a = Arab(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert a.topic == 'COMPUT'

    def test_everything_together(self):
        # 'groß', de > fr
        api_raw = {
            "header": "1. gro\u00df <span class=\"style\"><acronym title=\"informal\">inf</acronym></span> <span class=\"sense\">(besonders)</span>:",
            "translations": [
                {
                    "source": "<span class=\"example\">sich nicht <strong class=\"tilde\">gro\u00df</strong> um <acronym title=\"etwas\">etw</acronym> k\u00fcmmern</span>",
                    "target": "ne pas s&#39;occuper des masses de <acronym title=\"quelque chose\">qc</acronym> <span class=\"style\"><acronym title=\"informal\">inf</acronym></span>"
                },
                {
                    "source": "<span class=\"example\">was soll man da schon <strong class=\"tilde\">gro\u00df</strong> machen/sagen?</span>",
                    "target": "qu&#39;est-ce qu&#39;on peut bien faire/dire de plus ? <span class=\"style\"><acronym title=\"informal\">inf</acronym></span>"
                }
            ]
        }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.raw == api_raw
        assert a.headword == "groß"
        assert len(a.translations) == 2
        assert a.type == 'headword'
        assert a.num == 1
        assert a.style == 'informal'
        assert a.sense == 'besonders'

    def test_empty_api_dict(self):
        api_raw = {}
        with pytest.raises(KeyError):
            _ = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)

    def test_warning_for_unhandled_tags(self):
        # invented string with unhandled tag
        api_raw = {
            "header": "1. gro\u00df <span class=\"UNHANDLED\"><acronym title=\"informal\">inf</acronym></span> <span class=\"sense\">(besonders)</span>:",
            "translations": [
                {
                    "source": "<span class=\"example\">sich nicht <strong class=\"tilde\">gro\u00df</strong> um <acronym title=\"etwas\">etw</acronym> k\u00fcmmern</span>",
                    "target": "ne pas s&#39;occuper des masses de <acronym title=\"quelque chose\">qc</acronym> <span class=\"style\"><acronym title=\"informal\">inf</acronym></span>"
                },
                {
                    "source": "<span class=\"example\">was soll man da schon <strong class=\"tilde\">gro\u00df</strong> machen/sagen?</span>",
                    "target": "qu&#39;est-ce qu&#39;on peut bien faire/dire de plus ? <span class=\"style\"><acronym title=\"informal\">inf</acronym></span>"
                }
            ]
        }
        with pytest.warns(UserWarning):
            a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
            assert a.raw == api_raw
            assert a.headword == "groß"
            assert len(a.translations) == 2
            assert a.type == 'headword'
            assert a.num == 1
            assert a.style is None
            assert a.sense == 'besonders'


class TestTranslation:
    """
    Tests for Translation.
    """

    def test_raw(self):
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw, False, False, False)
        assert t.raw == api_raw

    def test_opendict_true(self):
        # 'ad', en > fr (adapted)
        api_raw = {"opendict": True,
                   "source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw, False, False, False)
        assert t.opendict is True

    def test_opendict_none(self):
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw, False, False, False)
        assert t.opendict is None

    def test_source(self, mocker):
        spy = mocker.spy(pons_dictionary.entry.TranslationEntry, "__init__")
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw, False, False, False)

        spy.assert_any_call(t.source, api_raw['source'], False, False, False)
        assert isinstance(t.source, pons_dictionary.entry.TranslationEntry)

    def test_target(self, mocker):
        spy = mocker.spy(pons_dictionary.entry.TranslationEntry, "__init__")
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw, False, False, False)

        spy.assert_any_call(t.target, api_raw['target'], False, False, False)
        assert isinstance(t.target, pons_dictionary.entry.TranslationEntry)


class TestTranslationEntry:
    """
    Tests for TranslationEntry.

    First set of tests is simple testing of each attribute. Second set of tests is testing the overall behavior of
    TranslationEntry for specific corner cases. If an unexpected behavior arises in normal use, the offending raw API
    string can be copied at the end in a new specific test.
    """

    def test_raw(self):
        # 'live', en > fr
        api_raw = '<span class="example">real <strong class="tilde">live</strong></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.raw == api_raw

    def test_type_none(self):
        # 'live', en > fr (adapted)
        api_raw = 'real <strong class="tilde">live</strong>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type is None

    def test_type_headword(self):
        # 'ad', en > fr
        api_raw = '<strong class="headword">advertisement</strong> <span class="sense">(in newspaper)</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type == 'headword'

    def test_type_example(self):
        # 'live', en > fr
        api_raw = '<span class="example">real <strong class="tilde">live</strong></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type == 'example'

    def test_type_definition(self):
        # 'bier', de
        api_raw = '<span class="definition">ein aus Hopfen, Malz, Hefe und Wasser durch Gärung hergestelltes alkoholisches Getränk</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type == 'definition'

    def test_type_idiom_proverb(self):
        # 'love', en > fr
        api_raw = '<span class="idiom_proverb"><strong class="tilde">love</strong> me, <strong class="tilde">love</strong> my dog</span> <span class="rhetoric"><acronym title="proverb">prov</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type == 'idiom_proverb'

    def test_type_complement(self):
        # 'annonce', fr > de
        api_raw = '<span class="complement"><strong class="tilde">annonce</strong> de décès</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type == 'complement'

    def test_type_explanation(self):
        # 'beer', en > fr
        api_raw = '<span class="explanation">bière à base de gingembre</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type == 'explanation'

    def test_category(self):
        # 'aimer', fr > de
        api_raw = 'qui s&#39;aime se taquine/se chamaille <span class="grammar VERB"><acronym title="reflexive">refl</acronym></span> <span class="category"><acronym title="proverb">prov</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.category == 'proverb'

    def test_category_with_acronym(self):
        # 'aimer', fr > de
        api_raw = 'qui s&#39;aime se taquine/se chamaille <span class="grammar VERB"><acronym title="reflexive">refl</acronym></span> <span class="category"><acronym title="proverb">prov</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.category == 'prov'

    def test_colloc(self):
        # 'abbrechen', de > fr
        api_raw = '<strong class="headword">abbrechen</strong> <span class="colloc">(Ast)</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.colloc == 'Ast'

    def test_collocator(self):
        # 'cancel', en > fr
        api_raw = '<strong class="headword">cancel</strong> <span class="collocator">order</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.collocator == 'order'

    def test_info(self):
        # 'groß', de > fr
        api_raw = 'grand(e) <span class="info"><acronym title="prefixed">prefixed</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.info == "prefixed"

    def test_info_with_acronym(self):
        # 'groß', de > fr
        api_raw = 'grand(e) <span class="info"><acronym title="prefixed">prefixed</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.info == "prefixed"

    def test_modus(self):
        # 'undertake', en > fr
        api_raw = '<span class="example">to <strong class="tilde">undertake</strong> to</span> <span class="modus">+<acronym title="infinitive">infin</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.modus == "infinitive"

    def test_modus_with_acronym(self):
        # 'undertake', en > fr
        api_raw = '<span class="example">to <strong class="tilde">undertake</strong> to</span> <span class="modus">+<acronym title="infinitive">infin</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.modus == "infin"

    def test_region(self):
        # 'big', en > fr
        api_raw = '<span class="example">to be <strong class="tilde">big</strong> on <acronym title="something">sth</acronym></span> <span class="region"><acronym title="American English" class="Am">Am</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.region == 'American English'

    def test_region_with_acronym(self):
        # 'big', en > fr
        api_raw = '<span class="example">to be <strong class="tilde">big</strong> on <acronym title="something">sth</acronym></span> <span class="region"><acronym title="American English" class="Am">Am</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.region == 'Am'

    def test_restriction(self):
        # 'groß', de > fr
        api_raw = '<span class="idiom_proverb"><strong class="tilde">groß</strong> machen</span> <span class="restriction"><acronym title="language of children">childspeak</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.restriction == 'language of children'

    def test_restriction_with_acronym(self):
        # 'groß', de > fr
        api_raw = '<span class="idiom_proverb"><strong class="tilde">groß</strong> machen</span> <span class="restriction"><acronym title="language of children">childspeak</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.restriction == 'childspeak'

    def test_rhetoric(self):
        # 'to love', en > fr
        api_raw = '<span class="idiom_proverb"><strong class="tilde">love</strong> me, <strong class="tilde">love</strong> my dog</span> <span class="rhetoric"><acronym title="proverb">prov</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.rhetoric == 'proverb'

    def test_rhetoric_acronym(self):
        # 'to love', en > fr
        api_raw = '<span class="idiom_proverb"><strong class="tilde">love</strong> me, <strong class="tilde">love</strong> my dog</span> <span class="rhetoric"><acronym title="proverb">prov</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.rhetoric == 'prov'

    def test_sense(self):
        # 'ad', en > fr
        api_raw = '<strong class="headword">advertisement</strong> <span class="sense">(in newspaper)</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.sense == 'in newspaper'

    def test_style(self):
        # 'big', en > fr
        api_raw = '<span class="example">a <strong class="tilde">big</strong> eater</span> <span class="style"><acronym title="informal">inf</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.style == 'informal'

    def test_style_with_acronym(self):
        # 'big', en > fr
        api_raw = '<span class="example">a <strong class="tilde">big</strong> eater</span> <span class="style"><acronym title="informal">inf</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.style == 'inf'

    def test_subject(self):
        # 'abbrechen', de > fr
        api_raw = '<strong class="headword">abbrechen</strong> <span class="topic"><acronym title="computing">COMPUT</acronym></span> <span class="subject">Verbindung, Verarbeitung:</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.subject == 'Verbindung, Verarbeitung'

    def test_topic(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.topic == ['commerce', 'law']

    def test_topic_with_acronym(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=True, acronyms_in_text=False, hints_in_text=False)
        assert te.topic == ['COMM', 'LAW']

    def test_text(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "gemischtwirtschaftliches Unternehmen"

    def test_text_with_hints(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=True)
        assert te.text == "gemischtwirtschaftliches Unternehmen [nt]"

    def test_everything_together(self):
        # 'abbrechen', de > fr
        api_raw = '<strong class="headword">abbrechen</strong> <span class="topic"><acronym title="computing">COMPUT</acronym></span> <span class="subject">Verbindung, Verarbeitung:</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.type == 'headword'
        assert te.text == 'abbrechen'
        assert te.topic == 'computing'
        assert te.subject == 'Verbindung, Verarbeitung'

    def test_empty_api_string(self):
        api_raw = ''
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.raw == ''
        assert te.text == ''
        assert te.type is None
        assert te.category is None
        assert te.colloc is None
        assert te.collocator is None
        assert te.info is None
        assert te.modus is None
        assert te.region is None
        assert te.restriction is None
        assert te.rhetoric is None
        assert te.sense is None
        assert te.style is None
        assert te.subject is None
        assert te.topic is None

    def test_warning_for_unhandled_tags(self):
        # invented string with unhandled tag
        api_raw = 'test <span class="UNHANDLED"><acronym title="neuter">nt</acronym></span>'
        with pytest.warns(UserWarning):
            te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
            assert te.text == "test"

    def test_str_(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert str(te) == te.text

    # Test for specific strings, essentially problematic corner cases
    def test_corner_string_1(self):
        # 'live', en > fr
        api_raw = '<span class="example">as long as <acronym title="somebody">sb</acronym> <strong class="tilde">lives</strong></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "as long as somebody lives"

    def test_corner_string_1_with_acronym(self):
        # 'live', en > fr
        api_raw = '<span class="example">as long as <acronym title="somebody">sb</acronym> <strong class="tilde">lives</strong></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=True, hints_in_text=False)
        assert te.text == "as long as sb lives"

    def test_corner_string_2(self):
        # 'live', en > fr
        api_raw = 'tant qu&#39;il y aura de la vie'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "tant qu'il y aura de la vie"

    def test_corner_string_3(self):
        # 'live', en > fr
        api_raw = '<span class="example">to only <strong class="tilde">live</strong> for <acronym title="somebody">sb</acronym>/<acronym title="something">sth</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "to only live for somebody/something"

    def test_corner_string_4(self):
        # 'live', en > fr
        api_raw = 'appât  <span class="genus"><acronym title="masculine">m</acronym></span>  vivant'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "appât vivant"

    def test_corner_string_4_with_hints(self):
        # 'live', en > fr
        api_raw = 'appât  <span class="genus"><acronym title="masculine">m</acronym></span>  vivant'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=True)
        assert te.text == "appât [m] vivant"

    def test_corner_string_5(self):
        # 'big', en > fr
        api_raw = '<span class="example">she&#39;s <strong class="tilde">big</strong> [<span class="or"><acronym title="or">or</acronym></span> a <strong class="tilde">big</strong> name] in finance</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "she's big [or a big name] in finance"

    def test_corner_string_6(self):
        # 'big', en > fr
        api_raw = '<span class="explanation"><span class="emphasize">Big Ben</span> était à l&#39;origine le surnom donné à la grande cloche de la tour de la &quot;Houses of Parliament&quot; coulée en 1856, surnom hérité du &quot;Chief Commissionner of Works&quot; de l&#39;époque, Sir Benjamin Hall. De nos jours, ce nom est utilisé pour désigner la grande horloge et la tour. Le carillon de &quot;Big Ben&quot; sert de sonal à certains journaux télévisés et radiophoniques.</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "Big Ben était à l'origine le surnom donné à la grande cloche de la tour de la \"Houses of " \
                          "Parliament\" coulée en 1856, surnom hérité du \"Chief Commissionner of Works\" de " \
                          "l'époque, Sir Benjamin Hall. De nos jours, ce nom est utilisé pour désigner la grande " \
                          "horloge et la tour. Le carillon de \"Big Ben\" sert de sonal à certains journaux " \
                          "télévisés et radiophoniques."

    def test_corner_string_7(self):
        # 'rapper', en > fr
        api_raw = 'rappeur<span class="feminine">(-euse)</span> <span class="genus"><acronym title="masculine">m</acronym></span> <span class="genus">(<acronym title="feminine">f</acronym>)</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "rappeur(-euse)"

    def test_corner_string_7_with_hints(self):
        # 'rapper', en > fr
        api_raw = 'rappeur<span class="feminine">(-euse)</span> <span class="genus"><acronym title="masculine">m</acronym></span> <span class="genus">(<acronym title="feminine">f</acronym>)</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=True)
        assert te.text == "rappeur(-euse) [m(f)]"

    def test_corner_string_8(self):
        # 'cut', en > fr
        api_raw = '<span class="idiom_proverb">to <strong class="tilde">cut</strong> a fine figure</span>, <span class="idiom_proverb">to  <strong class="tilde">cut</strong> quite a figure</span>, <span class="idiom_proverb">[<span class="or"><acronym title="or">or</acronym></span> <span class="region"><acronym title="British English" class="Brit">Brit</acronym></span> dash]</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "to cut a fine figure, to cut quite a figure, [or dash]"

    def test_corner_string_9(self):
        # 'undertake', en > fr
        api_raw = '<span class="example">to <strong class="tilde">undertake</strong> to</span> <span class="modus">+<acronym title="infinitive">infin</acronym></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "to undertake to"

    def test_corner_string_10(self):
        # 'Bier', de
        api_raw = 'Eines der beliebtesten Getränke in Deutschland ist das <b>Bier</b>.'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "Eines der beliebtesten Getränke in Deutschland ist das Bier."

    def test_corner_string_11(self):
        # 'Bier', de
        api_raw = 'Das Herstellen von Bier nennt man <i>Brauen</i>; eine Firma, die Bier braut, heißt <i>Brauerei.</i>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "Das Herstellen von Bier nennt man Brauen; eine Firma, die Bier braut, heißt Brauerei."

    def test_corner_string_12_with_hints(self):
        # 'big', en > fr
        api_raw = 'les grandes entreprises <span class="number">fpl</span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=True)
        assert te.text == "les grandes entreprises [fpl]"

    def test_corner_string_13(self):
        # 'gros', fr > de
        api_raw = '<acronym title="etwas">etw</acronym> en gros  <span class="target">[<span class="or"><acronym title="oder">o.</acronym></span> im Großen]</span>  kaufen/verkaufen'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=True)
        assert te.text == "etwas en gros [oder im Großen] kaufen/verkaufen"

    def test_corner_string_13_with_acronyms(self):
        # 'gros', fr > de
        api_raw = '<acronym title="etwas">etw</acronym> en gros  <span class="target">[<span class="or"><acronym title="oder">o.</acronym></span> im Großen]</span>  kaufen/verkaufen'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=True, hints_in_text=True)
        assert te.text == "etw en gros [o. im Großen] kaufen/verkaufen"

    def test_corner_string_14(self):
        # 'gros', fr > de
        api_raw = '[genau]so klug wie vorher sein'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "[genau]so klug wie vorher sein"

    def test_corner_string_15(self):
        # 'après', fr > de
        api_raw = '<span class="example">[dans] <strong class="tilde">l&#39;après-midi</strong></span>'
        te = TranslationEntry(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert te.text == "[dans] l'après-midi"
