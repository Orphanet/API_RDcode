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
        response = self.client.open(
            '/{lang}/ClinicalEntity/ApproximateName/{label}'.format(lang='lang_example', label='label_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_by_name(self):
        """Test case for list_by_name

        Search for a clinical entity by preferred term
        """
        response = self.client.open(
            '/{lang}/ClinicalEntity/FindbyName/{label}'.format(lang='lang_example', label='label_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_name(self):
        """Test case for list_name

        Search for a clinical entity's preferred term by ORPHAcode
        """
        response = self.client.open(
            '/{lang}/ClinicalEntity/orphacode/{orphacode}/Name'.format(lang='lang_example', orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
