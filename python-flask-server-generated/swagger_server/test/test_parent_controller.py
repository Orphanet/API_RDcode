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
        # print("list_parent")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/Classification/{hchid}/orphacode/{orphacode}/Parent'.format(lang=lang, hchid=147, orphacode=558),
                method='GET', headers={"api_key": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
