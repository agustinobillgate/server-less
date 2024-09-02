from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Genlayout

def read_genlayoutbl(keystr:str):
    t_genlayout_list = []
    genlayout = None

    t_genlayout = None

    t_genlayout_list, T_genlayout = create_model_like(Genlayout)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_genlayout_list, genlayout


        nonlocal t_genlayout
        nonlocal t_genlayout_list
        return {"t-genlayout": t_genlayout_list}

    genlayout = db_session.query(Genlayout).filter(
            (func.lower(Genlayout.key) == (keystr).lower())).first()

    if genlayout:
        t_genlayout = T_genlayout()
        t_genlayout_list.append(t_genlayout)

        buffer_copy(genlayout, t_genlayout)

    return generate_output()