# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings
import html.parser

# import third-party modules
import bs4

# import your own module
from pons_dictionary.translation import Translation
import pons_dictionary.parser as parser


class Arab:
    """
    All data pertaining to an Arab.

    [...]
    """

    def __init__(self, pons_api_arab: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        # Initialize attributes
        self._raw = pons_api_arab
        self._headword = None
        self._translations = None
        self._type = None

        self._abbreviation_of = None
        self._auxiliary_verb = None
        self._collocator = None
        self._info = None
        self._num = None
        self._other = None
        self._region = None
        self._rhetoric = None
        self._sense = None
        self._style = None
        self._topic = None


        # Parsing pons_api_arab dict

        # Handle translations
        translations_list = []
        for translation in pons_api_arab["translations"]:
            translations_list.append(Translation(translation, acronyms_in_fields, acronyms_in_text, hints_in_text))
        if len(translations_list) > 0:
            self._translations = translations_list

        # Parse "header" string
        soup = bs4.BeautifulSoup(html.unescape(pons_api_arab["header"]), "html.parser")

        soup, abbreviation_of = parser.extract_attribute(soup, tag_class="indirect_reference_ABBR", use_acronyms=acronyms_in_fields)
        if abbreviation_of is not None:
            self._abbreviation_of = abbreviation_of.replace("abbreviation of ", "")
        soup, self._auxiliary_verb = parser.extract_attribute(soup, tag_class="auxiliary_verb", use_acronyms=acronyms_in_fields)
        soup, self._collocator = parser.extract_attribute(soup, tag_class="collocator", use_acronyms=acronyms_in_fields)
        soup, self._info = parser.extract_attribute(soup, tag_class="info", use_acronyms=acronyms_in_fields)
        soup, self._other = parser.extract_attribute(soup, tag_class="indirect_reference_OTHER", use_acronyms=acronyms_in_fields)
        soup, self._region = parser.extract_attribute(soup, tag_class="region", use_acronyms=acronyms_in_fields)
        soup, self._rhetoric = parser.extract_attribute(soup, tag_class="rhetoric", use_acronyms=acronyms_in_fields)
        soup, self._sense = parser.extract_attribute(soup, tag_class="sense", use_acronyms=acronyms_in_fields)
        soup, self._style = parser.extract_attribute(soup, tag_class="style", use_acronyms=acronyms_in_fields)
        soup, self._topic = parser.extract_attribute(soup, tag_class="topic", use_acronyms=acronyms_in_fields)

        # Unhandled tags?
        for el in soup.contents:
            if isinstance(el, bs4.Tag):
                warnings.warn(f"Unexpected pattern found in API str ({str(el)}), removed from API str.",
                              UserWarning)
                el.extract()

        soup.smooth()
        remaining_text = str(soup)

        # Get num
        num_pattern = re.compile(r'(\d*). ', re.UNICODE)
        num_match = num_pattern.match(remaining_text)
        if num_match is not None:
            num_string = num_match.group(1)
            self._num = int(num_string)
            remaining_text = remaining_text.replace(num_match.group(0), '')

        # Get type & headword
        remaining_text = remaining_text.strip(" :+,")
        if remaining_text:
            phrases_pattern = re.compile(r'Phrases', re.UNICODE)
            phrases_match = phrases_pattern.match(remaining_text)
            if phrases_match is not None:
                self._type = "phrases"
                remaining_text = remaining_text.replace(phrases_match.group(0), '')
            else:
                self._type = "headword"
                self._headword = remaining_text

    @property
    def raw(self) -> dict:
        return self._raw

    @property
    def headword(self) -> str:
        return self._headword

    @property
    def type(self) -> str:
        return self._type

    @property
    def translations(self) -> typing.List[Translation]:
        return self._translations

    @property
    def abbreviation_of(self) -> str:
        return self._abbreviation_of

    @property
    def auxiliary_verb(self) -> str:
        return self._auxiliary_verb

    @property
    def collocator(self) -> str:
        return self._collocator

    @property
    def info(self) -> str:
        return self._info

    @property
    def num(self) -> int:
        return self._num

    @property
    def other(self) -> str:
        return self._other

    @property
    def region(self) -> str:
        return self._region

    @property
    def rhetoric(self) -> str:
        return self._rhetoric

    @property
    def sense(self) -> str:
        return self._sense

    @property
    def style(self) -> str:
        return self._style

    @property
    def topic(self) -> str:
        return self._topic