import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.synonym import Synonym  # noqa: E501
from swagger_server import util


def list_synonym(lang, orphacode):  # noqa: E501
    """Search for the synonym(s) of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode required with a collection of related synonyms. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: Synonym
    """
    return 'do some magic!'
