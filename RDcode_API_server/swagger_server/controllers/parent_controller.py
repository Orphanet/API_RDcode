import operator

import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.parent import Parent  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_parent(lang, hchid, orphacode):  # noqa: E501
    """Search for clinical entity&#x27;s parent(s) by ORPHAcode and the unique identifier of the classification

    The result retrieves the clinical entity&#x27;s ORPHAcode and preferred term as well as the unique identifier and the name of the queried classification, and the clinical entity&#x27;s parent(s), specifying ORPHAcode and preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param hchid: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each classification upon its creation.
    :type hchid: int
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Parent
    """
    es = config.elastic_server

    index = "rdcode_orphaclassification_{}_{}".format(hchid, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": \"" + str(orphacode) + "\"}}," \
            "\"_source\":[\"Date\"," \
                         "\"Classification.ID of the classification\"," \
                         "\"Classification.Name of the classification\"," \
                         "\"ORPHAcode\"," \
                         "\"Preferred term\"," \
                         "\"Parent\"]}"

    response = single_res(es, index, query)

    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        code_list = ",".join(["\"" + str(code) + "\"" for code in response["Parent"]])
        query = "{\"query\": {\"terms\": {\"ORPHAcode\": [" + code_list + "]}}," \
                "\"_source\":[\"ORPHAcode\", \"Preferred term\"]}"

        response_parent = multiple_res(es, index, query, 1000)
        # Test to return error
        if isinstance(response_parent, str) or isinstance(response_parent, tuple):
            return response_parent
        response_parent.sort(key=operator.itemgetter('ORPHAcode'))
        response["Parent"] = response_parent

        # return yaml if needed
        response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
