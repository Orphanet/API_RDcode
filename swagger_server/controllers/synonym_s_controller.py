import connexion

from swagger_server.models.approx_findby_name import ApproxFindbyName  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.synonym import Synonym  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_synonym(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s synonym(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and a collection of related synonyms. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Synonym
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Synonym\"]}"

    response = single_res(es, index, query)

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response


def list_synonym_by_approx_name(lang, label):  # noqa: E501
    """Search for a clinical entity by approximate synonym

    The result retrieves the list of clinical entity&#x27;s ORPHAcode and its preferred term based on an approximate label search # noqa: E501

    :param lang: Language
    :type lang: str
    :param label: Approximate synonym of the clinical entity
    :type label: str

    :rtype: ApproxFindbyName
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    # print(label)

    # Special FUZZY MATCH query
    query_term_list = []
    for term in label.strip().split(" "):
        query_term = "{{\"query_string\": {{\"default_field\": \"Synonym\", \"query\": \"*{}*\"}}}}".format(term)
        query_term += ", {{\"fuzzy\": {{\"Synonym\": {{\"value\" :\"{}\", \"fuzziness\": \"AUTO\"}}}}}}".format(term)
        # print(query_term)
        query_term_list.append(query_term)
        # query_term_list.append(additional_query_term)
    query_term_list = "[" + ", ".join(query_term_list) + "]"
    # print(query_term_list)

    query = "{\"query\": {\"bool\": {\"should\": " + query_term_list + "}}" + \
            ",\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\"]}"

    # print(query)
    response = multiple_res(es, index, query, 10000)
    # print(response)

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response


def list_synonym_by_name(lang, label):  # noqa: E501
    """Search for a clinical entity by synonym

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param label: Synonym of the clinical entity
    :type label: str

    :rtype: FindbyName
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    # Special EXACT MATCH query with keyword
    query = "{\"query\": {\"term\": {\"Synonym.keyword\": " + "\"{}\"".format(label) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\"]}"

    response = single_res(es, index, query)

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
