# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings
import html

# import third-party modules
import bs4

# import your own module


class TranslationEntry:
    """
    Data related to a TranslationEntry, which is either the source or target of a translation.

    [...]
    """

    # NOTES:
    # - We have acronyms in <acronym title="value">abbreviation</acronym>
    #   -- We keep the value
    #   -- TODO: Offer possibility to keep acronym instead, in fields and text independently
    # - We have information that we want to read in tags span with the class indicating the category
    #   --  We want to delete the tags and their content from the final string
    # - We have the type-defining span / strong that is around the rich text string
    #   --  We want to save the type and delete the tags, but keep their contents.
    # - We have translation hints that are in tags span
    #   --  We delete them completely or keep their content
    #   -- TODO: Offer possibility to keep hints
    #   --  If content is kept, and not surrounded by parenthesis, add parenthesis

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
        self._soup = bs4.BeautifulSoup(html.unescape(self._raw), "html.parser")

        self._category = self._get_attribute_from_soup(tag="span", tag_class="category",
                                                       use_acronyms=acronyms_in_fields, delete_tag=True)
        self._colloc = self._get_attribute_from_soup(tag="span", tag_class="colloc",
                                                     use_acronyms=acronyms_in_fields, delete_tag=True)
        self._collocator = self._get_attribute_from_soup(tag="span", tag_class="collocator",
                                                         use_acronyms=acronyms_in_fields, delete_tag=True)
        self._info = self._get_attribute_from_soup(tag="span", tag_class="info",
                                                    use_acronyms=acronyms_in_fields, delete_tag=True)
        self._modus = self._get_attribute_from_soup(tag="span", tag_class="modus",
                                                    use_acronyms=acronyms_in_fields, delete_tag=True)
        self._region = self._get_attribute_from_soup(tag="span", tag_class="region",
                                                     use_acronyms=acronyms_in_fields, delete_tag=True)
        self._restriction = self._get_attribute_from_soup(tag="span", tag_class="restriction",
                                                          use_acronyms=acronyms_in_fields, delete_tag=True)
        self._rhetoric = self._get_attribute_from_soup(tag="span", tag_class="rhetoric",
                                                       use_acronyms=acronyms_in_fields, delete_tag=True)
        self._sense = self._get_attribute_from_soup(tag="span", tag_class="sense",
                                                    use_acronyms=acronyms_in_fields, delete_tag=True)
        self._style = self._get_attribute_from_soup(tag="span", tag_class="style",
                                                    use_acronyms=acronyms_in_fields, delete_tag=True)
        self._subject = self._get_attribute_from_soup(tag="span", tag_class="subject",
                                                      use_acronyms=acronyms_in_fields, delete_tag=True)
        self._topic = self._get_attribute_from_soup(tag="span", tag_class="topic",
                                                    use_acronyms=acronyms_in_fields, delete_tag=True)

        # In-string parameters
        type_possible_values = ["headword", "example", "idiom_proverb", "complement", "explanation", "definition"]
        tag_class_to_unwrap = ["tilde", "emphasize", "feminine", "or", "target"]
        tag_name_to_unwrap = ["b", "i"]
        hints_possible_values = ["grammar", "case", "number", "object-case", "modus",
                               "indirect_reference_OTHER", "or", "genus"]


        for el in self._soup.contents:
            if el.name in ["span", "strong"]:
                if el["class"][0] in type_possible_values:
                    self._type = el["class"][0]
                    el.unwrap()

        for el in self._soup.contents:
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
        for el in self._soup.contents:
            if el.name == "acronym":
                if acronyms_in_text:
                    el.replace_with(el.contents[0])
                else:
                    el.replace_with(el["title"])

        # Unhandled tags?
        for el in self._soup.contents:
            if isinstance(el, bs4.Tag):
                warnings.warn(f"Unexpected pattern found in API str ({str(el)}), removed from API str.",
                              UserWarning)
                el.extract()

        self._soup.smooth()
        remaining_text = str(self._soup)

        # Specific formatting cases
        # - Eliminate 2+ spaces
        spaces_pattern = re.compile(r'\s{2,}', re.UNICODE)
        for match in spaces_pattern.finditer(remaining_text):
            remaining_text = remaining_text.replace(match.group(0), ' ')
        # - Format for masculine/feminine words
        remaining_text = remaining_text.replace("[m] [(f)]", "[m(f)]")

        self._text = remaining_text.strip(" :+,")

    def _get_attribute_from_soup(self, tag: str, tag_class: typing.Union[typing.List[str], str, None],
                                 use_acronyms: bool, delete_tag: bool):
        ret_values = []
        soup = self._soup

        tags = soup.find_all(tag, class_=tag_class)

        for tag in tags:
            contents = tag.encode_contents().decode("utf-8").strip(" :+)(,[]")

            for acronym in tag.find_all("acronym"):
                if use_acronyms:
                    acronym_value = acronym.contents[0]
                else:
                    acronym_value = acronym['title']

                contents = contents.replace(str(acronym), acronym_value)

            ret_values.append(contents)

            if delete_tag:
                tag.extract()

        self._soup = soup

        if len(ret_values) == 0:
            return None
        elif len(ret_values) == 1:
            return ret_values[0]
        else:
            return ret_values

    def __str__(self) -> str:
        if self.text is not None:
            return self.text
        else:
            return self.raw

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
