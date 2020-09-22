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

    response_raw = single_res(es, index, query)

    # Check for error, an error will be returned as text or tuple
    if isinstance(response_raw, str) or isinstance(response_raw, tuple):
        return response_raw
    else:
        # If an DisorderDisorderAssociation is applicable return the Target ORPHAcode and Relation
        # from the DisorderDisorderAssociation
        response = {"Date": response_raw["Date"],
                            "ORPHAcode": response_raw["ORPHAcode"],
                            "Status": response_raw["Status"],
                            "Relation": "No relation: the entity is active",
                            "Target ORPHAcode": "No target ORPHAcode: the entity is active",
                    }
        # If the entity is NOT active ("FlagValue" != 1)
        if int(response_raw["FlagValue"]) != 1:
            # "DisorderDisorderAssociation" contains information
            if response_raw["DisorderDisorderAssociation"] is not None:
                # Multiple associations can occur but ATM there is only one association["TargetDisorder"]
                for association in response_raw["DisorderDisorderAssociation"]:
                    if association["TargetDisorder"]:
                        if association["TargetDisorder"]["ORPHAcode"]:
                            response["Relation"] = association["DisorderDisorderAssociationType"]
                            response["Target ORPHAcode"] = association["TargetDisorder"]["ORPHAcode"]
                            break
            else:
                # DisorderDisorderAssociation is NOT applicable if there is no records
                response["Relation"] = "Not Applicable"
                response["Target ORPHAcode"] = "Not Applicable"

            # return yaml if needed
            response = if_yaml(connexion.request.accept_mimetypes.best, response)
        return response
