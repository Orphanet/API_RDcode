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
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/orphacode/{orphacode}/ORPHAcodeAgregation'.format(lang='lang_example', orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
