import connexion
import six

from swagger_server.models.classification import Classification  # noqa: E501
from swagger_server.models.entities_by_classification import EntitiesByClassification  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util


def list_classification(lang, orphacode):  # noqa: E501
    """Search for the list of classification(s) of the clinical entity by its ORPHAcode.

    The result is the ORPHAcode and preferred term of the clinical entity with a data set or each classification where the clinical entity is present (set includes: unique identifier of the classification, name of the classification, ORPHAcode and name of the n+1 clinical entity). # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param orphacode: The ORPHAcode is a unique identifier to reference an Orphanet&#x27;s concept
    :type orphacode: int

    :rtype: Classification
    """
    return 'do some magic!'


def list_orpha_by_classification(lang, hchid):  # noqa: E501
    """Search for the list of clinical entities&#x27; ORPHAcodes in one specific classification by the unique identifer of the classification.

    The result is a data set including ORPHAcode, status, preferred term and definition of all clinical entities. # noqa: E501

    :param lang: Desired language
    :type lang: str
    :param hchid: The hierarchy ID (hchID) is a number which refers to an Orphanet classification
    :type hchid: int

    :rtype: EntitiesByClassification
    """
    return 'do some magic!'
