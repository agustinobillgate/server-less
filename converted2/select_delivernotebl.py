#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def select_delivernotebl():

    prepare_cache ([L_ophdr])

    t_l_ophdr_data = []
    l_ophdr = None

    t_l_ophdr = None

    t_l_ophdr_data, T_l_ophdr = create_model("T_l_ophdr", {"datum":date, "lager_nr":int, "docu_nr":string, "lscheinnr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_ophdr_data, l_ophdr


        nonlocal t_l_ophdr
        nonlocal t_l_ophdr_data

        return {"t-l-ophdr": t_l_ophdr_data}

    for l_ophdr in db_session.query(L_ophdr).filter(
             (L_ophdr.op_typ == ("STI").lower())).order_by(L_ophdr.lager_nr).all():
        t_l_ophdr = T_l_ophdr()
        t_l_ophdr_data.append(t_l_ophdr)

        t_l_ophdr.datum = l_ophdr.datum
        t_l_ophdr.lager_nr = l_ophdr.lager_nr
        t_l_ophdr.docu_nr = l_ophdr.docu_nr
        t_l_ophdr.lscheinnr = l_ophdr.lscheinnr

    return generate_output()