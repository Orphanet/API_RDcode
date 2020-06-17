import operator

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
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the database upon creation of the entity.
    :type orphacode: int

    :rtype: Classification
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature_{}".format(lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\",  \"Preferred term\"]}"

    # First query to find the chosen disorder info
    response = single_res(es, index, query)
    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        # Query the selected orphacode in all classifications
        index = "rdcode_orphaclassification_*_{}".format(lang.lower())

        size = 1000

        query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
                "\"_source\":[\"Classification\"]}"

        response_classification = multiple_res(es, index, query, size)
        # Test to return error
        if isinstance(response_classification, str) or isinstance(response_classification, tuple):
            return response_classification
        else:
            refined_classification = []
            # Select desired information
            for classification in response_classification:
                classif_info = {"ID of the classification": classification["Classification"]["ID of the classification"],
                        "Name of the classification": classification["Classification"]["Name of the classification"]}
                refined_classification.append(classif_info)
            # Sort by classification ID
            refined_classification.sort(key=operator.itemgetter('ID of the classification'))
            # Append the classification response to the disorder response
            response["Classification"] = refined_classification
        return response


def list_orpha_by_classification(lang, hchid):  # noqa: E501
    """Search for the list of clinical entities&#x27; ORPHAcodes in one specific classification by the unique identifer of the classification.

    The result is a data set including ORPHAcode, status, preferred term and definition of all clinical entities. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param hchid: The hierarchy ID (hchID) is a specific identifier attributed to an Orphanet classification.
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
                "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\"]}"

        response = uncapped_res(es, index, query, size, scroll_timeout)
    return response
