# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server.models.entities_by_classification import EntitiesByClassification  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestClassificationController(BaseTestCase):
    """ClassificationController integration test stubs"""

    def test_list_classification(self):
        """Test case for list_classification

        Search for the list of classification(s) of the clinical entity by its ORPHAcode.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/orphacode/{orphacode}/Classification'.format(lang='lang_example', orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_orpha_by_classification(self):
        """Test case for list_orpha_by_classification

        Search for the list of clinical entities' ORPHAcodes in one specific classification by the unique identifer of the classification.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/Classification/{hchid}'.format(lang='lang_example', hchid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
