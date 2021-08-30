# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pytest

# import your own module
from pons_dictionary.translation_entry import TranslationEntry


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
        te = TranslationEntry(api_raw)
        assert te.raw == api_raw

    def test_type(self):
        # 'live', en > fr
        api_raw = '<span class="example">real <strong class="tilde">live</strong></span>'
        te = TranslationEntry(api_raw)
        assert te.type == 'example'

    def test_type_none(self):
        # 'live', en > fr (adapted)
        api_raw = 'real <strong class="tilde">live</strong>'
        te = TranslationEntry(api_raw)
        assert te.type is None

    def test_type_headword(self):
        # 'ad', en > fr
        api_raw = '<strong class="headword">advertisement</strong> <span class="sense">(in newspaper)</span>'
        te = TranslationEntry(api_raw)
        assert te.type == 'headword'

    def test_category(self):
        # 'aimer', fr > de
        api_raw = 'qui s&#39;aime se taquine/se chamaille <span class="grammar VERB"><acronym title="reflexive">refl</acronym></span> <span class="category"><acronym title="proverb">prov</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.category == 'proverb'

    def test_colloc(self):
        # 'abbrechen', de > fr
        api_raw = '<strong class="headword">abbrechen</strong> <span class="colloc">(Ast)</span>'
        te = TranslationEntry(api_raw)
        assert te.colloc == 'Ast'

    def test_collocator(self):
        # 'cancel', en > fr
        api_raw = '<strong class="headword">cancel</strong> <span class="collocator">order</span>'
        te = TranslationEntry(api_raw)
        assert te.collocator == 'order'

    def test_region(self):
        # 'big', en > fr
        api_raw = '<span class="example">to be <strong class="tilde">big</strong> on <acronym title="something">sth</acronym></span> <span class="region"><acronym title="American English" class="Am">Am</acronym></span>'
        te = TranslationEntry(api_raw)
        # BUG: span example does not go to end of str, but we delete the first <span and the absolute last </span>.
        assert te.region == 'American English'

    def test_rhetoric(self):
        # 'to love', en > fr
        api_raw = '<span class="idiom_proverb"><strong class="tilde">love</strong> me, <strong class="tilde">love</strong> my dog</span> <span class="rhetoric"><acronym title="proverb">prov</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.rhetoric == 'proverb'

    def test_sense(self):
        # 'ad', en > fr
        api_raw = '<strong class="headword">advertisement</strong> <span class="sense">(in newspaper)</span>'
        te = TranslationEntry(api_raw)
        assert te.sense == 'in newspaper'

    def test_style(self):
        # 'big', en > fr
        api_raw = '<span class="example">a <strong class="tilde">big</strong> eater</span> <span class="style"><acronym title="informal">inf</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.style == 'informal'

    def test_subject(self):
        # 'abbrechen', de > fr
        api_raw = '<strong class="headword">abbrechen</strong> <span class="topic"><acronym title="computing">COMPUT</acronym></span> <span class="subject">Verbindung, Verarbeitung:</span>'
        te = TranslationEntry(api_raw)
        assert te.subject == 'Verbindung, Verarbeitung'

    def test_topic(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.topic == ['commerce', 'law']

    def test_text(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.text == "gemischtwirtschaftliches Unternehmen"

    def test_everything_together(self):
        # 'abbrechen', de > fr
        api_raw = '<strong class="headword">abbrechen</strong> <span class="topic"><acronym title="computing">COMPUT</acronym></span> <span class="subject">Verbindung, Verarbeitung:</span>'
        te = TranslationEntry(api_raw)
        assert te.type == 'headword'
        assert te.text == 'abbrechen'
        assert te.topic == 'computing'
        assert te.subject == 'Verbindung, Verarbeitung'

    def test_warning_for_unhandled_tags(self):
        # invented string with unhandled tag
        api_raw = 'test <span class="UNHANDLED"><acronym title="neuter">nt</acronym></span>'
        with pytest.warns(UserWarning):
            te = TranslationEntry(api_raw)
            assert te.text == "test"

    def test_str_(self):
        # 'unternehmen', de > fr
        api_raw = 'gemischtwirtschaftliches <strong class="tilde">Unternehmen</strong> <span class="grammar SUBST"><acronym title="neuter">nt</acronym></span> <span class="topic"><acronym title="commerce">COMM</acronym></span>, <span class="topic"><acronym title="law">LAW</acronym></span>'
        te = TranslationEntry(api_raw)
        assert str(te) == "gemischtwirtschaftliches Unternehmen"


    # Test for specific strings, essentially problematic corner cases
    def test_corner_string_1(self):
        pass