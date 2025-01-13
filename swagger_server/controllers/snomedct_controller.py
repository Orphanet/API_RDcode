import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_omim import FindbyOMIM  # noqa: E501
from swagger_server.models.omim import Omim  # noqa: E501
from swagger_server import util


def list_orpha_by_snomed(lang, snomedcode):  # noqa: E501
    """Search for a clinical entity&#x27;s ORPHAcode by SNOMED CT code

    The result retrieves the SNOMED CT code as well as annotated ORPHAcode(s) and preferred term, specifying the characterisation of the alignment between the clinical entity and SNOMED CT code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param snomedcode: SNOMED attributed code
    :type snomedcode: int

    :rtype: FindbyOMIM
    """
    return 'do some magic!'


def list_snomed(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s SNOMED CT code(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as annotated SNOMED CT code(s), specifying the characterisation of the alignment between the clinical entity and SNOMED CT code, and the status of the mapping (validated/not yet validated) # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Omim
    """
    return 'do some magic!'
