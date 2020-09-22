import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orph_acode_aggregation import ORPHAcodeAggregation  # noqa: E501
from swagger_server import util


def list_aggregation(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s aggregation code by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode, its preferred term as well as the ORPHAcode and the preferred term of the aggregation code. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: ORPHAcodeAggregation
    """
    return 'do some magic!'
