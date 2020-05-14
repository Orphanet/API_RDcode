import connexion

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.findby_omim import FindbyOMIM  # noqa: E501
from swagger_server import util


def list_orpha_by_omim(lang, omimcode):  # noqa: E501
    """Search for the clinical entity&#x27;s information by OMIM code.

    The result is a data set including ORPHAcode, status, preferred term, definition, the relationship between the clinical entity and the OMIM code and the status of the mapping. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param omimcode: Unique OMIM identifier
    :type omimcode: int

    :rtype: FindbyOMIM
    """
    return 'do some magic!'
