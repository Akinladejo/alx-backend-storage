#!/usr/bin/env python3
""" Write a Python function that returns all students sorted by average score
"""

def top_students(mongo_collection):
    """ mongo_collection will be the pymongo collection object
        - The top must be ordered
        - The average score must be part of each item
          returns with key = averageScore
    """
    top_st = mongo_collection.aggregate([
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ])

    return list(top_st)

# The following part is only for testing the function
if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    # Sample data
    j_students = [
        { 'name': "John", 'topics': [{ 'title': "Algo", 'score': 10.3 },{ 'title': "C", 'score': 6.2 }, { 'title': "Python", 'score': 12.1 }]},
        { 'name': "Bob", 'topics': [{ 'title': "Algo", 'score': 5.4 },{ 'title': "C", 'score': 4.9 }, { 'title': "Python", 'score': 7.9 }]},
        { 'name': "Sonia", 'topics': [{ 'title': "Algo", 'score': 14.8 },{ 'title': "C", 'score': 8.8 }, { 'title': "Python", 'score': 15.7 }]},
        { 'name': "Amy", 'topics': [{ 'title': "Algo", 'score': 9.1 },{ 'title': "C", 'score': 14.2 }, { 'title': "Python", 'score': 4.8 }]},
        { 'name': "Julia", 'topics': [{ 'title': "Algo", 'score': 10.5 },{ 'title': "C", 'score': 10.2 }, { 'title': "Python", 'score': 10.1 }]}
    ]

    students_collection.delete_many({})  # Clear existing documents in the collection
    students_collection.insert_many(j_students)

    students = students_collection.find()
    for student in students:
        print("[{}] {} - {}".format(student.get('_id'), student.get('name'), student.get('topics')))

    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'), student.get('averageScore')))
