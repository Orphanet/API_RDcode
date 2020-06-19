# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Typology(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, typology: str=None):  # noqa: E501
        """Typology - a model defined in Swagger

        :param _date: The _date of this Typology.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this Typology.  # noqa: E501
        :type orph_acode: int
        :param typology: The typology of this Typology.  # noqa: E501
        :type typology: str
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'typology': str
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'typology': 'Typology'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._typology = typology

    @classmethod
    def from_dict(cls, dikt) -> 'Typology':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Typology of this Typology.  # noqa: E501
        :rtype: Typology
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this Typology.


        :return: The _date of this Typology.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this Typology.


        :param _date: The _date of this Typology.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this Typology.


        :return: The orph_acode of this Typology.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this Typology.


        :param orph_acode: The orph_acode of this Typology.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def typology(self) -> str:
        """Gets the typology of this Typology.


        :return: The typology of this Typology.
        :rtype: str
        """
        return self._typology

    @typology.setter
    def typology(self, typology: str):
        """Sets the typology of this Typology.


        :param typology: The typology of this Typology.
        :type typology: str
        """
        allowed_values = ["biological anomaly", "clinical subtype", "clinical syndrome", "disease", "etiological subtype", "Clinical group", "histopathological subtype", "malformation syndrome", "morphological anomaly", "particular clinical situation in a disease or syndrome", "Category"]  # noqa: E501
        if typology not in allowed_values:
            raise ValueError(
                "Invalid value for `typology` ({0}), must be one of {1}"
                .format(typology, allowed_values)
            )

        self._typology = typology
