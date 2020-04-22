# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class TargetEntity(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, status: str=None, relation: str=None, target_orph_acode: int=None):  # noqa: E501
        """TargetEntity - a model defined in Swagger

        :param _date: The _date of this TargetEntity.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this TargetEntity.  # noqa: E501
        :type orph_acode: int
        :param status: The status of this TargetEntity.  # noqa: E501
        :type status: str
        :param relation: The relation of this TargetEntity.  # noqa: E501
        :type relation: str
        :param target_orph_acode: The target_orph_acode of this TargetEntity.  # noqa: E501
        :type target_orph_acode: int
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'status': str,
            'relation': str,
            'target_orph_acode': int
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'status': 'Status',
            'relation': 'Relation',
            'target_orph_acode': 'Target ORPHAcode'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._status = status
        self._relation = relation
        self._target_orph_acode = target_orph_acode

    @classmethod
    def from_dict(cls, dikt) -> 'TargetEntity':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TargetEntity of this TargetEntity.  # noqa: E501
        :rtype: TargetEntity
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this TargetEntity.


        :return: The _date of this TargetEntity.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this TargetEntity.


        :param _date: The _date of this TargetEntity.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this TargetEntity.


        :return: The orph_acode of this TargetEntity.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this TargetEntity.


        :param orph_acode: The orph_acode of this TargetEntity.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def status(self) -> str:
        """Gets the status of this TargetEntity.


        :return: The status of this TargetEntity.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this TargetEntity.


        :param status: The status of this TargetEntity.
        :type status: str
        """
        allowed_values = ["Active", "Active_Historical entity", "Inactive_Deprecated entity", "Inactive_Obsolete entity", "Inactive_Non Rare disease in Europe"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def relation(self) -> str:
        """Gets the relation of this TargetEntity.


        :return: The relation of this TargetEntity.
        :rtype: str
        """
        return self._relation

    @relation.setter
    def relation(self, relation: str):
        """Sets the relation of this TargetEntity.


        :param relation: The relation of this TargetEntity.
        :type relation: str
        """
        allowed_values = ["referred to", "Moved to"]  # noqa: E501
        if relation not in allowed_values:
            raise ValueError(
                "Invalid value for `relation` ({0}), must be one of {1}"
                .format(relation, allowed_values)
            )

        self._relation = relation

    @property
    def target_orph_acode(self) -> int:
        """Gets the target_orph_acode of this TargetEntity.


        :return: The target_orph_acode of this TargetEntity.
        :rtype: int
        """
        return self._target_orph_acode

    @target_orph_acode.setter
    def target_orph_acode(self, target_orph_acode: int):
        """Sets the target_orph_acode of this TargetEntity.


        :param target_orph_acode: The target_orph_acode of this TargetEntity.
        :type target_orph_acode: int
        """

        self._target_orph_acode = target_orph_acode