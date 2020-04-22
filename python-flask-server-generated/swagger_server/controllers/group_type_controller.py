import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.group_type import GroupType  # noqa: E501
from swagger_server import util


def list_group(lang, orphacode):  # noqa: E501
    """Search for the type of group of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode required with its related type of group. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: GroupType
    """
    return 'do some magic!'
