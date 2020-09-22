import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.target_entity import TargetEntity  # noqa: E501
from swagger_server import util


def list_target(lang, orphacode):  # noqa: E501
    """Search for the target of an inactive clinical entity by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode, its status (inactive), the related target ORPHAcode as well as the relationship between the clinical entity and its target ORPHAcode. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: TargetEntity
    """
    return 'do some magic!'
