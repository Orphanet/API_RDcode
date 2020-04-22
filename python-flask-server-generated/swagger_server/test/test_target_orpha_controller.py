# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.target_entity import TargetEntity  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTargetORPHAController(BaseTestCase):
    """TargetORPHAController integration test stubs"""

    def test_list_target(self):
        """Test case for list_target

        Search for the target entity by the obsolete or deprecated clinical entity's ORPHAcode.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/orphacode/{orphacode}/TargetEntity'.format(lang='lang_example', orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
