# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.icd10_references import Icd10References  # noqa: F401,E501
from swagger_server import util


class Icd10(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, preferred_term: str=None, references: List[Icd10References]=None):  # noqa: E501
        """Icd10 - a model defined in Swagger

        :param _date: The _date of this Icd10.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this Icd10.  # noqa: E501
        :type orph_acode: int
        :param preferred_term: The preferred_term of this Icd10.  # noqa: E501
        :type preferred_term: str
        :param references: The references of this Icd10.  # noqa: E501
        :type references: List[Icd10References]
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'preferred_term': str,
            'references': List[Icd10References]
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'preferred_term': 'Preferred term',
            'references': 'References'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._preferred_term = preferred_term
        self._references = references

    @classmethod
    def from_dict(cls, dikt) -> 'Icd10':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The icd10 of this Icd10.  # noqa: E501
        :rtype: Icd10
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this Icd10.


        :return: The _date of this Icd10.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this Icd10.


        :param _date: The _date of this Icd10.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this Icd10.


        :return: The orph_acode of this Icd10.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this Icd10.


        :param orph_acode: The orph_acode of this Icd10.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def preferred_term(self) -> str:
        """Gets the preferred_term of this Icd10.


        :return: The preferred_term of this Icd10.
        :rtype: str
        """
        return self._preferred_term

    @preferred_term.setter
    def preferred_term(self, preferred_term: str):
        """Sets the preferred_term of this Icd10.


        :param preferred_term: The preferred_term of this Icd10.
        :type preferred_term: str
        """

        self._preferred_term = preferred_term

    @property
    def references(self) -> List[Icd10References]:
        """Gets the references of this Icd10.


        :return: The references of this Icd10.
        :rtype: List[Icd10References]
        """
        return self._references

    @references.setter
    def references(self, references: List[Icd10References]):
        """Sets the references of this Icd10.


        :param references: The references of this Icd10.
        :type references: List[Icd10References]
        """

        self._references = references
