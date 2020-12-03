# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.approx_findby_name import ApproxFindbyName  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.name import Name  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPreferredTermController(BaseTestCase):
    """PreferredTermController integration test stubs"""

    def test_list_by_approx_name(self):
        """Test case for list_by_approx_name

        Search for a clinical entity by approximate preferred term
        """
        # print("list_by_name")
        for test in [("CS", "Marfanův"),
                     ("DE", "Marfan"),
                     ("EN", "Marfan"),
                     ("ES", "Marfan"),
                     ("FR", "Marfan"),
                     ("IT", "Marfan"),
                     ("NL", "Marfan"),
                     ("PL", "Marfana"),
                     ("PT", "Marfan")]:
            # print(test)
            response = self.client.open(
                '/{lang}/ClinicalEntity/ApproximateName/{label}'.format(lang=test[0], label=test[1]),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))

    def test_list_by_name(self):
        """Test case for list_by_name

        Search for a clinical entity by preferred term
        """
        # print("list_by_name")
        for test in [("CS", "Marfanův syndrom"),
                     ("DE", "Marfan-Syndrom"),
                     ("EN", "Marfan syndrome"),
                     ("ES", "Síndrome de Marfan"),
                     ("FR", "Syndrome de Marfan"),
                     ("IT", "Sindrome di Marfan"),
                     ("NL", "Syndroom van Marfan"),
                     ("PL", "Zespół Marfana"),
                     ("PT", "Síndrome de Marfan")]:
            # print(test)
            response = self.client.open(
                '/{lang}/ClinicalEntity/FindbyName/{label}'.format(lang=test[0], label=test[1]),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))

    def test_list_name(self):
        """Test case for list_name

        Search for a clinical entity's preferred term by ORPHAcode
        """
        # print("list_name")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/orphacode/{orphacode}/Name'.format(lang=lang, orphacode=558),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
