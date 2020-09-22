# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class OmimReferences(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, code_omim: int=None, disorder_mapping_relation: str=None, disorder_mapping_validation_status: str=None):  # noqa: E501
        """OmimReferences - a model defined in Swagger

        :param code_omim: The code_omim of this OmimReferences.  # noqa: E501
        :type code_omim: int
        :param disorder_mapping_relation: The disorder_mapping_relation of this OmimReferences.  # noqa: E501
        :type disorder_mapping_relation: str
        :param disorder_mapping_validation_status: The disorder_mapping_validation_status of this OmimReferences.  # noqa: E501
        :type disorder_mapping_validation_status: str
        """
        self.swagger_types = {
            'code_omim': int,
            'disorder_mapping_relation': str,
            'disorder_mapping_validation_status': str
        }

        self.attribute_map = {
            'code_omim': 'Code OMIM',
            'disorder_mapping_relation': 'DisorderMappingRelation',
            'disorder_mapping_validation_status': 'DisorderMappingValidationStatus'
        }
        self._code_omim = code_omim
        self._disorder_mapping_relation = disorder_mapping_relation
        self._disorder_mapping_validation_status = disorder_mapping_validation_status

    @classmethod
    def from_dict(cls, dikt) -> 'OmimReferences':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The omim_References of this OmimReferences.  # noqa: E501
        :rtype: OmimReferences
        """
        return util.deserialize_model(dikt, cls)

    @property
    def code_omim(self) -> int:
        """Gets the code_omim of this OmimReferences.


        :return: The code_omim of this OmimReferences.
        :rtype: int
        """
        return self._code_omim

    @code_omim.setter
    def code_omim(self, code_omim: int):
        """Sets the code_omim of this OmimReferences.


        :param code_omim: The code_omim of this OmimReferences.
        :type code_omim: int
        """

        self._code_omim = code_omim

    @property
    def disorder_mapping_relation(self) -> str:
        """Gets the disorder_mapping_relation of this OmimReferences.


        :return: The disorder_mapping_relation of this OmimReferences.
        :rtype: str
        """
        return self._disorder_mapping_relation

    @disorder_mapping_relation.setter
    def disorder_mapping_relation(self, disorder_mapping_relation: str):
        """Sets the disorder_mapping_relation of this OmimReferences.


        :param disorder_mapping_relation: The disorder_mapping_relation of this OmimReferences.
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
        """Gets the disorder_mapping_validation_status of this OmimReferences.


        :return: The disorder_mapping_validation_status of this OmimReferences.
        :rtype: str
        """
        return self._disorder_mapping_validation_status

    @disorder_mapping_validation_status.setter
    def disorder_mapping_validation_status(self, disorder_mapping_validation_status: str):
        """Sets the disorder_mapping_validation_status of this OmimReferences.


        :param disorder_mapping_validation_status: The disorder_mapping_validation_status of this OmimReferences.
        :type disorder_mapping_validation_status: str
        """
        allowed_values = ["Validated", "Not yet validated"]  # noqa: E501
        if disorder_mapping_validation_status not in allowed_values:
            raise ValueError(
                "Invalid value for `disorder_mapping_validation_status` ({0}), must be one of {1}"
                .format(disorder_mapping_validation_status, allowed_values)
            )

        self._disorder_mapping_validation_status = disorder_mapping_validation_status
