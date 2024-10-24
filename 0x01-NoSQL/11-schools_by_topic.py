#!/usr/bin/env python3
""" Python function that returns the list of schools having a specific topic """

def schools_by_topic(mongo_collection, topic):
    """ 
    Retrieve a list of schools that offer a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection object.
        topic (str): The topic to search for.

    Returns:
        list: A list of school documents matching the topic.
    """
    return list(mongo_collection.find({"topics": topic}))
