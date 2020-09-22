import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.parent import Parent  # noqa: E501
from swagger_server import util


def list_parent(lang, hchid, orphacode):  # noqa: E501
    """Search for clinical entity&#x27;s parent(s) by ORPHAcode and the unique identifier of the classification

    The result retrieves the clinical entity&#x27;s ORPHAcode and preferred term as well as the unique identifier and the name of the queried classification, and the clinical entity&#x27;s parent(s), specifying ORPHAcode and preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param hchid: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each classification upon its creation.
    :type hchid: int
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Parent
    """
    return 'do some magic!'
