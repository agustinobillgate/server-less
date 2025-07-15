#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def read_usr_listbl(case_type:int, uname:string):
    t_bediener_data = []
    bediener = None

    t_bediener = None

    t_bediener_data, T_bediener = create_model("T_bediener", {"nr":int, "userinit":string, "username":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_data, bediener
        nonlocal case_type, uname


        nonlocal t_bediener
        nonlocal t_bediener_data

        return {"t-bediener": t_bediener_data}

    if case_type == 1:

        bediener = get_cache (Bediener, {"username": [(eq, uname)],"flag": [(eq, 0)],"betriebsnr": [(eq, 1)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        return generate_output()

    elif case_type == 2:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.username == (uname).lower()) & (Bediener.flag == 0) & (Bediener.betriebsnr == 1)).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)


    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.flag == 0)).order_by(Bediener.username).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)


    return generate_output()