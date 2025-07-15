#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from functions.htpchar import htpchar
from models import Akt_line

def prepare_chg_notesbl(linenr:int):
    record_use = False
    init_time = 0
    init_date = None
    p_400 = ""
    p_405 = ""
    p_406 = ""
    p_407 = ""
    t_akt_line_data = []
    flag_ok:bool = False
    akt_line = None

    t_akt_line = None

    t_akt_line_data, T_akt_line = create_model_like(Akt_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal record_use, init_time, init_date, p_400, p_405, p_406, p_407, t_akt_line_data, flag_ok, akt_line
        nonlocal linenr


        nonlocal t_akt_line
        nonlocal t_akt_line_data

        return {"record_use": record_use, "init_time": init_time, "init_date": init_date, "p_400": p_400, "p_405": p_405, "p_406": p_406, "p_407": p_407, "t-akt-line": t_akt_line_data}


    flag_ok, init_time, init_date = get_output(check_timebl(1, linenr, None, "akt-line", None, None))

    if not flag_ok:
        record_use = True

        return generate_output()

    akt_line = get_cache (Akt_line, {"linenr": [(eq, linenr)]})

    if akt_line:
        t_akt_line = T_akt_line()
        t_akt_line_data.append(t_akt_line)

        buffer_copy(akt_line, t_akt_line)
    p_400 = get_output(htpchar(400))
    p_405 = get_output(htpchar(405))
    p_406 = get_output(htpchar(406))
    p_407 = get_output(htpchar(407))

    return generate_output()