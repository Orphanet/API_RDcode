import connexion

from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.name import Name  # noqa: E501

import config
from controllers.query_controller import *


def list_by_name(lang, label):  # noqa: E501
    """Search for a clinical entity by preferred term

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param label: Dataset
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

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response


def list_name(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s preferred term by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Name
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\"]}"

    response = single_res(es, index, query)

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
