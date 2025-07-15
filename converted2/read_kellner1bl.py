#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Kellner

def read_kellner1bl(curr_dept:int, kellner_nr:int, user_init:string):
    t_bediener_data = []
    t_kellner_data = []
    bediener = kellner = None

    t_bediener = t_kellner = None

    t_bediener_data, T_bediener = create_model_like(Bediener)
    t_kellner_data, T_kellner = create_model("T_kellner", {"kellner_nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_data, t_kellner_data, bediener, kellner
        nonlocal curr_dept, kellner_nr, user_init


        nonlocal t_bediener, t_kellner
        nonlocal t_bediener_data, t_kellner_data

        return {"t-bediener": t_bediener_data, "t-kellner": t_kellner_data}


    if user_init != "":

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)],"flag": [(eq, 0)]})

        if not bediener:

            return generate_output()
        t_bediener = T_bediener()
        t_bediener_data.append(t_bediener)

        buffer_copy(bediener, t_bediener)

        kellner = get_cache (Kellner, {"kellner_nr": [(eq, to_int(bediener.userinit))],"departement": [(eq, curr_dept)]})

        if not kellner:

            return generate_output()
        t_kellner = T_kellner()
        t_kellner_data.append(t_kellner)

        buffer_copy(kellner, t_kellner)

    elif kellner_nr != 0:

        kellner = get_cache (Kellner, {"kellner_nr": [(eq, kellner_nr)],"departement": [(eq, curr_dept)]})

        if not kellner:

            return generate_output()
        t_kellner = T_kellner()
        t_kellner_data.append(t_kellner)

        buffer_copy(kellner, t_kellner)

        if kellner.kellner_nr < 10:

            bediener = get_cache (Bediener, {"userinit": [(eq, to_string(kellner.kellner_nr, "99"))]})
        else:

            bediener = get_cache (Bediener, {"userinit": [(eq, to_string(kellner.kellner_nr))]})

        if not bediener:

            return generate_output()
        t_bediener = T_bediener()
        t_bediener_data.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    return generate_output()