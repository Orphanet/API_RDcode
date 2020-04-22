# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.name import Name  # noqa: E501
from swagger_server.test import BaseTestCase


class TestNameController(BaseTestCase):
    """NameController integration test stubs"""

    def test_list_by_name(self):
        """Test case for list_by_name

        Search for the clinical entity's information by name.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/FindbyName/{label}'.format(lang='lang_example', label='label_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_name(self):
        """Test case for list_name

        Search for the preferred term of the clinical entity by its ORPHAcode.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/orphacode/{orphacode}/Name'.format(lang='lang_example', orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
