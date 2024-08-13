#!/usr/bin/env python3

"""
Python function that inserts a new document in a collection based on kwargs:
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in the collection based on kwargs.

    Args:
        mongo_collection: The pymongo collection object.
        kwargs: Key-value pairs representing the document fields and values.

    Returns:
    The ID of the inserted document.
    """
    if mongo_collection is None:
        return None

    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
