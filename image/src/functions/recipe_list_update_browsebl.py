from functions.additional_functions import *
import decimal
from models import H_rezept

def recipe_list_update_browsebl():
    t_h_rezept_list = []
    h_rezept = None

    t_h_rezept = None

    t_h_rezept_list, T_h_rezept = create_model_like(H_rezept)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_rezept_list, h_rezept


        nonlocal t_h_rezept
        nonlocal t_h_rezept_list
        return {"t-h-rezept": t_h_rezept_list}

    for h_rezept in db_session.query(H_rezept).all():
        t_h_rezept = T_h_rezept()
        t_h_rezept_list.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

    return generate_output()