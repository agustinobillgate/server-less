from functions.additional_functions import *
import decimal
from models import Argt_line

def load_argt_linebl(argtno:int):
    t_argt_line_list = []
    argt_line = None

    t_argt_line = None

    t_argt_line_list, T_argt_line = create_model_like(Argt_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_argt_line_list, argt_line


        nonlocal t_argt_line
        nonlocal t_argt_line_list
        return {"t-argt-line": t_argt_line_list}

    for argt_line in db_session.query(Argt_line).filter(
            (Argt_line.argtnr == argtno)).all():
        t_argt_line = T_argt_line()
        t_argt_line_list.append(t_argt_line)

        buffer_copy(argt_line, t_argt_line)

    return generate_output()