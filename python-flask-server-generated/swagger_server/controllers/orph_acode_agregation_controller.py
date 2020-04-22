import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orph_acode_agregation import ORPHAcodeAgregation  # noqa: E501
from swagger_server import util


def list_agregation(lang, orphacode):  # noqa: E501
    """Search for or check the ORPHAcode agregation level of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode and the preferred term of the agregation level of the ORPHAcode that was sought. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: ORPHAcodeAgregation
    """
    return 'do some magic!'
