"""
import sys
sys.path.append("/opt/python/lib/python3.9/site-packages/")
"""

#Version 1.0.0.26
import importlib, csv, json, datetime
import watchtower, logging, traceback
from functions.additional_functions import *
# from functions.check_userkeybl import *
from decimal import Decimal
from models.base import get_database_session
from contextlib import asynccontextmanager

# from flask import Flask, request, abort, Response
# from flask_cors import CORS

from fastapi import FastAPI, Request, HTTPException
from starlette import status

from typing import Any
import typing

from _demo_config import * 

def current_milli_time():
    import time
    return round(time.time() * 1000)


# set_db_and_schema("vhp_1")
start_time = current_milli_time()

#updated 1.0.0.14
update_table_name_list = {}
curr_module = ""
curr_service = ""

def update_table_name(module, function_name, prev_table_name, updated_table_name):
    global update_table_name_list
    #updated 1.0.0.20

    if module + "_" + function_name not in update_table_name_list:
        update_table_name_list[module + "_" + function_name] = {}
    update_table_name_list[module + "_" + function_name][prev_table_name] = updated_table_name


#updated 1.0.0.6
update_field_mapping = {
    "char":"CHAR",
    "str":"STR",
    "code":"CODE",
    "id":"ID",
    "name":"NAME",
    "selected":"SELECTED",

    "flag":"Flag",
    "integerflag":"integerFlag",
    "doneflag":"doneFlag",
    "grpflag":"grpFlag",
    "successflag":"successFlag",
    "selectflag":"selectFlag",
    "finishflag":"finishFlag",

    "gastid":"gastID",
    "resno":"resNo",
    "resnr":"resNr",
    "reslinno":"reslinNo",

    "lnlFilepath":"LnLFilepath",
    "lnlFilepath1":"LnLFilepath1",
    "lnlProg":"LnLProg",

    "bankettp1":"Bankettp1",
    "bankettp2":"Bankettp2",
    "bankettp3":"Bankettp3",
    "bankettp4":"Bankettp4",
    "lvanzvat":"lvAnzVat",
    "vat_artlist":"vatArtlist",
    "cashdrwProg":"CashDrwProg",
    "msgint":"msgInt",
    "msgstr":"msgStr",
    "htpint":"htpInt",
    "hkdiscrepancyList":"hkDiscrepancyList",
    "successflag":"successFlag",
    "comproom1":"compRoom1",
    "comproom2":"compRoom2",
    "houseroom1":"HouseRoom1",
    "houseroom2":"HouseRoom2",
    "segm1list":"segm1List",
    "room-exccomp":"room-excComp",
    "varkey":"varKey",
    "varvalue":"varValue",
    "createid":"createID",
    "totCh1reactive":"totCh1Reactive",
    "rsvname":"rsvName",
    "rmtype":"rmType",
    "kategorie":"Kategorie",
    "layer3list":"layer3List",
    "adult1":"Adult1",
    "base64imagefile":"base64ImageFile",

    "bankettfsnr":"Bankettfsnr",
    "tagungfsnr":"Tagungfsnr",
    "tagungp2":"Tagungp2",
    "departtyp":"Departtyp",

    #updated 1.0.0.8
    "b1title": "b1Title",
    "b2title": "b2Title",
    "rmplan": "rmPlan",
    "tdate": "tDate",
    "roomnr": "roomNr",
    "guestnr": "guestNr",
    "guestname": "guestName",
    "totaladult": "totalAdult",
    "totalcompli": "totalCompli",
    "totalchild": "totalChild",
    "totaluse": "totalUse",
    "dummychr": "dummyChr",
    "flEknr": "fLEknr",
    "blEknr": "bLEknr",
    "tischno": "tischNo",

    #updated 1.0.0.9
    "rmcat":"rmCat",
    "rcode":"rCode",
    "markno":"markNo",

    #updated 1.0.0.13
    "tagungp3":"Tagungp3",
    "tagungp4":"Tagungp4",
    "propid":"propID",

    #updated 1.0.0.14
    "base64Imagefile": "base64ImageFile",
    "rmno": "rmNo",
    "errcode": "errCode",
    "menu": "MENU",

    #updated 1.0.0.15
    "refno": "refNo",
    "voucherno": "voucherNo",
    "voucherno1": "voucherNo1",
    "voucherno2": "voucherNo2",
    "arrecid": "arRecid",
    "newpayment": "newPayment",
    "newfpayment": "newfPayment",
    "room-exccomp": "room-excComp",
    "houseroom1": "houseRoom1",
    "houseroom2": "houseRoom2",
    "houseroom2": "houseRoom2",
    "cashbasis": "cashBasis",
    "rmtypevhp": "rmtypeVHP",
    "rmtypebe": "rmtypeBE",
    "mesvalue": "mesValue",
    "currencyvhp": "currencyVHP",
    "currencybe": "currencybe",
    "nationvhp": "nationVHP",
    "nationbe": "nationBE",
    "preis": "Preis",
    "reihenfolge": "Reihenfolge",
    "next_2nd_price": "Next_2nd_price",
    "yield_": "yield",

    #updated 1.0.0.16
    "day-setting": "Day-setting",
    "gloanz": "gloAnz",
    "gresanz": "gresAnz",
    "resanz": "resAnz",
    "resnrstr": "resnrStr",
    "deptno": "deptNo",
    "gname": "Gname",
    "outstr": "outStr",
    "usefor": "Usefor",
    # "enfid": "EngID",
    "groupid": "GroupID",
    "duration-nr": "Duration-nr",
    "activeflag": "activeFlag",
    "skill": "Skill",
    "plz": "PLZ",
    "rcvid": "rcvID",
    "rcvname": "rcvName",
    "pi-type":"PI-type",
    "pi-status":"PI-status",
    "chequeno":"chequeNo",
    "bankname":"bankName",
    "duedate": "dueDate",
    "postdate": "PostDate",
    "cid": "CID",
    "mid": "MID",
    "printed1a": "printed1A",
    "printed2a": "printed2A",
    "canceldate": "cancelDate",
    "cancelid": "cancelID",
    "pidocuno": "piDocuNo",
    "gcPiacctBezeich": "gcPIacctBezeich",
    "returnamt": "returnAmt",
    "billdate": "billDate",
    "fromdate": "fromDate",
    "todate": "toDate",

    #updated 1.0.0.17
    "engid": "EngID",

    #updated 1.0.0.18
    "uppercasename": "upperCaseName",
    "delayrate": "delayRate",
    "delaypull": "delayPull",
    "delayavail": "delayAvail",
    "pushall": "pushAll",
    "vcwsagent": "vsWSAgent",
    "vcwsagent1": "vsWSAgent1",
    "vcwsagent2": "vsWSAgent2",
    "vcwsagent3": "vsWSAgent3",
    "vcwsagent4": "vsWSAgent4",
    "vcwsagent5": "vsWSAgent5",
    "vcwebhost": "vsWebHost",
    "vcwebport": "vcWebPort",
    "incltentative": "inclTentative",

    #updated 1.0.0.20
    "typebill": "typeBill",
    "roomno": "roomNo",
    "prevbala": "prevBala",

    #updated 1.0.0.22
    "create_by": ["Create_by", "Create_By"],
    "created_by": ["Created_by", "Created_By"],
    "deptname": ["deptName","DeptName","DeptNAME","DEPTNAME"]

}

#updated 1.0.0.14
update_table_name("vhpOU","splitbillPrepare","lhbline","Lhbline")

#updated 1.0.0.15
update_table_name("HouseKeeping","getStoreRoomDiscrepancyList","hkdiscrepancyList","hkDiscrepancyList")

update_table_name("vhpFOR","bonusNightCheck","resDynarate","ResDynarate")
update_table_name("vhpFOR","searchByVoucher","tResVoucherno","tResVoucherNo")

update_table_name("vhpSS","addRoomAdmin","dynarateList","dynaRateList")
update_table_name("vhpSS","ratecodeAdmWrite","tb3buff","tb3Buff")

#updated 1.0.0.16
update_table_name("vhpSS","egStaffPrepare","dept","Dept")
# update_table_name("vhpSS","egStaffPrepare","userskill","Userskill")

#updated 1.0.0.17
update_table_name("vhpSS","egStaffPrepare","userskill","UserSkill")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ⏳ STARTUP
    print("Warming up database engines...")

    tenant_session = get_database_session("postgresql+psycopg://postgres:password@localhost:5432/tenants")
    try:
        tenant_session.execute(text("SELECT 1"))
    finally:
        tenant_session.close()

    fallback_session = get_database_session("postgresql+psycopg://postgres:password@localhost:5432/vhp_rental")
    try:
        fallback_session.execute(text("SELECT 1"))
    finally:
        fallback_session.close()

    print("Warm-up complete ✅")

    yield  # 🔄 This is where FastAPI will handle requests

    # 🧹 SHUTDOWN (optional cleanup)
    print("Shutting down...")


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
                                input_data[outer_input_param_name][inner_input_param_name] = input_data[outer_input_param_name]
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
            elif not type(param_data_type[0]) in {int,  Decimal, float, complex, str, list, tuple, range, dict, set, 
                                                  frozenset, bool, bytes, bytearray, memoryview, type(None)} and \
                not param_data_type[0] in {int, Decimal, float, complex, str, list, tuple, range, dict, set, 
                                                  frozenset, bool, bytes, bytearray, memoryview, type(None)}:
                                                    
                data_list = input_data[param_name]
                if not isinstance(data_list,list):
                    input_data[param_name] = [data_list]
                    data_list = input_data[param_name]   
                
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
                            if not field.name in data_list[0]:
                                if field.name.replace("_","-") in data_list[0]:
                                    fieldNameList.append(field.name)
                                else:
                                    for field_name in data_list[0].keys():
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


"""
def lambda_handler(event, lambda_context):
    path = event.get("path")
    request = event.get("body")
"""

# app = Flask(__name__)

# CORS(app)
# set_db_and_schema("vhp_1")

app = FastAPI()
# Use lifespan handler in your app
# app = FastAPI(lifespan=lifespan)


# logging.basicConfig(level=logging.ERROR)

# @app.errorhandler(Exception)
# def handle_error(e):
#     # Retrieve the full stack trace of the exception
#     stack_trace = traceback.format_exc()
    
#     # Log the error message and the stack trace
#     # app.logger.error(f"An error occurred: {e}\nStack Trace:\n{stack_trace}")
#     # return stack_trace, 500
#     return e, 500


# @app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
# @app.route('/<path:path>', methods=['GET', 'POST'])
# @app.get("/{path_param}")
# @app.post("/{path_param}")

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

    return handle_get_post(request, input_data, body_str)

def handle_get_post(request: Request, input_data: Dict[str, Any] = {}, body_str:str = ""):
    url = str(request.url)
    headers = dict(request.headers)

    # print(headers)

    if not hasattr(local_storage,"app"):
        local_storage.app = app

    return handle_dynamic_data(url, headers, input_data, body_str)



def handle_dynamic_data(url:str, headers: Dict[str, Any], input_data: Dict[str, Any] = {}, body_str:str = ""):
    #updated 1.0.0.14
    global curr_module, curr_service, start_time

    #updated 1.0.0.18
    initialize_local_storage()

    curr_module = ""
    curr_service = ""

    # start_time = current_milli_time()


    signature = headers.get("x-signature")
    nonce = headers.get("x-nonce")
    timestamp = headers.get("x-timestamp")

    path = url.replace("http://","").replace("https://","")
    output_data = {}
    
    hotel_schema = ""
    ok_flag = False

    # headers_input_data = input_data.get("headers")

    if "request" in input_data:
        input_data = input_data["request"]

    # if headers_input_data:
    #     for key in headers_input_data:
    #         if to_string(headers_input_data[key]) != headers.get(key.lower()):
    #             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    #         input_data[key] = headers.get(key.lower())

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

    hotel_schema = input_data.get("hotel_schema")
    if not hotel_schema:
        hotel_schema = input_data.get("hotel_schema")


    if not hotel_schema:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Wrong or missing hotel code")

    else:        
        vhp_module = entry(2,path,"/")
        service_name = entry(3,path,"/")

        module_mapping = {
            "vhpPOS": "vhpOU"
        }

        if vhp_module in module_mapping:
            vhp_module = module_mapping(vhp_module)

        #updated 1.0.0.14
        curr_module = vhp_module
        curr_service = service_name
                    

        if num_entries(path,"/") == 6:
            service_name += entry(5,path,"/")

        # #TODO: handle logs for lambda
        # handler = watchtower.CloudWatchLogHandler(
        #     log_group='vhp',
        #     stream_name=f'{hotel_schema}_Stream' 
        # )
        # app.logger.addHandler(handler)

        # start_time = current_milli_time()

        set_db_and_schema(hotel_schema)
        if not local_storage.db_session:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Wrong or missing hotel code")

        # print("connect_db: ", current_milli_time() - start_time)
        # start_time = current_milli_time()

        db_session = local_storage.db_session
        
        # upload_file_s3("testing","test","aaaaaa")
        with open('modules/' + vhp_module + '/_mapping.txt', mode ='r') as file:   
            mapping_service = csv.DictReader(file)
            function_name = ""

            for mapping in mapping_service:
                if mapping['service'] == service_name:
                    function_name = mapping["function"]
                    break
            
            if function_name == "":
                db_session.close()
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        print(function_name + ".py")
        module_name = "functions." + function_name
        #TODO: create a list of program which does not need to check userkey

        # ok_flag = get_output(check_userkeybl(input_data["inputUsername"], input_data["inputUserkey"]))
        ok_flag = True
        if function_name[0].isdigit():
            function_name = "_" + function_name
        if not ok_flag:
            db_session.close()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        else:
            input_data.pop("inputUsername")
            input_data.pop("inputUserkey")
            input_data.pop("hotelCode",None)
            input_data.pop("hotelcode",None)

            # Check if module and function exists
            if importlib.util.find_spec(module_name):
                module = importlib.import_module(module_name)
                if hasattr(module, function_name):
                    obj = getattr(module, function_name)

                    # print("start update input format: ", current_milli_time() - start_time)
                    # start_time = current_milli_time()

                    update_input_format(obj,input_data)
                    # print("end update input format: ", current_milli_time() - start_time)
                    # start_time = current_milli_time()
                    output_data =  obj(**input_data)
                    initialize_local_storage()

                    # try:
                    #     output_data =  obj(**input_data)
                    # except Exception as e:
                    #     output_data = {"error":e.args}

                    if output_data == None:
                        output_data = {}
                else:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        db_session.commit()
        db_session.close()

    if output_data == None:
        output_data = {}


    # print("start update output format: ", current_milli_time() - start_time)
    # start_time = current_milli_time()
    update_output_format(output_data)
    
    # print("end update output format: ", current_milli_time() - start_time)
    # start_time = current_milli_time()

    output_data["outputOkFlag"] = ok_flag

    # response = Response(response=json.dumps({"response":output_data}, cls=CustomJSONEncoder, separators=(',', ':')),
    #                     status=200,mimetype='application/json')
    # return json.dumps({"response":output_data}, cls=CustomJSONEncoder)
    # return response

    return {"response":output_data}

# app.run(host ="0.0.0.0", port = 8000, debug=True)
