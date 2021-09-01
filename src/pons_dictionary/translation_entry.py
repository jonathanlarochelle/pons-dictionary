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

    Properties:
        raw: raw string from API
        text: simple text of the translation entry
        type: of the translations entry
        category:
        collocator:
        object_case:
        region:
        rhetoric:
        sense:
        style:
        subject:
        topic:
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

    def __init__(self, api_str: str):
        # Initialize attributes
        self._raw = api_str
        self._text = None
        self._type = None

        self._category = None
        self._colloc = None
        self._collocator = None
        self._modus = None
        self._region = None
        self._rhetoric = None
        self._sense = None
        self._style = None
        self._subject = None
        self._topic = None

        # PARSING of API string
        self._soup = bs4.BeautifulSoup(html.unescape(api_str), "html.parser")

        self._category = self._get_attribute_from_soup(tag="span", tag_class="category",
                                                       use_acronyms=False, delete_tag=True)
        self._colloc = self._get_attribute_from_soup(tag="span", tag_class="colloc",
                                                     use_acronyms=False, delete_tag=True)
        self._collocator = self._get_attribute_from_soup(tag="span", tag_class="collocator",
                                                         use_acronyms=False, delete_tag=True)
        self._modus = self._get_attribute_from_soup(tag="span", tag_class="modus",
                                                    use_acronyms=False, delete_tag=True)
        self._region = self._get_attribute_from_soup(tag="span", tag_class="region",
                                                     use_acronyms=False, delete_tag=True)
        self._rhetoric = self._get_attribute_from_soup(tag="span", tag_class="rhetoric",
                                                       use_acronyms=False, delete_tag=True)
        self._sense = self._get_attribute_from_soup(tag="span", tag_class="sense",
                                                    use_acronyms=False, delete_tag=True)
        self._style = self._get_attribute_from_soup(tag="span", tag_class="style",
                                                    use_acronyms=False, delete_tag=True)
        self._subject = self._get_attribute_from_soup(tag="span", tag_class="subject",
                                                      use_acronyms=False, delete_tag=True)
        self._topic = self._get_attribute_from_soup(tag="span", tag_class="topic",
                                                    use_acronyms=False, delete_tag=True)

        # In-string parameters
        # Parse type (anything but headword)
        valid_types = ["headword", "example", "idiom_proverb", "complement", "explanation"]
        for el in self._soup.contents:
            if el.name in ["span", "strong"]:
                if el["class"][0] in valid_types:
                    self._type = el["class"][0]
                    el.unwrap()

        # Tags to unwrap
        tags_to_unwrap = ["tilde", "emphasize", "feminine", "or"]
        for el in self._soup.contents:
            if el.name in ["span", "strong"]:
                if el["class"][0] in tags_to_unwrap:
                    el.unwrap()

        # Tags to remove completely
        span_classes_to_ignore = ["grammar", "case", "number", "object-case", "modus",
                                  "target", "info", "indirect_reference_OTHER", "or", "genus"]
        for el in self._soup.contents:
            if el.name in ["span"]:
                if el["class"][0] in span_classes_to_ignore:
                    el.extract()

        # Acronyms
        acronyms_in_text = False
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

        # Final text string formatting
        # - remove square brackets
        brackets_pattern = re.compile(r'\[.*\]', re.UNICODE)
        for match in brackets_pattern.finditer(remaining_text):
            remaining_text = remaining_text.replace(match.group(0), '')
        # - Eliminate 2+ spaces
        spaces_pattern = re.compile(r'\s{2,}', re.UNICODE)
        for match in spaces_pattern.finditer(remaining_text):
            remaining_text = remaining_text.replace(match.group(0), ' ')


        self._text = remaining_text.strip(" :+(,[")

    @staticmethod
    def _process_acronym(string: str, use_acronym: bool = False):
        pattern = re.compile(r'<acronym title="(.*?)"(?:.*?)>(.*?)</acronym>',
                             re.UNICODE)  # Group 1 is non-abbreviated, group 2 is abbreviated
        for match in pattern.finditer(string):
            if use_acronym:
                string = string.replace(match.group(0), match.group(2))
            else:
                string = string.replace(match.group(0), match.group(1))
        return string

    def _get_attribute_from_soup(self, tag: str, tag_class: typing.Union[typing.List[str], str, None],
                                 use_acronyms: bool, delete_tag: bool):
        ret_values = []
        soup = self._soup

        if tag_class is not None:
            tags = soup.find_all(tag, class_=tag_class)
        else:
            tags = soup.find_all(tag)

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

    def _parse_from_pattern(self, pattern: re.Pattern, string: str) -> typing.Union[typing.List[str], str]:
         """
         Looks in string for values contained in the group 1 of pattern.
         If no values found, returns None;
         If 1 value found, returns the value as a string;
         If more than 1 values found, returns a list of values as strings.
         """
         matches = pattern.finditer(string)
         values = []
         for m in matches:
             values.append(self._process_acronym(m.group(1)))

         if len(values) == 0:
             return None
         elif len(values) == 1:
             return values[0]
         else:
             return values

    @staticmethod
    def _strip_string_from_pattern(pattern: re.Pattern, string: str) -> str:
        """
        Removes all matches of pattern in string.
        """
        matches = pattern.finditer(string)
        for m in matches:
            string = string.replace(m.group(0), '')
        return string

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
    def modus(self):
        return self._modus

    @property
    def region(self):
        return self._region

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
