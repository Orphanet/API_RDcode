# coding: utf-8

from __future__ import absolute_import
from datetime import datetime  # noqa: F401

from typing import List  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.classification_classification import ClassificationClassification  # noqa: F401,E501
from swagger_server import util


class Classification(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, preferred_term: str=None, classification: List[ClassificationClassification]=None):  # noqa: E501
        """Classification - a model defined in Swagger

        :param _date: The _date of this Classification.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this Classification.  # noqa: E501
        :type orph_acode: int
        :param preferred_term: The preferred_term of this Classification.  # noqa: E501
        :type preferred_term: str
        :param classification: The classification of this Classification.  # noqa: E501
        :type classification: List[ClassificationClassification]
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'preferred_term': str,
            'classification': List[ClassificationClassification]
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'preferred_term': 'Preferred term',
            'classification': 'Classification'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._preferred_term = preferred_term
        self._classification = classification

    @classmethod
    def from_dict(cls, dikt) -> 'Classification':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Classification of this Classification.  # noqa: E501
        :rtype: Classification
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this Classification.


        :return: The _date of this Classification.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this Classification.


        :param _date: The _date of this Classification.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this Classification.


        :return: The orph_acode of this Classification.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this Classification.


        :param orph_acode: The orph_acode of this Classification.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def preferred_term(self) -> str:
        """Gets the preferred_term of this Classification.


        :return: The preferred_term of this Classification.
        :rtype: str
        """
        return self._preferred_term

    @preferred_term.setter
    def preferred_term(self, preferred_term: str):
        """Sets the preferred_term of this Classification.


        :param preferred_term: The preferred_term of this Classification.
        :type preferred_term: str
        """

        self._preferred_term = preferred_term

    @property
    def classification(self) -> List[ClassificationClassification]:
        """Gets the classification of this Classification.


        :return: The classification of this Classification.
        :rtype: List[ClassificationClassification]
        """
        return self._classification

    @classification.setter
    def classification(self, classification: List[ClassificationClassification]):
        """Sets the classification of this Classification.


        :param classification: The classification of this Classification.
        :type classification: List[ClassificationClassification]
        """

        self._classification = classification
