# -*- coding: utf-8 -*-

# import built-in module
import typing
import html

# import third-party modules

# import your own module
import bs4

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