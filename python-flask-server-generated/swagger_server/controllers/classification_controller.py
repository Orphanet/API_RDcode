import connexion

from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server.models.entities_by_classification import EntitiesByClassification  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_classification(lang, orphacode):  # noqa: E501
    """Search for the list of classification(s) of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode and preferred term of the clinical entity with a data set or each classification where the clinical entity is present (set includes: unique identifier of the classification, name of the classification, ORPHAcode and name of the n+1 clinical entity). # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: Classification
    """
    return 'do some magic!'


def list_orpha_by_classification(lang, hchid):  # noqa: E501
    """Search for the list of clinical entities&#x27; ORPHAcodes in one specific classification by the unique identifer of the classification.

    The result is a data set including ORPHAcode, status, preferred term and definition of all clinical entities. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param hchid: The hierarchy ID (hchID) is a number which refers to an Orphanet classification
    :type hchid: int

    :rtype: EntitiesByClassification
    """
    es = config.elastic_server

    index = "rdcode_orphaclassification_{}_{}".format(hchid, lang.lower())

    query = "{\"query\": {\"match_all\": {}}," \
            "\"_source\":[\"ORPHAcode\"]}"

    size = 1000

    scroll_timeout = config.scroll_timeout

    response_orphacode_hierarchy = uncapped_res(es, index, query, size, scroll_timeout)

    # Test to return error
    if isinstance(response_orphacode_hierarchy, str) or isinstance(response_orphacode_hierarchy, tuple):
        return response_orphacode_hierarchy
    else:
        index = "rdcode_orphanomenclature"
        index = "{}_{}".format(index, lang.lower())

        code_list = ",".join(["\"" + str(code["ORPHAcode"]) + "\"" for code in response_orphacode_hierarchy])
        query = "{\"query\": {\"terms\": {\"ORPHAcode\": [" + code_list + "]}}," \
                "\"_source\":[\"Date\", \"ORPHAcode\", \"Definition\", \"Preferred term\", \"Status\"]}"

        response = uncapped_res(es, index, query, size, scroll_timeout)
    return response
