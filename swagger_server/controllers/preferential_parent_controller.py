import connexion
import six

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.orpha_to_children import OrphaToChildren  # noqa: E501
from swagger_server.models.orpha_to_parent import OrphaToParent  # noqa: E501
from swagger_server.models.parent_list import ParentList  # noqa: E501
from swagger_server import util

from swagger_server import config
from swagger_server.controllers.query_controller import *

from swagger_server.controllers.classification_controller import classifications_list

def orpha_parent(lang, orphacode):  # noqa: E501
    """Search for a clinical entity&#x27;s preferential parent by ORPHAcode

    The result retrieves the clinical entity&#x27;s ORPHAcode and its preferential parent. # noqa: E501

    :param lang: Language
    :type lang: str
    :param orphacode: A unique and time-stable numerical identifier attributed randomly by the Orphanet database to each clinical entity upon its creation.
    :type orphacode: int

    :rtype: OrphaToParent
    """

    es = config.elastic_server
    
    index = "rdcode_orphalinearisation"
    index = "{}_{}".format(index, lang.lower())

    query = "{\"query\": {\"match\": {\"ORPHAcode\": " + str(orphacode) + "}}," \
            "\"_source\":[\"Date\", \"ORPHAcode\",\"Preferred term\", \"DisorderDisorderAssociation\"]}"
    
    response = single_res(es, index, query)

    if isinstance(response, str) or isinstance(response, tuple):
        return response
    
    tmp = {
        "ORPHAcode": response["DisorderDisorderAssociation"][0]["TargetDisorder"]["ORPHAcode"],
        "Preferred term": response["DisorderDisorderAssociation"][0]["TargetDisorder"]["Preferred term"]
    }

    new_response = {
        "ORPHAcode": response["ORPHAcode"],
        "Preferred term": response["Preferred term"],
        "Date": response["Date"],
        "Preferential parent": tmp
    }

    return new_response


def parents_list(lang):  # noqa: E501
    """Search for all preferential parents

    The result retrieves all clinical entities being preferential parents. # noqa: E501

    :param lang: Language
    :type lang: str

    :rtype: ParentList
    """
    return [
        {"Preferred term": "Rare cardiac diseases", "ORPHAcode": "97929"},
        {"Preferred term": "Rare developmental defect during embryogenesis", "ORPHAcode": "93890"},
        {"Preferred term": "Rare surgical cardiac disease", "ORPHAcode": "97965"},
        {"Preferred term": "Rare inborn errors of metabolism", "ORPHAcode": "68367"},
        {"Preferred term": "Rare gastroenterological diseases", "ORPHAcode": "97935"},
        {"Preferred term": "Rare genetic diseases", "ORPHAcode": "98053"},
        {"Preferred term": "Rare neurologic diseases", "ORPHAcode": "98006"},
        {"Preferred term": "Rare abdominal surgical diseases", "ORPHAcode": "165711"},
        {"Preferred term": "Rare hepatic diseases", "ORPHAcode": "57146"},
        {"Preferred term": "Rare respiratory diseases", "ORPHAcode": "97955"},
        {"Preferred term": "Rare urogenital diseases", "ORPHAcode": "101433"},
        {"Preferred term": "Rare surgical thoracic diseases", "ORPHAcode": "97962"},
        {"Preferred term": "Rare skin diseases", "ORPHAcode": "89826"},
        {"Preferred term": "Rare renal diseases", "ORPHAcode": "93626"},
        {"Preferred term": "Rare ophthalmic diseases", "ORPHAcode": "97966"},
        {"Preferred term": "Rare endocrine diseases", "ORPHAcode": "97968"},
        {"Preferred term": "Rare hematologic diseases", "ORPHAcode": "97992"},
        {"Preferred term": "Rare immune disease", "ORPHAcode": "98004"},
        {"Preferred term": "Rare systemic or rheumatological disease", "ORPHAcode": "98023"},
        {"Preferred term": "Rare odontologic disease", "ORPHAcode": "98026"},
        {"Preferred term": "Rare circulatory system disease", "ORPHAcode": "98028"},
        {"Preferred term": "Rare bone diseases", "ORPHAcode": "162964"},
        {"Preferred term": "Rare otorhinolaryngologic diseases", "ORPHAcode": "98036"},
        {"Preferred term": "Rare infertility", "ORPHAcode": "98047"},
        {"Preferred term": "Rare neoplastic diseases", "ORPHAcode": "250908"},
        {"Preferred term": "Rare infectious diseases", "ORPHAcode": "68416"},
        {"Preferred term": "Rare disorder due to toxic effects", "ORPHAcode": "108999"},
        {"Preferred term": "Rare gynecologic or obstetric disease", "ORPHAcode": "96344"},
        {"Preferred term": "Rare maxillo-facial surgical disease", "ORPHAcode": "68329"},
        {"Preferred term": "Rare disorder potentially indicated for transplant or complication after transplant", "ORPHAcode": "565779"},
                ]