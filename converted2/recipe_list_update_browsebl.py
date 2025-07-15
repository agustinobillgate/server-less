#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept

def recipe_list_update_browsebl():
    t_h_rezept_data = []
    h_rezept = None

    t_h_rezept = None

    t_h_rezept_data, T_h_rezept = create_model_like(H_rezept)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_rezept_data, h_rezept


        nonlocal t_h_rezept
        nonlocal t_h_rezept_data

        return {"t-h-rezept": t_h_rezept_data}

    for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():
        t_h_rezept = T_h_rezept()
        t_h_rezept_data.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

    return generate_output()