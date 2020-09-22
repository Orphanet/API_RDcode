import connexion
import six

from swagger_server.models.approx_findby_name import ApproxFindbyName  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.name import Name  # noqa: E501
from swagger_server import util


def list_by_approx_name(lang, label):  # noqa: E501
    """Search for a clinical entity by approximate preferred term

    The result retrieves the list of clinical entity&#x27;s ORPHAcode and its preferred term based on an approximate label search # noqa: E501

    :param lang: Language
    :type lang: str
    :param label: Preferred term of the clinical entity
    :type label: str

    :rtype: ApproxFindbyName
    """
    return 'do some magic!'


def list_by_name(lang, label):  # noqa: E501
    """Search for a clinical entity by preferred term

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param label: Preferred term of the clinical entity
    :type label: str

    :rtype: FindbyName
    """
    return 'do some magic!'


def list_name(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s preferred term by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Name
    """
    return 'do some magic!'
