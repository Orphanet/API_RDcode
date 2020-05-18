# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orph_acode_agregation import ORPHAcodeAgregation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestORPHAcodeAgregationController(BaseTestCase):
    """ORPHAcodeAgregationController integration test stubs"""

    def test_list_agregation(self):
        """Test case for list_agregation

        Search for or check the ORPHAcode agregation level of the clinical entity by its ORPHAcode.
        """
        # print("list_agregation")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/orphacode/{orphacode}/ORPHAcodeAgregation'.format(lang=lang, orphacode=558),
                method='GET', headers={"api_key": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
