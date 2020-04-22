import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_name import FindbyName  # noqa: E501
from swagger_server.models.name import Name  # noqa: E501
from swagger_server import util


def list_by_name(lang, label):  # noqa: E501
    """Search for the clinical entity&#x27;s information by name.

    The result is a data set including ORPHAcode, status, preferred term and  definition. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param label: Entity name
    :type label: str

    :rtype: FindbyName
    """
    return 'do some magic!'


def list_name(lang, orphacode):  # noqa: E501
    """Search for the preferred term of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode required with its preferred term. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: Name
    """
    return 'do some magic!'
