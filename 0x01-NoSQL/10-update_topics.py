#!/usr/bin/env python3

"""
function that changes all topics of a school document based on the name:
"""


def update_topics(mongo_collection, name, topics):
    """
    Updates the 'topics' field of all documents in the collection where
        the 'name' matches the given name.
    Args:
        mongo_collection: The pymongo collection object.
        name (str): The name of the school to update.
        topics (list): The new list of topics to set for the matching
            documents.

    Returns:
        The result of the update operation.
    """

    if mongo_collection is None:
        return None

    result = mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
            )
    return result
