import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.target_entity import TargetEntity  # noqa: E501
from swagger_server import util


import config
from controllers.query_controller import *


def list_target(lang, orphacode):  # noqa: E501
    """Search for the target entity by the obsolete or deprecated clinical entity&#x27;s ORPHAcode.

    The result is the ORPHAcode and the status of the required entity, with additional &#x27;referred to&#x27; or &#x27;moved to&#x27; relations pointing to the target ORPHAcode. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the database upon creation of the entity.
    :type orphacode: int

    :rtype: TargetEntity
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Status\", \"DisorderDisorderAssociation\"]}"

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
        if response["DisorderDisorderAssociation"] is not None:
            for association in response["DisorderDisorderAssociation"]:
                if association["OutDisorder"]:
                    response_default["Relation"] = association["DisorderDisorderAssociationType"]
                    response_default["Target ORPHAcode"] = association["OutDisorder"]["ORPHAcode"]
                    break
        else:
            # If an DisorderDisorderAssociation is NOT applicable
            pass
        return response_default
    return response
