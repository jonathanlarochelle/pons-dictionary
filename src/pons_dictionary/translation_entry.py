# -*- coding: utf-8 -*-

# import built-in module
import re
import typing
import warnings

# import third-party modules

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
        self._region = None
        self._rhetoric = None
        self._sense = None
        self._style = None
        self._subject = None
        self._topic = None

        # PARSING of API string
        # End-of-string parameters

        # Parse category
        category_pattern = re.compile(r'<span class="category">(.*?)</span>', re.UNICODE)  # Group 1 is category
        self._category = self._parse_from_pattern(category_pattern, api_str)
        api_str = self._strip_string_from_pattern(category_pattern, api_str)

        # Parse colloc
        colloc_pattern = re.compile(r'<span class="colloc">\((.*?)\)</span>', re.UNICODE)  # Group 1 is colloc
        self._colloc = self._parse_from_pattern(colloc_pattern, api_str)
        api_str = self._strip_string_from_pattern(colloc_pattern, api_str)

        # Parse collocator
        collocator_pattern = re.compile(r'<span class="collocator">(.*?)</span>', re.UNICODE)  # Group 1 is collocator
        self._collocator = self._parse_from_pattern(collocator_pattern, api_str)
        api_str = self._strip_string_from_pattern(collocator_pattern, api_str)

        # Parse region
        region_pattern = re.compile(r'<span class="region">(.*?)</span>', re.UNICODE)  # Group 1 is region
        self._region = self._parse_from_pattern(region_pattern, api_str)
        api_str = self._strip_string_from_pattern(region_pattern, api_str)

        # Parse rhetoric
        rhetoric_pattern = re.compile(r'<span class="rhetoric">(.*?)</span>', re.UNICODE)  # Group 1 is rhetoric
        self._rhetoric = self._parse_from_pattern(rhetoric_pattern, api_str)
        api_str = self._strip_string_from_pattern(rhetoric_pattern, api_str)

        # Parse sense
        sense_pattern = re.compile(r'<span class="sense">\((.*?)\)</span>', re.UNICODE)  # Group 1 is sense
        self._sense = self._parse_from_pattern(sense_pattern, api_str)
        api_str = self._strip_string_from_pattern(sense_pattern, api_str)

        # Parse style
        style_pattern = re.compile(r'<span class="style">(.*?)</span>', re.UNICODE)  # Group 1 is style
        self._style = self._parse_from_pattern(style_pattern, api_str)
        api_str = self._strip_string_from_pattern(style_pattern, api_str)

        # Parse subject
        subject_pattern = re.compile(r'<span class="subject">(.*?):</span>', re.UNICODE)  # Group 1 is subject
        self._subject = self._parse_from_pattern(subject_pattern, api_str)
        api_str = self._strip_string_from_pattern(subject_pattern, api_str)

        # Parse topic
        topic_pattern = re.compile(r'<span class="topic">(.*?)</span>', re.UNICODE)  # Group 1 is topic
        self._topic = self._parse_from_pattern(topic_pattern, api_str)
        api_str = self._strip_string_from_pattern(topic_pattern, api_str)

        # In-string parameters
        # Parse type (anything but headword)
        type_pattern = re.compile(r'<span class="(.*?)">(.*)</span>',
                                  re.UNICODE)  # Group 1 is type, Group 2 is rest of string
        type_match = type_pattern.match(api_str)
        if type_match is not None:
            self._type = type_match.group(1)
            api_str = type_match.group(2)

        type_headword_pattern = re.compile(r'<strong class="(headword)">(.*)</strong>',
                                           re.UNICODE)  # Group 1 is type, Group 2 is rest of string
        type_headword_match = type_headword_pattern.match(api_str)
        if type_headword_match is not None:
            self._type = type_headword_match.group(1)
            api_str = type_headword_match.group(2)

        # Eliminate remaining tags
        # <strong class="tilde">[A]</strong> -> strip tags, keep [A]
        tilde_pattern = re.compile(r'<strong class="tilde">(.*?)</strong>', re.UNICODE)
        for match in tilde_pattern.finditer(api_str):
            api_str = api_str.replace(match.group(0), match.group(1))

        # other tags: strip
        span_classes_to_ignore = ["grammar SUBST", "grammar VERB"]
        general_pattern = re.compile(r'<span class="(.*?)">(.*?)</span>', re.UNICODE)

        for match in general_pattern.finditer(api_str):
            if match.group(1) not in span_classes_to_ignore:
                warnings.warn(f"Unexpected pattern found in API str ({match.group(0)}), removed from API str.",
                              UserWarning)
            api_str = api_str.replace(match.group(0), '')

        self._text = api_str.strip(', ')

    @staticmethod
    def _process_acronym(str_with_acronym: str, use_acronym: bool = False):
        pattern = re.compile(r'<acronym title="(.*?)"(?:.*)?>(.*?)</acronym>',
                             re.UNICODE)  # Group 1 is non-abbreviated, group 2 is abbreviated
        match = pattern.match(str_with_acronym)
        if match is not None:
            if use_acronym:
                str_without_acronym = match.group(2)
            else:
                str_without_acronym = match.group(1)
        else:
            str_without_acronym = str_with_acronym
        return str_without_acronym

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
