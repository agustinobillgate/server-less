#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mast_art

def read_mast_artbl(case_type:int, int1:int, int2:int, int3:int, int4:int, int5:int):
    t_mast_art_list = []
    mast_art = None

    t_mast_art = None

    t_mast_art_list, T_mast_art = create_model_like(Mast_art)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mast_art_list, mast_art
        nonlocal case_type, int1, int2, int3, int4, int5


        nonlocal t_mast_art
        nonlocal t_mast_art_list

        return {"t-mast-art": t_mast_art_list}

    if case_type == 1:

        for mast_art in db_session.query(Mast_art).filter(
                 (Mast_art.resnr == int1)).order_by(Mast_art._recid).all():
            t_mast_art = T_mast_art()
            t_mast_art_list.append(t_mast_art)

            buffer_copy(mast_art, t_mast_art)

    elif case_type == 2:

        mast_art = get_cache (Mast_art, {"resnr": [(eq, int1)],"departement": [(eq, int2)],"artnr": [(eq, int3)]})

        if mast_art:
            t_mast_art = T_mast_art()
            t_mast_art_list.append(t_mast_art)

            buffer_copy(mast_art, t_mast_art)

    return generate_output()