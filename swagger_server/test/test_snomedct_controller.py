# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_omim import FindbyOMIM  # noqa: E501
from swagger_server.models.omim import Omim  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSNOMEDCTController(BaseTestCase):
    """SNOMEDCTController integration test stubs"""

    def test_list_orpha_by_snomed(self):
        """Test case for list_orpha_by_snomed

        Search for a clinical entity's ORPHAcode by SNOMED-CT code
        """
        response = self.client.open(
            '/{lang}/ClinicalEntity/SNOMED-CT/{snomedcode}'.format(lang='CS', snomedcode=19346006),
            method='GET', headers={"apiKey": "test"})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_snomed(self):
        """Test case for list_snomed

        Search for a clinical entity's SNOMED-CT code(s) by ORPHAcode
        """
        response = self.client.open(
            '/{lang}/ClinicalEntity/orphacode/{orphacode}/SNOMED-CT'.format(lang='PT', orphacode=558),
            method='GET', headers={"apiKey": "test"})
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
