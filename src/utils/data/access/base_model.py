"""
 ****************************************************************************
 Filename:          base_model.py
 _description:      The base model class for storage

 Creation Date:     03/05/2020
 Author:            Dmitry Didenko
                    Alexander Nogikh
                    Alexander Voronov

 Do NOT modify or remove this copyright and confidentiality notice!
 Copyright (c) 2001 - $Date: 2015/01/14 $ Seagate Technology, LLC.
 The code contained herein is CONFIDENTIAL to Seagate Technology, LLC.
 Portions are also trade secret. Any use, duplication, derivation, distribution
 or disclosure of this code, for any reason, not expressly authorized is
 prohibited. All other rights are expressly reserved by Seagate Technology, LLC.
 ****************************************************************************
"""


from schematics.models import Model


PRIMARY_KEY_FIELD = "_id"


class PrimaryKey:

    def __init__(self, model_id=None):
        self._id = model_id or PRIMARY_KEY_FIELD

    def __get__(self, instance, owner):
        if instance is None:
            # It means that this method is called from class itself
            return getattr(owner, self._id)

        return getattr(instance, self._id)

    def __set__(self, instance, value):
        if instance is None:
            raise TypeError("'__set__' method is called when instance is None")
        setattr(instance, self._id, value)


class PrimaryKeyValue:

    def __init__(self, model_id=None):
        self._id = model_id or PRIMARY_KEY_FIELD

    def __get__(self, instance, owner):
        if instance is None:
            primary_key_field = getattr(owner, self._id)
            return getattr(owner, primary_key_field)

        primary_key_field = getattr(instance, self._id)
        return getattr(instance, primary_key_field)

    def __set__(self, instance, value):
        if instance is None:
            raise TypeError("'__set__' method is called when instance is None")

        primary_key_field = getattr(instance, self._id)
        setattr(instance, primary_key_field, value)


class BaseModel(Model):
    """
    Base model
    """

    _id = None  # This field used as Primary key of the Model
    primary_key = PrimaryKey()
    primary_key_val = PrimaryKeyValue()

    # TODO: based on primary key we can define compare operations for BaseModel instances
    # TODO: based on primary key we can define hashing of BaseModel instances
