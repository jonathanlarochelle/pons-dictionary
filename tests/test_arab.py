# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pons_dictionary.arab
import pytest

# import your own module
from pons_dictionary.arab import Arab


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
        spy = mocker.spy(pons_dictionary.arab.Translation, "__init__")
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
        assert isinstance(a.translations[0], pons_dictionary.arab.Translation)
        assert isinstance(a.translations[1], pons_dictionary.arab.Translation)

    def test_translations_none(self):
        # Never encountered a case without translations so far, but it is useful to consider.
        # 'cut', en > fr (adapted)
        api_raw = {"header": "Phrases:",
                   "translations": []
                   }
        a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)
        assert a.translations is None

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
            a = Arab(api_raw, acronyms_in_fields=False, acronyms_in_text=False, hints_in_text=False)

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

    # Test for specific strings, essentially problematic corner cases
    def test_corner_string_1(self):
        pass