from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Ratecode, Queasy

def load_ratecode2bl(case_type:int, markno:int, prcode:str, argtno:int, zikatno:int, adult:int, child1:int, child2:int, w_day:int, startdate:date, enddate:date, s_recid:int):
    error_flag = False
    child_error = False
    error_msg = ""
    ratecode = queasy = None

    t_ratecode = qbuff = None

    t_ratecode_list, T_ratecode = create_model_like(Ratecode, {"s_recid":int})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, child_error, error_msg, ratecode, queasy
        nonlocal qbuff


        nonlocal t_ratecode, qbuff
        nonlocal t_ratecode_list
        return {"error_flag": error_flag, "child_error": child_error, "error_msg": error_msg}

    if num_entries(prcode, ";") >= 1:
        prcode = entry(0, prcode, ";")

    if case_type == 3:

        ratecode = db_session.query(Ratecode).filter(
                (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode._recid != s_recid) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  (not Ratecode.startperiod >= enddate) &  (not Ratecode.endperiod <= startdate)).first()

        if ratecode:
            error_flag = True
    elif case_type == 4:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (func.lower(Queasy.char1) == (prcode).lower())).first()

        if queasy:

            if not queasy.logi2:

                if num_entries(queasy.char3, ";") > 2:

                    ratecode = db_session.query(Ratecode).filter(
                            (Ratecode.marknr == markno) &  (Ratecode.code == entry(1, queasy.char3, ";")) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  ((Ratecode.startperiod <= startdate)) &  ((Ratecode.endperiod >= enddate))).first()

                    if not ratecode:
                        error_flag = True
                        child_error = True

                        return generate_output()
                else:

                    for qbuff in db_session.query(Qbuff).filter(
                            (Qbuff.key == 2) &  (num_entries(Qbuff.char3, ";") > 2) &  (entry(1, Qbuff.char3, ";") == queasy.char1)).all():

                        ratecode = db_session.query(Ratecode).filter(
                                (Ratecode.marknr == markno) &  (Ratecode.code == qbuff.char1) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  ((Ratecode.startperiod >= startdate)) &  ((Ratecode.endperiod > enddate))).first()

                        if ratecode:
                            error_flag = True
                            child_error = True
                            error_msg = ratecode.CODE + "   " +\
                                    to_string(ratecode.startperiode) +\
                                    " - " +\
                                    to_string(ratecode.endperiode)

                            return generate_output()

                        ratecode = db_session.query(Ratecode).filter(
                                (Ratecode.marknr == markno) &  (Ratecode.code == qbuff.char1) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  ((Ratecode.startperiod < startdate)) &  ((Ratecode.endperiod <= enddate))).first()

                        if ratecode:
                            error_flag = True
                            child_error = True
                            error_msg = ratecode.CODE + "   " +\
                                    to_string(ratecode.startperiode) +\
                                    " - " +\
                                    to_string(ratecode.endperiode)

                            return generate_output()


        if s_recid == None:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  (not (Ratecode.startperiod > enddate)) &  (not (Ratecode.endperiod < startdate))).first()
        else:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode._recid != s_recid) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  (not (Ratecode.startperiod > enddate)) &  (not (Ratecode.endperiod < startdate))).first()

        if ratecode:
            error_flag = True

    return generate_output()