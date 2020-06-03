# coding: utf-8

from __future__ import absolute_import
from datetime import datetime  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ClinicalEntityInner(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, _date: datetime=None, orph_acode: int=None, status: str=None, preferred_term: str=None, definition: str=None):  # noqa: E501
        """ClinicalEntityInner - a model defined in Swagger

        :param _date: The _date of this ClinicalEntityInner.  # noqa: E501
        :type _date: datetime
        :param orph_acode: The orph_acode of this ClinicalEntityInner.  # noqa: E501
        :type orph_acode: int
        :param status: The status of this ClinicalEntityInner.  # noqa: E501
        :type status: str
        :param preferred_term: The preferred_term of this ClinicalEntityInner.  # noqa: E501
        :type preferred_term: str
        :param definition: The definition of this ClinicalEntityInner.  # noqa: E501
        :type definition: str
        """
        self.swagger_types = {
            '_date': datetime,
            'orph_acode': int,
            'status': str,
            'preferred_term': str,
            'definition': str
        }

        self.attribute_map = {
            '_date': 'Date',
            'orph_acode': 'ORPHAcode',
            'status': 'Status',
            'preferred_term': 'Preferred term',
            'definition': 'Definition'
        }
        self.__date = _date
        self._orph_acode = orph_acode
        self._status = status
        self._preferred_term = preferred_term
        self._definition = definition

    @classmethod
    def from_dict(cls, dikt) -> 'ClinicalEntityInner':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ClinicalEntity_inner of this ClinicalEntityInner.  # noqa: E501
        :rtype: ClinicalEntityInner
        """
        return util.deserialize_model(dikt, cls)

    @property
    def _date(self) -> datetime:
        """Gets the _date of this ClinicalEntityInner.


        :return: The _date of this ClinicalEntityInner.
        :rtype: datetime
        """
        return self.__date

    @_date.setter
    def _date(self, _date: datetime):
        """Sets the _date of this ClinicalEntityInner.


        :param _date: The _date of this ClinicalEntityInner.
        :type _date: datetime
        """

        self.__date = _date

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this ClinicalEntityInner.


        :return: The orph_acode of this ClinicalEntityInner.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this ClinicalEntityInner.


        :param orph_acode: The orph_acode of this ClinicalEntityInner.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def status(self) -> str:
        """Gets the status of this ClinicalEntityInner.


        :return: The status of this ClinicalEntityInner.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status: str):
        """Sets the status of this ClinicalEntityInner.


        :param status: The status of this ClinicalEntityInner.
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
    def preferred_term(self) -> str:
        """Gets the preferred_term of this ClinicalEntityInner.


        :return: The preferred_term of this ClinicalEntityInner.
        :rtype: str
        """
        return self._preferred_term

    @preferred_term.setter
    def preferred_term(self, preferred_term: str):
        """Sets the preferred_term of this ClinicalEntityInner.


        :param preferred_term: The preferred_term of this ClinicalEntityInner.
        :type preferred_term: str
        """

        self._preferred_term = preferred_term

    @property
    def definition(self) -> str:
        """Gets the definition of this ClinicalEntityInner.


        :return: The definition of this ClinicalEntityInner.
        :rtype: str
        """
        return self._definition

    @definition.setter
    def definition(self, definition: str):
        """Sets the definition of this ClinicalEntityInner.


        :param definition: The definition of this ClinicalEntityInner.
        :type definition: str
        """

        self._definition = definition