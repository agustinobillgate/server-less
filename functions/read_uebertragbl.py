#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Uebertrag

def read_uebertragbl(case_type:int, int1:int, date1:date, date2:date, deci1:Decimal):
    t_uebertrag_data = []
    uebertrag = None

    t_uebertrag = None

    t_uebertrag_data, T_uebertrag = create_model_like(Uebertrag)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_uebertrag_data, uebertrag
        nonlocal case_type, int1, date1, date2, deci1


        nonlocal t_uebertrag
        nonlocal t_uebertrag_data

        return {"t-uebertrag": t_uebertrag_data}

    if case_type == 1:

        for uebertrag in db_session.query(Uebertrag).filter(
                 (Uebertrag.datum <= date2) & (Uebertrag.datum >= date1)).order_by(Uebertrag.datum).all():
            t_uebertrag = T_uebertrag()
            t_uebertrag_data.append(t_uebertrag)

            buffer_copy(uebertrag, t_uebertrag)

    return generate_output()