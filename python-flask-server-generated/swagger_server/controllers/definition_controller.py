import connexion

from swagger_server.models.definition import Definition  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_definition(lang, orphacode):  # noqa: E501
    """Search for the definition of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode required with its definition. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: Definition
    """
    es = config.elastic_server

    index = "orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"Definition\", \"ORPHAcode\"]}"

    response = single_res(es, index, query)
    return response
