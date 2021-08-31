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

    def test_modus(self):
        # 'undertake', en > fr
        api_raw = '<span class="example">to <strong class="tilde">undertake</strong> to</span> <span class="modus">+<acronym title="infinitive">infin</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.modus == "infinitive"

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
        # 'live', en > fr
        api_raw = '<span class="example">as long as <acronym title="somebody">sb</acronym> <strong class="tilde">lives</strong></span>'
        te = TranslationEntry(api_raw)
        assert te.text == "as long as somebody lives"

    def test_corner_string_2(self):
        # 'live', en > fr
        api_raw = 'tant qu&#39;il y aura de la vie'
        te = TranslationEntry(api_raw)
        assert te.text == "tant qu'il y aura de la vie"

    def test_corner_string_3(self):
        # 'live', en > fr
        api_raw = '<span class="example">to only <strong class="tilde">live</strong> for <acronym title="somebody">sb</acronym>/<acronym title="something">sth</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.text == "to only live for somebody/something"

    def test_corner_string_4(self):
        # 'live', en > fr
        api_raw = 'appât  <span class="genus"><acronym title="masculine">m</acronym></span>  vivant'
        te = TranslationEntry(api_raw)
        assert te.text == "appât vivant"

    def test_corner_string_5(self):
        # 'big', en > fr
        api_raw = '<span class="example">she&#39;s <strong class="tilde">big</strong> [<span class="or"><acronym title="or">or</acronym></span> a <strong class="tilde">big</strong> name] in finance</span>'
        te = TranslationEntry(api_raw)
        assert te.text == "she's big in finance"

    def test_corner_string_6(self):
        # 'big', en > fr
        api_raw = '<span class="explanation"><span class="emphasize">Big Ben</span> était à l&#39;origine le surnom donné à la grande cloche de la tour de la &quot;Houses of Parliament&quot; coulée en 1856, surnom hérité du &quot;Chief Commissionner of Works&quot; de l&#39;époque, Sir Benjamin Hall. De nos jours, ce nom est utilisé pour désigner la grande horloge et la tour. Le carillon de &quot;Big Ben&quot; sert de sonal à certains journaux télévisés et radiophoniques.</span>'
        te = TranslationEntry(api_raw)
        assert te.text == "Big Ben était à l'origine le surnom donné à la grande cloche de la tour de la \"Houses of " \
                          "Parliament\" coulée en 1856, surnom hérité du \"Chief Commissionner of Works\" de " \
                          "l'époque, Sir Benjamin Hall. De nos jours, ce nom est utilisé pour désigner la grande " \
                          "horloge et la tour. Le carillon de \"Big Ben\" sert de sonal à certains journaux " \
                          "télévisés et radiophoniques."

    def test_corner_string_7(self):
        # 'rapper', en > fr
        api_raw = 'rappeur<span class="feminine">(-euse)</span> <span class="genus"><acronym title="masculine">m</acronym></span> <span class="genus">(<acronym title="feminine">f</acronym>)</span>'
        te = TranslationEntry(api_raw)
        assert te.text == "rappeur(-euse)"

    def test_corner_string_8(self):
        # 'cut', en > fr
        # TODO: Tough one, multiple "type" span in one entry
        api_raw = '<span class="idiom_proverb">to <strong class="tilde">cut</strong> a fine figure</span>, <span class="idiom_proverb">to  <strong class="tilde">cut</strong> quite a figure</span>, <span class="idiom_proverb">[<span class="or"><acronym title="or">or</acronym></span> <span class="region"><acronym title="British English" class="Brit">Brit</acronym></span> dash]</span>'
        te = TranslationEntry(api_raw)
        assert te.text == "to cut a fine figure, to cut quite a figure"

    def test_corner_string_9(self):
        # 'undertake', en > fr
        api_raw = '<span class="example">to <strong class="tilde">undertake</strong> to</span> <span class="modus">+<acronym title="infinitive">infin</acronym></span>'
        te = TranslationEntry(api_raw)
        assert te.text == "to undertake to"