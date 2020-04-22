# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Type(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, type: str=None):  # noqa: E501
        """Type - a model defined in Swagger

        :param _date: The _date of this Type.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this Type.  # noqa: E501
        :type orph_acode: int
        :param type: The type of this Type.  # noqa: E501
        :type type: str
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'type': str
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'type': 'Type'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._type = type

    @classmethod
    def from_dict(cls, dikt) -> 'Type':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Type of this Type.  # noqa: E501
        :rtype: Type
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this Type.


        :return: The _date of this Type.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this Type.


        :param _date: The _date of this Type.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this Type.


        :return: The orph_acode of this Type.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this Type.


        :param orph_acode: The orph_acode of this Type.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def type(self) -> str:
        """Gets the type of this Type.


        :return: The type of this Type.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Type.


        :param type: The type of this Type.
        :type type: str
        """
        allowed_values = ["biological anomaly", "clinical subtype", "clinical syndrome", "disease", "etiological subtype", "Clinical group", "histopathological subtype", "malformation syndrome", "morphological anomaly", "particular clinical situation in a disease or syndrome", "Category"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type
