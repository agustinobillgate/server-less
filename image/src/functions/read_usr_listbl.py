from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener

def read_usr_listbl(case_type:int, uname:str):
    t_bediener_list = []
    bediener = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model("T_bediener", {"nr":int, "userinit":str, "username":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, bediener


        nonlocal t_bediener
        nonlocal t_bediener_list
        return {"t-bediener": t_bediener_list}

    if case_type == 1:

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (uname).lower()) &  (Bediener.flag == 0) &  (Bediener.betriebsnr == 1)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        return generate_output()

    elif case_type == 2:

        for bediener in db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (uname).lower()) &  (Bediener.flag == 0) &  (Bediener.betriebsnr == 1)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)


    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                (Bediener.flag == 0)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)


    return generate_output()