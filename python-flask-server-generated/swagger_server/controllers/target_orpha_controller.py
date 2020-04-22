import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.target_entity import TargetEntity  # noqa: E501
from swagger_server import util


def list_target(lang, orphacode):  # noqa: E501
    """Search for the target entity by the obsolete or deprecated clinical entity&#x27;s ORPHAcode.

    The result is the ORPHAcode and the status of the required entity, with additional &#x27;referred to&#x27; or &#x27;moved to&#x27; relations pointing to the target ORPHAcode. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: TargetEntity
    """
    return 'do some magic!'
