import connexion

from swagger_server.models.clinical_entity import ClinicalEntity  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_entities(lang):  # noqa: E501
    """Search for all Orphanet clinical entities

    The result is a collection of clinical entities (active/inactive) specifying the ORPHAcode, the preferred term, the status and the definition (when one exists) for each entity. # noqa: E501

    :param lang: Language
    :type lang: str

    :rtype: ClinicalEntity
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match_all\": {}}, " \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Definition\", \"Preferred term\", \"Status\"]}"

    size = 1000

    scroll_timeout = config.scroll_timeout

    response = uncapped_res(es, index, query, size, scroll_timeout)
    return response
