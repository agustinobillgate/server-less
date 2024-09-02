from functions.additional_functions import *
import decimal
from models import Argt_line

def read_argt_linebl(case_type:int, argtno:int, artno:int, dept:int):
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

    if case_type == 1:

        if artno == None:

            for argt_line in db_session.query(Argt_line).filter(
                    (Argt_line.argtnr == argtno)).all():
                t_argt_line = T_argt_line()
                t_argt_line_list.append(t_argt_line)

                buffer_copy(argt_line, t_argt_line)

            return generate_output()

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line.argtnr == argtno) &  (Argt_line.argt_artnr == artno) &  (Argt_line.departement == dept)).first()

        if argt_line:
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 2:

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line.argtnr == argtno) &  (Argt_line.betrag != 0)).first()

        if argt_line:
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 3:

        argt_line = db_session.query(Argt_line).filter(
                (Argt_line._recid == argtno)).first()

        if argt_line:
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)
    elif case_type == 4:

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == argtno) &  (not Argt_line.kind2)).all():
            t_argt_line = T_argt_line()
            t_argt_line_list.append(t_argt_line)

            buffer_copy(argt_line, t_argt_line)

    return generate_output()