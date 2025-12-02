#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode

def load_ratecode1bl(case_type:int, markno:int, prcode:string, argtno:int, zikatno:int, adult:int, child1:int, child2:int, w_day:int, startdate:date, enddate:date, s_recid:int):
    t_ratecode_data = []
    ratecode = None

    t_ratecode = None

    t_ratecode_data, T_ratecode = create_model_like(Ratecode, {"s_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ratecode_data, ratecode
        nonlocal case_type, markno, prcode, argtno, zikatno, adult, child1, child2, w_day, startdate, enddate, s_recid


        nonlocal t_ratecode
        nonlocal t_ratecode_data

        return {"t-ratecode": t_ratecode_data}

    def cr_t_ratecode():

        nonlocal t_ratecode_data, ratecode
        nonlocal case_type, markno, prcode, argtno, zikatno, adult, child1, child2, w_day, startdate, enddate, s_recid


        nonlocal t_ratecode
        nonlocal t_ratecode_data


        t_ratecode = T_ratecode()
        t_ratecode_data.append(t_ratecode)

        buffer_copy(ratecode, t_ratecode)
        t_ratecode.s_recid = ratecode._recid


    if case_type == 1:

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.marknr == markno) & (Ratecode.code == (prcode).lower()) & (Ratecode.argtnr == argtno) & (Ratecode.zikatnr == zikatno)).order_by(Ratecode._recid).all():
            cr_t_ratecode()

    elif case_type == 2:

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == (prcode))).order_by(Ratecode._recid).all():
            cr_t_ratecode()

    elif case_type == 3:

        ratecode = get_cache (Ratecode, {"marknr": [(eq, markno)],"code": [(eq, prcode)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, zikatno)],"_recid": [(ne, s_recid)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)],"wday": [(eq, w_day)],"startperiode": [(ge, enddate)],"endperiode": [(le, startdate)]})

        if ratecode:
            cr_t_ratecode()
    elif case_type == 4:

        if s_recid == None:

            ratecode = get_cache (Ratecode, {"marknr": [(eq, markno)],"code": [(eq, prcode)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, zikatno)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)],"wday": [(eq, w_day)],"startperiode": [(ge, enddate)],"endperiode": [(le, startdate)]})
        else:

            ratecode = get_cache (Ratecode, {"marknr": [(eq, markno)],"code": [(eq, prcode)],"argtnr": [(eq, argtno)],"zikatnr": [(eq, zikatno)],"_recid": [(ne, s_recid)],"erwachs": [(eq, adult)],"kind1": [(eq, child1)],"kind2": [(eq, child2)],"wday": [(eq, w_day)],"startperiode": [(ge, enddate)],"endperiode": [(le, startdate)]})

        if ratecode:
            cr_t_ratecode()
    elif case_type == 5:

        ratecode = get_cache (Ratecode, {"code": [(eq, prcode)],"zikatnr": [(eq, zikatno)]})

        if ratecode:
            cr_t_ratecode()

    return generate_output()