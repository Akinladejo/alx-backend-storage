#!/usr/bin/env python3
""" Write a Python function that lists all documents in a collection """

def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection): The collection object to list documents from.

    Returns:
        list: A list of all documents in the collection, or an empty list if no documents exist.
    """
    documents = list(mongo_collection.find())
    return documents
