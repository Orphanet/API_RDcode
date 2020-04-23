import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.type import Type  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_type(lang, orphacode):  # noqa: E501
    """Search for the type of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode required with its related type. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: Type
    """
    es = config.elastic_server

    index = "orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Type\"]}"

    response = single_res(es, index, query)
    return response
