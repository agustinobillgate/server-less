import sys
sys.path.append("/opt/python3.10/site-packages/")

import json
from datetime import datetime
# import psycopg2
from sqlalchemy import  create_engine, Column, Integer, String, JSON, DateTime, Text, func
from sqlalchemy.orm import sessionmaker, declarative_base

import csv, json, datetime
# import watchtower, logging, traceback
from functions.additional_functions import *
from functions.check_userkeybl import *
from decimal import Decimal

from models.base import  Base, engine
from models.base import get_database_session

def demorudy(json_data: json):
    # print("3.LocalStorage.Session", local_storage.db_session)
    input_data = json.loads(json_data)
    print("Ini dalam function")
    # print("LS:", local_storage.db_session)
    output = {"response" : "oooook",
              "total": 999,
              "status": "BERHASIL"}
    print(input_data, output)
    return output