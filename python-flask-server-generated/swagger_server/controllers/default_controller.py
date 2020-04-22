import connexion
import six

from swagger_server.models.clinical_entity import ClinicalEntity  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util


def list_entities(lang):  # noqa: E501
    """Search for all Orphanet clinical entities.

    The result is a data set that includes an ORPHAcode, the status, the preferred term and the definition (when one exists) of each active Orphanet clinical entity. # noqa: E501

    :param lang: Desired language
    :type lang: str

    :rtype: ClinicalEntity
    """
    return 'do some magic!'
