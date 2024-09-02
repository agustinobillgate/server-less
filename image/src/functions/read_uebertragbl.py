from functions.additional_functions import *
import decimal
from datetime import date
from models import Uebertrag

def read_uebertragbl(case_type:int, int1:int, date1:date, date2:date, deci1:decimal):
    t_uebertrag_list = []
    uebertrag = None

    t_uebertrag = None

    t_uebertrag_list, T_uebertrag = create_model_like(Uebertrag)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_uebertrag_list, uebertrag


        nonlocal t_uebertrag
        nonlocal t_uebertrag_list
        return {"t-uebertrag": t_uebertrag_list}

    if case_type == 1:

        for uebertrag in db_session.query(Uebertrag).filter(
                (Uebertrag.datum <= date2) &  (Uebertrag.datum >= date1)).all():
            t_uebertrag = T_uebertrag()
            t_uebertrag_list.append(t_uebertrag)

            buffer_copy(uebertrag, t_uebertrag)

    return generate_output()