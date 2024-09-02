from functions.additional_functions import *
import decimal
from models import Nebenst

def write_nebenstbl(case_type:int, t_nebenst:[T_nebenst]):
    success_flag = False
    nebenst = None

    t_nebenst = None

    t_nebenst_list, T_nebenst = create_model_like(Nebenst, {"n_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nebenst


        nonlocal t_nebenst
        nonlocal t_nebenst_list
        return {"success_flag": success_flag}

    t_nebenst = query(t_nebenst_list, first=True)

    if not t_nebenst:

        return generate_output()

    if case_type == 1:
        nebenst = Nebenst()
        db_session.add(nebenst)

        buffer_copy(t_nebenst, nebenst)

        success_flag = True
    elif case_type == 2:

        nebenst = db_session.query(Nebenst).filter(
                (Nebenst._recid == t_Nebenst.n_id)).first()

        if nebenst:
            buffer_copy(t_nebenst, nebenst)

            success_flag = True

    return generate_output()