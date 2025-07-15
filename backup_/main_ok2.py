docker_version = "1.0.0.24.689"
#Version 1.0.0.17

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
from functions.check_userkeybl import *
from decimal import Decimal
import asyncio

# from flask import Flask, request, abort, Response
# from flask_cors import CORS
from fastapi import FastAPI, Response, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from typing import Dict, Any

from _demo_config import * 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mangum import Mangum

from models.guestbook import Guestbook
# print("1:", docker_version)

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


#updated 1.0.0.14
update_table_name_list = {}
curr_module = ""
curr_service = ""

def update_table_name(module, function_name, prev_table_name, updated_table_name):
    global update_table_name_list
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
    "rmytpebe": "rmtypebe",
    "mesvalue": "mesValue",
    "currencyvhp": "currencyVHP",
    "currencybe": "currencyBE",
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
    "description": "DESCRIPTION",

    #updated 1.0.0.19
    "tableno": "tableNo",
    "billno": "billNo",
    "artno": "artNo",

    #updated 1.0.0.20
    "roomnumber": "roomNumber",
    "checkoutdate": "checkoutDate",
    "checkouttime": "checkoutTime",
    "checkintime": "checkinDate",
    "checkinTime": "checkinTime",

    #updated 1.0.0.21
    "hkdiscrepancylist": "hkDiscrepancyList",
    "thartikel1": "tHArtikel1",
    "menu": "MENU",
    "multivat": "multiVat",
    "zeroflag": "zeroFlag",
    "multicash": "multiCash",
    "pricedecimal": "priceDecimal",
    "foreignrate": "foreignRate",
    "doublecurrency": "doubleCurrency",
    "exchgRate": "exchgRate",
    "mustprint": "mustPrint",
    "flwarn": "flWarn",
    "maxlapos": "maxLapos",
    "cashlessflag": "cashlessFlag",
    "thbill": "tHBill",
    "thbillline": "tHBillLine",
    "lhbline": "Lhbline",
    "tkellner": "tKellner",
    "indgastnr":"indGastnr",
    "piDocuno":"piDocuNo",
    # "postdate": "PostDate",
    "tLorderhdr": "tLOrderhdr",
    "addvat": "addVAT",
    "availaddvat": "availAddVat",
    "tpushlist":"tPushList",
    "rcodevhp": "rcodeVHP",
    "rcodebe": "rcodeBE",
    "argtvhp": "argtVHP",
    "rmatproduct": "rmAtproduct",
    "lavail": "lAvail",
    "b1list":"b1List",

    #updated 1.0.0.22
    "deptno": "DeptNo",
    "dept": "Dept",
    "tb3buff": "tb3Buff",

    # Rd vhpENG/egRepmaintainPrepare
    # "categ-nr":"Categ-nr",
    # "categ-nm":"Categ-nm",
    "categ-sel":"Categ-sel",
    "avail-addvat":"avail-addVAT",
    "availAddvat": "availAddVat",
    "pic-dept":"pic-Dept",
    "guestflag": "GuestFlag",
    "hourmax":"HourMax",
    "metermax": "MeterMax",
    "meterrec": "MeterRec",
    "smove":"sMove",
    "estworkdate":"estWorkDate",
    "location":"Location",
    "pic":"PIC",
    "reqstatus":"reqStatus",
    "done-by":"Done-by",
    "done-date":"Done-date",
    "done-time":"Done-time",
    "ex-finishtime":"ex-finishTime",
    "ex-finishtime1":"ex-finishTime1",
    "outsourceflag":"outsourceFlag",
    "reasonstatus":"ReasonStatus",
    "reasondonetime":"ReasonDoneTime",
    "delete-flag":"Delete-Flag",
    "source-name":"Source-name", 

    "blcpy":"blCpy",
    "lsno":"lsNo",
    "stno":"stNo",
    "year": "YEAR",
    "month": "MONTH",
    "strmonth": "strMONTH",
    "dailyrec":"dailyRec",
    "tmaintain":"tMaintain",
    "mainaction":"MainAction",
    "room-selected":"room-Selected",
    "tmaintask": "tMaintask",
    "tstatus": "tStatus",
    "tfrequency": "tFrequency",
    "tlocation": "tLocation",
    "tfstat":"tFStat",
    "svendor": "sVendor",
    "engid": "EngId",
    "maintask": "Maintask",
    "copyrequest": "CopyRequest",
    "lrate": "lRate",

    #updated 1.0.0.24
    "defaultflag": "defaultFlag",

    #updated 1.0.0.25
    "piAcctno": "piAcctNo",
    "giroTempacct" : "giroTempAcct",
    "payAcctno" : "payAcctNo",
    "tGcPibline" : "tGcPIbline",

    #updated 1.0.0.26r
    "cl": "CL",
    "strpanjang": "strPanjang",

    #updated 1.0.0.27r
    "yr": "Yr",

    #updated 1.0.0.28r
    "type":"TYPE",
    "spec": "Spec",

    # "Categ-nr": "categ-nr",
    # "Categ-nm": "categ-nm",

    #updated 1.0.0.29r
    "msgStrq":"msgStrQ",
    
    #updated 1.0.0.30r
    "date":"DATE",
    "anfdate": "anfDate",
    "enddate":"endDate",

    #updated 1.0.0.31r
    "tGcPibline": "tGcPIbline",

    "uppercasename": "upperCaseName",
    "delayrate": "delayRate",
    "delaypull": "delayPull",
    "delayavail": "delayAvail",
    "pushall": "pushAll",
    "vcwsagent": "vcWSAgent",
    "vcwsagent1": "vcWSAgent1",
    "vcwsagent2": "vcWSAgent2",
    "vcwsagent3": "vcWSAgent3",
    "vcwsagent4": "vcWSAgent4",
    "vcwsagent5": "vcWSAgent5",
    "vcwebhost": "vcWebHost",
    "vcwebport": "vcWebPort",
    "incltentative": "inclTentative",

    #updated 1.0.0.33r
    "overclFlag": "overCLFlag",

    #updated 1.0.0.34r
    "typebill": "typeBill",
    "roomno": "roomNo",
    "prevbala": "prevBala",
    
    #updated 1.0.0.35r (16-Mei-2025)
    "reqCreated": "reqCREATEd",  # s_stockout_btn_gobl

    #updated 1.0.0.36r (19-Mei-2025) egSubTaskPrepare
    "sourceform": "sourceForm",
    "othersflag": "OthersFlag",


    #updated 1.0.0.37r (23-Mei-2025) vhpFOR/monthlyFcastDDown1List1",
    "adult": "Adult",
    "arrtime": "ArrTime",
    "deptime": "DepTime",
    "phoneno": "PhoneNo",
    "claimby": "ClaimBy",


   
  



    
}
docker_version += ".r"

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

#updated 1.0.0.21
update_table_name("vhpSC","rmAtproductCreateUmsatz1","b1list","b1List")
update_table_name("vhpSC","rmAtproductCreateUmsatz1","rmatproduct","rmAtproduct")

#updated 1.0.0.22
update_table_name("HouseKeeping","getStoreRoomDiscrepancyList","hkdiscrepancy-list","hk-discrepancy-list")
update_table_name("vhpOU","splitbillPrepare","menu","MENU")
update_table_name("vhpGC","addGCPi1","postDate","PostDate")
update_table_name("vhpGC","addGCPi1","postdate","PostDate")

update_table_name("vhpGC","gcPilist","PI-status","pi-status")
update_table_name("vhpGC","gcPilist","PostDate","postDate")
update_table_name("vhpGC","gcPilist","postdate","postDate")

update_table_name("vhpENG","egRephistorypropPrepare","activeflag","ActiveFlag")

update_table_name("vhpENG","egChgReqPrepare","activeflag","ActiveFlag")
update_table_name("vhpENG","egPropertymeterPrepare","activeflag","ActiveFlag")

update_table_name("vhpENG","egPropertyPrepare","activeflag","ActiveFlag")
update_table_name("vhpENG","egReceivedPrepare","activeflag","ActiveFlag")
update_table_name("vhpENG","egReceivedPrepare","EngId","EngID")
update_table_name("vhpENG","egReceivedPrepare","engid","EngID")

update_table_name("vhpENG","egMkreqPrepare","EngId","EngID")
update_table_name("vhpENG","egMkreqPrepare","engid","EngID")

update_table_name("vhpENG","egRephistoryroomPrepare","EngId","EngID")
update_table_name("vhpENG","egRephistoryroomPrepare","engid","EngID")

update_table_name("vhpENG","egReqlistPrepare","EngId","EngID")
update_table_name("vhpENG","egReqlistPrepare","engid","EngID")
#---
update_table_name("vhpENG","egRephistorypropPrepare","EngId","EngID")
update_table_name("vhpENG","egRephistorypropPrepare","engid","EngID")

update_table_name("vhpENG","egRephistorymovePrepare","EngId","EngID")
update_table_name("vhpENG","egRephistorymovePrepare","engid","EngID")

update_table_name("vhpENG","egActionPrepare","EngId","EngID")
update_table_name("vhpENG","egActionPrepare","engid","EngID")

update_table_name("vhpENG","egMaincalendarPrepare","EngId","EngID")
update_table_name("vhpENG","egMaincalendarPrepare","engid","EngID")

update_table_name("vhpENG","egMaincalendardelDisp","EngId","EngID")
update_table_name("vhpENG","egMaincalendardelDisp","engid","EngID")



update_table_name("vhpENG","egMainschedulePrepare","activeflag","ActiveFlag")
update_table_name("vhpENG","egMainschedulePrepare","EngId","EngID")
update_table_name("vhpENG","egMainschedulePrepare","engid","EngID")
update_table_name("vhpENG","egMainschedulePrepare","Delete-Flag","delete-flag")

update_table_name("vhpENG","egRephistorymoveCreateBrowse","smove","sMove")

# egRepmaintainPrepare, ada EngId dan engid
update_table_name("vhpENG","egRepmaintainPrepare","EngId","EngID")
update_table_name("vhpENG","egRepmaintainPrepare","engid","EngID")
update_table_name("vhpENG","egRepmaintainPrepare","tmaintask","tMaintask")
update_table_name("vhpENG","egRepmaintainPrepare","tstatus","tStatus")
update_table_name("vhpENG","egRepmaintainPrepare","tfrequency","tFrequency")
update_table_name("vhpENG","egRepmaintainPrepare","tlocation","tLocation")


#updated 1.0.0.23
update_table_name("vhpSS","egStaffPrepare","EngId","EngID")
update_table_name("vhpSS","egStaffPrepare","engid","EngID")
update_table_name("vhpSS","egStaffPrepare","dept","Dept")
update_table_name("vhpSS","egStaffPrepare","userskill","userSkill")


update_table_name("vhpENG","egDurationPrepare","engid","EngID")

update_table_name("vhpSS","ratecodeAdmWrite","tb3buff","tb3Buff")
update_table_name("vhpAR","soaRelease","deptno","deptNo")
# update_table_name("vhpAR","soaRelease","DeptNo","deptNo")

#updated 1.0.0.24
update_table_name("vhpINV","storeReqInsPrepare","deptno","deptNo")

#updated 1.0.0.25
update_table_name("vhpINV","chgStoreRequestLoadData","deptno","deptNo")

#updated 1.0.0.28
update_table_name("vhpENG","egPropertyListBtnGo","type","TYPE")
update_table_name("vhpENG","egPropertyListBtnGo","spec","Spec")

update_table_name("vhpENG","egSelMainAll","Categ-nr","categ-nr")
update_table_name("vhpENG","egSelMainAll","Categ-nm","categ-nm")

#updated 1.0.0.29
update_table_name("vhpENG","egReprequestcancelPrepare","Categ-nr","categ-nr")
update_table_name("vhpENG","egReprequestcancelPrepare","Categ-nm","categ-nm")

update_table_name("vhpENG","egRepdurationPrepare","Categ-nr","categ-nr")
update_table_name("vhpENG","egRepdurationPrepare","Categ-nm","categ-nm")


#updated 1.0.0.32, 16-4-2025
update_table_name("vhpSS","egResourcePrepare","engid","EngID")
update_table_name("vhpSS","egLocationPrepare","engid","EngID")
update_table_name("vhpSS","egCategoryPrepare","engid","EngID")
update_table_name("vhpSS","egBuildingPrepare","engid","EngID")
update_table_name("vhpENG","egChgReqPrepare","engid","EngID")
update_table_name("vhpENG","egChgReqPrepare","tFStat","tFStat")
update_table_name("vhpENG","egChgReqPrepare","svendor","sVendor")
update_table_name("vhpENG","egPropertyLoad","svendor","tEgProperty")
update_table_name("vhpENG","egPropertymeterPrepare","outputOkFlag","ActiveFlag")
update_table_name("vhpENG","egPropertyPrepare","outputOkFlag","ActiveFlag")
update_table_name("vhpENG","egPropertyPrepare","Categ-nr","categ-nr")
update_table_name("vhpENG","egPropertyPrepare","Categ-nm","categ-nm")
update_table_name("vhpENG","egReprequestcancelPrepare","Categ-nr","categ-nr")
update_table_name("vhpENG","egReprequestcancelPrepare","Categ-nm","categ-nm")
update_table_name("vhpENG","egRepdurationPrepare","Categ-nr","categ-nr")
update_table_name("vhpENG","egRepdurationPrepare","Categ-nm","categ-nm")

update_table_name("vhpENG","egReprequestcancelPrepare","mainaction","MainAction")
update_table_name("vhpENG","egReprequestcancelPrepare","tmaintain","tMaintain")

update_table_name("vhpSS","egMaintaskBtnDelart","flcode","flCode")
update_table_name("vhpSS","egCategoryBtnExit","flcode","flCode")

update_table_name("HouseKeeping","updateAddLostAndFound","phoneno","PhoneNo")
update_table_name("vhpGC","prepareAddGCPi","tGcPibline","tGcPIbline")

# update_table_name("HouseKeeping","getStoreRoomDiscrepancyList","hkdiscrepancy-list","hk-discrepancy-list")
update_table_name("vhpHK","getStoreRoomDiscrepancyList","hkdiscrepancyList","hkDiscrepancyList")

#updated 1.0.0.33 2025-05-14
update_table_name("vhpINV","storeReqInsPrepare","deptno","deptNo")
update_table_name("vhpINV","storeReqInsPrepare","deptname","deptName")
update_table_name("vhpINV","storeReqInsPrepare","appstr","appStr")
update_table_name("vhpINV","storeReqInsPrepare","appflag","appFlag")

#updated 1.0.0.36r (19-Mei-2025) egSubTaskPrepare
update_table_name("vhpENG","egSubTaskPrepare","engid","EngID")

#updated 1.0.0.37r (22-Mei-2025) egRepmaintainPrepare
update_table_name("vhpENG","egRepmaintainPrepare","Categ-nr","categ-nr")
update_table_name("vhpENG","egRepmaintainPrepare","Categ-nm","categ-nm")


#updated 1.0.0.37r (23-Mei-2025) vhpFOR/monthlyFcastDDown1List1",

update_table_name("vhpFOR","monthlyFcastDDown1List1","adult","Adult")
update_table_name("vhpFOR","monthlyFcastDDown1List1","arrtime","ArrTime")
update_table_name("vhpFOR","monthlyFcastDDown1List1","deptime","DepTime")

#updated 1.0.0.38r (26-Mei-2025) vhpFOR/monthlyFcastDDown1List1",
update_table_name("vhpENG","egReqlistLoad","copyrequest","copyRequest")
# update_table_name("vhpENG","egReqlistLoad","action","Action")
# update_table_name("vhpENG","egReqlistLoad","smaintain","sMaintain")

#updated 1.0.0.39r (27-Mei-2025) fb_flashbl
update_table_name("vhpENG","egMainscheduleedPrepare","EngId","EngID")
update_table_name("vhpENG","egMainscheduleedPrepare","engid","EngID")

#updated 1.0.0.38r (9-Juni-2025) vhpENG/egRepdurationDisp,
update_table_name("vhpENG","egRepdurationDisp","copyrequest","copyRequest")
update_table_name("vhpENG","egRepdurationDisp","tlocation","tLocation")
update_table_name("vhpENG","egRepdurationDisp","tmaintask","tMaintask")
update_table_name("vhpENG","egRepdurationDisp","main-nr","Main-nr")
update_table_name("vhpENG","egRepdurationDisp","main-nm","Main-nm")






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
            elif not type(param_data_type[0]) in {int, Decimal, float, complex, str, list, tuple, range, dict, set, 
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
                                    data[update_field_mapping[updateFieldName]] = data[updateFieldName]
                                else:
                                    new_field_name = updateFieldName.replace("_","-").replace("--","_")

                                    if new_field_name in update_field_mapping:
                                        new_field_name = update_field_mapping[new_field_name]

                                    data[new_field_name] = data.pop(updateFieldName)
   

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
                output_data[update_field_mapping[key]] = output_data[key]


        #updated 1.0.0.14
        curr_module_function = curr_module + "_" + curr_service
        
        if curr_module_function in update_table_name_list and camelCaseKey in update_table_name_list[curr_module_function]:
            output_data[update_table_name_list[curr_module_function][camelCaseKey]] = output_data[camelCaseKey]
            output_data.pop(camelCaseKey)

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

    return handle_get_post(request, input_data, body_str)

def handle_get_post(request: Request, input_data: Dict[str, Any] = {}, body_str:str = ""):
    url = str(request.url)
    headers = dict(request.headers)

    print("Hd:", headers)
    # print("Request:", request)

    if not hasattr(local_storage,"app"):
        local_storage.app = app

    return handle_dynamic_data(url, headers, input_data, body_str)

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

    """
    if timestamp and abs(to_int(timestamp) - int(datetime.now().strftime('%s'))) > 600:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid timestamp")                

    if not signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing signature")                

    if not nonce:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Nonce")                

    if not timestamp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing timestamp")                

    if  signature and nonce and timestamp and body_str and signature != sha1_hex(body_str + "|" + nonce + "|" + timestamp):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid value")                
    """
    ui_request_id = input_data.get("ui_request_id", "None")
    is_existing_json = False
    inputUsername = input_data.get("inputUsername")
    hotel_schema = input_data.get("hotel_schema")
    output_data = {}
    if not hotel_schema:
        hotel_schema = input_data.get("hotel_schema")

    print("hotel_schema:", hotel_schema, ui_request_id)

    #------------------------ Main Function ------------------------------
    try:
        ok_flag = "False"
        # output_data = {}
    
        if hotel_schema:
            vhp_module = entry(2,path,"/")
            service_name = entry(3,path,"/")

            #updated 1.0.0.14
            curr_module = vhp_module
            curr_service = service_name

            if num_entries(path,"/") == 5:
                service_name += entry(4,path,"/")

            print("Module/Service:", vhp_module, service_name)

            set_db_and_schema(hotel_schema)
            db_session = local_storage.db_session
            print("db_session:", db_session)

            try:
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
            except Exception as e:
                print("Error:", e)
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            finally:
                # db_session.close()
                file.close()

            module_name = "functions." + function_name
            # ok_flag = get_output(check_userkeybl(input_data["inputUsername"], input_data["inputUserkey"]))
            version = ""
            if os.environ.get('AWS_EXECUTION_ENV'):
                version = get_function_version(module_name, function_name, "/var/task/functions/")
            else:
                # version = "localhost, " + get_function_version(module_name, function_name, "/usr1/serverless/src/functions/")     
                version = "localhost"
            print("Main.py, running on:", version)
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
                        print("Start BigResponse:", newRequest.userinit, newRequest_recid)
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
                            print("Existing JSON:")
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
                        module = importlib.import_module(module_name)
                        if hasattr(module, function_name):
                            try:
                                print("Calling getAttr:", function_name)   
                                obj = getattr(module, function_name)
                                # print("UpdateInputFormat:", function_name)  
                                update_input_format(obj,input_data)
                                # print("Start Call:", function_name)  
                                output_data =  obj(**input_data)
                                # print("New Output:", output_data)
                                # print("Got New Output:")
                                orig_infostr = "end"
                                if output_data is None:
                                    output_data = {}


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
                                        close_session()
                                except Exception as e:
                                    pass
                        else:
                            # db_session.close()
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
                print("OutputData:", len(data_string))
                # print(data_string)

        # ------------------------------------------------------------------------------
        if is_existing_json == False:
            output_data["output_Ok_Flag"] = str(ok_flag)
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
    ServerInfo["aws_request_id"] = aws_request_id
    
    ServerInfo["AWSFunction"] =  lambda_function_name
    ServerInfo["AWSCloudWatch"] = log_stream_name
    return {
        "response": output_data,
        "serverinfo": ServerInfo
    }


    aws_request_id = request.headers.get("X-Amzn-RequestId", "Not Available")
    print("AWS Request ID:", aws_request_id)


# infostr -> request Id
# imagefile -> content
"""
Saat ini masih mencukupi, Pak.
Jadi ada infostr (char) bisa utk letakkan nama file, utk contentnya bisa disimpan dalam imagefile (blob).
Lalu untuk created date/timestamp disini ada field created (date) dan zeit (integer).
Kemudian masih ada beberapa field lainnya dan ada reserve field jga seperti reserve-char, reserve-int, dan reserve-logic..
Jadi bsk coba saya info ke Mba Fitria utk simpan temp datanya disini dlu, Pak..
"""


# clear_8 = text("""
#                 DELETE FROM res_line WHERE resstatus = 8 AND ankunft != abreise 
#                 """)
# db_session.execute(clear_8, {})
