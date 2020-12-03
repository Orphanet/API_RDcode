# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class FindbyOMIMReferences(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, orph_acode: int=None, preferred_term: str=None, disorder_mapping_relation: str=None, disorder_mapping_validation_status: str=None):  # noqa: E501
        """FindbyOMIMReferences - a model defined in Swagger

        :param orph_acode: The orph_acode of this FindbyOMIMReferences.  # noqa: E501
        :type orph_acode: int
        :param preferred_term: The preferred_term of this FindbyOMIMReferences.  # noqa: E501
        :type preferred_term: str
        :param disorder_mapping_relation: The disorder_mapping_relation of this FindbyOMIMReferences.  # noqa: E501
        :type disorder_mapping_relation: str
        :param disorder_mapping_validation_status: The disorder_mapping_validation_status of this FindbyOMIMReferences.  # noqa: E501
        :type disorder_mapping_validation_status: str
        """
        self.swagger_types = {
            'orph_acode': int,
            'preferred_term': str,
            'disorder_mapping_relation': str,
            'disorder_mapping_validation_status': str
        }

        self.attribute_map = {
            'orph_acode': 'ORPHAcode',
            'preferred_term': 'Preferred term',
            'disorder_mapping_relation': 'DisorderMappingRelation',
            'disorder_mapping_validation_status': 'DisorderMappingValidationStatus'
        }
        self._orph_acode = orph_acode
        self._preferred_term = preferred_term
        self._disorder_mapping_relation = disorder_mapping_relation
        self._disorder_mapping_validation_status = disorder_mapping_validation_status

    @classmethod
    def from_dict(cls, dikt) -> 'FindbyOMIMReferences':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FindbyOMIM_References of this FindbyOMIMReferences.  # noqa: E501
        :rtype: FindbyOMIMReferences
        """
        return util.deserialize_model(dikt, cls)

    @property
    def orph_acode(self) -> int:
        """Gets the orph_acode of this FindbyOMIMReferences.


        :return: The orph_acode of this FindbyOMIMReferences.
        :rtype: int
        """
        return self._orph_acode

    @orph_acode.setter
    def orph_acode(self, orph_acode: int):
        """Sets the orph_acode of this FindbyOMIMReferences.


        :param orph_acode: The orph_acode of this FindbyOMIMReferences.
        :type orph_acode: int
        """

        self._orph_acode = orph_acode

    @property
    def preferred_term(self) -> str:
        """Gets the preferred_term of this FindbyOMIMReferences.


        :return: The preferred_term of this FindbyOMIMReferences.
        :rtype: str
        """
        return self._preferred_term

    @preferred_term.setter
    def preferred_term(self, preferred_term: str):
        """Sets the preferred_term of this FindbyOMIMReferences.


        :param preferred_term: The preferred_term of this FindbyOMIMReferences.
        :type preferred_term: str
        """

        self._preferred_term = preferred_term

    @property
    def disorder_mapping_relation(self) -> str:
        """Gets the disorder_mapping_relation of this FindbyOMIMReferences.


        :return: The disorder_mapping_relation of this FindbyOMIMReferences.
        :rtype: str
        """
        return self._disorder_mapping_relation

    @disorder_mapping_relation.setter
    def disorder_mapping_relation(self, disorder_mapping_relation: str):
        """Sets the disorder_mapping_relation of this FindbyOMIMReferences.


        :param disorder_mapping_relation: The disorder_mapping_relation of this FindbyOMIMReferences.
        :type disorder_mapping_relation: str
        """
        allowed_values = ["E (Exact mapping: the two concepts are equivalent)", "NTBT (ORPHA code's Narrower Term maps to a Broader Term)", "BTNT (ORPHA code's Broader Term maps to a Narrower Term)", "NTBT/E (ORPHA code's Narrower Term maps to a Broader Term because of an Exact mapping with a synonym in the target terminology)", "BTNT/E", "ND (not yet decided/unable to decide)"]  # noqa: E501
        if disorder_mapping_relation not in allowed_values:
            raise ValueError(
                "Invalid value for `disorder_mapping_relation` ({0}), must be one of {1}"
                .format(disorder_mapping_relation, allowed_values)
            )

        self._disorder_mapping_relation = disorder_mapping_relation

    @property
    def disorder_mapping_validation_status(self) -> str:
        """Gets the disorder_mapping_validation_status of this FindbyOMIMReferences.


        :return: The disorder_mapping_validation_status of this FindbyOMIMReferences.
        :rtype: str
        """
        return self._disorder_mapping_validation_status

    @disorder_mapping_validation_status.setter
    def disorder_mapping_validation_status(self, disorder_mapping_validation_status: str):
        """Sets the disorder_mapping_validation_status of this FindbyOMIMReferences.


        :param disorder_mapping_validation_status: The disorder_mapping_validation_status of this FindbyOMIMReferences.
        :type disorder_mapping_validation_status: str
        """
        allowed_values = ["Validated", "Not yet validated"]  # noqa: E501
        if disorder_mapping_validation_status not in allowed_values:
            raise ValueError(
                "Invalid value for `disorder_mapping_validation_status` ({0}), must be one of {1}"
                .format(disorder_mapping_validation_status, allowed_values)
            )

        self._disorder_mapping_validation_status = disorder_mapping_validation_status
