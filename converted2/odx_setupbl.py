#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

t_param_data, T_param = create_model("T_param", {"number":int, "bezeich":string, "val":string})

def odx_setupbl(case_type:int, user_init:string, t_param_data:[T_param]):

    prepare_cache ([Queasy, Bediener, Res_history])

    before:string = ""
    queasy = bediener = res_history = None

    t_param = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal before, queasy, bediener, res_history
        nonlocal case_type, user_init


        nonlocal t_param

        return {"t-param": t_param_data}

    if case_type == 1:

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 1)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 1
            queasy.char1 = "Main Url"
            queasy.char3 = ""

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 2)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 2
            queasy.char1 = "Client ID"
            queasy.char3 = ""

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 3)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 3
            queasy.char1 = "Client Secret"
            queasy.char3 = ""

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 4)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 4
            queasy.char1 = "Cookie"
            queasy.char3 = ""

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 5)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 5
            queasy.char1 = "Property Code"
            queasy.char3 = ""

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 6)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 6
            queasy.char1 = "Terminal ID"
            queasy.char3 = ""

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 7)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 7
            queasy.char1 = "PMS ID"
            queasy.char3 = ""

        queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, 8)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 242
            queasy.number1 = 8
            queasy.char1 = "Logfile Path"
            queasy.char3 = ""

    elif case_type == 2:

        for t_param in query(t_param_data, sort_by=[("number",False)]):

            queasy = get_cache (Queasy, {"key": [(eq, 242)],"number1": [(eq, t_param.number)]})

            if queasy:

                if queasy.char3 != t_param.val:
                    before = queasy.char3
                    queasy.char3 = t_param.val

                    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.action = "ODX Setup"
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Changes From: " + before + " To: " + t_param.val


    t_param_data.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 242) & (Queasy.number1 != 99)).order_by(number1).all():
        t_param = T_param()
        t_param_data.append(t_param)

        t_param.number = queasy.number1
        t_param.bezeich = queasy.char1
        t_param.val = queasy.char3

    return generate_output()