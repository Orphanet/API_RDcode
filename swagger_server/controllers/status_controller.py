import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.status import Status  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_status(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s status by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its status (active/inactive). # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Status
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"Status\"]}"

    response = single_res(es, index, query)

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
