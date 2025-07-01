#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Uebertrag

def dump_uebertragbl():
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

    for uebertrag in db_session.query(Uebertrag).order_by(Uebertrag._recid).all():
        t_uebertrag = T_uebertrag()
        t_uebertrag_list.append(t_uebertrag)

        buffer_copy(uebertrag, t_uebertrag)

    return generate_output()