# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.entity_by_icd import EntityByIcd  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.icd10 import ICD10  # noqa: E501
from swagger_server.test import BaseTestCase


class TestICD10Controller(BaseTestCase):
    """ICD10Controller integration test stubs"""

    def test_list_icd10(self):
        """Test case for list_icd10

        Search for ICD10 code(s) of the clinical entity by its ORPHAcode.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/orphacode/{orphacode}/ICD10'.format(lang='lang_example', orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_orpha_by_icd10(self):
        """Test case for list_orpha_by_icd10

        Search for the clinical entity's ORPHAcode by ICD-10 code.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/ICD10/{ICD10}/'.format(lang='lang_example', icd10='icd10_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
