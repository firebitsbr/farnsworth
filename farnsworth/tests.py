#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests Endpoint
"""

__authors__ = "Kevin Borgolte"
__version__ = "0.0.0"


from . import app, postgres
from flask import request
from utils import jsonify, filter_query


@app.route("/tests")
@jsonify
def tests_status():
    """The ``/tests`` endpoint can be used to check if the API is reachable
    and if it is alive.

    The JSON response looks like::

        [{"id": <numerical id>,
          "ctn_id": <id of the challenge tree node>,
          "job_id": <id of the job that created the test, optional>,
          "type": <type of the job>,
          "data": <test data, base64-encoded>
         }, ...]

    :return: a list of dictionaries as above
    """
    cursor = postgres.cursor()

    filterable_cols = ['id', 'ctn_id', 'job_id']

    cursor.execute(*filter_query("""SELECT id, ctn_id, job_id, type, data
                                      FROM tests""",
                                 filterable_cols, request.args))

    return cursor.fetchall()


@app.route("/tests", methods=["POST"])
@jsonify
def tests_add():
    cursor = postgres.cursor(dictionary=False)

    tests = request.get_json()
    if isinstance(tests, dict):
        tests = [tests]

    cursor.executemany("""INSERT INTO tests (ctn_id, job_id, type, data)
                          VALUES (%(ctn_id)s, %(job_id)s, %(type)s, %(data)s)""",
                       tuple(tests))

    return {"status": "added"}  # FIXME should check if added