#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nebenst

def read_nebenstbl(case_type:int, finroom:string, rechno:int):
    t_nebenst_data = []
    nebenst = None

    t_nebenst = None

    t_nebenst_data, T_nebenst = create_model_like(Nebenst, {"n_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nebenst_data, nebenst
        nonlocal case_type, finroom, rechno


        nonlocal t_nebenst
        nonlocal t_nebenst_data

        return {"t-nebenst": t_nebenst_data}

    if case_type == 1:

        nebenst = get_cache (Nebenst, {"zinr": [(eq, finroom)],"nebst_type": [(eq, 3)]})
    elif case_type == 2:

        nebenst = get_cache (Nebenst, {"zinr": [(eq, finroom)],"rechnr": [(eq, rechno)]})
    elif case_type == 3:

        nebenst = get_cache (Nebenst, {"nebenstelle": [(eq, finroom)]})
    elif case_type == 4:

        nebenst = get_cache (Nebenst, {"nebenstelle": [(eq, finroom)],"_recid": [(ne, rechno)]})
    elif case_type == 5:

        nebenst = get_cache (Nebenst, {"nebenstelle": [(eq, finroom)],"nebst_type": [(eq, rechno)]})

    if nebenst:
        t_nebenst = T_nebenst()
        t_nebenst_data.append(t_nebenst)

        buffer_copy(nebenst, t_nebenst)
        t_nebenst.n_id = nebenst._recid

    return generate_output()