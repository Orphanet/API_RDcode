# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.definition import Definition  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefinitionController(BaseTestCase):
    """DefinitionController integration test stubs"""

    def test_list_definition(self):
        """Test case for list_definition

        Search for the definition of the clinical entity by its ORPHAcode.
        """
        response = self.client.open(
            '/{lang}/ClinicalEntity/orphacode/{orphacode}/Definition'.format(lang='EN', orphacode=558),
            method='GET', headers={"api_key": "test"})
        if isinstance(response.json, str):
            response.status = "500"
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
