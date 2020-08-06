import operator

import connexion

from swagger_server.models.entity_by_icd import EntityByIcd  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.icd10 import Icd10  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


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
    query = "{\"query\": {\"match\": {\"Code ICD.Code ICD10\": \"" + str(icd10) + "\"}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\", \"Code ICD\"]}"

    response_icd_to_orpha = multiple_res(es, index, query, 1000)

    # Test to return error
    if isinstance(response_icd_to_orpha, str) or isinstance(response_icd_to_orpha, tuple):
        return response_icd_to_orpha
    else:
        response = {}
        references = []
        # Source data are organized from the perspective of ORPHA concept
        # 1 ORPHAcode => X ICD
        # response_icd_to_orpha is a list of object containing "Code ICD"
        # "Code ICD" is also a list of object that need to be filtrated by ICD
        for ref in response_icd_to_orpha:
            reference = {"ORPHAcode": int(ref["ORPHAcode"]),
                         "Preferred term": ref["Preferred term"],
                         "DisorderMappingRelation": "",
                         "DisorderMappingValidationStatus": ""}
            for CodeICD in ref["Code ICD"]:
                if CodeICD["Code ICD10"] == icd10:
                    reference["DisorderMappingRelation"] = CodeICD["DisorderMappingRelation"]
                    reference["DisorderMappingICDRelation"] = CodeICD["DisorderMappingICDRelation"]
                    reference["DisorderMappingValidationStatus"] = CodeICD["DisorderMappingValidationStatus"]
            references.append(reference)
        # Sort references by Orphacode
        references.sort(key=operator.itemgetter("ORPHAcode"))
        # Compose the final response
        response["Date"] = response_icd_to_orpha[0]["Date"]
        response["Code ICD10"] = icd10
        response["References"] = references

        # return yaml if needed
        response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
