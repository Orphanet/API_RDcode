import operator

import connexion
import json

from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server.models.entities_by_classification import EntitiesByClassification  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *

def classifications_list(lang):  # noqa: E501
    """Search for all classifications hcid.

    The result retrieves all classifications hcid and their names. # noqa: E501

    :param lang: Language
    :type lang: str

    :rtype: ClassificationsList
    """

    classifications = [
        {"ID of the classification": "146", "Name of the classification": "Orphanet classification of rare cardiac diseases", "ORPHAcode": "156265"},
        {"ID of the classification": "147", "Name of the classification": "Orphanet classification of rare developmental anomalies during embryogenesis", "ORPHAcode": "156268"},
        {"ID of the classification": "148", "Name of the classification": "Orphanet classification of rare cardiac malformations", "ORPHAcode": "156271"},
        {"ID of the classification": "150", "Name of the classification": "Orphanet classification of rare inborn errors of metabolism", "ORPHAcode": "156449"},
        {"ID of the classification": "152", "Name of the classification": "Orphanet classification of rare gastroenterological diseases", "ORPHAcode": "156557"},
        {"ID of the classification": "156", "Name of the classification": "Orphanet classification of rare genetic diseases", "ORPHAcode": "158293"},
        {"ID of the classification": "181", "Name of the classification": "Orphanet classification of rare neurological diseases", "ORPHAcode": "162508"},
        {"ID of the classification": "182", "Name of the classification": "Orphanet classification of rare abdominal surgical diseases", "ORPHAcode": "162647"},
        {"ID of the classification": "183", "Name of the classification": "Orphanet classification of rare hepatic diseases", "ORPHAcode": "162651"},
        {"ID of the classification": "184", "Name of the classification": "Orphanet classification of rare respiratory diseases", "ORPHAcode": "162655"},
        {"ID of the classification": "185", "Name of the classification": "Orphanet classification of rare urogenital diseases", "ORPHAcode": "162706"},
        {"ID of the classification": "186", "Name of the classification": "Orphanet classification of rare surgical thoracic diseases", "ORPHAcode": "162709"},
        {"ID of the classification": "187", "Name of the classification": "Orphanet classification of rare skin diseases", "ORPHAcode": "162712"},
        {"ID of the classification": "188", "Name of the classification": "Orphanet classification of rare renal diseases", "ORPHAcode": "162715"},
        {"ID of the classification": "189", "Name of the classification": "Orphanet classification of rare ophthalmic diseases", "ORPHAcode": "162718"},
        {"ID of the classification": "193", "Name of the classification": "Orphanet classification of rare endocrine diseases", "ORPHAcode": "162946"},
        {"ID of the classification": "194", "Name of the classification": "Orphanet classification of rare hematological diseases", "ORPHAcode": "162949"},
        {"ID of the classification": "195", "Name of the classification": "Orphanet classification of rare immunological diseases", "ORPHAcode": "162952"},
        {"ID of the classification": "196", "Name of the classification": "Orphanet classification of rare systemic and rheumatological diseases", "ORPHAcode": "162955"},
        {"ID of the classification": "197", "Name of the classification": "Orphanet classification of rare odontological diseases", "ORPHAcode": "162958"},
        {"ID of the classification": "198", "Name of the classification": "Orphanet classification of rare circulatory system diseases", "ORPHAcode": "162961"},
        {"ID of the classification": "199", "Name of the classification": "Orphanet classification of rare bone diseases", "ORPHAcode": "162964"},
        {"ID of the classification": "200", "Name of the classification": "Orphanet classification of rare otorhinolaryngological diseases", "ORPHAcode": "162967"},
        {"ID of the classification": "201", "Name of the classification": "Orphanet classification of rare infertility disorders", "ORPHAcode": "162970"},
        {"ID of the classification": "202", "Name of the classification": "Orphanet classification of rare neoplastic diseases", "ORPHAcode": "162973"},
        {"ID of the classification": "203", "Name of the classification": "Orphanet classification of rare infectious diseases", "ORPHAcode": "162976"},
        {"ID of the classification": "204", "Name of the classification": "Orphanet classification of rare diseases due to toxic effects", "ORPHAcode": "162979"},
        {"ID of the classification": "205", "Name of the classification": "Orphanet classification of rare gynecological and obstetric diseases", "ORPHAcode": "162982"},
        {"ID of the classification": "209", "Name of the classification": "Orphanet classification of rare surgical maxillo-facial diseases", "ORPHAcode": "164019"},
        {"ID of the classification": "212", "Name of the classification": "Orphanet classification of rare allergic diseases", "ORPHAcode": "164832"},
        {"ID of the classification": "216", "Name of the classification": "Orphanet classification of rare teratologic diseases", "ORPHAcode": "168923"},
        {"ID of the classification": "231", "Name of the classification": "Orphanet classification of rare systemic and rheumatological diseases of childhood", "ORPHAcode": "280338"},
        {"ID of the classification": "233", "Name of the classification": "Orphanet classification of rare transplant-related diseases", "ORPHAcode": "506203"}
    ]

    return classifications

def list_classification(lang, orphacode):  # noqa: E501
    """Search for the classification(s) to which a clinical entity belongs by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as a collection of dataset specifying the unique identifier and the name of the classification(s) to which the searched clinical entity belongs. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
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

            # return yaml if needed
            response = if_yaml(connexion.request.accept_mimetypes.best, response)
        return response


def list_orpha_by_classification(lang, hchid):  # noqa: E501
    """Search for all ORPHAcodes and preferred terms within a specific classification by the unique identifer of the classification

    The result is a collection of clinical entities (ORPHAcode and preferred term) belonging to the queried classification. # noqa: E501

    :param lang: Language
    :type lang: str
    :param hchid: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each classification upon its creation.
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
        # Test to return error
        if isinstance(response, str) or isinstance(response, tuple):
            return response
        # Sort by classification ID
        response.sort(key=operator.itemgetter('ORPHAcode'))

        # return yaml if needed
        response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
