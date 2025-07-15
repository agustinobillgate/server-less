#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_types

def read_mc_typesbl(case_type:int, curr_i:int):
    t_mc_types_data = []
    mc_types = None

    t_mc_types = None

    t_mc_types_data, T_mc_types = create_model_like(Mc_types)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mc_types_data, mc_types
        nonlocal case_type, curr_i


        nonlocal t_mc_types
        nonlocal t_mc_types_data

        return {"t-mc-types": t_mc_types_data}

    if case_type == 1:

        mc_types = get_cache (Mc_types, {"nr": [(eq, curr_i)]})

        if mc_types:
            t_mc_types = T_mc_types()
            t_mc_types_data.append(t_mc_types)

            buffer_copy(mc_types, t_mc_types)
    elif case_type == 2:

        for mc_types in db_session.query(Mc_types).filter(
                 (Mc_types.activeflag)).order_by(Mc_types._recid).all():
            t_mc_types = T_mc_types()
            t_mc_types_data.append(t_mc_types)

            buffer_copy(mc_types, t_mc_types)


    return generate_output()