from functions.additional_functions import *
import decimal
from models import Mc_types

def read_mc_typesbl(case_type:int, curr_i:int):
    t_mc_types_list = []
    mc_types = None

    t_mc_types = None

    t_mc_types_list, T_mc_types = create_model_like(Mc_types)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_mc_types_list, mc_types


        nonlocal t_mc_types
        nonlocal t_mc_types_list
        return {"t-mc-types": t_mc_types_list}

    if case_type == 1:

        mc_types = db_session.query(Mc_types).filter(
                (Mc_types.nr == curr_i)).first()

        if mc_types:
            t_mc_types = T_mc_types()
            t_mc_types_list.append(t_mc_types)

            buffer_copy(mc_types, t_mc_types)
    elif case_type == 2:

        for mc_types in db_session.query(Mc_types).filter(
                (Mc_types.activeflag)).all():
            t_mc_types = T_mc_types()
            t_mc_types_list.append(t_mc_types)

            buffer_copy(mc_types, t_mc_types)


    return generate_output()