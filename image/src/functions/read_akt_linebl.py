from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Akt_line

def read_akt_linebl(case_type:int, linenr:int, datum:date, usrinit:str):
    t_akt_line_list = []
    akt_line = None

    t_akt_line = None

    t_akt_line_list, T_akt_line = create_model_like(Akt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_line_list, akt_line


        nonlocal t_akt_line
        nonlocal t_akt_line_list
        return {"t-akt-line": t_akt_line_list}

    if case_type == 1:

        akt_line = db_session.query(Akt_line).filter(
                (Akt_line.linenr == linenr)).first()

        if akt_line:
            t_akt_line = T_akt_line()
            t_akt_line_list.append(t_akt_line)

            buffer_copy(akt_line, t_akt_line)
    elif case_type == 2:

        akt_line = db_session.query(Akt_line).filter(
                (Akt_line.linenr == linenr)).first()

        if akt_line:
            t_akt_line = T_akt_line()
            t_akt_line_list.append(t_akt_line)

            buffer_copy(akt_line, t_akt_line)
    elif case_type == 3:

        akt_line = db_session.query(Akt_line).filter(
                (func.lower(Akt_line.userinit) == (usrinit).lower()) &  (Akt_line.datum >= (datum - 1)) &  (Akt_line.datum <= datum)).first()
        t_akt_line = T_akt_line()
        t_akt_line_list.append(t_akt_line)

        buffer_copy(akt_line, t_akt_line)

    return generate_output()