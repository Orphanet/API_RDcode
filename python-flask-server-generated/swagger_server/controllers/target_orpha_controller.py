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
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: TargetEntity
    """
    es = config.elastic_server

    index = "orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Status\", \"DisorderDisorderAssociation\"]}"

    response = single_res(es, index, query)

    # Check for error, an error will be returned as text or tuple
    if isinstance(response, str) or isinstance(response, tuple):
        pass
    else:
        # If an DisorderDisorderAssociation is applicable return the ORPHAcode and Preferred term from the DisorderDisorderAssociation
        if response["DisorderDisorderAssociation"]:
            # treated_response = {}
            response = {"Date": response["Date"],
                        "ORPHAcode": response["ORPHAcode"],
                        "Relation": response["DisorderDisorderAssociation"][0]["DisorderDisorderAssociationType"],
                        "Status": response["Status"],
                        "Target ORPHAcode": response["DisorderDisorderAssociation"][0]["OutDisorder"]["ORPHAcode"],
                        }
        else:
            # If an AggregationLevel is NOT applicable return the ORPHAcode and Preferred term from the query
            response = {"Date": response["Date"],
                        "ORPHAcode": response["ORPHAcode"],
                        "Relation": "Not applicable",
                        "Status": response["Status"],
                        "Target ORPHAcode": "Not applicable",
                        }
    return response
