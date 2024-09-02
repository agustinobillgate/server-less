from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def select_delivernotebl():
    t_l_ophdr_list = []
    l_ophdr = None

    t_l_ophdr = None

    t_l_ophdr_list, T_l_ophdr = create_model("T_l_ophdr", {"datum":date, "lager_nr":int, "docu_nr":str, "lscheinnr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_ophdr_list, l_ophdr


        nonlocal t_l_ophdr
        nonlocal t_l_ophdr_list
        return {"t-l-ophdr": t_l_ophdr_list}

    for l_ophdr in db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.op_typ) == "STI")).all():
        t_l_ophdr = T_l_ophdr()
        t_l_ophdr_list.append(t_l_ophdr)

        t_l_ophdr.datum = l_ophdr.datum
        t_l_ophdr.lager_nr = l_ophdr.lager_nr
        t_l_ophdr.docu_nr = l_ophdr.docu_nr
        t_l_ophdr.lscheinnr = l_ophdr.lscheinnr

    return generate_output()