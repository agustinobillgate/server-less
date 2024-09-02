from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Ratecode

def load_ratecode1bl(case_type:int, markno:int, prcode:str, argtno:int, zikatno:int, adult:int, child1:int, child2:int, w_day:int, startdate:date, enddate:date, s_recid:int):
    t_ratecode_list = []
    ratecode = None

    t_ratecode = None

    t_ratecode_list, T_ratecode = create_model_like(Ratecode, {"s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ratecode_list, ratecode


        nonlocal t_ratecode
        nonlocal t_ratecode_list
        return {"t-ratecode": t_ratecode_list}

    def cr_t_ratecode():

        nonlocal t_ratecode_list, ratecode


        nonlocal t_ratecode
        nonlocal t_ratecode_list


        t_ratecode = T_ratecode()
        t_ratecode_list.append(t_ratecode)

        buffer_copy(ratecode, t_ratecode)
        t_ratecode.s_recid = ratecode._recid

    if case_type == 1:

        for ratecode in db_session.query(Ratecode).filter(
                (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno)).all():
            cr_t_ratecode()

    elif case_type == 2:

        for ratecode in db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower())).all():
            cr_t_ratecode()

    elif case_type == 3:

        ratecode = db_session.query(Ratecode).filter(
                (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode._recid != s_recid) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  (not Ratecode.startperiod >= enddate) &  (not Ratecode.endperiod <= startdate)).first()

        if ratecode:
            cr_t_ratecode()
    elif case_type == 4:

        if s_recid == None:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  (not Ratecode.startperiod >= enddate) &  (not Ratecode.endperiod <= startdate)).first()
        else:

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.marknr == markno) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtno) &  (Ratecode.zikatnr == zikatno) &  (Ratecode._recid != s_recid) &  (Ratecode.erwachs == adult) &  (Ratecode.kind1 == child1) &  (Ratecode.kind2 == child2) &  (Ratecode.wday == w_day) &  (not Ratecode.startperiod >= enddate) &  (not Ratecode.endperiod <= startdate)).first()

        if ratecode:
            cr_t_ratecode()
    elif case_type == 5:

        ratecode = db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.zikatnr == zikatno)).first()

        if ratecode:
            cr_t_ratecode()

    return generate_output()