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

class BadDictionaryError(PonsDictionaryError):
    """ Desired dictionary does not exist."""
    pass