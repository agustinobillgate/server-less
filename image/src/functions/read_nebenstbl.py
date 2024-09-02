from functions.additional_functions import *
import decimal
from models import Nebenst

def read_nebenstbl(case_type:int, finroom:str, rechno:int):
    t_nebenst_list = []
    nebenst = None

    t_nebenst = None

    t_nebenst_list, T_nebenst = create_model_like(Nebenst, {"n_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nebenst_list, nebenst


        nonlocal t_nebenst
        nonlocal t_nebenst_list
        return {"t-nebenst": t_nebenst_list}

    if case_type == 1:

        nebenst = db_session.query(Nebenst).filter(
                (Nebenst.zinr == finroom) &  (Nebenst.nebst_type == 3)).first()
    elif case_type == 2:

        nebenst = db_session.query(Nebenst).filter(
                (Nebenst.zinr == finroom) &  (Nebenst.rechnr == rechno)).first()
    elif case_type == 3:

        nebenst = db_session.query(Nebenst).filter(
                (Nebenstelle == finroom)).first()
    elif case_type == 4:

        nebenst = db_session.query(Nebenst).filter(
                (Nebenstelle == finroom) &  (Nebenst._recid != rechno)).first()
    elif case_type == 5:

        nebenst = db_session.query(Nebenst).filter(
                (Nebenstelle == finroom) &  (Nebenst.nebst_type == rechno)).first()

    if nebenst:
        t_nebenst = T_nebenst()
        t_nebenst_list.append(t_nebenst)

        buffer_copy(nebenst, t_nebenst)
        t_nebenst.n_id = nebenst._recid

    return generate_output()