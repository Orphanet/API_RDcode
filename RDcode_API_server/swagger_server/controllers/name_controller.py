import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.name import Name  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_by_name(lang, label):  # noqa: E501
    """Search for the clinical entity&#x27;s information by name.

    The result is a data set including ORPHAcode, status, preferred term and  definition. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param label: Entity preferred term
    :type label: str

    :rtype: FindbyName
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    # Special EXACT MATCH query with keyword
    query = "{\"query\": {\"term\": {\"Preferred term.keyword\": " + "\"{}\"".format(label) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\"]}"

    response = single_res(es, index, query)
    return response


def list_name(lang, orphacode):  # noqa: E501
    """Search for the preferred term of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode required with its preferred term. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the database upon creation of the entity.
    :type orphacode: int

    :rtype: Name
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\"]}"

    response = single_res(es, index, query)
    return response
