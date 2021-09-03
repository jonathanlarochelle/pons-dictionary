# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings
import html.parser

# import third-party modules
import bs4

# import your own module

def extract_attribute(soup: bs4.BeautifulSoup, tag_class: str,
                      use_acronyms: bool) -> typing.Tuple[bs4.BeautifulSoup, str]:
    ret_values = []

    tags = soup.find_all(class_=tag_class)

    for tag in tags:
        # Parse acronyms
        for acronym in tag.find_all("acronym"):
            if use_acronyms:
                acronym_value = acronym.contents[0]
            else:
                acronym_value = acronym['title']
            acronym.replace_with(acronym_value)
        # Unwrap all other tags
        for el in tag.contents:
            if isinstance(el, bs4.Tag):
                el.unwrap()

        contents = html.unescape(tag.encode_contents().decode("utf-8"))
        ret_values.append(contents.strip(" :+)(,[]→<>"))
        tag.extract()

    if len(ret_values) == 0:
        return (soup, None)
    elif len(ret_values) == 1:
        return (soup, ret_values[0])
    else:
        return (soup, ret_values)


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

        soup, self._category = extract_attribute(soup, tag_class="category", use_acronyms=acronyms_in_fields)
        soup, self._colloc = extract_attribute(soup, tag_class="colloc", use_acronyms=acronyms_in_fields)
        soup, self._collocator = extract_attribute(soup, tag_class="collocator", use_acronyms=acronyms_in_fields)
        soup, self._info = extract_attribute(soup, tag_class="info", use_acronyms=acronyms_in_fields)
        soup, self._modus = extract_attribute(soup, tag_class="modus", use_acronyms=acronyms_in_fields)
        soup, self._region = extract_attribute(soup, tag_class="region", use_acronyms=acronyms_in_fields)
        soup, self._restriction = extract_attribute(soup, tag_class="restriction", use_acronyms=acronyms_in_fields)
        soup, self._rhetoric = extract_attribute(soup, tag_class="rhetoric", use_acronyms=acronyms_in_fields)
        soup, self._sense = extract_attribute(soup, tag_class="sense", use_acronyms=acronyms_in_fields)
        soup, self._style = extract_attribute(soup, tag_class="style", use_acronyms=acronyms_in_fields)
        soup, self._subject = extract_attribute(soup, tag_class="subject", use_acronyms=acronyms_in_fields)
        soup, self._topic = extract_attribute(soup, tag_class="topic", use_acronyms=acronyms_in_fields)

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


class Translation:
    """
    A Translation is comprised of a source (original expression) and a target (translated expression).
    """

    def __init__(self, pons_api_translation_dict: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        # Initialize attributes
        self._raw = pons_api_translation_dict
        self._opendict = None
        self._source = None
        self._target = None

        # Parsing pons_translation_obj
        if "opendict" in pons_api_translation_dict:
            self._opendict = pons_api_translation_dict['opendict']

        if "source" in pons_api_translation_dict:
            self._source = TranslationEntry(pons_api_translation_dict['source'], acronyms_in_fields, acronyms_in_text,
                                            hints_in_text)

        if "target" in pons_api_translation_dict:
            self._target = TranslationEntry(pons_api_translation_dict['target'], acronyms_in_fields, acronyms_in_text,
                                            hints_in_text)

    @property
    def raw(self) -> dict:
        return self._raw

    @property
    def opendict(self) -> bool:
        return self._opendict

    @property
    def source(self) -> TranslationEntry:
        return self._source

    @property
    def target(self) -> TranslationEntry:
        return self._target


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
        self._translations = []
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
        for translation in pons_api_arab["translations"]:
            self._translations.append(Translation(translation, acronyms_in_fields, acronyms_in_text, hints_in_text))

        # Parse "header" string
        soup = bs4.BeautifulSoup(html.unescape(pons_api_arab["header"]), "html.parser")

        soup, abbreviation_of = extract_attribute(soup, tag_class="indirect_reference_ABBR", use_acronyms=acronyms_in_fields)
        if abbreviation_of is not None:
            self._abbreviation_of = abbreviation_of.replace("abbreviation of ", "")
        soup, self._auxiliary_verb = extract_attribute(soup, tag_class="auxiliary_verb", use_acronyms=acronyms_in_fields)
        soup, self._collocator = extract_attribute(soup, tag_class="collocator", use_acronyms=acronyms_in_fields)
        soup, self._info = extract_attribute(soup, tag_class="info", use_acronyms=acronyms_in_fields)
        soup, self._other = extract_attribute(soup, tag_class="indirect_reference_OTHER", use_acronyms=acronyms_in_fields)
        soup, self._region = extract_attribute(soup, tag_class="region", use_acronyms=acronyms_in_fields)
        soup, self._rhetoric = extract_attribute(soup, tag_class="rhetoric", use_acronyms=acronyms_in_fields)
        soup, self._sense = extract_attribute(soup, tag_class="sense", use_acronyms=acronyms_in_fields)
        soup, self._style = extract_attribute(soup, tag_class="style", use_acronyms=acronyms_in_fields)
        soup, self._topic = extract_attribute(soup, tag_class="topic", use_acronyms=acronyms_in_fields)

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
            alternate_headword_tag, alt_spelling_rule = extract_attribute(alternate_headword_tag, tag_class="headword_spelling", use_acronyms=acronyms_in_fields)
            soup, alt_headword = extract_attribute(soup, tag_class="headword", use_acronyms=acronyms_in_fields)
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

        soup, self._auxiliary_verb = extract_attribute(soup, tag_class="auxiliary_verb", use_acronyms=acronyms_in_fields)
        soup, self._flexion = extract_attribute(soup, tag_class="flexion", use_acronyms=acronyms_in_fields)
        soup, self._genus = extract_attribute(soup, tag_class="genus", use_acronyms=acronyms_in_fields)
        soup, self._modus = extract_attribute(soup, tag_class="modus", use_acronyms=acronyms_in_fields)
        soup, self._number = extract_attribute(soup, tag_class="number", use_acronyms=acronyms_in_fields)
        soup, self._object_case = extract_attribute(soup, tag_class="object-case", use_acronyms=acronyms_in_fields)
        soup, self._phonetics = extract_attribute(soup, tag_class="phonetics", use_acronyms=acronyms_in_fields)
        soup, self._region = extract_attribute(soup, tag_class="region", use_acronyms=acronyms_in_fields)
        soup, self._sense = extract_attribute(soup, tag_class="sense", use_acronyms=acronyms_in_fields)
        soup, self._style = extract_attribute(soup, tag_class="style", use_acronyms=acronyms_in_fields)
        soup, self._topic = extract_attribute(soup, tag_class="topic", use_acronyms=acronyms_in_fields)
        soup, self._verbclass = extract_attribute(soup, tag_class="verbclass", use_acronyms=acronyms_in_fields)
        soup, self._spelling_source = extract_attribute(soup, tag_class="headword_spelling", use_acronyms=acronyms_in_fields)
        soup, self._wordclass = extract_attribute(soup, tag_class="wordclass", use_acronyms=acronyms_in_fields)

        soup, self._info = extract_attribute(soup, tag_class="info", use_acronyms=acronyms_in_fields)

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


class Entry:
    """
    All data pertaining to an Entry.

    [...]
    """

    def __init__(self, pons_api_entry: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        # Initialize attributes
        self._opendict = None
        self._roms = []

        # Parsing pons_api_entry dict
        self._opendict = pons_api_entry['opendict']

        # Parsing roms
        for rom in pons_api_entry["roms"]:
            self._roms.append(Rom(rom, acronyms_in_fields, acronyms_in_text, hints_in_text))

    @property
    def opendict(self) -> bool:
        return self._opendict

    @property
    def roms(self) -> typing.List[Rom]:
        return self._roms


class EntryWithSecondaryEntries:
    """
    All data pertaining to an Entry with secondary entries.

    [...]
    """

    def __init__(self, pons_api_entry: dict, acronyms_in_fields: bool, acronyms_in_text: bool,
                 hints_in_text: bool):
        self._primary_entry = Entry(pons_api_entry["primary_entry"], acronyms_in_fields, acronyms_in_text, hints_in_text)
        self._secondary_entries = []
        for secondary_entry in pons_api_entry["secondary_entries"]:
            self._secondary_entries.append(Entry(secondary_entry, acronyms_in_fields, acronyms_in_text, hints_in_text))

    @property
    def primary_entry(self) -> Entry:
        return self._primary_entry

    @property
    def secondary_entries(self) -> typing.List[Entry]:
        return self._secondary_entries












