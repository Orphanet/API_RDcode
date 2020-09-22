import connexion
import six

from swagger_server.models.child import Child  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util


def list_child(lang, orphacode, hchid):  # noqa: E501
    """Search for a clinical entity&#x27;s child(ren) by ORPHAcode and the unique identifier of a classification

    The result retrieves the clinical entity&#x27;s ORPHAcode and preferred term as well as the unique identifier and the name of the queried classification, and the clinical entity&#x27;s child(ren), specifying ORPHAcode and preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int
    :param hchid: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each classification upon its creation.
    :type hchid: int

    :rtype: Child
    """
    return 'do some magic!'
