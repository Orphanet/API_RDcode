import connexion
import six

from swagger_server.models.diff import Diff  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util
from swagger_server.controllers.query_controller import *
from swagger_server import config
from swagger_server.controllers.summary_controller import *

def diff(orphacode):  # noqa: E501
    """Search for differences on a clinical entity since previous release

    The result retrieves the ORPHAcode&#x27;s corresponding clinical entity with their preferred term, classification level, activity status and a flag indicating if said clinicalm entity has been updated since previous Nomenclature pack release. # noqa: E501

    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Diff
    """

    es = config.elastic_server

    index = "rdcode_orpha_diff"
    
    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\",\"Preferred term\", \"ClassificationLevel\", \"TotalStatus\"]}"
    
    response = single_res(es, index, query)
    
    if isinstance(response, str) or isinstance(response, tuple):
        summary = {key: orpha_summary("en", orphacode)[key] for key in ["ORPHAcode", "Preferred term", "ClassificationLevel", "Status"]}
        summary.update({"Updated": "false"})
        return summary
        
    response["Updated"] = "true"
    return response
