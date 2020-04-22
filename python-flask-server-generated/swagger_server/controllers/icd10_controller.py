import connexion
import six

from swagger_server.models.entity_by_icd import EntityByIcd  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.icd10 import ICD10  # noqa: E501
from swagger_server import util


def list_icd10(lang, orphacode):  # noqa: E501
    """Search for ICD10 code(s) of the clinical entity by its ORPHAcode.

    The result is a collection of data including ORPHAcode, the stable URL pointing to the specific page of the clinical entity on the Orphanet website, characterisation of the alignment between the clinical entity and ICD-10, and status of the mapping (Validated or Not yet valiated). # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: ICD10
    """
    return 'do some magic!'


def list_orpha_by_icd10(lang, icd10):  # noqa: E501
    """Search for the clinical entity&#x27;s ORPHAcode by ICD-10 code.

    The result is a dataset including ORPHAcode, status, preferred term and definition. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param icd10: ICD10 code of entity
    :type icd10: str

    :rtype: EntityByIcd
    """
    return 'do some magic!'
