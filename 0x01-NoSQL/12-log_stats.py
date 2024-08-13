#!/usr/bin/env python3

"""
Python script that provides some stats about Nginx logs stored in MongoDB
"""


def nginx_logs(db):
    """
    Counts and prints statistics about the Nginx logs in the provided
        MongoDB database.

    Parameters:
    db (pymongo.database.Database): The MongoDB database object.

    Output:
        Prints the total number of logs, counts of each HTTP method,
            and counts of
        logs with method "GET" and path "/status".
    """
    count_logs = db.nginx.count_documents({})

    # db.nginx.find({ method: 'GET', method: 'POST',}).count()
    count_get = db.nginx.count_documents({"method": "GET"})
    count_post = db.nginx.count_documents({"method": "POST"})
    count_put = db.nginx.count_documents({"method": "PUT"})
    count_patch = db.nginx.count_documents({"method": "PATCH"})
    count_delete = db.nginx.count_documents({"method": "DELETE"})

    result2 = db.nginx.count_documents({
        "method": "GET",
        "path": "/status"
        })

    print(count_logs, "logs")
    print("Methods:")
    print("\tmethod GET:", count_get)
    print("\tmethod POST:", count_post)
    print("\tmethod PUT:", count_put)
    print("\tmethod PATCH:", count_patch)
    print("\tmethod DELETE:", count_delete)
    print(result2, "status check")


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_logs(db)
