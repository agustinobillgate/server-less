#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line

def read_argt_line_1bl(case_type:int, argtno:int, artno:int, dept:int, vt_percnt:int):
    t_argt_line_list = []
    argt_line = None

    t_argt_line = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_argt_line_list, argt_line
        nonlocal case_type, argtno, artno, dept, vt_percnt


        nonlocal t_argt_line
        nonlocal t_argt_line_list

        return {"t-argt-line": t_argt_line_list}

    if case_type == 1:

        if artno == None:

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == argtno)).order_by(Argt_line._recid).all():
                t_argt_line = T_argt_line()
                t_argt_line_list.append(t_argt_line)

                buffer_copy(argt_line, t_argt_line)

            return generate_output()

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, argtno)],"argt_artnr": [(eq, artno)],"departement": [(eq, dept)]})

        if argt_line:
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 2:

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, argtno)],"betrag": [(ne, 0)]})

        if argt_line:
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 3:

        argt_line = get_cache (Argt_line, {"_recid": [(eq, argtno)]})

        if argt_line:
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 4:

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == argtno) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 5:

        if artno == None:

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == argtno) & (Argt_line.vt_percnt == vt_percnt)).order_by(Argt_line._recid).all():
                t_argt_line = T_argt_line()
                t_argt_line_list.append(t_argt_line)

                buffer_copy(argt_line, t_argt_line)

            return generate_output()

        argt_line = get_cache (Argt_line, {"argtnr": [(eq, argtno)],"argt_artnr": [(eq, artno)],"departement": [(eq, dept)],"vt_percnt": [(eq, vt_percnt)]})

        if argt_line:
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)

    return generate_output()