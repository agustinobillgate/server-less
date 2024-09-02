from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def prepare_sel_transnote1bl(f_lager:int):
    t_l_ophdr_list = []
    l_ophdr = None

    t_l_ophdr = None

    t_l_ophdr_list, T_l_ophdr = create_model("T_l_ophdr", {"datum":date, "lager_nr":int, "lscheinnr":str, "docu_nr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_ophdr_list, l_ophdr


        nonlocal t_l_ophdr
        nonlocal t_l_ophdr_list
        return {"t-l-ophdr": t_l_ophdr_list}

    for l_ophdr in db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.op_typ) == "STT") &  (L_ophdr.lager_nr == f_lager)).all():
        t_l_ophdr = T_l_ophdr()
        t_l_ophdr_list.append(t_l_ophdr)

        t_l_ophdr.datum = l_ophdr.datum
        t_l_ophdr.lager_nr = l_ophdr.lager_nr
        t_l_ophdr.lscheinnr = l_ophdr.lscheinnr
        t_l_ophdr.docu_nr = l_ophdr.docu_nr

    return generate_output()