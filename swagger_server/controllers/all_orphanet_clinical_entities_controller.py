import connexion
import six

from swagger_server.models.all_clinical_entity import AllClinicalEntity  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util


def list_entities(lang):  # noqa: E501
    """Search for all Orphanet clinical entities

    The result is a collection of clinical entities (active/inactive) specifying the ORPHAcode, the preferred term, the status and the definition (when one exists) for each entity. # noqa: E501

    :param lang: Language
    :type lang: str

    :rtype: AllClinicalEntity
    """
    return 'do some magic!'
