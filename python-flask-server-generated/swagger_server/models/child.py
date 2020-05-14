# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.child_child import ChildChild  # noqa: F401,E501
from swagger_server.models.parent_classification import ParentClassification  # noqa: F401,E501
from swagger_server import util


class Child(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, orph_acode: int=None, preferred_term: str=None, classification: ParentClassification=None, child: List[ChildChild]=None):  # noqa: E501
        """Child - a model defined in Swagger

        :param orph_acode: The orph_acode of this Child.  # noqa: E501
        :type orph_acode: int
        :param preferred_term: The preferred_term of this Child.  # noqa: E501
        :type preferred_term: str
        :param classification: The classification of this Child.  # noqa: E501
        :type classification: ParentClassification
        :param child: The child of this Child.  # noqa: E501
        :type child: List[ChildChild]
        """
        self.swagger_types = {
            'orph_acode': int,
            'preferred_term': str,
            'classification': ParentClassification,
            'child': List[ChildChild]
        }

        self.attribute_map = {
            'orph_acode': 'ORPHAcode',
            'preferred_term': 'Preferred term',
            'classification': 'Classification',
            'child': 'Child'
        }
        self._orph_acode = orph_acode
        self._preferred_term = preferred_term
        self._classification = classification
        self._child = child

    @classmethod
    def from_dict(cls, dikt) -> 'Child':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Child of this Child.  # noqa: E501
        :rtype: Child
        """
        return util.deserialize_model(dikt, cls)

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this Child.


        :return: The orph_acode of this Child.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this Child.


        :param orph_acode: The orph_acode of this Child.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def preferred_term(self) -> str:
        """Gets the preferred_term of this Child.


        :return: The preferred_term of this Child.
        :rtype: str
        """
        return self._preferred_term

    @preferred_term.setter
    def preferred_term(self, preferred_term: str):
        """Sets the preferred_term of this Child.


        :param preferred_term: The preferred_term of this Child.
        :type preferred_term: str
        """

        self._preferred_term = preferred_term

    @property
    def classification(self) -> ParentClassification:
        """Gets the classification of this Child.


        :return: The classification of this Child.
        :rtype: ParentClassification
        """
        return self._classification

    @classification.setter
    def classification(self, classification: ParentClassification):
        """Sets the classification of this Child.


        :param classification: The classification of this Child.
        :type classification: ParentClassification
        """

        self._classification = classification

    @property
    def child(self) -> List[ChildChild]:
        """Gets the child of this Child.


        :return: The child of this Child.
        :rtype: List[ChildChild]
        """
        return self._child

    @child.setter
    def child(self, child: List[ChildChild]):
        """Sets the child of this Child.


        :param child: The child of this Child.
        :type child: List[ChildChild]
        """

        self._child = child
