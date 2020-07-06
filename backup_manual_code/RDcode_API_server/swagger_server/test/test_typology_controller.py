# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.typology import Typology  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTypologyController(BaseTestCase):
    """TypologyController integration test stubs"""

    def test_list_typology(self):
        """Test case for list_typology

        Search for a clinical entity's typology by ORPHAcode.
        """
        # print("list_type")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/orphacode/{orphacode}/Typology'.format(lang=lang, orphacode=558),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
