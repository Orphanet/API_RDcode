import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orphanet_url import OrphanetURL  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *


def list_url(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s URL by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its stable URL pointing to the specific page of the clinical entity on the Orphanet website (www.orpha.net). # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: OrphanetURL
    """
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"OrphanetURL\"]}"

    response = single_res(es, index, query)

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
