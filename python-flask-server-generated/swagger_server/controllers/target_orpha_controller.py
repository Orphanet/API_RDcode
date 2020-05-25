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
        # If an DisorderDisorderAssociation is applicable return the ORPHAcode and Preferred term from the DisorderDisorderAssociation
        if response["DisorderDisorderAssociation"]:
            DisorderDisorderAssociation = []
            for association in response["DisorderDisorderAssociation"]:
                try:
                    DisorderDisorderAssociation.append({"Relation": association["DisorderDisorderAssociationType"],
                                                        "Target ORPHAcode": association["OutDisorder"]["ORPHAcode"]})
                except TypeError:
                    DisorderDisorderAssociation.append({"Relation": association["DisorderDisorderAssociationType"],
                                                        "Target ORPHAcode": association["InDisorder"]["ORPHAcode"]})
            response = {"Date": response["Date"],
                        "ORPHAcode": response["ORPHAcode"],
                        "Status": response["Status"],
                        "DisorderDisorderAssociation": DisorderDisorderAssociation
                        }
        else:
            # If an AggregationLevel is NOT applicable return the ORPHAcode and Preferred term from the query
            response = {"Date": response["Date"],
                        "ORPHAcode": response["ORPHAcode"],
                        "Status": response["Status"],
                        "Relation": "Not applicable",
                        "Target ORPHAcode": "Not applicable",
                        }
    return response
