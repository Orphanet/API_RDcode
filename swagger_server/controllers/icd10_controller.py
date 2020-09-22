import connexion
import six

from swagger_server.models.entity_by_icd import EntityByIcd  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.icd10 import Icd10  # noqa: E501
from swagger_server import util


def list_icd10(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s ICD10 code(s) by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferred term as well as annotated ICD-10 code(s), specifying the characterisation of the alignment between the clinical entity and ICD-10 code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Icd10
    """
    return 'do some magic!'


def list_orpha_by_icd10(lang, icd10):  # noqa: E501
    """Search for a clinical entity&#x27;s ORPHAcode(s) by ICD-10 code

    The result retrieves the ICD-10 code as well as annotated ORPHAcode(s) and preferred term, specifying the characterisation of the alignment between the clinical entity and ICD-10 code, and the status of the mapping (validated/not yet validated). # noqa: E501

    :param lang: Language
    :type lang: str
    :param icd10: ICD10 code of entity
    :type icd10: str

    :rtype: EntityByIcd
    """
    return 'do some magic!'
