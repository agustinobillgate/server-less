docker_version = "0.30"
print("Start:", docker_version)
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

# ---------------------------------------------------------------------------------

# """
# import sys
# sys.path.append("/opt/python/lib/python3.9/site-packages/")
# """
import os, sys,importlib, csv, json, datetime, platform
from urllib.parse import urlparse
from pprint import pprint
import watchtower, logging, traceback
from functions.additional_functions import *
from functions.check_userkeybl import *
from decimal import Decimal

# from flask import Flask, request, abort, Response
# from flask_cors import CORS
from fastapi import FastAPI, Response, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from typing import Dict, Any

from _demo_config import * 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mangum import Mangum

from models.htlogs import Htlogs
# print("1:", docker_version)

log_agent = vhp_module = service_name = hotel_code = inputUsername = ""

request_headers = {"Content-Type": "application/json"}

response_headers = {
    "Access-Control-Allow-Origin": "*", 
    "Access-Control-Allow-Methods": "OPTIONS, GET, POST, PUT, DELETE",
    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Max-Age": "600",  # Preflight request cache time
}

# set_db_and_schema("vhp_1")

def generate_response(body):
    return {
            'statusCode': 200,
            'headers': response_headers,
            'body': body
        }

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

def load_config(filename: str) -> dict:
    with open(filename, "r") as file:
        config = json.load(file)
    return config

def update_input_format(obj,input_data):
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
                outer_input_param_name = camelCase(param_name.removesuffix("_list"))
                inner_input_param_name = param_name.removesuffix("_list").replace("_","-")

                if outer_input_param_name in input_data:
                    input_data[param_name] = input_data[outer_input_param_name][inner_input_param_name]
                    input_data.pop(outer_input_param_name)
                    # for i in range(0,len(input_data[param_name])):
                    #     input_data[param_name][i] = param_data_type[0](**input_data[param_name][i])        


        if not param_name in input_data:
            if not isinstance(param_data_type, list):
                if param_data_type == bool:
                    input_data[param_name] = False
                elif param_data_type == str:
                    input_data[param_name] = ""
                elif param_data_type == int:
                    input_data[param_name] = 0
                elif param_data_type == float:
                    input_data[param_name] = 0.0
                elif param_data_type == decimal:
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
        #----- Tambahan, untuk eliminate " "
        elif param_data_type == str and type(input_value) == str:
            input_data[param_name] = input_value.strip()
        elif isinstance(param_data_type, list):
            if param_data_type[0] == bool:  
                for i in range(len(input_data[param_name])):
                    input_data[param_name][i] =  convert_to_bool(input_data[param_name][i])
            elif param_data_type[0] == date:
                for i in range(len(input_data[param_name])):
                    input_data[param_name][i] =  get_date_input(input_data[param_name][i])
            elif param_data_type[0] == int:
                for i in range(len(input_data[param_name])):
                    input_data[param_name][i] =  convert_to_int(input_data[param_name][i])

            elif not type(param_data_type[0]) in {int, float, complex, str, list, tuple, range, dict, set, 
                                                  frozenset, bool, bytes, bytearray, memoryview, type(None)}:
                data_list = input_data[param_name]
                if not isinstance(data_list,list):
                    input_data[param_name] = [data_list]
                    data_list = input_data[param_name]   
                
                if len(data_list) > 0:
                    fieldNameList = []
                    boolFormatList = []
                    dateFormatList = []
                    check_recid = False
                    for field in fields(param_data_type[0]):
                        if field.name == "_recid":
                            check_recid = True

                        if field.type == date:
                            dateFormatList.append(field.name)
                        elif field.type == bool:
                            boolFormatList.append(field.name)                    

                        if (not field.name in data_list[0] and 
                                # field.name.replace("_","-") in data_list):
                                field.name.replace("_","-") in data_list[0]):
                            fieldNameList.append(field.name)

                    if check_recid or len(fieldNameList) > 0 or len(dateFormatList) > 0 or len(boolFormatList) > 0:
                        for data in data_list:
                            if check_recid:
                                if data.get("_recid") == 0 or not "_recid" in data:
                                    data["_recid"] = None

                            for name in fieldNameList:
                                data_field_name = name.replace("_","-")
                                data[name] = data[data_field_name]
                                data.pop(data_field_name)
                            
                            for name in dateFormatList:
                                # data[name] = get_date_temp_table(data[name])
                                data[name] = get_date_temp_table(data.get(name))

                            for name in boolFormatList:
                                data[name] = convert_to_bool(data.get(name))
                                # data[name] = convert_to_bool(data[name])
                
                    ignore_key_list = []
                    param_key_list = [field.name for field in fields(param_data_type[0])]
                    for key in data_list[0].keys():
                        if not key in param_key_list:
                            ignore_key_list.append(key)

                    for i in range(0,len(data_list)):
                        for key in ignore_key_list:                            
                            data_list[i].pop(key)

                        data_list[i] = param_data_type[0](**data_list[i])        

    input_data_keys = list(input_data.keys())

    for input_param_name in input_data_keys:
        if not input_param_name in param_name_list:
            input_data.pop(input_param_name)


    # for param_name in input_data.keys():
    #     if not param_name in param_list(obj)

def update_output_format(output_data):
    key_list = list(output_data.keys())

    for key in key_list:
        camelCaseKey = camelCase(key)
        if type(output_data[key]) == list and len(output_data[key]) > 0:
            if type(output_data[key][0]) == date:
                for i in range(len(output_data[key])):
                    output_data[key][i] = create_output_date(output_data[key][i])
                
            elif not type(output_data[key][0]) in {int, float, complex, str, list, tuple, range, dict, set, frozenset, bool, bytes, bytearray, memoryview, type(None)}:
                fieldNameList = []
                dateFormatList = []
                dateArrayFormatList = []

                output_data[camelCaseKey] = {key: output_data[key]}
                if camelCaseKey != key:
                    output_data.pop(key)            

                # Create List of fields, which needs to be updated and formatted
                data_list = output_data[camelCaseKey][key]

                if len(data_list) > 0:
                    if(type(data_list[0]) != dict):
                        for i in range(len(data_list)):
                            data_list[i] = vars(data_list[i])

                    for field_name in data_list[0]:
                        if (type(data_list[0][field_name]) == list and 
                            type(data_list[0][field_name][0]) == date):
                            dateArrayFormatList.append(field_name)
                        elif type(data_list[0][field_name]) == date:
                            dateFormatList.append(field_name)
                        if "_" in field_name :
                            fieldNameList.append(field_name)

                    if (len(fieldNameList) > 0 or 
                        len(dateFormatList) > 0 or 
                        len(dateArrayFormatList) > 0):
                        for data in data_list:
                            for dateFormatField in dateFormatList:
                                if data[dateFormatField] != None:
                                    data[dateFormatField] = set_date_temp_table(data[dateFormatField])
                            for dateFormatField in dateArrayFormatList:
                                for i in range(len(data[dateFormatField])):
                                    if data[dateFormatField][i] != None:
                                        data[dateFormatField][i] = set_date_temp_table(data[dateFormatField][i])
                            for updateFieldName in fieldNameList:
                                data[(updateFieldName.replace("_","-"))] = data.pop(updateFieldName)
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

app = FastAPI()
handler = Mangum(app)
origins = ["*"]
log_debugging = "Start"
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
@app.get("/{path_param}")
@app.post("/{path_param}")
@app.post("/{path_param:path}")
async def handle_dynamic_data(request: Request, input_data: Dict[str, Any]):
    # print("Request:", request.path_params["path_param"])
    log_agent = output_json_str = error_message = module_name = function_name = vhp_module = service_name = hotel_code = inputUsername = json_dbsize = ""
    client_ip = request.headers.get("X-Forwarded-For")
    amzn_trace_id = request.headers.get("X-Amzn-Trace-Id")
    user_agent = request.headers.get("User-Agent")
    path = str(request.url).replace("http://","").replace("https://","")
    version_info = sys.version_info
    version_py = f", Python {version_info.major}.{version_info.minor}.{version_info.micro}"
    app_info = "Docker:" + docker_version + version_py
    
    if not hasattr(local_storage,"app"):
        local_storage.app = app
    output_data_size = 0
    ServerInfo = {}
    output_data = {}
    output_data["logStatus"] = "None"
    
    hotel_schema_key = "hotel_schema"
    # hotel_schema_key = "hotelcode"
    hotel_schema = ""
    inputUsername = ""
    ok_flag = False
    local_storage.debugging = log_debugging
    
    # print("5:", docker_version)
    hostname_parts = path.split(".")
    apigw = hostname_parts[0]
    # ------------------------------------------------------
    # Log
    # ------------------------------------------------------
    # DB_HOST = "localhost" 
    # DB_NAME = "vhp"
    # DB_USER = "postgres"
    # DB_PASSWORD = "bali2000"
    # ------------------------------------------------------
    # DB_HOST = "52.220.146.33"
    # DB_NAME = "vhp"
    # DB_USER = "postgres"
    # DB_PASSWORD = "VHPLite#2023"
    # ------------------------------------------------------
    # DB_HOST = "vhp-devtest.cjxtrsmbui3n.ap-southeast-1.rds.amazonaws.com"
    # DB_NAME = "vhpdb"
    # DB_USER = "vhpadmin"
    # DB_PASSWORD = "bFdq8QsQoxH1vAvO"
    try:
        config = load_config("config.json")
        use_db = config["use_db"]
        db0_config = config["database"][use_db]
        DB_HOST = db0_config["DB_HOST"]
        DB_NAME = db0_config["DB_NAME"]
        DB_USER = db0_config["DB_USER"]
        DB_PASSWORD = db0_config["DB_PASSWORD"]
        DB_PORT = db0_config["DB_PORT"]

        # ------------------------------------------------------
        # DB_HOST = "db-vhplite.cjjyqihtbwnm.ap-southeast-1.rds.amazonaws.com"
        # DB_NAME = "postgres"
        # DB_USER = "adminvhplite23"
        # DB_PASSWORD = "superlite#rds"
        # ------------------------------------------------------
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print("UseDB:", use_db)
        log_engine = create_engine(DATABASE_URL)
        log_Session = sessionmaker(bind=log_engine)

        dblog_session = log_Session()
        print("DBSession:", dblog_session)
        newlog = Htlogs()
        newlog.timestart = datetime.now()
        newlog.apigateway = apigw
        newlog.ip = client_ip
        newlog.endpoint = path
        newlog.awsreqid = amzn_trace_id
        newlog.useragent = user_agent
        
        newlog.serverinfo = os.environ['AWS_LAMBDA_FUNCTION_NAME'] + "|" + module_name + ", Docker:" + docker_version
        newlog.param1 = json.dumps(input_data)
        newlog.log = os.environ['AWS_LAMBDA_FUNCTION_NAME'] 
        dblog_session.add(newlog)
        dblog_session.commit()
        logid = newlog.id
        ServerInfo["logid"] = logid
        ServerInfo["path"] = path
        ServerInfo["version"] = app_info
        ServerInfo["ipclient"] = client_ip
        ServerInfo["useragent"] = user_agent

        dblog_session.close()
    except Exception as e:
        # Log the error to database
        error_message = traceback.format_exc()
        output_data["error"] = "Check DB Config, Check ServerInfo below."
        # response = {"response":output_data}
        print("Error:", error_message)
        response = json.dumps({"response":output_data}, cls=CustomJSONEncoder, separators=(',', ':'))
        return response
    finally:
        pass
    
    if "request" in input_data:
        input_data = input_data["request"]      

    inputUsername = input_data.get("inputUsername")
    debug = input_data.get("debug", "")
    print("LogId/Debug:", logid, debug)
    if debug == "1":
        print("InputData:", input_data)
        print ("Log/Path/Request:", newlog.id, path)

    hotel_schema = input_data.get(hotel_schema_key)
    if not hotel_schema:
        hotel_schema = input_data.get(hotel_schema_key)

    #------------------------ Main Function ------------------------------
    try:
        ok_flag = "False"
        output_data = {}
        if hotel_schema:
            vhp_module = entry(2,path,"/")
            service_name = entry(3,path,"/")
            if debug == "1":
                print("Module/Service:", vhp_module, service_name)

            set_db_and_schema(hotel_schema)
            db_session = local_storage.db_session
            
            # folder_path = 'modules/' + vhp_module
            # # Get a list of all files in the folder
            # file_list = os.listdir(folder_path)

            # Print the full paths of the files
            # print("Files in the folder:")
            # for file_name in file_list:
            #     file_path = os.path.join(folder_path, file_name)
            #     print(file_path)

            with open('modules/' + vhp_module + '/_mapping.txt', mode ='r') as file:   
                mapping_service = csv.DictReader(file)
                function_name = ""

                for mapping in mapping_service:
                    # print(mapping)
                    if mapping['service'] == service_name:
                        function_name = mapping["function"]
                        break
                
                if function_name == "":
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            module_name = "functions." + function_name
            if debug == "1":
                print("Module/Function:", module_name)
            #TODO: create a list of program which does not need to check userkey

            ok_flag = get_output(check_userkeybl(input_data["inputUsername"], input_data["inputUserkey"]))
            local_storage.debugging = local_storage.debugging + ",OK:" + str(ok_flag)
            ok_flag = "true"
            if ok_flag:
                if function_name != 'get_bediener_infobl':
                    input_data.pop("inputUsername")
                input_data.pop("inputUserkey")
                input_data.pop(hotel_schema_key,None)
                input_data.pop(hotel_schema_key,None)
                input_data.pop(hotel_schema_key,None)
                input_data.pop(hotel_schema_key,None)
                # print("InputData:")
                # pprint(input_data)
                # Check if module and function exists
                if importlib.util.find_spec(module_name):
                    module = importlib.import_module(module_name)
                    if hasattr(module, function_name):
                        obj = getattr(module, function_name)
                        update_input_format(obj,input_data)
                        output_data =  obj(**input_data)
                    else:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

            db_session.commit()
            db_session.close()
            # print("Output:", output_data)
            if output_data is None:
                print("OutputData:None")
                local_storage.debugging = local_storage.debugging + ',Output:None'
                data_string = ''
            else:
                print("OutputData:NotNone")
                data_string = ''.join(str(value) for value in output_data.values())
            output_data_size = len(data_string)

        # ------------------------------------------------------------------------------
        print("Output:", output_data_size)
        # output_data["htlcode"] = hotel_code
        # output_data["inputUsername"] = inputUsername
        output_data["output_Ok_Flag"] = str(ok_flag)
        update_output_format(output_data)
        data_string = ''.join(str(value) for value in output_data.values())
        output_data_size = len(data_string)
        log = dblog_session.query(Htlogs).filter(Htlogs.id==logid).first()
        if log:
            log.htl_code = hotel_schema
            log.userid = inputUsername
            timeend = datetime.now()
            log.endpoint = vhp_module + "/" + service_name 
            log.lendata = output_data_size  
            log.log = os.environ['AWS_LAMBDA_FUNCTION_NAME'] +  "|" + module_name
            log.serverinfo = "CloudWatch:" + os.environ['AWS_LAMBDA_LOG_STREAM_NAME'] + "|" + "Docker:" + docker_version
            log.timestamp = timeend
            dblog_session.commit()
            dblog_session.close()
        
        # response = JSONResponse(
        #                 content= {"response": output_data}, 
        #                 status_code=200, 
        #                 headers=response_headers
        #             )
        # response = {"response":output_data}
        
        # return response
        # update_output_format(output_data)
        
    except Exception as e:
        # Log the error to database
        error_message = traceback.format_exc()
        output_data["error"] = f"Check: {function_name}, Check detail error in ServerInfo below."
        print("Error:", error_message)
        log = dblog_session.query(Htlogs).filter(Htlogs.id==logid).first()
        if log:
            log.htl_code = hotel_schema
            log.userid = inputUsername
            timeend = datetime.now()
            log.endpoint = vhp_module + "/" + service_name 
            log.log = os.environ['AWS_LAMBDA_FUNCTION_NAME'] + "|" + module_name + "Err:" + error_message
            log.timestamp = timeend
            dblog_session.commit()
            dblog_session.close()

    finally:
        dblog_session.close()

    response = {
        "response" :output_data
    }
    # dblog_session.close()
    ServerInfo["debug"] = debug
    ServerInfo["version"] = docker_version
    ServerInfo["ipclient"] = client_ip
    ServerInfo["finally"] = "yes"
    ServerInfo["Debuging"] = local_storage.debugging
    ServerInfo["error"] = error_message
    ServerInfo["modfunc"] = module_name  + "/" + service_name 
    ServerInfo["lendata"] = output_data_size
    ServerInfo["AWSFunction"] =  os.environ['AWS_LAMBDA_FUNCTION_NAME']
    ServerInfo["LogDB"] = use_db + ":" + DB_HOST.split('.')[0].replace("vhp", "vxx", -1).replace("login", "lox", -1)  + "/" + DB_NAME.replace('postgres', 'pxxxsss', -1)
    ServerInfo["AWSCloudWatch"] =  os.environ["AWS_LAMBDA_LOG_STREAM_NAME"]
    ServerInfo["AWSRequestId"] = amzn_trace_id
    ServerInfo["pythonVersion"] = platform.python_version()
    return {
        "response": output_data,
        "serverinfo": ServerInfo
    }