#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nebenst

t_nebenst_data, T_nebenst = create_model_like(Nebenst, {"n_id":int})

def write_nebenstbl(case_type:int, t_nebenst_data:[T_nebenst]):
    success_flag = False
    nebenst = None

    t_nebenst = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nebenst
        nonlocal case_type


        nonlocal t_nebenst

        return {"success_flag": success_flag}

    t_nebenst = query(t_nebenst_data, first=True)

    if not t_nebenst:

        return generate_output()

    if case_type == 1:
        nebenst = Nebenst()
        db_session.add(nebenst)

        buffer_copy(t_nebenst, nebenst)
        pass
        success_flag = True
    elif case_type == 2:

        nebenst = get_cache (Nebenst, {"_recid": [(eq, t_nebenst.n_id)]})

        if nebenst:
            buffer_copy(t_nebenst, nebenst)
            pass
            success_flag = True

    return generate_output()