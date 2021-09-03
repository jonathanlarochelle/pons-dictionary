# -*- coding: utf-8 -*-

# import built-in module
import json

# import third-party modules
import pytest
import requests
import responses

# import your own module
import pons_dictionary.pons_dictionary
from pons_dictionary.pons_dictionary import PonsDictionary
from pons_dictionary.exceptions_warnings import BadDictionaryError, PonsApiRequestError
from pons_dictionary.entry import Entry


class TestPonsDictionary:
    """ Tests for PonsDictionary. """

    @pytest.fixture
    def mock_json_content(self):
        with open("pons_api_reference_data/de_to_fr/pons_Apfel.json") as f:
            return json.load(f)

    def test_bad_dictionary(self):
        with pytest.raises(BadDictionaryError):
            pd = PonsDictionary(from_language="fr",
                                to_language="bad",
                                api_key="SECRET")

    def test_untested_dictionary(self):
        with pytest.warns(UserWarning):
            pd = PonsDictionary(from_language="fr",
                                to_language="it",
                                api_key="SECRET")

    @responses.activate
    def test_request_payload(self, mock_json_content):
        p = {"q": "Apfel",
             "l": "defr",
             "in": "de",
             "fm": "False",
             "ref": "True",
             'language': 'en'}

        responses.add(responses.GET, url=f"https://api.pons.com/v1/dictionary?"
                                         f"q={p['q']}&"
                                         f"l={p['l']}&"
                                         f"in={p['in']}&"
                                         f"fm={p['fm']}&"
                                         f"ref={p['ref']}&"
                                         f"language={p['language']}",
                      headers={"X-Secret": "SECRET"},
                      json=mock_json_content, status=200)

        pd = PonsDictionary(from_language="de",
                            to_language="fr",
                            api_key="SECRET")
        _ = pd.search("Apfel")

    @responses.activate
    def test_bad_api_key(self):
        responses.add(responses.GET, "https://api.pons.com/v1/dictionary",
                      json={}, status=403)

        pd = PonsDictionary(from_language="fr",
                            to_language="de",
                            api_key="SECRET")

        with pytest.raises(PonsApiRequestError):
            _ = pd.search("Apfel")

    @responses.activate
    def test_request_status_OK(self, mock_json_content):
        responses.add(responses.GET, "https://api.pons.com/v1/dictionary",
                      json=mock_json_content, status=200)

        pd = PonsDictionary(from_language="fr",
                            to_language="de",
                            api_key="SECRET")
        res = pd.search("Apfel")

        assert isinstance(res, list)
        assert isinstance(res[0], Entry)
        assert isinstance(res[1], Entry)

    @responses.activate
    def test_request_status_NO_CONTENT(self):
        responses.add(responses.GET, "https://api.pons.com/v1/dictionary",
                      json={}, status=204)

        pd = PonsDictionary(from_language="fr",
                            to_language="de",
                            api_key="SECRET")
        res = pd.search("Armory")

        assert isinstance(res, list)
        assert len(res) == 0

    @responses.activate
    def test_request_status_NOT_FOUND(self):
        responses.add(responses.GET, "https://api.pons.com/v1/dictionary",
                      json={}, status=404)

        pd = PonsDictionary(from_language="fr",
                            to_language="de",
                            api_key="SECRET")

        with pytest.raises(PonsApiRequestError):
            _ = pd.search("")

    @responses.activate
    def test_request_status_NOT_AUTHORIZED(self):
        responses.add(responses.GET, "https://api.pons.com/v1/dictionary",
                      json={}, status=403)

        pd = PonsDictionary(from_language="fr",
                            to_language="de",
                            api_key="SECRET")

        with pytest.raises(PonsApiRequestError):
            _ = pd.search("")

    @responses.activate
    def test_request_status_INTERNAL_SERVER_ERROR(self):
        responses.add(responses.GET, "https://api.pons.com/v1/dictionary",
                      json={}, status=500)

        pd = PonsDictionary(from_language="fr",
                            to_language="de",
                            api_key="SECRET")

        with pytest.raises(PonsApiRequestError):
            _ = pd.search("")

    @responses.activate
    def test_request_status_SERVICE_UNAVAILABLE(self):
        responses.add(responses.GET, "https://api.pons.com/v1/dictionary",
                      json={}, status=503)

        pd = PonsDictionary(from_language="fr",
                            to_language="de",
                            api_key="SECRET")

        with pytest.raises(PonsApiRequestError):
            _ = pd.search("")
