import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orphanet_url import OrphanetURL  # noqa: E501
from swagger_server import util


import config
from controllers.query_controller import *


def list_url(lang, orphacode):  # noqa: E501
    """Search for the OrphanetURL of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode and the stable URL pointing to the specific page of the clinical entity on the Orphanet website of the ORPHAcode. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: OrphanetURL
    """
    es = config.elastic_server

    index = "orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\", \"OrphanetURL\"]}"

    response = single_res(es, index, query)
    return response
