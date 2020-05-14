import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orph_acode_agregation import ORPHAcodeAgregation  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_agregation(lang, orphacode):  # noqa: E501
    """Search for or check the ORPHAcode agregation level of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode and the preferred term of the agregation level of the ORPHAcode that was sought. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the database upon creation of the entity.
    :type orphacode: int

    :rtype: ORPHAcodeAgregation
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"AggregationLevelSection\", \"Preferred term\", \"ORPHAcode\"]}"

    response = single_res(es, index, query)

    # Check for error, an error will be returned as text or tuple
    if isinstance(response, str) or isinstance(response, tuple):
        pass
    else:
        # If an AggregationLevel is applicable return the ORPHAcode and Preferred term from the Aggregation
        if response["AggregationLevelSection"]["AggregationLevel"]:
            # treated_response = {}
            response = {"Date": response["Date"],
                        "ORPHAcodeAggregation": response["AggregationLevelSection"]["AggregationLevel"][0]["ORPHAcodeAggregation"],
                        "Preferred term": response["AggregationLevelSection"]["AggregationLevel"][0]["Preferred term"],
                        }
        else:
            # If an AggregationLevel is NOT applicable return the ORPHAcode and Preferred term from the query
            response = {"Date": response["Date"],
                        "ORPHAcodeAggregation": response["ORPHAcode"],
                        "Preferred term": response["Preferred term"],
                        }
    return response
