import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.parent import Parent  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_parent(lang, hchid, orphacode):  # noqa: E501
    """Search for information about the n+1 (parent) of the clinical entity in one specific classification by the clinical entity&#x27;s ORPHAcode and unique identifier of the classification.

    The result is a data set including ORPHAcode, status, preferred term and definition of all clinical entities. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param hchid: The hierarchy ID (hchID) is a number which refers to an Orphanet classification
    :type hchid: int
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: Parent
    """
    es = config.elastic_server

    index = "rdcode_orphaclassification_{}_{}".format(hchid, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": \"" + str(orphacode) + "\"}}," \
            "\"_source\":[\"Date\"," \
                         "\"classification.ID of the classification\"," \
                         "\"classification.Name of the classification\"," \
                         "\"ORPHAcode\"," \
                         "\"Preferred term\"," \
                         "\"parents\"]}"

    response = single_res(es, index, query)

    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        code_list = ",".join(["\"" + str(code) + "\"" for code in response["parents"]])
        query = "{\"query\": {\"terms\": {\"ORPHAcode\": [" + code_list + "]}}," \
                "\"_source\":[\"ORPHAcode\", \"Preferred term\"]}"

        response_parents = multiple_res(es, index, query, 1000)
        response["parents"] = response_parents
    return response