# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules
import pytest

# import your own module
from pons_dictionary.translation_entry import TranslationEntry


class TestTranslationEntryBS4:
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