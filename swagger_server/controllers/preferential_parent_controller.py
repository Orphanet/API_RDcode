import connexion
import six

from swagger_server.models.children_list import ChildrenList  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orpha_to_children import OrphaToChildren  # noqa: E501
from swagger_server.models.orpha_to_parent import OrphaToParent  # noqa: E501
from swagger_server.models.parent_list import ParentList  # noqa: E501
from swagger_server import util

from swagger_server import config
from swagger_server.controllers.query_controller import *
from swagger_server.controllers.classification_controller import classifications_list

def children_list(lang, orphacode):  # noqa: E501
    """Search for a preferential parent children by ORPHAcode

    The result retrieves all entities having corresponding preferential parent with their preferred term. # noqa: E501

    :param lang: Language
    :type lang: str

    :rtype: ChildrenList
    """

    es = config.elastic_server

    index = "rdcode_orphalinearisation"
    index = "{}_{}".format(index, lang.lower())

    variants = {
        "en" : "Preferential parent",
        "fr" : "Parent préférentiel",
        "es" : "Cabeza de clasificación preferencial",
        "de" : "Bevorzugte Zuordnung",
        "it" : "Termine madre preferenziale",
        "pt" : "Progenitor preferencial",
        "pl" : "Uprzywilejowany rodzic",
        "nl" : "Preferentiële ouder"
    }

    query = {
        "query" : {
        "match_all": {}
        },
        "_source": ["Date", "ORPHAcode", "Preferred term", "DisorderDisorderAssociation"]
    }

    response = multiple_res(es, index, query, size=10000)

    if isinstance(response, str) or isinstance(response, tuple):
        return response

    parentsDict = { }
 
    for disorder in response:
        associations = disorder["DisorderDisorderAssociation"]
        if associations is None:
            continue
        for association in associations:
            if association["DisorderDisorderAssociationType"] == variants[lang.lower()]:
                parent = association["TargetDisorder"]["ORPHAcode"]
                parent_name = association["TargetDisorder"]["Preferred term"]
                if parent not in parentsDict:
                    parentsDict.update({parent : []})
                parentsDict[parent].append({
                    "ORPHAcode" : disorder["ORPHAcode"], 
                    "Preferred term": disorder["Preferred term"],
                    "Preferential parent" : {
                        "ORPHAcode" : parent,
                        "Preferred term" : parent_name
                    }})

    try:
        return parentsDict[orphacode]
    except Exception:
        return "Clinical entity does not exist or is not a preferential parent."


def orpha_parent(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s preferential parent by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferential parent. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: OrphaToParent
    """

    es = config.elastic_server
    
    index = "rdcode_orphalinearisation"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\",\"Preferred term\", \"DisorderDisorderAssociation\"]}"
    
    response = single_res(es, index, query)

    if isinstance(response, str) or isinstance(response, tuple):
        return response
    
    tmp = {
        "ORPHAcode": response["DisorderDisorderAssociation"][0]["TargetDisorder"]["ORPHAcode"],
        "Preferred term": response["DisorderDisorderAssociation"][0]["TargetDisorder"]["Preferred term"]
    }

    new_response = {
        "ORPHAcode": response["ORPHAcode"],
        "Preferred term": response["Preferred term"],
        "Date": response["Date"],
        "Preferential parent": tmp
    }

    return new_response


def parents_list(lang):  # noqa: E501
    """Search for all preferential parents

    The result retrieves all clinical entities being preferential parents. # noqa: E501

    :param lang: Language
    :type lang: str

    :rtype: ParentList
    """
    es = config.elastic_server

    index = "rdcode_orphalinearisation"
    index = "{}_{}".format(index, lang.lower())

    variants = {
        "en" : "Preferential parent",
        "fr" : "Parent préférentiel",
        "es" : "Cabeza de clasificación preferencial",
        "de" : "Bevorzugte Zuordnung",
        "it" : "Termine madre preferenziale",
        "pt" : "Progenitor preferencial",
        "pl" : "Uprzywilejowany rodzic",
        "nl" : "Preferentiële ouder"
    }

    query = {
        "query" : {
        "match_all": {}
        },
        "_source": ["Date", "ORPHAcode", "Preferred term", "DisorderDisorderAssociation"]
    }

    response = multiple_res(es, index, query, size=10000)

    if isinstance(response, str) or isinstance(response, tuple):
        return response

    parentsDict = []
 
    for disorder in response:
        associations = disorder["DisorderDisorderAssociation"]
        if associations is None:
            continue
        for association in associations:
            if association["DisorderDisorderAssociationType"] == variants[lang.lower()]:
                parent = association["TargetDisorder"]["ORPHAcode"]
                parent_name = association["TargetDisorder"]["Preferred term"]
                tmp = {
                        "ORPHAcode" : parent,
                        "Preferred term" : parent_name
                    }
                if tmp not in parentsDict:
                    parentsDict.append(tmp)
    return parentsDict