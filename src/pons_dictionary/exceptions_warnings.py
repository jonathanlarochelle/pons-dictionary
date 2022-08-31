# -*- coding: utf-8 -*-

# import built-in module

# import third-party modules

# import your own module

class PonsDictionaryError(Exception):
    """ Base class for other exceptions."""
    pass


class PonsApiRequestError(PonsDictionaryError):
    """ PONS API Request raises an error."""
    pass


class UnsupportedDictionaryError(PonsDictionaryError):
    """ Desired dictionary is not supported."""
    pass


class UnsupportedLanguageError(PonsDictionaryError):
    """ Desired language is not supported."""
    pass