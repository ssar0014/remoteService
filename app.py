import flask
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask_marshmallow import Marshmallow
import os
import datetime
from datetime import datetime
import pickle
import matplotlib
import matplotlib.pyplot as plt, mpld3

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# init database
# currently local database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
# add this to remove warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialze SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
marsh = Marshmallow(app)

# Build a class/model for our responses stored in our db
class Response(db.Model):
    # define the db schema
    id = db.Column(db.Integer, primary_key=True) # auto_increment is True by default
    job_id = db.Column(db.String(80), unique = True, nullable=False)
    service_name = db.Column(db.String(80), unique = True, nullable=False)
    service_start_datetime = db.Column(db.DateTime(), nullable=False)
    service_end_datetime = db.Column(db.DateTime(), nullable=False)
    service_results = db.Column(db.JSON, nullable=False)

    # constructor
    def __init__(self, job_id, service_name, service_start_datetime, service_end_datetime,\
                    service_results):
                    self.job_id = job_id
                    self.service_name = service_name
                    self.service_start_datetime = service_start_datetime
                    self.service_end_datetime = service_end_datetime
                    self.service_results = service_results


# response schema
class ResponseSchema(marsh.Schema):
    class Meta:
        fields = ('job_id', 'service_name', 'service_start_datetime', 'service_end_datetime',\
                    'service_results')
# init schema
responseSchema = ResponseSchema()
multiResponseSchema = ResponseSchema(many=True)

# get some dummy data and push it to the database,
# then create a route to check the database entry. this will also be used as a means to
# fetch results stored in the database
pickleData = pickle.load(open(os.path.join(basedir,'data.pkl'),'rb'))
jsonPickleData = mpld3.fig_to_dict(pickleData)
dummy_data = {  'job_id':'RMS_009',\
                'service_name':'Remote Job 9',\
                'service_start_datetime':datetime.now(),\
                'service_end_datetime':datetime.now(),\
                'service_results': jsonPickleData
            }

# create routes
@app.route('/response', methods=['GET'])
def get_response():
    db_entry = Response(dummy_data['job_id'],\
                        dummy_data['service_name'],\
                        dummy_data['service_start_datetime'],\
                        dummy_data['service_end_datetime'],\
                        dummy_data['service_results'])

    db.session.add(db_entry)
    db.session.commit()
    response = Response.query.all()
    response = multiResponseSchema.dump(response)
    return(jsonify(response))

# This bit of code runs the actual app
# Run server
if __name__ == "__main__":
    app.run(debug=True)
