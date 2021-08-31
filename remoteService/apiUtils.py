import flask
from flask import Flask, jsonify, request
import os
import requests
import json
import ast

class apiResults(object):
    def __init__(self):
        self.response_dict = {}
        self.entities_dict = {}
        self.fetchRoute = "https://internmatch-staging2.gada.io/qwanda/baseentitys/fetch25"
        self.attributeRoute = "https://internmatch-staging2.gada.io/qwanda/baseentitys/"
# init class object
api = apiResults()

# init app
app = Flask(__name__)

# set endpoints
@app.route('/api/response', methods=['POST'])
def get_response():
    headers = dict(request.headers)

    data = request.get_data().decode('utf8')
    data = data.replace("\n", "")
    data = data.replace(" ", "")

    api.response_dict["searchBE"] = data
    api.response_dict["headers"] = headers

    return(f"SEARCH BASE ENTITY RECEIVED")

@app.route('/api/look', methods=['GET'])
def get_look():
    return(f"SEARCH BASE ENTITY: \n{api.response_dict['searchBE']}\n \nAUTH TOKEN: \n{api.response_dict['headers']['Authorization']}")

@app.route('/api/sendSearch', methods=['GET'])
def get_search():
    searchBE = api.response_dict["searchBE"]
    authToken = api.response_dict["headers"]["Authorization"]
    headers = {'Content-Type': 'application/json',\
                'Accept': 'application/json',\
                'Authorization': authToken}

    try:
        result = requests.post(api.fetchRoute,\
                                headers=headers,\
                                data=searchBE).json()

        api.entities_dict = result
    except:
        api.entities_dict = {}

    return(api.entities_dict)

# @app.route('/api/runRemoteService', methods=['POST'])
# def run_service():
