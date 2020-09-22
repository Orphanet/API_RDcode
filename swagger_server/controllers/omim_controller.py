import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_omim import FindbyOMIM  # noqa: E501
from swagger_server.models.omim import Omim  # noqa: E501
from swagger_server import util


def list_omim(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s OMIM code(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as annotated OMIM code(s), specifying the characterisation of the alignment between the clinical entity and OMIM code, and the status of the mapping (validated/not yet validated) # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Omim
    """
    return 'do some magic!'


def list_orpha_by_omim(lang, omimcode):  # noqa: E501
    """Search for a clinical entity&#x27;s ORPHAcode by OMIM code

    The result retrieves the OMIM code as well as annotated ORPHAcode(s) and preferred term, specifying the characterisation of the alignment between the clinical entity and OMIM code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param omimcode: Unique identifier of concepts in the Online Mendelian Inheritance in Man.
    :type omimcode: int

    :rtype: FindbyOMIM
    """
    return 'do some magic!'
