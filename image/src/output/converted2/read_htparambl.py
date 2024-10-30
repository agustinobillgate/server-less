from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam

def read_htparambl(case_type:int, paramno:int, paramgrup:int):
    t_htparam_list = []
    htparam = None

    t_htparam = None

    t_htparam_list, T_htparam = create_model_like(Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_htparam_list, htparam
        nonlocal case_type, paramno, paramgrup


        nonlocal t_htparam
        nonlocal t_htparam_list

        return {"t-htparam": t_htparam_list}

    if case_type == 1:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == paramno)).first()

        if htparam:
            t_htparam = T_htparam()
            t_htparam_list.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 2:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == paramgrup)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_list.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 3:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == paramno) & (Htparam.paramgruppe == paramgrup)).first()

        if htparam:
            t_htparam = T_htparam()
            t_htparam_list.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 4:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramnr <= paramno)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_list.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 5:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramnr >= 1) & (Htparam.paramnr <= 16)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_list.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 6:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == paramgrup)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_list.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 7:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == paramno) & (func.lower(Htparam.bezeich) != ("Not used").lower())).first()

        if htparam:
            t_htparam = T_htparam()
            t_htparam_list.append(t_htparam)

            buffer_copy(htparam, t_htparam)

    return generate_output()