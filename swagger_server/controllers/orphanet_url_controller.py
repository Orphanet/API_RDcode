import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orphanet_url import OrphanetURL  # noqa: E501
from swagger_server import util


def list_url(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s URL by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its stable URL pointing to the specific page of the clinical entity on the Orphanet website (www.orpha.net). # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: OrphanetURL
    """
    return 'do some magic!'
