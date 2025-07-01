#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_line

def read_akt_linebl(case_type:int, linenr:int, datum:date, usrinit:string):
    t_akt_line_list = []
    akt_line = None

    t_akt_line = None

    t_akt_line_list, T_akt_line = create_model_like(Akt_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_line_list, akt_line
        nonlocal case_type, linenr, datum, usrinit


        nonlocal t_akt_line
        nonlocal t_akt_line_list

        return {"t-akt-line": t_akt_line_list}

    if case_type == 1:

        akt_line = get_cache (Akt_line, {"linenr": [(eq, linenr)]})

        if akt_line:
            t_akt_line = T_akt_line()
            t_akt_line_list.append(t_akt_line)

            buffer_copy(akt_line, t_akt_line)
    elif case_type == 2:

        akt_line = get_cache (Akt_line, {"linenr": [(eq, linenr)]})

        if akt_line:
            t_akt_line = T_akt_line()
            t_akt_line_list.append(t_akt_line)

            buffer_copy(akt_line, t_akt_line)
    elif case_type == 3:

        akt_line = get_cache (Akt_line, {"userinit": [(eq, usrinit)],"datum": [(ge, datum - timedelta(days=1)),(le, datum)]})
        t_akt_line = T_akt_line()
        t_akt_line_list.append(t_akt_line)

        buffer_copy(akt_line, t_akt_line)

    return generate_output()