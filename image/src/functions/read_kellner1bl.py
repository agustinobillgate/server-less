from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Kellner

def read_kellner1bl(curr_dept:int, kellner_nr:int, user_init:str):
    t_bediener_list = []
    t_kellner_list = []
    bediener = kellner = None

    t_bediener = t_kellner = None

    t_bediener_list, T_bediener = create_model_like(Bediener)
    t_kellner_list, T_kellner = create_model("T_kellner", {"kellner_nr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, t_kellner_list, bediener, kellner


        nonlocal t_bediener, t_kellner
        nonlocal t_bediener_list, t_kellner_list
        return {"t-bediener": t_bediener_list, "t-kellner": t_kellner_list}


    if user_init != "":

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower()) &  (Bediener.flag == 0)).first()

        if not bediener:

            return generate_output()
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

        kellner = db_session.query(Kellner).filter(
                (kellner_nr == to_int(bediener.userinit)) &  (Kellner.departement == curr_dept)).first()

        if not kellner:

            return generate_output()
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        buffer_copy(kellner, t_kellner)

    elif kellner_nr != 0:

        kellner = db_session.query(Kellner).filter(
                (kellner_nr == kellner_nr) &  (Kellner.departement == curr_dept)).first()

        if not kellner:

            return generate_output()
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        buffer_copy(kellner, t_kellner)

        if kellner_nr < 10:

            bediener = db_session.query(Bediener).filter(
                    (Bediener.userinit == to_string(kellner_nr, "99"))).first()
        else:

            bediener = db_session.query(Bediener).filter(
                    (Bediener.userinit == to_string(kellner_nr))).first()

        if not bediener:

            return generate_output()
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    return generate_output()