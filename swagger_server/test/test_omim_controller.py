# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_omim import FindbyOMIM  # noqa: E501
from swagger_server.models.omim import Omim  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOMIMController(BaseTestCase):
    """OMIMController integration test stubs"""

    def test_list_omim(self):
        """Test case for list_omim

        Search for a clinical entity's OMIM code(s) by ORPHAcode
        """
        # print("list_OMIM")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/orphacode/{orphacode}/OMIM'.format(lang=lang, orphacode=558),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))

    def test_list_orpha_by_omim(self):
        """Test case for list_orpha_by_omim

        Search for a clinical entity's ORPHAcode by OMIM code
        """
        # print("list_orpha_by_omim")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/FindbyOMIM/{codeOMIM}'.format(lang=lang, codeOMIM=154700),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
