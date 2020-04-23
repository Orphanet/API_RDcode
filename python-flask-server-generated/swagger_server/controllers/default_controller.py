import connexion

from swagger_server.models.clinical_entity import ClinicalEntity  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_entities(lang):  # noqa: E501
    """Search for all Orphanet clinical entities.

    The result is a data set that includes an ORPHAcode, the status, the preferred term and the definition (when one exists) of each active Orphanet clinical entity. # noqa: E501

    :param lang: Desired language
    :type lang: str

    :rtype: ClinicalEntity
    """
    es = config.elastic_server

    index = "orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match_all\": {}}, " \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Definition\", \"Preferred term\", \"Status\"]}"

    size = 1000

    scroll_timeout = config.scroll_timeout

    response = uncapped_res(es, index, query, size, scroll_timeout)
    return response
