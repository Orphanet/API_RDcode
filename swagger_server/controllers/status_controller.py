import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.status import Status  # noqa: E501
from swagger_server import util


def list_status(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s status by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its status (active/inactive). # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Status
    """
    return 'do some magic!'
