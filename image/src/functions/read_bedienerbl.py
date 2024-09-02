from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener

def read_bedienerbl(userno:int, user_init:str):
    t_bediener_list = []
    bediener = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, bediener


        nonlocal t_bediener
        nonlocal t_bediener_list
        return {"t-bediener": t_bediener_list}

    if user_init == "&Sales Group":

        for bediener in db_session.query(Bediener).filter(
                (Bediener.user_group == userno) &  (Bediener.flag == 0)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        return generate_output()

    if user_init != "":

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if not bediener:

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.username) == (user_init).lower())).first()

    elif userno != 0:

        bediener = db_session.query(Bediener).filter(
                (Bediener.nr == userno)).first()

    if bediener:
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    return generate_output()