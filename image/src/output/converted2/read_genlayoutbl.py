#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Genlayout

def read_genlayoutbl(keystr:string):
    t_genlayout_list = []
    genlayout = None

    t_genlayout = None

    t_genlayout_list, T_genlayout = create_model_like(Genlayout)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_genlayout_list, genlayout
        nonlocal keystr


        nonlocal t_genlayout
        nonlocal t_genlayout_list

        return {"t-genlayout": t_genlayout_list}

    genlayout = get_cache (Genlayout, {"key": [(eq, keystr)]})

    if genlayout:
        t_genlayout = T_genlayout()
        t_genlayout_list.append(t_genlayout)

        buffer_copy(genlayout, t_genlayout)

    return generate_output()