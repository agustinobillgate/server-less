from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order, Htparam, Brief

def mk_pr_btn_printbl(l_orderhdr_docu_nr:str):
    briefnr = 0
    p_220 = 0
    err_code = 0
    l_order = htparam = brief = None

    l_od = None

    L_od = create_buffer("L_od",L_order)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal briefnr, p_220, err_code, l_order, htparam, brief
        nonlocal l_orderhdr_docu_nr
        nonlocal l_od


        nonlocal l_od
        return {"briefnr": briefnr, "p_220": p_220, "err_code": err_code}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 687)).first()
    briefnr = htparam.finteger

    if briefnr == 0:
        err_code = 1

        return generate_output()

    brief = db_session.query(Brief).filter(
             (Brief.briefnr == briefnr)).first()

    if not brief:
        err_code = 2

        return generate_output()

    l_od = db_session.query(L_od).filter(
             (func.lower(L_od.docu_nr) == (l_orderhdr_docu_nr).lower())).first()

    if l_od:
        err_code = 3

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 220)).first()
        p_220 = htparam.finteger

    return generate_output()