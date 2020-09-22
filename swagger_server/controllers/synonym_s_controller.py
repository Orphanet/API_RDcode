import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.synonym import Synonym  # noqa: E501
from swagger_server import util


def list_synonym(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s synonym(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and a collection of related synonyms. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Synonym
    """
    return 'do some magic!'
