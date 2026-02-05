docker_version = "1.0.0.24.691"

#Version 1.0.0.26

print("Re Start:", docker_version)

# ---------------------------------------------------------------------------------
# Main.py FASTAPI
# uvicorn main_fastapi:app --reload --host 0.0.0.0
# http://52.220.146.33:8000/dev/rest/vhpGL/getChartOfAccount
# {
#     "request": {
#       "caseType": 4,
#         "int1": 0,
#         "int2": 0,
#         "char1": " ",
#         "char2": " ",
#       "inputUserkey": "17779884C63E6D9E166B59B9B4E5F8D0025A0772",
#       "inputUsername": "sindata",
#       "hotelcode": "vhpweb"
#     }
# }
# Set User di pgadmin 
# CREATE USER qcserverless WITH PASSWORD 'qc2024';
# CREATE USER username WITH PASSWORD 'your_password';
# GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA your_schema TO username;
# ---------------------------------------------------------------------------------

#  Setup Localhost FastAPI
# - install python
# - install pip Environment (https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/)
# - create env -> 
# - python -m venv env
# - create folder dimana main.py akan dijalankan
# - copy requirements.txt
# - pip install -r requirements.txt
# edit config.json, bila perlu untuk mengarahkan DB
# jalankan:uvicorn main:app --reload --host 0.0.0.0

# Function URL
# https://vtrifvn3snaofpvkn3ym47sz6i0mmjwz.lambda-url.ap-southeast-1.on.aws/
# 
# contoh pemakaian Function URL
# https://vtrifvn3snaofpvkn3ym47sz6i0mmjwz.lambda-url.ap-southeast-1.on.aws/dev/vhpSM/taNationstatGoList
#
# ---------------------------------------------------------------------------------

# """
# import sys
# sys.path.append("/opt/python/lib/python3.9/site-packages/")
# """
import os, sys,importlib, csv, json, datetime, platform, inspect, re, ast
from urllib.parse import urlparse
from pprint import pprint
import watchtower, logging, traceback
from functions.additional_functions import *
# from functions.check_userkeybl import *
from decimal import Decimal
import asyncio
from models.base import get_database_session
from contextlib import asynccontextmanager
from pathlib import Path

# from flask import Flask, request, abort, Response
# from flask_cors import CORS
from fastapi import FastAPI, Response, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from typing import Dict, Any

import typing
from dotenv import load_dotenv
from _demo_config import * 
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mangum import Mangum

from models.guestbook import Guestbook
from functions import log_program as lp

load_dotenv()


IS_DEV = os.getenv("APP_ENV", "prod").lower() != "prod"

MODULE_CACHE = {}
FUNCTION_CACHE = {}
SERVICE_MAP_CACHE = {}

ANDROID_MODULE_CACHE = {}
ANDROID_FUNCTION_CACHE = {}
ANDROID_SERVICE_MAP_CACHE = {}

log_agent = vhp_module = service_name = hotel_code = inputUsername = orig_infostr = existing_json_data = ""
is_existing_json = False

request_headers = {"Content-Type": "application/json"}

response_headers = {
    "Access-Control-Allow-Origin": "*", 
    "Access-Control-Allow-Methods": "OPTIONS, GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "600",  # Preflight request cache time
}

#------------ Log Table -------------------------------------
db_session = None
dblogin_session = None
url = URL.create(
    "postgresql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME")
)
log_engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=log_engine)
dblog_session = SessionLocal()
local_storage.dblog_session = dblog_session

log_id = 0

skip_list = {   "Common/checkPermission2",
                "Common/getHTParam0", 
                "Common/readHtparam",
                "Common/checkTime",
                "Common/checkPermission", 
                "Common/loadDateTimeServer1",
                "Common/checkStrongPassword"}

# ----------------- log activity -----------------------------#
def log_activity(endpoint:string, userid:string, hotel_schema:string) -> int:
    global dblog_session

    if endpoint in skip_list:
        return 0
    
    recid = 0
    try:
        sql = """
            INSERT INTO public.logs_endpoint (endpoint, userid, hotel_schema) 
            VALUES (:endpoint, :userid, :hotel_schema) RETURNING id
            """
        # print("Logging activity:", sql)
        log_results = dblog_session.execute(text(sql), {
                    "endpoint": endpoint,
                    "userid": userid,
                    "hotel_schema": hotel_schema
                })
        dblog_session.commit()
        dblog_session.close()
        recid = log_results.scalar()
        # print("Logged activity with recid:", recid)
    except Exception as e:
        print("Error logging activity:", e)
        recid = 0
    finally:
        return recid

def log_activity_end(log_id: int, error_message: str) -> int:
    global dblog_session

    if log_id <= 0:
        return 0

    try:
        sql = """
            UPDATE public.logs_endpoint SET time_end = NOW(), error_message = :error_message WHERE id = :log_id
            """
        log_results = dblog_session.execute(text(sql), {
                    "log_id": log_id,
                    "error_message": error_message
                })
        dblog_session.commit()
        
    except Exception as e:
        print("Error ending activity log:", e)
    finally:
        dblog_session.close()
        dblog_session.close()
        log_engine.dispose()

    return log_id

#------------------ end of log session ------------------#

#updated 1.0.0.14
update_field_mapping = {}
update_table_name_list = {}
update_field_table_name_mapping = {}
update_field_by_function_mapping = {}

mtime_update_field_mapping = 0
mtime_update_table_name_list = 0
mtime_update_field_table_name_mapping = 0
mtime_update_field_by_function_mapping = 0

path_update_field_mapping = "/usr1/serverless/src/additional_files/global_mapping.json"
path_update_table_name_list = "/usr1/serverless/src/additional_files/update_table_name_mapping.json"
path_update_field_table_name_mapping = "/usr1/serverless/src/additional_files/update_field_table_name_mapping.json"
path_update_field_by_function_mapping = "/usr1/serverless/src/additional_files/update_field_by_function_mapping.json"

curr_module = ""
curr_service = ""

def update_table_name(module, function_name, prev_table_name, updated_table_name):
    global update_table_name_list
    #updated 1.0.0.20

    if module + "_" + function_name not in update_table_name_list:
        update_table_name_list[module + "_" + function_name] = {}
    update_table_name_list[module + "_" + function_name][prev_table_name] = updated_table_name


def update_field_table_name(module, function_name, table_name, prev_field_name, updated_field_name):
    check_str = f"{module}_{function_name}"

    if check_str not in update_field_table_name_mapping:
        update_field_table_name_mapping[check_str] = {}

    if table_name not in update_field_table_name_mapping[check_str]:
        update_field_table_name_mapping[check_str][table_name] = {}

    update_field_table_name_mapping[check_str][table_name][prev_field_name] = updated_field_name

def update_field_by_function(module, function_name, old_field, updated_field_name):
    check_str = f"{module}_{function_name}"

    if check_str not in update_field_by_function_mapping:
        update_field_by_function_mapping[check_str] = {}

    update_field_by_function_mapping[check_str][old_field] = updated_field_name 
    

#updated 1.0.0.6

def get_function_version(module_name, function_name, file_path):
    # file_path  = "/var/task/functions/" + function_name + ".py"
    # file_path  = "/usr1/serverless/src/functions/" + function_name + ".py"
    file_path = file_path + function_name + ".py"
    
    print("File Path:", file_path)
    try:
        file_timestamp = os.path.getmtime(file_path)
        formatted_timestamp = datetime.fromtimestamp(file_timestamp).strftime('%Y-%m-%d %H:%M')
        
        # Open the Python file and read the first line
        with open(file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            
            # Check if the first line matches the version pattern
            match = re.match(r"#using conversion tools version:\s*(\S+)", first_line)
            if match:
                return match.group(1) + " (" + formatted_timestamp + ")"
            else:
                print(f"No version information found in the file {file_path}")
                return  + "None (" + formatted_timestamp + ")" 
    except Exception as e:
        print(f"Error reading the file {file_path}: {e}")
        return None
    finally:
        file.close()


def json_serializer(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float (or use str(obj) if needed)
    if isinstance(obj, datetime.date):
        return obj.isoformat()  # Convert date to string
    raise TypeError(f"Type {type(obj)} not serializable")


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, date):
            return obj.isoformat()
        elif type(obj) == timedelta:
            return obj.days
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def update_input_format_v1(obj,input_data):
    # Update the input object if variable has "-"
    # Update date data from string into data                                      
    param_list = parameter_and_inner_types(obj)
    param_name_list = []
    lower_param_names = [param.lower() for param in list(input_data.keys())]

    for param_name,param_data_type in param_list.items():
        param_name_list.append(param_name)

        if not param_name in input_data:

            if camelCase(param_name) in input_data:
                input_data[param_name] = input_data[camelCase(param_name)]
                input_data.pop(camelCase(param_name))
            elif param_name in lower_param_names:
                curr_input_param_name = ""
                for input_param_name in input_data.keys():
                    if input_param_name.lower() == param_name:
                        curr_input_param_name = input_param_name
                        break

                input_data[param_name] = input_data[curr_input_param_name]
                input_data.pop(curr_input_param_name)

            elif isinstance(param_data_type, list):
                #updated 1.0.0.21
                outer_input_param_name = camelCase(param_name.removesuffix("_data"))
                inner_input_param_name = param_name.removesuffix("_data").replace("_","-")
                # outer_input_param_name = camelCase(param_name.removesuffix("_list"))
                # inner_input_param_name = param_name.removesuffix("_list").replace("_","-")

                tmp_input_data = input_data

                #updated 1.0.0.4
                if not outer_input_param_name in input_data:
                    for field_name in input_data:
                        if outer_input_param_name.lower() == field_name.lower():
                            outer_input_param_name = field_name
                            break

                if outer_input_param_name in input_data:
                    if not inner_input_param_name in input_data[outer_input_param_name]:
                        for field_name in input_data[outer_input_param_name]:
                            if inner_input_param_name.lower() == field_name.lower():
                                input_data[outer_input_param_name][inner_input_param_name] = input_data[outer_input_param_name][field_name]
                                input_data[outer_input_param_name].pop(field_name)
                                break

                    if inner_input_param_name in input_data[outer_input_param_name]:
                        input_data[param_name] = input_data[outer_input_param_name][inner_input_param_name]
                        input_data.pop(outer_input_param_name)

                # if outer_input_param_name in input_data:
                #     input_data[param_name] = input_data[outer_input_param_name][inner_input_param_name]
                #     input_data.pop(outer_input_param_name)
                # else:
                #     #updated 1.0.0.3
                #     outer_input_param_name = outer_input_param_name[0].upper() + outer_input_param_name[1:]
                #     inner_input_param_name = inner_input_param_name[0].upper() + inner_input_param_name[1:]

                #     if outer_input_param_name in input_data:
                #         input_data[param_name] = input_data[outer_input_param_name][inner_input_param_name]
                #         input_data.pop(outer_input_param_name)

        if not param_name in input_data:
            if not isinstance(param_data_type, list) :
                if param_data_type == bool:
                    input_data[param_name] = False
                elif param_data_type == str:
                    input_data[param_name] = ""
                elif param_data_type == int:
                    input_data[param_name] = 0
                elif param_data_type == float:
                    input_data[param_name] = 0.0
            #updated 1.0.0.19
                # elif param_data_type == decimal:
                elif param_data_type == Decimal:
                    input_data[param_name] = 0.0
                else:
                    input_data[param_name] = None
                

        input_value = input_data[param_name]

        if param_data_type == date:
            input_data[param_name] = get_date_input(input_value)
        elif param_data_type == bool and type(input_value) == str:
            input_data[param_name] = convert_to_bool(input_value)
        elif param_data_type == int and type(input_value) == str:
            input_data[param_name] = convert_to_int(input_value.strip(" "))
        elif param_data_type == str and type(input_value) == int:
            input_data[param_name] = to_string(input_value)
        #updated 1.0.0.1
        #updated 1.0.0.19
        # elif param_data_type == decimal:
        elif param_data_type == Decimal:
            input_data[param_name] = to_decimal(input_value)

        elif isinstance(param_data_type, list):
            if param_data_type[0] == bool:  
                for i in range(len(input_data[param_name])):
                    input_data[param_name][i] =  convert_to_bool(input_data[param_name][i])
            elif param_data_type[0] == date:
                for i in range(len(input_data[param_name])):
                    input_data[param_name][i] =  get_date_input(input_data[param_name][i])
                    # input_data[param_name][i] =  ExtendedDate.from_date(get_date_input(input_data[param_name][i]))
            elif param_data_type[0] == int:
                for i in range(len(input_data[param_name])):
                    input_data[param_name][i] =  convert_to_int(input_data[param_name][i])


            #updated 1.0.0.1
            #updated 1.0.0.19
            # elif not type(param_data_type[0]) in {int, decimal, float, complex, str, list, tuple, range, dict, set, 
            #                                       frozenset, bool, bytes, bytearray, memoryview, type(None)} and \
            #     not param_data_type[0] in {int, decimal, float, complex, str, list, tuple, range, dict, set, 
            #                                       frozenset, bool, bytes, bytearray, memoryview, type(None)}:
            elif not type(param_data_type[0]) in {int,  Decimal, float, complex, str, list, tuple, range, dict, set, frozenset, bool, bytes, bytearray, memoryview, type(None)} \
            and not param_data_type[0] in {int, Decimal, float, complex, str, list, tuple, range, dict, set, frozenset, bool, bytes, bytearray, memoryview, type(None)}:
                                                    
                data_list = input_data[param_name]

                if not isinstance(data_list,list):
                    input_data[param_name] = [data_list]
                    data_list = input_data[param_name] 

                all_keys_from_input = list(
                    {key.replace("_", "-") for d in data_list for key in d.keys()}
                )

                
                if len(data_list) > 0:
                    fieldNameList = []
                    boolFormatList = []
                    dateFormatList = []

                    #updated 1.0.0.10
                    bytesFormatList = []
                    
                    
                    check_recid = False

                    for field in fields(param_data_type[0]):

                        if field.name == "_recid":
                            check_recid = True
                        else:
                            if field.type == date:
                                dateFormatList.append(field.name)
                            elif field.type == bool:
                                boolFormatList.append(field.name)
                            #updated 1.0.0.10
                            elif field.type == bytes:
                                bytesFormatList.append(field.name)           


                            # updated 1.0.0.5
                            if not field.name in all_keys_from_input:
                                if field.name.replace("_","-") in all_keys_from_input:
                                    fieldNameList.append(field.name)
                                else:
                                    for field_name in all_keys_from_input:
                                        if field.name == field_name.lower():
                                            fieldNameList.append(field_name)
                                            break

                            # if (not field.name in data_list[0] and 
                            #         # field.name.replace("_","-") in data_list):
                            #         field.name.replace("_","-") in data_list[0]):
                            #     fieldNameList.append(field.name)
                    if check_recid or len(fieldNameList) > 0 or len(dateFormatList) > 0 or len(boolFormatList) > 0:
                        for data in data_list:
                            if check_recid:
                                if data.get("_recid") == 0 or not "_recid" in data:
                                    data["_recid"] = None

                            for name in fieldNameList:

                                #updated 1.0.0.5
                                data_field_name = name.replace("_","-")
                                    
                                if data_field_name in data.keys():
                                    data[name.lower()] = data[data_field_name]
                                    data.pop(data_field_name)
                            
                            for name in dateFormatList:
                                # data[name] = get_date_temp_table(data[name])
                                data[name] = get_date_temp_table(data.get(name))

                            for name in boolFormatList:
                                data[name] = convert_to_bool(data.get(name))
                                # data[name] = convert_to_bool(data[name])

                            #updated 1.0.0.10
                            for name in bytesFormatList:
                                data[name] = base64.b64decode(data.get(name))
                
                    ignore_key_list = []
                    param_key_list = [field.name for field in fields(param_data_type[0])]
                    for key in all_keys_from_input:
                        if (not key in param_key_list):
                            ignore_key_list.append(key)

                    for i in range(0,len(data_list)):
                        for key in ignore_key_list:
                            if key in data_list[i].keys():                            
                                data_list[i].pop(key)

                        data_list[i] = param_data_type[0](**data_list[i])

    input_data_keys = list(input_data.keys())

    for input_param_name in input_data_keys:
        if not input_param_name in param_name_list:
            input_data.pop(input_param_name)


    # for param_name in input_data.keys():
    #     if not param_name in param_list(obj)

# Oscar - enchance speed
def update_input_format(obj, input_data):
    param_list = parameter_and_inner_types(obj)
    param_name_list = list(param_list.keys())

    lower_key_map = {k.lower(): k for k in input_data}

    for param_name, param_data_type in param_list.items():
        param_lower = param_name.lower()
        param_camel = camelCase(param_name)

        # Normalize parameter name
        if param_name not in input_data:
            if param_camel in input_data:
                input_data[param_name] = input_data.pop(param_camel)

            elif param_lower in lower_key_map:
                real_key = lower_key_map[param_lower]
                input_data[param_name] = input_data.pop(real_key)

            elif isinstance(param_data_type, list):
                outer_name = camelCase(param_name.removesuffix("_data"))
                inner_name = param_name.removesuffix("_data").replace("_", "-")

                outer_key = lower_key_map.get(outer_name.lower())
                if outer_key and isinstance(input_data.get(outer_key), dict):
                    inner_map = {
                        k.lower(): k for k in input_data[outer_key]
                    }
                    if inner_name.lower() in inner_map:
                        real_inner = inner_map[inner_name.lower()]
                        input_data[param_name] = input_data[outer_key].pop(real_inner)
                        input_data.pop(outer_key)

        # Default values
        if param_name not in input_data:
            if isinstance(param_data_type, list):
                input_data[param_name] = []
            elif param_data_type == bool:
                input_data[param_name] = False
            elif param_data_type == str:
                input_data[param_name] = ""
            elif param_data_type == int:
                input_data[param_name] = 0
            elif param_data_type in (float, Decimal):
                input_data[param_name] = 0.0
            else:
                input_data[param_name] = None

        value = input_data[param_name]

        # Primitive conversions
        if param_data_type == date:
            input_data[param_name] = get_date_input(value)

        elif param_data_type == bool and isinstance(value, str):
            input_data[param_name] = convert_to_bool(value)

        elif param_data_type == int and isinstance(value, str):
            input_data[param_name] = convert_to_int(value.strip())

        elif param_data_type == str and isinstance(value, int):
            input_data[param_name] = str(value)

        elif param_data_type == Decimal:
            input_data[param_name] = to_decimal(value)

        # List handling
        elif isinstance(param_data_type, list):
            inner_type = param_data_type[0]

            if not isinstance(value, list):
                value = [value]

            # Primitive list types
            if inner_type in (bool, int, date):
                for i, v in enumerate(value):
                    if inner_type == bool:
                        value[i] = convert_to_bool(v)
                    elif inner_type == int:
                        value[i] = convert_to_int(v)
                    elif inner_type == date:
                        value[i] = get_date_input(v)

            # Complex dataclass list
            elif hasattr(inner_type, "__dataclass_fields__"):
                field_defs = fields(inner_type)
                field_names = {f.name for f in field_defs}

                date_fields = {f.name for f in field_defs if f.type == date}
                bool_fields = {f.name for f in field_defs if f.type == bool}
                bytes_fields = {f.name for f in field_defs if f.type == bytes}
                has_recid = "_recid" in field_names

                normalized_list = []

                for item in value:
                    normalized = {}

                    for k, v in item.items():
                        key = k.replace("-", "_").lower()
                        if key in field_names:
                            normalized[key] = v

                    if has_recid and not normalized.get("_recid"):
                        normalized["_recid"] = None

                    for k in date_fields:
                        normalized[k] = get_date_temp_table(normalized.get(k))

                    for k in bool_fields:
                        normalized[k] = convert_to_bool(normalized.get(k))

                    for k in bytes_fields:
                        if normalized.get(k):
                            normalized[k] = base64.b64decode(normalized[k])

                    normalized_list.append(inner_type(**normalized))

                input_data[param_name] = normalized_list

    # Remove unknown parameters
    for key in list(input_data.keys()):
        if key not in param_name_list:
            input_data.pop(key)


def update_output_format_v1(output_data):
    key_list = list(output_data.keys())

    for key in key_list:
        #updated 1.0.0.11
        if re.match(r".*__.*",key):
            updated_key = key.replace("__","")
            output_data[updated_key] = output_data.pop(key)
            key = updated_key

        camelCaseKey = camelCase(key)


        if type(output_data[key]) == list and len(output_data[key]) == 0:
            output_data[camelCaseKey] = {}
            output_data[camelCaseKey][key] = []

            #updated 1.0.0.13
            if camelCaseKey != key:
                output_data.pop(key)            


        elif type(output_data[key]) == list and len(output_data[key]) > 0:


            if type(output_data[key][0]) == date:
                for i in range(len(output_data[key])):
                    output_data[key][i] = create_output_date(output_data[key][i])
                
            elif not type(output_data[key][0]) in {int, float, complex, str, list, tuple, range, dict, set, frozenset, bool, bytes, bytearray, memoryview, type(None)}:
                fieldNameList = []
                dateFormatList = []
                dateArrayFormatList = []

                #updated 1.0.0.10
                bytesFormatList = []
                
                #updated 1.0.0.12
                output_data[camelCaseKey] = {key: output_data[key]}

                if camelCaseKey != key:
                    output_data.pop(key)            

                # Create List of fields, which needs to be updated and formatted
                data_list = output_data[camelCaseKey][key]

                if len(data_list) > 0:
                    if(type(data_list[0]) != dict):
                                                
                        for i in range(len(data_list)):
                            tmp_data = {}
                            for field in [field.name for field in fields(data_list[i])]:
                                tmp_data[field] = getattr(data_list[i], field)

                            data_list[i] = tmp_data
                            # data_list[i] = vars(data_list[i])

                    for field_name in data_list[0]:
                        if (type(data_list[0][field_name]) == list and 
                            type(data_list[0][field_name][0]) == date):
                            dateArrayFormatList.append(field_name)
                        elif type(data_list[0][field_name]) == date:
                            dateFormatList.append(field_name)
                            #updated 1.0.0.10
                        elif type(data_list[0][field_name]) == bytes:
                            bytesFormatList.append(field_name)

                        if field_name != "_recid" and "_" in field_name :
                            fieldNameList.append(field_name)
                        #updated 1.0.0.6
                        elif field_name in update_field_mapping.keys():
                            fieldNameList.append(field_name)

                    if (len(fieldNameList) > 0 or 
                        len(dateFormatList) > 0 or 
                        len(dateArrayFormatList) > 0 or

                        #updated 1.0.0.10
                        len(bytesFormatList) > 0):


                        for data in data_list:
                            for dateFormatField in dateFormatList:
                                if data[dateFormatField] != None:
                                    data[dateFormatField] = set_date_temp_table(data[dateFormatField])
                            for dateFormatField in dateArrayFormatList:
                                for i in range(len(data[dateFormatField])):
                                    if data[dateFormatField][i] != None:
                                        data[dateFormatField][i] = set_date_temp_table(data[dateFormatField][i])
                            
                            #updated 1.0.0.10
                            for bytesFormatField in bytesFormatList:
                                if data[bytesFormatField] != None:
                                    data[bytesFormatField] = base64_encode(data[bytesFormatField])

                            #updated 1.0.0.15
                            for updateFieldName in fieldNameList:
                                if updateFieldName in update_field_mapping.keys():

                                    #updated 1.0.0.22
                                    if type(update_field_mapping[updateFieldName]) == list:
                                        for i in range(0,len(update_field_mapping[updateFieldName])):
                                            data[update_field_mapping[updateFieldName][i]] = data[updateFieldName]
                                    else:                                            
                                        data[update_field_mapping[updateFieldName]] = data[updateFieldName]
                                    # data[update_field_mapping[updateFieldName]] = data[updateFieldName]

                                else:
                                    new_field_name = updateFieldName.replace("_","-").replace("--","_")

                                    #updated 1.0.0.23
                                    if new_field_name in update_field_mapping:
                                        new_field_name = update_field_mapping[new_field_name]
                                        data[new_field_name] = data[updateFieldName]
                                        data[new_field_name.lower()] = data.pop(updateFieldName)
                                    # data[new_field_name] = data.pop(updateFieldName)

                                    #updated 1.0.0.24
                                    elif new_field_name != updateFieldName:
                                            data[new_field_name.lower()] =  data.pop(updateFieldName)
                            # #updated 1.0.0.2
                            # for updateFieldName in fieldNameList:
                            #     if updateFieldName == "yield_":
                            #         data[(updateFieldName.replace("_",""))] = data.pop(updateFieldName)
                            #     #updated 1.0.0.6
                            #     elif updateFieldName in update_field_mapping.keys():
                            #         data[update_field_mapping[updateFieldName]] = data[updateFieldName]
                            #     else:
                            #         #updated 1.0.0.15
                            #         data[(updateFieldName.replace("_","-").replace("--","_"))] = data.pop(updateFieldName)
                            #         # data[(updateFieldName.replace("_","-"))] = data.pop(updateFieldName)
 
            #updated 1.0.0.7
            if key != camelCaseKey and key in list(output_data.keys()):                
                output_data[camelCaseKey] = output_data[key]
                output_data.pop(key)

        else:
            if type(output_data[key]) == date and output_data[key] != None:
                output_data[key] = output_data[key].strftime('%Y-%m-%d')
            elif type(output_data[key]) == bool:
                if output_data[key]:
                    output_data[key] = "true"
                elif output_data[key] == False:
                    output_data[key] = "false"
                else:
                    output_data[key] = None
                

            if camelCaseKey != key:
                output_data[camelCaseKey] = output_data.pop(key)
                key = camelCaseKey

            #updated 1.0.0.6
            if key in update_field_mapping.keys():

                #updated 1.0.0.26
                if type(update_field_mapping[key]) == list:
                    for field_name in update_field_mapping[key]:
                            output_data[field_name] = output_data[key]
                else:
                    output_data[update_field_mapping[key]] = output_data[key]


        #updated 1.0.0.14
        curr_module_function = curr_module + "_" + curr_service
        
        if curr_module_function in update_table_name_list and camelCaseKey in update_table_name_list[curr_module_function]:
            output_data[update_table_name_list[curr_module_function][camelCaseKey]] = output_data[camelCaseKey]
            output_data.pop(camelCaseKey)

# Oscar - enchance speed
def update_output_format(output_data):
    curr_module_function = f"{curr_module}_{curr_service}"

    table_name_map = update_table_name_list.get(curr_module_function, {})
    field_table_map = update_field_table_name_mapping.get(curr_module_function, {})
    field_func_map = update_field_by_function_mapping.get(curr_module_function, {})

    primitive_types = (
        int, float, complex, str, list, tuple, range,
        dict, set, frozenset, bool, bytes,
        bytearray, memoryview, type(None)
    )

    for original_key in list(output_data.keys()):
        key = original_key

        if "__" in key:
            new_key = key.replace("__", "")
            output_data[new_key] = output_data.pop(key)
            key = new_key

        camel_key = camelCase(key)
        value = output_data[key]

        # LIST HANDLING
        if isinstance(value, list):

            # empty list
            if not value:
                output_data[camel_key] = {key: []}
                if camel_key != key:
                    output_data.pop(key)
                continue

            first_item = value[0]

            # list of dates
            if isinstance(first_item, date):
                for i in range(len(value)):
                    value[i] = create_output_date(value[i])

            # list of objects / dict-like
            elif not isinstance(first_item, primitive_types):

                output_data[camel_key] = {key: value}
                if camel_key != key:
                    output_data.pop(key)

                data_list = output_data[camel_key][key]

                # convert dataclass objects → dict
                if data_list and not isinstance(data_list[0], dict):
                    for i, obj in enumerate(data_list):
                        data_list[i] = {
                            f.name: getattr(obj, f.name)
                            for f in fields(obj)
                        }

                field_name_list = []
                date_fields = []
                date_array_fields = []
                bytes_fields = []

                sample = data_list[0]

                for field_name, field_value in sample.items():
                    if isinstance(field_value, list) and field_value and isinstance(field_value[0], date):
                        date_array_fields.append(field_name)
                    elif isinstance(field_value, date):
                        date_fields.append(field_name)
                    elif isinstance(field_value, bytes):
                        bytes_fields.append(field_name)

                    if (
                        (field_name != "_recid" and "_" in field_name) 
                        or ((key in field_table_map) and (field_name in field_table_map[key]))
                        or (field_name in update_field_mapping)
                    ):
                        field_name_list.append(field_name)

                if field_name_list or date_fields or date_array_fields or bytes_fields:
                    for row in data_list:

                        for f in date_fields:
                            if row[f] is not None:
                                row[f] = set_date_temp_table(row[f])

                        for f in date_array_fields:
                            for i in range(len(row[f])):
                                if row[f][i] is not None:
                                    row[f][i] = set_date_temp_table(row[f][i])

                        for f in bytes_fields:
                            if row[f] is not None:
                                row[f] = base64_encode(row[f])

                        for old_field in field_name_list:
                            if (
                                key in field_table_map and
                                old_field in field_table_map[key]
                            ):
                                if type(field_table_map[key][old_field]) == list:
                                    for n in field_table_map[key][old_field]:
                                        row[n] = row[old_field]

                                    if old_field not in field_table_map[key][old_field]:
                                        row.pop(old_field)

                                else:
                                    row[field_table_map[key][old_field]] = row[old_field]

                                    if field_table_map[key][old_field] != old_field:
                                        row.pop(old_field)

                                # new_field = old_field.replace("_", "-").replace("--", "_").lower()
                                # row[new_field] = row.pop(old_field)

                            elif old_field in update_field_mapping:
                                if type(update_field_mapping[old_field]) == list:
                                    for n in update_field_mapping[old_field]:
                                        row[n] = row[old_field]

                                    if old_field not in update_field_mapping[old_field]:
                                        row.pop(old_field)

                                else:
                                    row[update_field_mapping[old_field]] = row[old_field]

                                    if update_field_mapping[old_field] != old_field :
                                        row.pop(old_field)

                                # new_field = old_field.replace("_", "-").replace("--", "_").lower()
                                # row[new_field] = row.pop(old_field)

                            else:
                                new_field = old_field.replace("_", "-").replace("--", "_").lower()
                                row[new_field] = row[old_field]

                                if new_field != old_field:
                                    row.pop(old_field)

            # final camelCase key normalization
            if key != camel_key and key in output_data:
                output_data[camel_key] = output_data.pop(key)

        # NON-LIST HANDLING
        else:
            if isinstance(value, date):
                output_data[key] = value.strftime('%Y-%m-%d')

            elif isinstance(value, bool):
                output_data[key] = "true" if value else "false"

            if key in field_func_map:
                if type(field_func_map[key]) == list:
                    for n in field_func_map[key]:
                        output_data[n] = output_data[key]

                    if key not in field_func_map[key]:
                        output_data.pop(key)

                else:
                    output_data[field_func_map[key]] = output_data[key]

                    if field_func_map[key] != key:
                        output_data.pop(key)


            elif key in update_field_mapping:
                if type(update_field_mapping[key]) == list:
                    for n in update_field_mapping[key]:
                        output_data[n] = output_data[key]

                    if key not in update_field_mapping[key]:
                        output_data.pop(key)
                else:
                    output_data[update_field_mapping[key]] = output_data[key]

                    if update_field_mapping[key] != key:
                        output_data.pop(key)

            else:
                output_data[camel_key] = output_data[key]

                if camel_key != key:
                    output_data.pop(key)

        # TABLE NAME UPDATE
        if camel_key in table_name_map:
            output_data[table_name_map[camel_key]] = output_data.pop(camel_key)


def decimal_converter(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # or str(obj) if needed
    return obj


def save_output_to_blob(session, json_data, ui_request_id, orig_infostr):
    record = session.query(Guestbook).filter_by(infostr=ui_request_id).first()
    if record:
        # record.json_data = json.dumps(json_data, indent=4)
        # record.imagefile = json.dumps(json_data, indent=4, default=json_serializer)
        # record.json_data = json.dumps(json_data, default=decimal_converter)
        record.imagefile = json.dumps(json_data, default=decimal_converter).encode("utf-8")
        record.orig_infostr = orig_infostr 
        if "|" in record.userinit:
            first, _ = record.userinit.split("|", 1)  # Keep only the first entry
            record.userinit = f"{first}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            record.userinit = f"{record.userinit}|{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        session.flush()  # Ensure changes are applied before commit
        session.commit()
        return "Updated successfully"
    else:
        return "Record not found"

"""
def lambda_handler(event, lambda_context):
    path = event.get("path")
    request = event.get("body")
"""

app = FastAPI()
handler = Mangum(app)
origins = ["*"]


log_debugging = ""
# print("3:", docker_version)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# print("4:", docker_version)
input_data = {}
templates = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    from functions.main_dashboard import main_dashboard
    query_params = dict(request.query_params)
    context = main_dashboard(query_params)
    context["request"] = request  # required for TemplateResponse
    return templates.TemplateResponse("dashboard.html", context)


@app.get("/{path_param:path}")
async def handle_get(request: Request):
    body_byte = await request.body()
    body_str = body_byte.decode("utf-8")

    input_data = {}
    if body_str:
        input_data = json.loads(body_str)
    
    return handle_get_post(request, input_data, body_str)

@app.post("/{path_param:path}")
async def handle_post(request: Request, input_data: Dict[str, Any] = {}):
    body_byte = await request.body()
    body_str = body_byte.decode("utf-8")

    reload_mapping()
    
    return handle_get_post(request, input_data, body_str)

def handle_get_post(request: Request, input_data: Dict[str, Any] = {}, body_str:str = ""):
    url = str(request.url)
    headers = dict(request.headers)

    # print("Hd:", headers)
    # print("Request:", request)

    if not hasattr(local_storage,"app"):
        local_storage.app = app

    return handle_dynamic_data(url, headers, input_data, body_str)


# Oscar - hot reload mapping without restarting main.py
def reload_mapping():
    global update_field_mapping, update_table_name_list, update_field_table_name_mapping, update_field_by_function_mapping
    global mtime_update_field_mapping, mtime_update_table_name_list, mtime_update_field_table_name_mapping, mtime_update_field_by_function_mapping
    global path_update_field_mapping, path_update_table_name_list, path_update_field_table_name_mapping, path_update_field_by_function_mapping

    exist_update_field_mapping = Path(path_update_field_mapping)
    exist_update_table_name_list = Path(path_update_table_name_list)
    exist_update_field_table_name_mapping = Path(path_update_field_table_name_mapping)
    exist_update_field_by_function_mapping = Path(path_update_field_by_function_mapping)


    if exist_update_field_mapping.exists():
        mtime = os.path.getmtime(path_update_field_mapping)
        if mtime != mtime_update_field_mapping:
            with open(path_update_field_mapping, "r", encoding="utf-8") as f:
                update_field_mapping = json.load(f)
                mtime_update_field_mapping = mtime

    if exist_update_table_name_list.exists():
        mtime = os.path.getmtime(path_update_table_name_list)
        if mtime != mtime_update_table_name_list:
            with open(path_update_table_name_list, "r", encoding="utf-8") as f:
                update_table_name_list = json.load(f)
                mtime_update_table_name_list = mtime

    if exist_update_field_table_name_mapping.exists():
        mtime = os.path.getmtime(path_update_field_table_name_mapping)
        if mtime != mtime_update_field_table_name_mapping:
            with open(path_update_field_table_name_mapping, "r", encoding="utf-8") as f:
                update_field_table_name_mapping = json.load(f)
                mtime_update_field_table_name_mapping = mtime

    if exist_update_field_by_function_mapping.exists():
        mtime = os.path.getmtime(path_update_field_by_function_mapping)
        if mtime != mtime_update_field_by_function_mapping:
            with open(path_update_field_by_function_mapping, "r", encoding="utf-8") as f:
                update_field_by_function_mapping = json.load(f)
                mtime_update_field_by_function_mapping = mtime


def handle_dynamic_data(url:str, headers: Dict[str, Any], input_data: Dict[str, Any] = {}, body_str:str = ""):

    #updated 1.0.0.18
    initialize_local_storage()
    log_agent = output_json_str = error_message = module_name = function_name = vhp_module = service_name = hotel_code = inputUsername = json_dbsize = ""
    X_Forwarded_For = headers.get("X-Forwarded-For") 
    user_agent = headers.get("User-Agent")
    
    version_info = sys.version_info
    version_py = f", Python {version_info.major}.{version_info.minor}.{version_info.micro}"
    app_info = "Docker:" + docker_version + version_py
    lambda_function_name = os.getenv('AWS_LAMBDA_FUNCTION_NAME', 'LOCAL_ENV')
    log_stream_name = os.getenv('AWS_LAMBDA_LOG_STREAM_NAME', 'LOCAL_LOG_STREAM')

    #updated 1.0.0.14
    global curr_module, curr_service
    curr_module = ""
    curr_service = ""
    orig_infostr = ""

    signature = headers.get("x-signature")
    nonce = headers.get("x-nonce")
    timestamp = headers.get("x-timestamp")

    path = str(url).replace("http://","").replace("https://","")
    output_data = {}
    output_data["logStatus"] = "None"
    output_data["error"] = ""
    ok_flag = False

    if not hasattr(local_storage,"app"):
        local_storage.app = app
    output_data_size = 0
    newRequest_recid = 0
    log_id = 0
    ServerInfo = {}
    hotel_schema = inputUsername = function_name = request_id = "" 
    
    local_storage.debugging = log_debugging
    
    # print("5:", docker_version)
    hostname_parts = path.split(".")
    apigw = hostname_parts[0]
    # ------------------------------------------------------
    # Log
    # ------------------------------------------------------
    try:
        lendata = 0           # newlog.id
        ServerInfo["lendata"] = lendata
        ServerInfo["path"] = path
        ServerInfo["version"] = app_info
        if X_Forwarded_For is not None:
            ServerInfo["X_Forwarded_For"] = X_Forwarded_For

        
    except Exception as e:
        error_message = ""
        output_data["error"] = ""
        # response = {"response":output_data}
        print("Error:", error_message)
        response = json.dumps({"response":output_data}, cls=CustomJSONEncoder, separators=(',', ':'))
        return response
    finally:
        
        initialize_local_storage()
        pass
    
    if "request" in input_data:
        input_data = input_data["request"]      

    # if headers_input_data:
    #     for key in headers_input_data:
    #         if to_string(headers_input_data[key]) != headers.get(key.lower()):
    #             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    #         input_data[key] = headers.get(key.lower())

    """ """
    # if timestamp and abs(to_int(timestamp) - int(datetime.now().strftime('%s'))) > 600:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid timestamp")                

    # if not signature:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature")                

    # if not nonce:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Nonce")                

    # if not timestamp:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing timestamp")                

    # if  signature and nonce and timestamp and body_str and signature != sha1_hex(body_str + "|" + nonce + "|" + timestamp):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid value")                
    
    ui_request_id = input_data.get("ui_request_id", "None")
    is_existing_json = False
    inputUsername = input_data.get("inputUsername")
    hotel_schema = input_data.get("hotel_schema").lower() if input_data.get("hotel_schema") else ""
    output_data = {}
    if not hotel_schema:
        hotel_schema = input_data.get("hotel_schema")

    # print("hotel_schema:", hotel_schema, ui_request_id)

    #------------------------ Main Function ------------------------------
    try:
        ok_flag = "False"
        # output_data = {}
    
        if hotel_schema:
            module_mapping = {
                "vhpPOS": "vhpOU"
            }
            vhp_war = entry(1,path,"/")
            vhp_module = entry(2,path,"/")
            if vhp_module in module_mapping:
                vhp_module = module_mapping[vhp_module]

            
            service_name = entry(3,path,"/")

            #updated 1.0.0.14
            curr_module = vhp_module
            curr_service = service_name

            if num_entries(path,"/") == 5:
                service_name += entry(4,path,"/")
            
            print("Schema/Module/Service/War:", hotel_schema, vhp_module, service_name, vhp_war)
            endpoint = vhp_module + "/" + service_name
            log_id = log_activity(endpoint, inputUsername, hotel_schema)

            set_db_and_schema(hotel_schema)
            db_session = local_storage.db_session
            # print("db_session:", db_session)

            try:
                with open('modules/' + vhp_war + '/' + vhp_module + '/_mapping.txt', mode ='r') as file:   
                    mapping_service = csv.DictReader(file)
                    function_name = ""

                    for mapping in mapping_service:
                        if mapping['service'] == service_name:
                            function_name = mapping["function"]
                            break
                    

                    if function_name == "":
                        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                        return JSONResponse(status_code=404, content={"error": f"Function not found, ({vhp_module}/{service_name})" })
                    # check file exists
                    file_name = f"{function_name}.py"
                    file_path = Path("functions") / file_name

                    if file_path.exists():
                        # print(f"File '{file_name}' exists.")
                        pass
                    else:
                        print(f"File '{file_name}' does NOT exist.")
                        return JSONResponse(status_code=404, content={"error": str(f"{file_name} not exists.")})
            except Exception as e:
                print("Error:", e)
                # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                return JSONResponse(status_code=404, content={"error": str(e)})

            finally:
                # db_session.close()
                file.close()

            module_name = "functions." + function_name
            # ok_flag = get_output(check_userkeybl(input_data["inputUsername"], input_data["inputUserkey"]))
            of_flag = True
            version = ""
            if os.environ.get('AWS_EXECUTION_ENV'):
                version = get_function_version(module_name, function_name, "/var/task/functions/")
            else:
                # version = "localhost, " + get_function_version(module_name, function_name, "/usr1/serverless/src/functions/")     
                version = "localhost"
            # print(f"Main.py {function_name} running on: {version}")
            ok_flag = "true"
            local_storage.debugging = f"{local_storage.debugging},Skip OK:{ok_flag}, {function_name} Ver:{version}"
            
            if ok_flag:
                if function_name != 'get_bediener_infobl':
                    input_data.pop("inputUsername")
                input_data.pop("inputUserkey")
                input_data.pop("hotel_schema",None)
                input_data.pop("hotel_schema",None)
                input_data.pop("hotel_schema",None)
                input_data.pop("hotel_schema",None)
                # Check if module and function exists

                # update 1.0.0.24 request_Id
                if ui_request_id != "None":
                    existing_request = db_session.query(Guestbook).filter_by(infostr=ui_request_id).first()
                    if not existing_request: 
                        orig_infostr = "start"
                        local_storage.debugging = local_storage.debugging + ',Start'
                        newRequest = Guestbook()
                        newRequest.cid = "SERVERLESS_BIGRESPONSE"
                        newRequest.userinit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        newRequest.infostr = ui_request_id
                        newRequest.orig_infostr = orig_infostr
                        newRequest.reserve_char[0] = vhp_module + "/" + service_name
                        newRequest.reserve_char[1] = json.dumps(input_data, default=decimal_converter)
                        db_session.add(newRequest)
                        db_session.commit()
                        newRequest_recid = newRequest._recid
                        # print("Start BigResponse:", newRequest.userinit, newRequest_recid)
                    else:
                        if existing_request.orig_infostr == "running":
                            existing_request.zeit = existing_request.zeit + 1
                            db_session.commit()
                            newRequest_recid = existing_request._recid  
                            # json_data = existing_request.json_data
                            orig_infostr = existing_request.orig_infostr  
                            reserve_char_0 = existing_request.reserve_char[0]
                            reserve_char_1 = existing_request.reserve_char[1]
                        if existing_request.orig_infostr == "end":
                            existing_request.zeit = existing_request.zeit + 1
                            db_session.commit()
                            # json_data = existing_request.json_data
                            json_data = existing_request.imagefile.decode('utf-8')
                            orig_infostr = existing_request.orig_infostr 
                            local_storage.debugging = local_storage.debugging + ',Retrieve'
                            # print("Existing JSON:", json_data)
                            # print("Existing JSON:")
                            is_existing_json = True
                            existing_json_data = json_data
                        else: 
                            output_data = {}
                            # output_data["status"] = existing_request.orig_infostr
                            # output_data["zeit"] = str(existing_request.zeit)
                            # output_data["cid"] = existing_request.cid
                else:
                    newRequest_recid = 0
                    orig_infostr = "None"
                    
                
                if orig_infostr=="start" or ui_request_id=="None":
                    existing_request = db_session.query(Guestbook).filter_by(infostr=ui_request_id).first()
                    if existing_request:
                        orig_infostr = "running"
                        newRequest.orig_infostr = "running"
                        local_storage.debugging = local_storage.debugging + ',Run'
                        db_session.commit()
                    if importlib.util.find_spec(module_name):
                        # print("Import Module:", module_name)
                        module = importlib.import_module(module_name)
                        # Rd, just to re-test, develop mode only
                        module = importlib.reload(module)   
                        if hasattr(module, function_name):
                            try:
                                # print("Calling getAttr:", function_name)   
                                obj = getattr(module, function_name)
                                update_input_format(obj,input_data)
                                # print("Start Call:", function_name)  
                                output_data =  obj(**input_data)
                                # print("New Output:", output_data)
                                # print("Got New Output:")
                                orig_infostr = "end"
                                if output_data is None:
                                    output_data = {}
                                    # Rd 23/7/2025
                                    # case: vhpSS/updVHPPrint, no output dari .p, outputOK true
                                    # 
                                    output_data["output_Ok_Flag"] = str(ok_flag)
                                else:
                                    output_data["output_Ok_Flag"] = str(ok_flag)


                            except Exception as e:
                                error_message = traceback.format_exc()
                                # output_data = {} 
                                output_data["error"] = f"Check: {function_name}, Check detail error in ServerInfo below."
                                print("Error:", error_message)
                               
                            finally:
                                # test Rd, 2403015
                                initialize_local_storage()
                                try:
                                    if db_session:
                                        db_session.commit()
                                        close_session()
                                except Exception as e:
                                    pass
                        else:
                            # db_session.close()
                            print("Else Not Found:", module_name)
                            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                    else:
                        # db_session.close()
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            if output_data is None:
                # print(":OutputData:None")
                # output_data = {}
                local_storage.debugging = local_storage.debugging + ',Output:None'
                data_string = ''
            else:
                
                data_string = ''.join(str(value) for value in output_data.values())
                # print("OutputData:", len(data_string))
                # print(data_string)

        # ------------------------------------------------------------------------------
        # Rd, 29/7/2025, outputOfFlag -> remark krn update long process sblmnya
        # output_data["outputOkFlag"] = str(ok_flag)
        # buka remark

        if is_existing_json == False:
            # output_data["output_Ok_Flag"] = str(ok_flag)
            if ui_request_id != "None":
                output_data["orig_infostr"] = "On Process"
            update_output_format(output_data)
            data_string = ''.join(str(value) for value in output_data.values())
        else:
            retrieved_json = json.loads(existing_json_data) 
            output_data = retrieved_json
            print("ExistingData:", len(output_data))
       
        output_data_size = len(data_string)
        ServerInfo["lendata"] = output_data_size

        if ui_request_id != "None" and is_existing_json == False:
            
            # print("Trying to save output:", output_data)
            print("Trying to save output:")
            local_storage.debugging = local_storage.debugging + ',End.'
            status_request_id = save_output_to_blob(db_session, output_data, ui_request_id, orig_infostr)
            print("orig:", orig_infostr, status_request_id)
            db_session.commit()

    except Exception as e:
        # db_session.rollback()
        # error_message = traceback.format_exc()
        # output_data["error"] = f"Check: {function_name}, Check detail error in ServerInfo below."
        # # print("Error:", error_message)
        try:
            if db_session:
                db_session.rollback()
        except Exception as e:
            pass

    finally:
        output_data["outputOkFlag"] = str(ok_flag)
        initialize_local_storage()
        try:
            if db_session:
                close_session()             #db_session.close()
        except Exception as e:
            pass
            # print("Error:", error_message)

    
    x_forwarded_for = headers.get("x-forwarded-for")
    aws_request_id = headers.get("x-amzn-trace-id", "Not Available")
    ServerInfo["x_forwarded_for"] = x_forwarded_for
    ServerInfo["version"] = docker_version
    ServerInfo["Debuging"] = local_storage.debugging
    ServerInfo["error"] = error_message
    ServerInfo["modfunc"] = module_name  + "/" + service_name 
    ServerInfo["ui_request_id"] = ui_request_id
    ServerInfo["newRequest_recid"] = newRequest_recid
    ServerInfo["orig_infostr"] = orig_infostr
    ServerInfo["log_id"] = log_id
    # ServerInfo["aws_request_id"] = aws_request_id    
    # ServerInfo["AWSFunction"] =  lambda_function_name
    # ServerInfo["AWSCloudWatch"] = log_stream_name
    log_activity_end(log_id, error_message)
    return {
        "response": output_data,
        "serverinfo": ServerInfo
    }

    aws_request_id = request.headers.get("X-Amzn-RequestId", "Not Available")
    print("AWS Request ID:", aws_request_id)


# Oscar - enchance speed
# handle_dynamic_data new version for increase speed
# def handle_dynamic_data_v1(url: str, headers: dict, input_data: dict = {}, body_str: str = ""):
#     initialize_local_storage()

#     global curr_module, curr_service

#     output_data = {}
#     ServerInfo = {}
#     db_session = None
#     error_message = ""
#     ok_flag = "false"

#     module_name = ""

#     mobile_version = False


#     def get_service_function(vhp_module: str, service_name: str) -> str:
#         nonlocal mobile_version

#         if mobile_version:
#             if vhp_module not in ANDROID_SERVICE_MAP_CACHE:
#                 mapping_path = Path(f"modules/VHPMobile/{vhp_module}/_mapping.txt")
#                 if not mapping_path.exists():
#                     raise FileNotFoundError(f"Mapping file not found for module {vhp_module}")

#                 with open(mapping_path, "r") as f:
#                     ANDROID_SERVICE_MAP_CACHE[vhp_module] = {
#                         row["service"]: row["function"]
#                         for row in csv.DictReader(f)
#                     }

#             service_map = ANDROID_SERVICE_MAP_CACHE[vhp_module]
#             if service_name not in service_map:
#                 raise KeyError(f"Service not found: {vhp_module}/{service_name}")
#         else:
#             if vhp_module not in SERVICE_MAP_CACHE:
#                 mapping_path = Path(f"modules/VHPWebBased/{vhp_module}/_mapping.txt")
#                 if not mapping_path.exists():
#                     raise FileNotFoundError(f"Mapping file not found for module {vhp_module}")

#                 with open(mapping_path, "r") as f:
#                     SERVICE_MAP_CACHE[vhp_module] = {
#                         row["service"]: row["function"]
#                         for row in csv.DictReader(f)
#                     }

#             service_map = SERVICE_MAP_CACHE[vhp_module]
#             if service_name not in service_map:
#                 raise KeyError(f"Service not found: {vhp_module}/{service_name}")

#         return service_map[service_name]


#     def load_function(function_name: str):
#         nonlocal module_name, mobile_version
        
#         cache_key = f"{module_name}.{function_name}"

#         if not IS_DEV and cache_key in FUNCTION_CACHE:
#             if mobile_version:
#                 return ANDROID_FUNCTION_CACHE[cache_key]
#             else:
#                 return FUNCTION_CACHE[cache_key]

#         if mobile_version:
#             module = ANDROID_MODULE_CACHE.get(module_name)
#         else:
#             module = MODULE_CACHE.get(module_name)

#         if not module or IS_DEV:
#             module = importlib.import_module(module_name)
#             if IS_DEV:
#                 module = importlib.reload(module)

#             if mobile_version:
#                 ANDROID_MODULE_CACHE[module_name] = module
#             else:
#                 MODULE_CACHE[module_name] = module

#         if not hasattr(module, function_name):
#             raise AttributeError(f"Function {function_name} not found in {module_name}")

#         func = getattr(module, function_name)

#         if mobile_version:
#             ANDROID_FUNCTION_CACHE[cache_key] = func
#         else:
#             FUNCTION_CACHE[cache_key] = func
            
#         return func


#     def validate_request(headers: dict, body_str: str):
#         signature = headers.get("x-signature")
#         nonce = headers.get("x-nonce")
#         timestamp = headers.get("x-timestamp")

#         # if not signature:
#         #     raise HTTPException(400, "Missing signature")
#         # if not nonce:
#         #     raise HTTPException(400, "Missing nonce")
#         # if not timestamp:
#         #     raise HTTPException(400, "Missing timestamp")

#         # if abs(to_int(timestamp) - int(datetime.now().timestamp())) > 600:
#         #     raise HTTPException(400, "Invalid timestamp")

#         # if signature != sha1_hex(body_str + "|" + nonce + "|" + timestamp):
#         #     raise HTTPException(400, "Invalid signature")


#     def execute_service_function(
#         vhp_module: str,
#         service_name: str,
#         input_data: dict
#     ):
#         nonlocal module_name, mobile_version

#         function_name = get_service_function(vhp_module, service_name)

#         if mobile_version:
#             module_name = f"functions.vhp_mobile.{function_name}"
#         else:
#             module_name = f"functions.{function_name}"

#         func = load_function(function_name)

#         update_input_format(func, input_data)
#         return func(**input_data)

#     try:        
#         validate_request(headers, body_str)

#         if "request" in input_data:
#             input_data = input_data["request"]

#         hotel_schema = (input_data.get("hotel_schema") or "").lower()
#         if not hotel_schema:
#             raise HTTPException(400, "Missing hotel_schema")

#         # python.staging.e1-vhp.com:10443/dev/vhpINV/getInvSubGroup
#         # -------------------0-------------1-----2---------3-------

#         # ws1.e1-vhp.com:8443/VHPWebBased1/rest/Common/checkPermission2
#         # -----------0-------------1--------2------3--------4----------

#         # ws1.e1-vhp.com:8443/VHPMobile1/rest/FrontOffice/storeSignatureBill
#         # ---------0--------------1-------2--------3-------------4----------

#         path = url.replace("http://", "").replace("https://", "")
#         path_split = path.split("/")

#         if re.match(r'^VHPMobile\d$', path_split[1]):
#             mobile_version = True


#         if mobile_version:
#             vhp_module = entry(3, path, "/")

#             path_list_service = path_split[4:]
#             service_name = "".join(path_list_service)
#         else:
#             vhp_module = entry(2, path, "/")

#             path_list_service = path_split[3:]
#             service_name = "".join(path_list_service)


#         curr_module = vhp_module
#         curr_service = service_name

#         print("Schema/Module/Service:", hotel_schema, vhp_module, service_name)

#         set_db_and_schema(hotel_schema)
#         db_session = local_storage.db_session

#         input_data.pop("hotel_schema", None)
#         input_data.pop("inputUserkey", None)
#         input_data.pop("inputUsername", None)

#         result = execute_service_function(vhp_module, service_name, input_data)

#         output_data = result or {}
#         output_data["output_Ok_Flag"] = "true"
#         ok_flag = "true"

#         update_output_format(output_data)

#         db_session.commit()

#     except Exception as e:
#         error_message = traceback.format_exc()
#         output_data = {"error": "Internal server error"}
#         print(f"Error: {str(e)}")

#         lp.write_log("error", f"{error_message}", "error.txt", "f")

#         if db_session:
#             db_session.rollback()

#     finally:
#         if db_session:
#             close_session()

#         if IS_DEV:
#             ServerInfo["mode"] = "DEV" if IS_DEV else "PROD"
#             ServerInfo["error"] = error_message
#             ServerInfo["modfunc"] = module_name
#             ServerInfo["ok"] = ok_flag
#             ServerInfo["path"] = vhp_module  + "/" + service_name

#             return {
#                 "response": output_data,
#                 "serverinfo": ServerInfo
#             }
        
#         else:
#             return {
#                 "response": output_data
#             }


# infostr -> request Id
# imagefile -> content


# clear_8 = text("""
#                 DELETE FROM res_line WHERE resstatus = 8 AND ankunft != abreise 
#                 """)
# db_session.execute(clear_8, {})

"""
SELECT * FROM test_detail td join test t on (t.id=td.test_id) 
where t.test_datetime::date = '2025-08-01' 
and td.compare_status like '%KeyError%'

LIMIT 100
"""

"""
SELECT vhp_module, endpoint_module,  compare_status FROM test_detail td join test t on (t.id=td.test_id) 
where t.test_datetime::date = '2025-08-01' 
and td.compare_status like '%AttributeError: "NoneType" object has no attribute %'
group by vhp_module, endpoint_module, compare_status
LIMIT 100
"""