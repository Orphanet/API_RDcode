# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_omim import FindbyOMIM  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOMIMController(BaseTestCase):
    """OMIMController integration test stubs"""

    def test_list_orpha_by_omim(self):
        """Test case for list_orpha_by_omim

        Search for the clinical entity's information by OMIM code.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/FindbyOMIM/{codeOMIM}'.format(lang='lang_example', code_omim=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
