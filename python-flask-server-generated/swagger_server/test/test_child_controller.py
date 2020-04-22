# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.child import Child  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestChildController(BaseTestCase):
    """ChildController integration test stubs"""

    def test_list_child(self):
        """Test case for list_child

        Search for information about the n-1 (child) of the clinical entity in one specific classification by the clinical entity's ORPHAcode and unique identifier of the classification.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/Classification/{hchid}/orphacode/{orphacode}/Child'.format(lang='lang_example', orphacode=1, hchid=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
