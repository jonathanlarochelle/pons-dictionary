# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings
import html.parser

# import third-party modules
import bs4

# import your own module
from pons_dictionary.arab import Arab
import pons_dictionary.parser as parser


class Rom:
    """
    All data pertaining to a Rom.

    [...]
    """

    def __init__(self, pons_api_rom: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        # Initialize attributes
        self._raw = pons_api_rom
        self._headword = None
        self._wordclass = None
        self._arabs = []

        self._alt_headword = None
        self._auxiliary_verb = None
        self._flexion = None
        self._genus = None
        self._headword_attributes = None
        self._info = None
        self._modus = None
        self._number = None
        self._object_case = None
        self._phonetics = None
        self._region = None
        self._sense = None
        self._spelling_source = None
        self._style = None
        self._topic = None
        self._verbclass = None

        # Parsing pons_api_rom dict

        # Handle arabs
        for arab in pons_api_rom["arabs"]:
            self._arabs.append(Arab(arab, acronyms_in_fields, acronyms_in_text, hints_in_text))

        # Parse "headword_full" string
        soup = bs4.BeautifulSoup(pons_api_rom["headword_full"], "html.parser")

        # Handle alternate headword
        alternate_headword_tag = soup.find(class_="headword")
        if alternate_headword_tag is not None:
            alternate_headword_tag, alt_spelling_rule = parser.extract_attribute(alternate_headword_tag, tag_class="headword_spelling", use_acronyms=acronyms_in_fields)
            soup, alt_headword = parser.extract_attribute(soup, tag_class="headword", use_acronyms=acronyms_in_fields)
            if alt_headword is not None:
                if alt_spelling_rule is not None:
                    self._alt_headword = [alt_headword, alt_spelling_rule]
                else:
                    self._alt_headword = [alt_headword, '']

        # Headword attributes
        headword_attributes_tags = soup.find_all(class_="headword_attributes")
        for tag in headword_attributes_tags:
            self._headword_attributes = tag["title"]
            tag.unwrap()

        soup, self._auxiliary_verb = parser.extract_attribute(soup, tag_class="auxiliary_verb", use_acronyms=acronyms_in_fields)
        soup, self._flexion = parser.extract_attribute(soup, tag_class="flexion", use_acronyms=acronyms_in_fields)
        soup, self._genus = parser.extract_attribute(soup, tag_class="genus", use_acronyms=acronyms_in_fields)
        soup, self._modus = parser.extract_attribute(soup, tag_class="modus", use_acronyms=acronyms_in_fields)
        soup, self._number = parser.extract_attribute(soup, tag_class="number", use_acronyms=acronyms_in_fields)
        soup, self._object_case = parser.extract_attribute(soup, tag_class="object-case", use_acronyms=acronyms_in_fields)
        soup, self._phonetics = parser.extract_attribute(soup, tag_class="phonetics", use_acronyms=acronyms_in_fields)
        soup, self._region = parser.extract_attribute(soup, tag_class="region", use_acronyms=acronyms_in_fields)
        soup, self._sense = parser.extract_attribute(soup, tag_class="sense", use_acronyms=acronyms_in_fields)
        soup, self._style = parser.extract_attribute(soup, tag_class="style", use_acronyms=acronyms_in_fields)
        soup, self._topic = parser.extract_attribute(soup, tag_class="topic", use_acronyms=acronyms_in_fields)
        soup, self._verbclass = parser.extract_attribute(soup, tag_class="verbclass", use_acronyms=acronyms_in_fields)
        soup, self._spelling_source = parser.extract_attribute(soup, tag_class="headword_spelling", use_acronyms=acronyms_in_fields)
        soup, self._wordclass = parser.extract_attribute(soup, tag_class="wordclass", use_acronyms=acronyms_in_fields)

        soup, self._info = parser.extract_attribute(soup, tag_class="info", use_acronyms=acronyms_in_fields)

        # Tags to unwrap or extract
        tag_classes_to_unwrap = ["feminine"]
        tags_to_extract = ["sup"]
        for el in soup.contents:
            if isinstance(el, bs4.Tag):
                if el.has_attr("class"):
                    if el["class"][0] in tag_classes_to_unwrap:
                        el.unwrap()
                if el.name in tags_to_extract:
                    el.extract()

        # Unhandled tags?
        for el in soup.contents:
            if isinstance(el, bs4.Tag):
                warnings.warn(f"Unexpected pattern found in API str ({str(el)}), removed from API str.",
                              UserWarning)
                el.extract()

        soup.smooth()
        remaining_text = str(soup).strip(" :+,*")
        self._headword = remaining_text

    @property
    def raw(self) -> dict:
        return self._raw

    @property
    def headword(self) -> str:
        return self._headword

    @property
    def wordclass(self) -> str:
        return self._wordclass

    @property
    def arabs(self) -> typing.List[Arab]:
        return self._arabs

    @property
    def alt_headword(self) -> str:
        return self._alt_headword

    @property
    def auxiliary_verb(self) -> str:
        return self._auxiliary_verb

    @property
    def flexion(self) -> str:
        return self._flexion

    @property
    def genus(self) -> str:
        return self._genus

    @property
    def headword_attributes(self) -> str:
        return self._headword_attributes

    @property
    def info(self) -> str:
        return self._info

    @property
    def modus(self) -> str:
        return self._modus

    @property
    def number(self) -> str:
        return self._number

    @property
    def object_case(self) -> str:
        return self._object_case

    @property
    def phonetics(self) -> str:
        return self._phonetics

    @property
    def region(self) -> str:
        return self._region

    @property
    def sense(self) -> str:
        return self._sense

    @property
    def spelling_source(self) -> str:
        return self._spelling_source

    @property
    def style(self) -> str:
        return self._style

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def verbclass(self) -> str:
        return self._verbclass
