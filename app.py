import flask
from flask import Flask, jsonify, request
import os
import requests
import json

# init app
app = Flask(__name__)

response_dict = {}
apiRoute = "https://internmatch-staging2.gada.io/qwanda/baseentitys/search25/"

@app.route('/api/response', methods=['POST'])
def get_response():
    headers = dict(request.headers)

    data = request.get_data().decode('utf8')
    data = data.replace("\n", "")
    data = data.replace(" ", "")

    response_dict["searchBE"] = data
    response_dict["headers"] = headers

    return(f"Response: \n{response_dict}")

@app.route('/api/look', methods=['GET'])
def get_look():
    return(f"SEARCH BASE ENTITY: \n{response_dict['searchBE']}\n \nAUTH TOKEN: \n{response_dict['headers']['Authorization']}")

@app.route('/api/sendSearch', methods=['GET'])
def get_search():
    ### this is the search25 part
    searchBE = response_dict["searchBE"]
    authToken = response_dict["headers"]["Authorization"]
    headers = {'Content-Type': 'application/json',\
                'Accept': 'application/json',\
                'Authorization': authToken}
    result = requests.post(apiRoute,\
                            headers=headers,\
                            data=searchBE)
    return(result.json())

# This bit of code runs the actual app
# Run server
if __name__ == "__main__":
    app.run(debug=True)
