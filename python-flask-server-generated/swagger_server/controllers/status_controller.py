import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.status import Status  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_status(lang, orphacode):  # noqa: E501
    """Search for the status of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode and the status of the ORPHAcode. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the database upon creation of the entity.
    :type orphacode: int

    :rtype: Status
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Status\"]}"

    response = single_res(es, index, query)
    return response
