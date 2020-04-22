# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.parent import Parent  # noqa: E501
from swagger_server.test import BaseTestCase


class TestParentController(BaseTestCase):
    """ParentController integration test stubs"""

    def test_list_parent(self):
        """Test case for list_parent

        Search for information about the n+1 (parent) of the clinical entity in one specific classification by the clinical entity's ORPHAcode and unique identifier of the classification.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/Classification/{hchid}/orphacode/{orphacode}/Parent'.format(lang='lang_example', hchid=1, orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()