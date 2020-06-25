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

        Search for a clinical entity's child(ren) by ORPHAcode and the unique identifier of a classification
        """
        # print("Child")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/Classification/{hchid}/orphacode/{orphacode}/Child'.format(lang=lang, orphacode=558, hchid=147),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
