# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.target_entity import TargetEntity  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTargetForInactiveORPHAcodeController(BaseTestCase):
    """TargetForInactiveORPHAcodeController integration test stubs"""

    def test_list_target(self):
        """Test case for list_target

        Search for the target of an inactive clinical entity by ORPHAcode
        """
        # print("list_target")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            for code in [558, 59]:
                # print(lang)
                response = self.client.open(
                    '/{lang}/ClinicalEntity/orphacode/{orphacode}/TargetEntity'.format(lang=lang, orphacode=code),
                    method='GET', headers={"apiKey": "test"})
                if isinstance(response.json, str):
                    response.status = "500"
                self.assert200(response,
                               'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
