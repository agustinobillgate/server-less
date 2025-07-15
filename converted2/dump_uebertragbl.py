#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Uebertrag

def dump_uebertragbl():
    t_uebertrag_data = []
    uebertrag = None

    t_uebertrag = None

    t_uebertrag_data, T_uebertrag = create_model_like(Uebertrag)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_uebertrag_data, uebertrag


        nonlocal t_uebertrag
        nonlocal t_uebertrag_data

        return {"t-uebertrag": t_uebertrag_data}

    for uebertrag in db_session.query(Uebertrag).order_by(Uebertrag._recid).all():
        t_uebertrag = T_uebertrag()
        t_uebertrag_data.append(t_uebertrag)

        buffer_copy(uebertrag, t_uebertrag)

    return generate_output()