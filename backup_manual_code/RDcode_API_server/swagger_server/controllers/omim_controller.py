import operator

import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_omim import FindbyOMIM  # noqa: E501
from swagger_server.models.omim import Omim  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_omim(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s OMIM code(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as annotated OMIM code(s), specifying the characterisation of the alignment between the clinical entity and OMIM code, and the status of the mapping (validated/not yet validated) # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Omim
    """
    es = config.elastic_server

    index = "rdcode_orpha_omim_mapping"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\",\"Preferred term\", \"Code OMIM\"]}"

    response = single_res(es, index, query)
    # Test to return error
    if isinstance(response, str) or isinstance(response, tuple):
        return response
    else:
        references = response.pop("Code OMIM")
        references.sort(key=operator.itemgetter("Code OMIM"))
        response["References"] = references

        # return yaml if needed
        response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response


def list_orpha_by_omim(lang, omimcode):  # noqa: E501
    """Search for a clinical entity&#x27;s ORPHAcode by OMIM code

    The result retrieves the OMIM code as well as annotated ORPHAcode(s) and preferred term, specifying the characterisation of the alignment between the clinical entity and OMIM code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param omimcode: Unique identifier of concepts in the Online Mendelian Inheritance in Man.
    :type omimcode: int

    :rtype: FindbyOMIM
    """
    es = config.elastic_server

    index = "rdcode_orpha_omim_mapping"
    index = "{}_{}".format(index, lang.lower())

    # Find every occurrences of the queried ICD code and return the associated Date, ORPHAcode, Preferred term, Refs ICD
    query = "{\"query\": {\"match\": {\"Code OMIM.Code OMIM\": \"" + str(omimcode) + "\"}}," \
                         "\"_source\":[\"Date\", \"ORPHAcode\", \"Preferred term\", \"Code OMIM\"]}"

    response_omim_to_orpha = multiple_res(es, index, query, 1000)

    # Test to return error
    if isinstance(response_omim_to_orpha, str) or isinstance(response_omim_to_orpha, tuple):
        return response_omim_to_orpha
    else:
        response = {}
        references = []
        # Source data are organized from the perspective of ORPHA concept
        # 1 ORPHAcode => X OMIM
        # response_icd_to_orpha is a list of object containing "Code OMIM"
        # "Code OMIM" is also a list of object that need to be filtrated by OMIM
        for ref in response_omim_to_orpha:
            reference = {"ORPHAcode": int(ref["ORPHAcode"]),
                         "Preferred term": ref["Preferred term"],
                         "DisorderMappingRelation": "",
                         "DisorderMappingValidationStatus": ""}
            for CodeOMIM in ref["Code OMIM"]:
                if CodeOMIM["Code OMIM"] == omimcode:
                    reference["DisorderMappingRelation"] = CodeOMIM["DisorderMappingRelation"]
                    reference["DisorderMappingValidationStatus"] = CodeOMIM["DisorderMappingValidationStatus"]
            references.append(reference)
        # Sort references by Orphacode
        references.sort(key=operator.itemgetter("ORPHAcode"))
        # Compose the final response
        response["Date"] = response_omim_to_orpha[0]["Date"]
        response["Code OMIM"] = omimcode
        response["References"] = references

        # return yaml if needed
        response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
