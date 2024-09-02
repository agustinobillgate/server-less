from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Counters, Queasy

def hk_lostfound_addbl(zinr:str, from_date:date, zeit:str, dept:int, reason:str, reportby:str, claim_date:date, phoneno:str, refno:str, foundby:str, location:str, submitted:str, user_init:str):
    s_list_list = []
    num:int = 0
    claim_date_str:str = ""
    bediener = counters = queasy = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":str, "zinr":str, "userinit":str, "bezeich":str, "foundby":str, "submitted":str, "reportby":str, "claim_date":date, "location":str, "refno":str, "phoneno":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, num, claim_date_str, bediener, counters, queasy
        nonlocal zinr, from_date, zeit, dept, reason, reportby, claim_date, phoneno, refno, foundby, location, submitted, user_init


        nonlocal s_list
        nonlocal s_list_list
        return {"s-list": s_list_list}

    if not bediener or not(bediener.userinit.lower()  == (user_init).lower()):
        bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    num = to_int(substring(zeit, 0, 2)) * 3600 +\
            to_int(substring(zeit, 2, 2)) * 60 + to_int(substring(zeit, 4, 2))

    if not counters or not(counters.counter_no == 11):
        counters = db_session.query(Counters).filter(
            (Counters.counter_no == 11)).first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 11
        counters.counter_bez = "Lost+Found Counter"


    counters.counter = counters.counter + 1

    if claim_date == None:
        claim_date_str = ""
    else:
        claim_date_str = to_string(claim_date)
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 7
    queasy.date1 = from_date
    queasy.number1 = num
    queasy.char1 = zinr
    queasy.number2 = bediener.nr
    queasy.char2 = reason
    queasy.betriebsnr = dept
    queasy.number3 = counters.counter
    foundby = replace_str(foundby, "|", "")
    submitted = replace_str(submitted, "|", "")
    reportby = replace_str(reportby, "|", "")
    phoneno = replace_str(phoneno, "|", "")
    refno = replace_str(refno, "|", "")
    location = replace_str(location, "|", "")
    queasy.char3 = foundby +\
            "|" + submitted +\
            "|" + entry(0, reportby, chr(2)) +\
            "|" + to_string(claim_date_str) +\
            "|" + phoneno +\
            "|" + refno +\
            "|" + location

    if num_entries(reportby, chr(2)) > 1:
        queasy.char3 = queasy.char3 + "|" + "|" + "|" + entry(1, reportby, chr(2))
    s_list = S_list()
    s_list_list.append(s_list)

    s_list.nr = queasy.number3
    s_list.date1 = queasy.date1
    s_list.zeit = to_string(queasy.number1, "HH:MM:SS")
    s_list.zinr = queasy.char1
    s_list.userinit = bediener.userinit
    s_list.bezeich = queasy.char2
    s_list.betriebsnr = queasy.betriebsnr
    s_list.foundby = foundby
    s_list.submitted = submitted
    s_list.reportby = reportby
    s_list.claim_date = claim_date
    s_list.s_recid = queasy._recid
    s_list.phoneno = phoneno
    s_list.refno = refno
    s_list.location = location

    return generate_output()