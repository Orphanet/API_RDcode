import connexion
import six

from swagger_server.models.diff import Diff  # noqa: E501
from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server import util


def diff(orphacode):  # noqa: E501
    """Search for differences on a clinical entity since previous release

    The result retrieves the ORPHAcode&#x27;s corresponding clinical entity with their preferred term, classification level, activity status and a flag indicating if said clinicalm entity has been updated since previous Nomenclature pack release. # noqa: E501

    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: Diff
    """
    return 'do some magic!'
