import operator

import connexion

from swagger_server import config
from swagger_server.controllers.query_controller import *


def list_icd10(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s ICD10 code(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as annotated ICD-10 code(s), specifying the characterisation of the alignment between the clinical entity and ICD-10 code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Icd10
    """
    es = config.elastic_server

    index = "rdcode_orpha_icd10_mapping"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\",\"Preferred term\", \"Code ICD\"]}"

    response = single_res(es, index, query)
    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        references = response.pop("Code ICD")
        references.sort(key=operator.itemgetter("Code ICD10"))
        response["References"] = references

        # return yaml if needed
        response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response


def list_orpha_by_icd10(lang, icd10):  # noqa: E501
    """Search for a clinical entity&#x27;s ORPHAcode(s) by ICD-10 code

    The result retrieves the ICD-10 code as well as annotated ORPHAcode(s) and preferred term, specifying the characterisation of the alignment between the clinical entity and ICD-10 code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param icd10: ICD10 code of entity
    :type icd10: str

    :rtype: EntityByIcd
    """
    es = config.elastic_server

    index = "rdcode_orpha_icd10_mapping"
    index = "{}_{}".format(index, lang.lower())

    # Find every occurrences of the queried ICD code and return the associated Date, ORPHAcode, Preferred term, Refs ICD
    # query = "{\"query\": {\"match\": {\"Code ICD.Code ICD10\": \"" + str(icd10) + "\"}}," \
    #         "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\", \"Code ICD\"]}"

    # icd10 = 'a0*'
    query = {
        "query": {
            "query_string": {
                "default_field": "Code ICD.Code ICD10",
                "query": str(icd10)
            }
        }
    }
    

    response_icd_to_orpha = multiple_res(es, index, query, 9999)

    # [ (x['ORPHAcode'], x['Code ICD'][0]['Code ICD10'])  for x in response_icd_to_orpha]

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
    response["Code ICD10"] = icd10
    response["References"] = []

    for hit in response_icd_to_orpha:
        reference = {
            "ORPHAcode": int(hit["ORPHAcode"]),
            "Preferred term": hit["Preferred term"]
        }

        for CodeICD in hit["Code ICD"]:
            # if CodeICD["Code ICD10"] == icd10:
            reference["ICD"] = CodeICD["Code ICD10"]
            reference["DisorderMappingRelation"] = CodeICD["DisorderMappingRelation"]
            reference["DisorderMappingICDRelation"] = CodeICD["DisorderMappingICDRelation"]
            reference["DisorderMappingValidationStatus"] = CodeICD["DisorderMappingValidationStatus"]

        response["References"].append(reference)

    # Sort references by Orphacode
    response["References"].sort(key=operator.itemgetter("ORPHAcode"))

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)

    return response
