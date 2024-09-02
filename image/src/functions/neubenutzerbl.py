from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener

def neubenutzerbl(case_type:int, name_str:str, id_str:str, nr:int):
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

    if case_type == 1:

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (name_str).lower()) &  (Bediener.flag == 0)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 2:

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (name_str).lower()) &  (func.lower(Bediener.usercode) == (id_str).lower()) &  (Bediener.betriebsnr == 0) &  (Bediener.flag == 0)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (name_str).lower()) &  (Bediener.betriebsnr == 1) &  (Bediener.flag == 0)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 4:

        bediener = db_session.query(Bediener).filter(
                (Bediener.nr == nr)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    return generate_output()