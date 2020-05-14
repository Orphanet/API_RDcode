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
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int
    :param hchid: The hierarchy ID (hchID) is a number which refers to an Orphanet classification
    :type hchid: int

    :rtype: Child
    """
    es = config.elastic_server

    index = "rdcode_orphaclassification_{}_{}".format(hchid, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": \"" + str(orphacode) + "\"}}," \
            "\"_source\":[\"Date\"," \
                         "\"classification.ID of the classification\"," \
                         "\"classification.Name of the classification\"," \
                         "\"ORPHAcode\"," \
                         "\"Preferred term\"," \
                         "\"childs\"]}"

    response = single_res(es, index, query)

    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        code_list = ",".join(["\"" + str(code) + "\"" for code in response["childs"]])
        query = "{\"query\": {\"terms\": {\"ORPHAcode\": [" + code_list + "]}}," \
                "\"_source\":[\"ORPHAcode\", \"Preferred term\"]}"

        response_childs = multiple_res(es, index, query, 1000)
        response["childs"] = response_childs
    return response
