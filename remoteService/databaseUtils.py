import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from datetime import datetime
import json

Base = declarative_base()
class Response(Base):
    __tablename__ = "Response"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    job_id = Column('job_id',String(80), unique = True, nullable=False)
    service_name = Column('service_name',String(80), unique = True, nullable=False)
    service_start_datetime = Column('service_start_datetime',DateTime(), nullable=False)
    service_end_datetime = Column('service_end_datetime',DateTime(), nullable=False)
    service_results = Column('service_results',JSON, nullable=False)

engine = create_engine('sqlite:///response.db', echo=False)
Base.metadata.create_all(bind = engine)

# CRUD functionality
# Create
def add_entry(job_id, name, start, end, results):
    # this stuff will be coming from the API
    # will need to be parsed using a json deserializer
    # for now this is dummy data
    # the results will need to be fetched from a different place
    Session = sessionmaker(bind = engine)
    session = Session()
    response = Response()
    response.job_id = job_id
    response.service_name = name
    response.service_start_datetime = start
    response.service_end_datetime = end
    response.service_results = results
    session.add(response)
    session.commit()
    session.close()

# Read
def read_entry(id):
    Session = sessionmaker(bind = engine)
    session = Session()
    results = session.query(Response).all()
    query_results = None
    for result in results:
        if result.id == id:
            query_results = (result.id, result.job_id, result.service_start_datetime, result.service_name, result.service_results)
            session.close()
            return query_results
    if query_results == None:
        session.close()
        return("ID NOT FOUND")

def read_all():
    Session = sessionmaker(bind = engine)
    session = Session()
    results = session.query(Response).all()
    query_results = None
    response_result = []
    for result in results:
        query_results = (result.id, result.job_id, result.service_name, result.service_results)
        response_result.append(query_results)
    session.close()
    return response_result

# Update
def update_entry(job_id, updated_result):
    Session = sessionmaker(bind = engine)
    session = Session()
    session.query(Response).filter(Response.job_id == job_id).\
                    update({"service_results": (updated_result)})
    session.commit()
    session.close()

# Delete
def delete_entry(job_id):
    Session = sessionmaker(bind = engine)
    session = Session()
    session.query(Response).filter(Response.job_id == job_id).delete()
    session.commit()
    session.close()

def fetch_results(job_id):
    Session = sessionmaker(bind = engine)
    session = Session()
    for u in session.query(Response).filter(Response.job_id == job_id):
        response_dict = u.__dict__
    return(response_dict['service_results'])
    session.close()
