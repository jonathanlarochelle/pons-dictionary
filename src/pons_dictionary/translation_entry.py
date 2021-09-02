# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings
import html

# import third-party modules
import bs4

# import your own module
import pons_dictionary.parser as parser


class TranslationEntry:
    """
    Data related to a TranslationEntry, which is either the source or target of a translation.

    [...]
    """

    def __init__(self, pons_api_string: str, acronyms_in_fields: bool, acronyms_in_text: bool, hints_in_text: bool):
        # Initialize attributes
        self._raw = pons_api_string
        self._text = None
        self._type = None

        self._category = None
        self._colloc = None
        self._collocator = None
        self._info = None
        self._modus = None
        self._region = None
        self._rhetoric = None
        self._sense = None
        self._style = None
        self._subject = None
        self._topic = None

        # PARSING of API string
        soup = bs4.BeautifulSoup(html.unescape(self._raw), "html.parser")

        soup, self._category = parser.extract_attribute(soup, tag_class="category", use_acronyms=acronyms_in_fields)
        soup, self._colloc = parser.extract_attribute(soup, tag_class="colloc", use_acronyms=acronyms_in_fields)
        soup, self._collocator = parser.extract_attribute(soup, tag_class="collocator", use_acronyms=acronyms_in_fields)
        soup, self._info = parser.extract_attribute(soup, tag_class="info", use_acronyms=acronyms_in_fields)
        soup, self._modus = parser.extract_attribute(soup, tag_class="modus", use_acronyms=acronyms_in_fields)
        soup, self._region = parser.extract_attribute(soup, tag_class="region", use_acronyms=acronyms_in_fields)
        soup, self._restriction = parser.extract_attribute(soup, tag_class="restriction", use_acronyms=acronyms_in_fields)
        soup, self._rhetoric = parser.extract_attribute(soup, tag_class="rhetoric", use_acronyms=acronyms_in_fields)
        soup, self._sense = parser.extract_attribute(soup, tag_class="sense", use_acronyms=acronyms_in_fields)
        soup, self._style = parser.extract_attribute(soup, tag_class="style", use_acronyms=acronyms_in_fields)
        soup, self._subject = parser.extract_attribute(soup, tag_class="subject", use_acronyms=acronyms_in_fields)
        soup, self._topic = parser.extract_attribute(soup, tag_class="topic", use_acronyms=acronyms_in_fields)

        # In-string parameters
        type_possible_values = ["headword", "example", "idiom_proverb", "complement", "explanation", "definition"]
        tag_class_to_unwrap = ["tilde", "emphasize", "feminine", "or", "target"]
        tag_name_to_unwrap = ["b", "i"]
        hints_possible_values = ["grammar", "case", "number", "object-case", "modus",
                               "indirect_reference_OTHER", "or", "genus"]


        for el in soup.contents:
            if el.name in ["span", "strong"]:
                if el["class"][0] in type_possible_values:
                    self._type = el["class"][0]
                    el.unwrap()

        for el in soup.contents:
            if el.name in ["span", "strong"]:
                if el["class"][0] in tag_class_to_unwrap:
                    el.unwrap()
                elif el["class"][0] in hints_possible_values:
                    if hints_in_text:
                        el.insert_before("[")
                        el.insert_after("]")
                        if el.acronym:
                            el.acronym.unwrap()
                        el.unwrap()
                    else:
                        el.extract()
            elif el.name in tag_name_to_unwrap:
                el.unwrap()

        # Acronyms
        for el in soup.contents:
            if el.name == "acronym":
                if acronyms_in_text:
                    el.replace_with(el.contents[0])
                else:
                    el.replace_with(el["title"])

        # Unhandled tags?
        for el in soup.contents:
            if isinstance(el, bs4.Tag):
                warnings.warn(f"Unexpected pattern found in API str ({str(el)}), removed from API str.",
                              UserWarning)
                el.extract()

        soup.smooth()
        remaining_text = str(soup)

        # Specific formatting cases
        # - Eliminate 2+ spaces
        spaces_pattern = re.compile(r'\s{2,}', re.UNICODE)
        for match in spaces_pattern.finditer(remaining_text):
            remaining_text = remaining_text.replace(match.group(0), ' ')
        # - Format for masculine/feminine words
        remaining_text = remaining_text.replace("[m] [(f)]", "[m(f)]")

        self._text = remaining_text.strip(" :+,")

    def __str__(self) -> str:
        return self.text

    @property
    def raw(self):
        return self._raw

    @property
    def text(self):
        return self._text

    @property
    def type(self):
        return self._type

    @property
    def category(self):
        return self._category

    @property
    def colloc(self):
        return self._colloc

    @property
    def collocator(self):
        return self._collocator

    @property
    def info(self):
        return self._info

    @property
    def modus(self):
        return self._modus

    @property
    def region(self):
        return self._region

    @property
    def restriction(self):
        return self._restriction

    @property
    def rhetoric(self):
        return self._rhetoric

    @property
    def sense(self):
        return self._sense

    @property
    def style(self):
        return self._style

    @property
    def subject(self):
        return self._subject

    @property
    def topic(self):
        return self._topic
