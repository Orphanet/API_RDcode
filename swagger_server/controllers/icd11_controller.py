import operator

import connexion

from swagger_server import config
from swagger_server.controllers.query_controller import *


def list_icd11(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s ICD11 code(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as annotated ICD-11 code(s), specifying the characterisation of the alignment between the clinical entity and ICD-11 code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Icd11
    """
    es = config.elastic_server

    index = "rdcode_orpha_icd11_mapping"
    index = "{}_{}".format(index, lang.lower())

    query = '{\"query\": {\"match\": {\"ORPHAcode\": ' + str(orphacode) + '}},' \
            '\"_source\":[\"ORPHAcode\", \"Preferred term\", \"OrphanetURL\", \"Code ICD\",\"Date\"]}'

    response = single_res(es, index, query)
    print(response, flush=True)
    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        references = response.pop("Code ICD")
        references.sort(key=operator.itemgetter("Code ICD11"))
        response["Code ICD11"] = references

        # return yaml if needed
        response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response


def list_orpha_by_icd11(lang, icd11):  # noqa: E501
    """Search for a clinical entity&#x27;s ORPHAcode(s) by ICD-10 code

    The result retrieves the ICD-11 code as well as annotated ORPHAcode(s) and preferred term, specifying the characterisation of the alignment between the clinical entity and ICD-11 code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param icd11: ICD11 code of entity
    :type icd11: str

    :rtype: EntityByIcd
    """
    es = config.elastic_server

    index = "rdcode_orpha_icd11_mapping"
    index = "{}_{}".format(index, lang.lower())

    query = {
        "query": {
            "query_string": {
                "default_field": "Code ICD.Code ICD11",
                "query": str(icd11)
            }
        }
    }

    response_icd_to_orpha = multiple_res(es, index, query, 9999)


    # Statement condition to return error
    if isinstance(response_icd_to_orpha, str) or isinstance(response_icd_to_orpha, tuple):
        return response_icd_to_orpha
    
    # If no response (response_icd_to_orpha) is ok, it needs to be formatted
    """     
    Source data are organized from the perspective of ORPHA concept
    1 ORPHAcode => X ICD
    response_icd_to_orpha is a list of object containing "Code ICD"
    "Code ICD" is also a list of object that need to be filtrated by ICD
    """
    response = {}
    response["Date"] = response_icd_to_orpha[0]["Date"]
    response["Code ICD11"] = icd11
    response["References"] = []

    for hit in response_icd_to_orpha:
        reference = {
            "ORPHAcode": int(hit["ORPHAcode"]),
            "Preferred term": hit["Preferred term"]
        }

        for CodeICD in hit["Code ICD"]:
            reference["Code ICD11"] = CodeICD["Code ICD11"]
            reference["DisorderMappingRelation"] = CodeICD["DisorderMappingRelation"]
            reference["DisorderMappingICDRelation"] = CodeICD["DisorderMappingICDRelation"]
            reference["DisorderMappingValidationStatus"] = CodeICD["DisorderMappingValidationStatus"]
            reference["DisorderMappingICDRefUrl"] = CodeICD["DisorderMappingICDRefUrl"]
            reference["DisorderMappingICDRefUri"] = CodeICD["DisorderMappingICDRefUri"]
        response["References"].append(reference)

    # Sort references by Orphacode
    response["References"].sort(key=operator.itemgetter("ORPHAcode"))

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)

    return response
