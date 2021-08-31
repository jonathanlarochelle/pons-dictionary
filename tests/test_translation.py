# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pytest

# import your own module
import pons_dictionary.translation
from pons_dictionary.translation import Translation


class TestTranslation:
    """
    Tests for Translation.
    """

    def test_raw(self):
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw)
        assert t.raw == api_raw

    def test_opendict_true(self):
        # 'ad', en > fr (adapted)
        api_raw = {"opendict": "true",
                   "source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw)
        assert t.opendict is True

    def test_opendict_false(self):
        # 'ad', en > fr (adapted)
        api_raw = {"opendict": "false",
                   "source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw)
        assert t.opendict is False

    def test_opendict_none(self):
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw)
        assert t.opendict is None

    def test_source(self, mocker):
        spy = mocker.spy(pons_dictionary.translation.TranslationEntry, "__init__")
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw)

        spy.assert_any_call(t.source, api_raw['source'])
        assert isinstance(t.source, pons_dictionary.translation.TranslationEntry)

    def test_target(self, mocker):
        spy = mocker.spy(pons_dictionary.translation.TranslationEntry, "__init__")
        # 'ad', en > fr
        api_raw = {"source": "<strong class=\"headword\">advertisement</strong>",
                   "target": "publicit\u00e9 <span class=\"genus\"><acronym title=\"feminine\">f</acronym></span>"
                   }
        t = Translation(api_raw)

        spy.assert_any_call(t.target, api_raw['target'])
        assert isinstance(t.target, pons_dictionary.translation.TranslationEntry)
