# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.approx_findby_name import ApproxFindbyName  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.synonym import Synonym  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSynonymSController(BaseTestCase):
    """SynonymSController integration test stubs"""

    def test_list_synonym(self):
        """Test case for list_synonym

        Search for a clinical entity's synonym(s) by ORPHAcode
        """
        # print("list_synonym")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/orphacode/{orphacode}/Synonym'.format(lang=lang, orphacode=558),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))

    def test_list_synonym_by_approx_name(self):
        """Test case for list_synonym_by_approx_name

        Search for a clinical entity by approximate synonym
        """
        # print("list_by_name")
        for test in [("CS", "Costů"),
                     ("DE", "Cost"),
                     ("EN", "Cost"),
                     ("ES", "Cost"),
                     ("FR", "Cost"),
                     ("IT", "Cost"),
                     ("NL", "Costasyndroo"),
                     ("PL", "Cost"),
                     ("PT", "Cost")]:
            # print(test)
            response = self.client.open(
                '/{lang}/ClinicalEntity/ApproximateName/{label}/Synonym'.format(lang=test[0], label=test[1]),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))

    def test_list_synonym_by_name(self):
        """Test case for list_synonym_by_name

        Search for a clinical entity by synonym
        """
        # print("list_by_name")
        for test in [("CS", "Costův"),
                     ("DE", "Costa"),
                     ("EN", "Costa"),
                     ("ES", "Costa"),
                     ("FR", "Costa"),
                     ("IT", "Costa"),
                     ("NL", "Costasyndroom"),
                     ("PL", "Costa"),
                     ("PT", "Costa")]:
            # print(test)
            response = self.client.open(
                '/{lang}/ClinicalEntity/ApproximateName/{label}/Synonym'.format(lang=test[0], label=test[1]),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
