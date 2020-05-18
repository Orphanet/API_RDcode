import connexion

from swagger_server.models.child import Child  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_child(lang, orphacode, hchid):  # noqa: E501
    """Search for information about the n-1 (child) of the clinical entity in one specific classification by the clinical entity&#x27;s ORPHAcode and unique identifier of the classification.

    The result returned the ORPHAcode and preferred term of the clinical entity with a data collection for the searched classification  (data set includes: unique identifier of the classification, name of the classification, ORPHAcode and name of the n-1 clinical entity also named as &#x27;child&#x27; of the clinical entity). # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the database upon creation of the entity.
    :type orphacode: int
    :param hchid: The hierarchy ID (hchID) is a specific identifier attributed to an Orphanet classification.
    :type hchid: int

    :rtype: Child
    """
    es = config.elastic_server

    index = "rdcode_orphaclassification_{}_{}".format(hchid, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": \"" + str(orphacode) + "\"}}," \
            "\"_source\":[\"Date\"," \
                         "\"Classification.ID of the classification\"," \
                         "\"Classification.Name of the classification\"," \
                         "\"ORPHAcode\"," \
                         "\"Preferred term\"," \
                         "\"Child\"]}"

    response = single_res(es, index, query)

    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        if not response["Child"]:
            response_child = []
        else:
            code_list = ",".join(["\"" + str(code) + "\"" for code in response["Child"]])
            query = "{\"query\": {\"terms\": {\"ORPHAcode\": [" + code_list + "]}}," \
                    "\"_source\":[\"ORPHAcode\", \"Preferred term\"]}"

            response_child = multiple_res(es, index, query, 1000)
            if isinstance(response_child, str) or isinstance(response_child, tuple):
                return response_child
        response["Child"] = response_child
    return response
