# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class GroupType(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, group_type: str=None):  # noqa: E501
        """GroupType - a model defined in Swagger

        :param _date: The _date of this GroupType.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this GroupType.  # noqa: E501
        :type orph_acode: int
        :param group_type: The group_type of this GroupType.  # noqa: E501
        :type group_type: str
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'group_type': str
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'group_type': 'GroupType'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._group_type = group_type

    @classmethod
    def from_dict(cls, dikt) -> 'GroupType':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The GroupType of this GroupType.  # noqa: E501
        :rtype: GroupType
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this GroupType.


        :return: The _date of this GroupType.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this GroupType.


        :param _date: The _date of this GroupType.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this GroupType.


        :return: The orph_acode of this GroupType.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this GroupType.


        :param orph_acode: The orph_acode of this GroupType.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def group_type(self) -> str:
        """Gets the group_type of this GroupType.


        :return: The group_type of this GroupType.
        :rtype: str
        """
        return self._group_type

    @group_type.setter
    def group_type(self, group_type: str):
        """Sets the group_type of this GroupType.


        :param group_type: The group_type of this GroupType.
        :type group_type: str
        """
        allowed_values = ["Group", "Disorder", "SubType"]  # noqa: E501
        if group_type not in allowed_values:
            raise ValueError(
                "Invalid value for `group_type` ({0}), must be one of {1}"
                .format(group_type, allowed_values)
            )

        self._group_type = group_type