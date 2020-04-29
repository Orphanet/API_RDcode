import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.group_type import GroupType  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_group(lang, orphacode):  # noqa: E501
    """Search for the type of group of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode required with its related type of group. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: GroupType
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"GroupType\", \"ORPHAcode\"]}"

    response = single_res(es, index, query)
    return response
