#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def read_bedienerbl(userno:int, user_init:string):
    t_bediener_list = []
    bediener = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, bediener
        nonlocal userno, user_init


        nonlocal t_bediener
        nonlocal t_bediener_list

        return {"t-bediener": t_bediener_list}

    if user_init.lower()  == ("&Sales Group").lower() :

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.user_group == userno) & (Bediener.flag == 0)).order_by(Bediener.username).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        return generate_output()

    if user_init != "":

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if not bediener:

            bediener = get_cache (Bediener, {"username": [(eq, user_init)]})

    elif userno != 0:

        bediener = get_cache (Bediener, {"nr": [(eq, userno)]})

    if bediener:
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    return generate_output()