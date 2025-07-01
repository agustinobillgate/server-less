#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Queasy

t_bediener_list, T_bediener = create_model_like(Bediener)
t_queasy_list, T_queasy = create_model_like(Queasy)

def benutzer_adminbl(case_type:int, mphone:string, email:string, pager:string, t_bediener_list:[T_bediener], t_queasy_list:[T_queasy]):

    prepare_cache ([Queasy])

    bediener = queasy = None

    t_bediener = t_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, queasy
        nonlocal case_type, mphone, email, pager


        nonlocal t_bediener, t_queasy

        return {}


    if case_type == 1:

        t_bediener = query(t_bediener_list, first=True)

        if t_bediener:
            bediener = Bediener()
            db_session.add(bediener)

            buffer_copy(t_bediener, bediener)

        t_queasy = query(t_queasy_list, first=True)

        if t_queasy:
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(t_queasy, queasy)
    else:

        t_bediener = query(t_bediener_list, first=True)

        if t_bediener:

            bediener = get_cache (Bediener, {"nr": [(eq, t_bediener.nr)]})

            if bediener:
                buffer_copy(t_bediener, bediener)
                pass

        queasy = get_cache (Queasy, {"key": [(eq, 134)],"number1": [(eq, t_bediener.nr)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 134


        else:
            pass
        queasy.number1 = t_bediener.nr
        queasy.char1 = mphone
        queasy.char2 = email
        queasy.char3 = pager


        pass

    return generate_output()