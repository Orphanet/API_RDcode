import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.target_entity import TargetEntity  # noqa: E501
from swagger_server import util


import config
from controllers.query_controller import *


def list_target(lang, orphacode):  # noqa: E501
    """Search for the target of an inactive clinical entity by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode, its status (inactive), the related target ORPHAcode as well as the relationship between the clinical entity and its target ORPHAcode. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: TargetEntity
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Status\", \"DisorderDisorderAssociation\", \"FlagValue\"]}"

    response = single_res(es, index, query)

    # Check for error, an error will be returned as text or tuple
    if isinstance(response, str) or isinstance(response, tuple):
        pass
    else:
        # If an DisorderDisorderAssociation is applicable return the Target ORPHAcode and Relation
        # from the DisorderDisorderAssociation
        response_default = {"Date": response["Date"],
                            "ORPHAcode": response["ORPHAcode"],
                            "Status": response["Status"],
                            "Relation": "No relation: the entity is active",
                            "Target ORPHAcode": "No target ORPHAcode: the entity is active",
                            }
        # If the entity is NOT active ("FlagValue" != 1)
        if int(response["FlagValue"]) != 1:
            # "DisorderDisorderAssociation" contains information
            if response["DisorderDisorderAssociation"] is not None:
                for association in response["DisorderDisorderAssociation"]:
                    if association["OutDisorder"]:
                        if association["OutDisorder"]["ORPHAcode"]:
                            response_default["Relation"] = association["DisorderDisorderAssociationType"]
                            response_default["Target ORPHAcode"] = association["OutDisorder"]["ORPHAcode"]
                            break
            else:
                # If an DisorderDisorderAssociation is NOT applicable
                response_default["Relation"] = "Not Applicable"
                response_default["Target ORPHAcode"] = "Not Applicable"
        return response_default
    return response
