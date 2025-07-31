#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 31/7/2025
# gitlab: 
# Ratecode.endperiod -> Ratecode.endperiode 
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Queasy

def load_ratecode2bl(case_type:int, markno:int, prcode:string, argtno:int, zikatno:int, adult:int, child1:int, child2:int, w_day:int, startdate:date, enddate:date, s_recid:int):

    prepare_cache ([Ratecode, Queasy])

    error_flag = False
    child_error = False
    error_msg = ""
    ratecode = queasy = None

    t_ratecode = qbuff = buf_rcode = None

    t_ratecode_data, T_ratecode = create_model_like(Ratecode, {"s_recid":int})

    Qbuff = create_buffer("Qbuff",Queasy)
    Buf_rcode = create_buffer("Buf_rcode",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, child_error, error_msg, ratecode, queasy
        nonlocal case_type, markno, prcode, argtno, zikatno, adult, child1, child2, w_day, startdate, enddate, s_recid
        nonlocal qbuff, buf_rcode


        nonlocal t_ratecode, qbuff, buf_rcode
        nonlocal t_ratecode_data

        return {"error_flag": error_flag, "child_error": child_error, "error_msg": error_msg}

    if num_entries(prcode, ";") >= 1:
        prcode = entry(0, prcode, ";")

    if case_type == 3:

        ratecode = get_cache (Ratecode, {"marknr": [(eq, markno)],"code": [(eq, prcode)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, zikatno)],"_recid": [(ne, s_recid)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)],"wday": [(eq, w_day)],"startperiode": [(ge, enddate)],"endperiode": [(le, startdate)]})

        if ratecode:
            error_flag = True
    elif case_type == 4:

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, prcode)]})

        if queasy:

            if not queasy.logi2:

                if num_entries(queasy.char3, ";") > 2:

                    ratecode = get_cache (Ratecode, {"marknr": [(eq, markno)],"code": [(eq, entry(1, queasy.char3, ";"))],"argtnr": [(eq, argtno)],"zikatnr": [(eq, zikatno)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)],"wday": [(eq, w_day)],"startperiode": [(le, startdate)],"endperiode": [(ge, enddate)]})

                    if not ratecode:
                        error_flag = True
                        child_error = True

                        buf_rcode = get_cache (Ratecode, {"marknr": [(eq, markno)],"code": [(eq, entry(1, queasy.char3, ";"))]})

                        if buf_rcode:
                            error_msg = buf_rcode.code + " " + to_string(buf_rcode.startperiode) + " - " + to_string(buf_rcode.endperiode)

                        return generate_output()

        if s_recid == None:
            # Rd, 31/7/2025
            # Ratecode.endperiod -> Ratecode.endperiode
            # ratecode = db_session.query(Ratecode).filter(
            #          (Ratecode.marknr == markno) & (Ratecode.code == (prcode).lower()) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == zikatno) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child1) & (Ratecode.kind2 == child2) & (Ratecode.wday == w_day) & (not_ (Ratecode.startperiod > enddate)) & (not_ (Ratecode.endperiod < startdate))).first()
            ratecode = db_session.query(Ratecode).filter(
                     (Ratecode.marknr == markno) & (Ratecode.code == (prcode).lower()) & (Ratecode.argtnr == argtno) & 
                     (Ratecode.zikatnr == zikatno) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child1) & 
                     (Ratecode.kind2 == child2) & (Ratecode.wday == w_day) & (not_ (Ratecode.startperiode > enddate)) & 
                     (not_ (Ratecode.endperiod < startdate))).first()
        
        else:
            # Rd, 31/7/2025
            # Ratecode.endperiod -> Ratecode.endperiode
            # ratecode = db_session.query(Ratecode).filter(
            #          (Ratecode.marknr == markno) & (Ratecode.code == (prcode).lower()) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == zikatno) & (Ratecode._recid != s_recid) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child1) & (Ratecode.kind2 == child2) & (Ratecode.wday == w_day) & (not_ (Ratecode.startperiod > enddate)) & (not_ (Ratecode.endperiod < startdate))).first()
            ratecode = db_session.query(Ratecode).filter(
                     (Ratecode.marknr == markno) & (Ratecode.code == (prcode).lower()) & (Ratecode.argtnr == argtno) & 
                     (Ratecode.zikatnr == zikatno) & (Ratecode._recid != s_recid) & (Ratecode.erwachs == adult) & 
                     (Ratecode.kind1 == child1) & (Ratecode.kind2 == child2) & (Ratecode.wday == w_day) & 
                     (not_ (Ratecode.startperiode > enddate)) & (not_ (Ratecode.endperiode < startdate))).first()

        if ratecode:
            error_flag = True

    return generate_output()