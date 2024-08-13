#!/usr/bin/env python3

"""
Python function that returns the list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Retrieves a list of school documents from the MongoDB collection
        that have a specific topic in their 'topics' field.

    Args:
    mongo_collection: A pymongo collection object representing the
        MongoDB collection to query.
    topic (str): The topic to search for within the 'topics'
        field of the school documents.

    Returns:
    list: A list of dictionaries representing the school documents
        that contain the specified topic in their 'topics' field.
        If no documents match the query or if the collection is None,
            an empty list is returned.
    """
    if mongo_collection is None:
        return None

    result = mongo_collection.find({"topics": topic})
    return list(result)
