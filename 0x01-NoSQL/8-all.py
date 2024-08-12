#!/usr/bin/env python3

""" MongoDB Operations with Python using pymongo """


def list_all(mongo_collection):
    """
    This function lists all documents in a pymongo collection.

    Args:
        mongo_collection: A pymongo collection object.

    Returns:
      A list of dictionaries representing the documents in the collection.
      An empty list if there are no documents in the collection.
  """

    if mongo_collection is None:
        return []
    return list(mongo_collection.find())
