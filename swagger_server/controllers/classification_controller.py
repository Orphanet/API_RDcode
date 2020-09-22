import connexion
import six

from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server.models.entities_by_classification import EntitiesByClassification  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util


def list_classification(lang, orphacode):  # noqa: E501
    """Search for the classification(s) to which a clinical entity belongs by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as a collection of dataset specifying the unique identifier and the name of the classification(s) to which the searched clinical entity belongs. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Classification
    """
    return 'do some magic!'


def list_orpha_by_classification(lang, hchid):  # noqa: E501
    """Search for all ORPHAcodes and preferred terms within a specific classification by the unique identifer of the classification

    The result is a collection of clinical entities (ORPHAcode and preferred term) belonging to the queried classification. # noqa: E501

    :param lang: Language
    :type lang: str
    :param hchid: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each classification upon its creation.
    :type hchid: int

    :rtype: EntitiesByClassification
    """
    return 'do some magic!'
