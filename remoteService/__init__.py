# follows the convention: from file import method

# a method is a function present in file.py python script which does something
# this __init__ file will be present in all sub directories, and will let python
# know that the directory/subdirectory is a module for the package
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
