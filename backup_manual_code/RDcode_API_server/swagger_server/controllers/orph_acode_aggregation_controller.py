import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orph_acode_aggregation import ORPHAcodeAggregation  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_aggregation(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s aggregation code by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode, its preferred term as well as the ORPHAcode and the preferred term of the aggregation code. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: ORPHAcodeAggregation
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
            response = {"Date": response["Date"],
                        "ORPHAcodeAggregation": response["AggregationLevelSection"]["AggregationLevel"][0]["ORPHAcode"],
                        "Preferred term": response["AggregationLevelSection"]["AggregationLevel"][0]["Preferred term"],
                        }
        else:
            # If an AggregationLevel is NOT applicable return the ORPHAcode and Preferred term from the query
            response = {"Date": response["Date"],
                        "ORPHAcodeAggregation": response["AggregationLevelSection"]["AggregationLevelStatus"],
                        "Preferred term": response["AggregationLevelSection"]["AggregationLevelStatus"],
                        }

            # return yaml if needed
            response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
