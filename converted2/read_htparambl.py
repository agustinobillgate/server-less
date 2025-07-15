#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def read_htparambl(case_type:int, paramno:int, paramgrup:int):
    t_htparam_data = []
    htparam = None

    t_htparam = None

    t_htparam_data, T_htparam = create_model_like(Htparam)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_htparam_data, htparam
        nonlocal case_type, paramno, paramgrup


        nonlocal t_htparam
        nonlocal t_htparam_data

        return {"t-htparam": t_htparam_data}

    if case_type == 1:

        htparam = get_cache (Htparam, {"paramnr": [(eq, paramno)]})

        if htparam:
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 2:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == paramgrup)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 3:

        htparam = get_cache (Htparam, {"paramnr": [(eq, paramno)],"paramgruppe": [(eq, paramgrup)]})

        if htparam:
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 4:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramnr <= paramno)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 5:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramnr >= 1) & (Htparam.paramnr <= 16)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 6:

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == paramgrup)).order_by(Htparam._recid).all():
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)
    elif case_type == 7:

        htparam = get_cache (Htparam, {"paramnr": [(eq, paramno)],"bezeichnung": [(ne, "not used")]})

        if htparam:
            t_htparam = T_htparam()
            t_htparam_data.append(t_htparam)

            buffer_copy(htparam, t_htparam)

    return generate_output()