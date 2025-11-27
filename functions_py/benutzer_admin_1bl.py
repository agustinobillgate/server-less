#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Queasy, Res_history

t_bediener_data, T_bediener = create_model_like(Bediener)
t_queasy_data, T_queasy = create_model_like(Queasy)

def benutzer_admin_1bl(case_type:int, mphone:string, email:string, pager:string, userinit:string, t_bediener_data:[T_bediener], t_queasy_data:[T_queasy]):

    prepare_cache ([Bediener, Queasy, Res_history])

    bediener = queasy = res_history = None

    t_bediener = t_queasy = None

    db_session = local_storage.db_session
    mphone = mphone.strip()
    email = email.strip()
    pager = pager.strip()
    userinit = userinit.strip()

    def generate_output():
        nonlocal bediener, queasy, res_history
        nonlocal case_type, mphone, email, pager, userinit


        nonlocal t_bediener, t_queasy

        return {}


    if case_type == 1:

        t_bediener = query(t_bediener_data, first=True)

        if t_bediener:
            bediener = Bediener()
            db_session.add(bediener)

            buffer_copy(t_bediener, bediener)

        t_queasy = query(t_queasy_data, first=True)

        if t_queasy:
            queasy = Queasy()
            db_session.add(queasy)

            buffer_copy(t_queasy, queasy)

        bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "User"
            res_history.aenderung = "Create New User For " + t_bediener.username


    else:

        t_bediener = query(t_bediener_data, first=True)

        if t_bediener:

            bediener = get_cache (Bediener, {"nr": [(eq, t_bediener.nr)]})

            if bediener:
                buffer_copy(t_bediener, bediener)
                pass

        # queasy = get_cache (Queasy, {"key": [(eq, 134)],"number1": [(eq, t_bediener.nr)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 134) &
                 (Queasy.number1 == t_bediener.nr)).with_for_update().first()

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

        bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "User"
            res_history.aenderung = "Update User Data For " + t_bediener.username

    return generate_output()