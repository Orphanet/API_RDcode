# coding: utf-8

from __future__ import absolute_import

from flask import json

from swagger_server.models.all_clinical_entity import AllClinicalEntity  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAllOrphanetClinicalEntitiesController(BaseTestCase):
    """AllOrphanetClinicalEntitiesController integration test stubs"""

    def test_list_entities(self):
        """Test case for list_entities

        Search for all Orphanet clinical entities
        """
        # print("AllClinicalEntities")
        for lang in ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]:
            # print(lang)
            response = self.client.open(
                '/{lang}/ClinicalEntity'.format(lang=lang),
                method='GET', headers={"apiKey": "test"})
            if isinstance(response.json, str):
                response.status = "500"
            self.assert200(response,
                           'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
