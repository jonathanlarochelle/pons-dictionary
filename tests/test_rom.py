# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pons_dictionary.arab
import pytest

# import your own module
from pons_dictionary.rom import Rom


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
        spy = mocker.spy(pons_dictionary.rom.Arab, "__init__")
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
        assert isinstance(r.arabs[0], pons_dictionary.rom.Arab)
        assert isinstance(r.arabs[1], pons_dictionary.rom.Arab)
        assert isinstance(r.arabs[2], pons_dictionary.rom.Arab)

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