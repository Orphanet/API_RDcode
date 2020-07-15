# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orph_acode_aggregation import ORPHAcodeAggregation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestORPHAcodeAggregationController(BaseTestCase):
    """ORPHAcodeAggregationController integration test stubs"""

    def test_list_aggregation(self):
        """Test case for list_aggregation

        Search for a clinical entity's aggregation code by ORPHAcode
        """
        # print("list_aggregation")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity/orphacode/{orphacode}/ORPHAcodeAggregation'.format(lang=lang, orphacode=558),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
