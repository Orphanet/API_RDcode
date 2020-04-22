# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.group_type import GroupType  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGroupTypeController(BaseTestCase):
    """GroupTypeController integration test stubs"""

    def test_list_group(self):
        """Test case for list_group

        Search for the type of group of the clinical entity by its ORPHAcode.
        """
        response = self.client.open(
            '/orphanet/ClinicalEntity/2-oas3//{lang}/ClinicalEntity/orphacode/{orphacode}/GroupType'.format(lang='lang_example', orphacode=1),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
