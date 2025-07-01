#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line

t_argt_line_list, T_argt_line = create_model_like(Argt_line)

def load_argt_line_1bl(case_type:int, argtno:int, argtnr:int, t_argt_line_list:[T_argt_line]):
    argt_line = None

    t_argt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal argt_line
        nonlocal case_type, argtno, argtnr


        nonlocal t_argt_line

        return {"t-argt-line": t_argt_line_list}

    if case_type == 1:

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == argtno)).order_by(Argt_line._recid).all():
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 2:

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == argtnr)).order_by(Argt_line._recid).all():
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)

    return generate_output()