# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Definition(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, definition: str=None):  # noqa: E501
        """Definition - a model defined in Swagger

        :param _date: The _date of this Definition.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this Definition.  # noqa: E501
        :type orph_acode: int
        :param definition: The definition of this Definition.  # noqa: E501
        :type definition: str
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'definition': str
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'definition': 'Definition'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._definition = definition

    @classmethod
    def from_dict(cls, dikt) -> 'Definition':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Definition of this Definition.  # noqa: E501
        :rtype: Definition
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this Definition.


        :return: The _date of this Definition.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this Definition.


        :param _date: The _date of this Definition.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this Definition.


        :return: The orph_acode of this Definition.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this Definition.


        :param orph_acode: The orph_acode of this Definition.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def definition(self) -> str:
        """Gets the definition of this Definition.


        :return: The definition of this Definition.
        :rtype: str
        """
        return self._definition

    @definition.setter
    def definition(self, definition: str):
        """Sets the definition of this Definition.


        :param definition: The definition of this Definition.
        :type definition: str
        """

        self._definition = definition
