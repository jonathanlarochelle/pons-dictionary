===============
PonsDictionary
===============

PONS Dictionary API interface.

Description
===========

Interface to faciliate the use of the PONS Dictionary API with Python. The PONS Dictionary is an online translation
dictionary for 20 languages.  This project is currently in development and the package has not yet been released. This
project is not affiliated with or officially supported by PONS.

Use
---
PonsDictionary obtains data from PONS via its Dictionary API. You need to register for a personal API key on the PONS
website: `PONS Online Dictionary API`_

.. _PONS Online Dictionary API: https://en.pons.com/p/online-dictionary/developers/api

PonsDictionary can be used in two ways, either by using a one-line call from the package or by instantiating a
PonsDictionary object.

.. code-block:: python
    import ponsdictionary as pons
    hits = pons.search(term="apple", from="en", to="fr", secret="[MY API KEY]")


.. code-block:: python
    import ponsdictionary as pons
    dictionary = pons.PonsDictionary(from="en", to="fr", secret="[MY API KEY]")
    hits = dictionary.search("apple")