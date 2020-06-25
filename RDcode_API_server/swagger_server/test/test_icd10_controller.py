# coding: utf-8

from __future__ import absolute_import

from flask import json

from swagger_server.models.entity_by_icd import EntityByIcd  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.icd10 import Icd10  # noqa: E501
from swagger_server.test import BaseTestCase


class TestICD10Controller(BaseTestCase):
    """ICD10Controller integration test stubs"""

    def test_list_icd10(self):
        """Test case for list_icd10

        Search for a clinical entity's ICD10 code(s) by ORPHAcode
        """
        # print("list_ICD10")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/orphacode/{orphacode}/ICD10'.format(lang=lang, orphacode=558),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))

    def test_list_orpha_by_icd10(self):
        """Test case for list_orpha_by_icd10

        Search for a clinical entity's ORPHAcode(s) by ICD-10 code
        """
        # print("list_orpha_by_icd10")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/ICD10/{icd10}'.format(lang=lang, icd10='Q87.4'),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
