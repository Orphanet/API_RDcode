import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orpha_summary import OrphaSummary  # noqa: E501
from swagger_server import util

import config
from controllers.query_controller import *
from controllers.preferential_parent_controller import orpha_parent


def orpha_summary(lang, orphacode):  # noqa: E501
    """Search for a clinical entity general informations.

    The result retrieves the ORPHAcode, preferred term, synonyms, definition, typology, Orphanet URL, status, preferential parent and classification level of the clinical entity. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: OrphaSummary
    """
    
    es = config.elastic_server

    index = "rdcode_orphanomenclature"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"Definition\", \"ORPHAcode\", \"Synonym\", \"Preferred term\", \"Typology\", \"Status\", \"ClassificationLevel\"]}"

    response = single_res(es, index, query)

    url = "http://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=fr&Expert=" + str(orphacode)

    pref_parent = orpha_parent(lang, orphacode)
    if not isinstance(pref_parent, tuple):
        response.update({
            "Orphanet URL": url,
            "Preferential parent": pref_parent["Preferential parent"]
            })

    # return yaml if needed
    response = if_yaml(connexion.request.accept_mimetypes.best, response)
    return response
