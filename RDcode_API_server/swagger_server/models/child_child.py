# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class ChildChild(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, child_orph_acode: int=None, child_preferred_term: str=None):  # noqa: E501
        """ChildChild - a model defined in Swagger

        :param child_orph_acode: The child_orph_acode of this ChildChild.  # noqa: E501
        :type child_orph_acode: int
        :param child_preferred_term: The child_preferred_term of this ChildChild.  # noqa: E501
        :type child_preferred_term: str
        """
        self.swagger_types = {
            'child_orph_acode': int,
            'child_preferred_term': str
        }

        self.attribute_map = {
            'child_orph_acode': 'Child ORPHAcode',
            'child_preferred_term': 'Child preferred term'
        }
        self._child_orph_acode = child_orph_acode
        self._child_preferred_term = child_preferred_term

    @classmethod
    def from_dict(cls, dikt) -> 'ChildChild':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Child_Child of this ChildChild.  # noqa: E501
        :rtype: ChildChild
        """
        return util.deserialize_model(dikt, cls)

    @property
    def child_orph_acode(self) -> int:
        """Gets the child_orph_acode of this ChildChild.


        :return: The child_orph_acode of this ChildChild.
        :rtype: int
        """
        return self._child_orph_acode

    @child_orph_acode.setter
    def child_orph_acode(self, child_orph_acode: int):
        """Sets the child_orph_acode of this ChildChild.


        :param child_orph_acode: The child_orph_acode of this ChildChild.
        :type child_orph_acode: int
        """

        self._child_orph_acode = child_orph_acode

    @property
    def child_preferred_term(self) -> str:
        """Gets the child_preferred_term of this ChildChild.


        :return: The child_preferred_term of this ChildChild.
        :rtype: str
        """
        return self._child_preferred_term

    @child_preferred_term.setter
    def child_preferred_term(self, child_preferred_term: str):
        """Sets the child_preferred_term of this ChildChild.


        :param child_preferred_term: The child_preferred_term of this ChildChild.
        :type child_preferred_term: str
        """

        self._child_preferred_term = child_preferred_term
