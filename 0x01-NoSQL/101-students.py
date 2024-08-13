#!/usr/bin/env python3

"""
Python function that returns all students sorted by average score
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.
    
    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.
    Returns:
        list: A list of dictionaries, each containing the student's name, _id, and averageScore,
            sorted by averageScore in descending order.
    """

    averageScore = []

    students = mongo_collection.find()

    for student in students:
        topics = student.get("topics")

        if topics is None or len(topics) == 0:
            continue

        Total = 0

        for topic in topics:
            score = topic.get('score', 0)
            Total += score

        students_Average_Score = Total / len(topics)

        student_result = {
                '_id': str(student.get('_id')),
                'name': student.get('name'),
                'averageScore': students_Average_Score
        }

        averageScore.append(student_result)

    sorted_results = []
    while averageScore:
        max_score = -float('inf')
        max_index = -1

        for i in range(len(averageScore)):
            if averageScore[i]['averageScore'] > max_score:
                max_score = averageScore[i]['averageScore']
                max_index = i

        sorted_results.append(averageScore.pop(max_index))
    return sorted_results
