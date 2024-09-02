from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener

def load_bedienerbl(case_type:int, int1:int, int2:int, char1:str):
    t_bediener_list = []
    bediener = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, bediener


        nonlocal t_bediener
        nonlocal t_bediener_list
        return {"t-bediener": t_bediener_list}

    if case_type == 1:

        for bediener in db_session.query(Bediener).filter(
                (Bediener.flag == int1) &  (func.lower(Bediener.username) >= (char1).lower())).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 2:

        for bediener in db_session.query(Bediener).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                (Bediener.flag == int1)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 4:

        bediener = db_session.query(Bediener).filter(
                (Bediener.user_group == int1) &  (Bediener.flag == int2)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 5:

        bediener = db_session.query(Bediener).filter(
                (Bediener._recid == int1)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid
    elif case_type == 6:

        for bediener in db_session.query(Bediener).filter(
                (Bediener.nr != 0)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
            t_bediener.rec_id = bediener._recid

    return generate_output()