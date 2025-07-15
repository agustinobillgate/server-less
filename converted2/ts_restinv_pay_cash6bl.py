#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Htparam

def ts_restinv_pay_cash6bl(curr_dept:int):

    prepare_cache ([Htparam])

    p_855 = 0
    t_h_artikel_data = []
    h_artikel = htparam = None

    t_h_artikel = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_855, t_h_artikel_data, h_artikel, htparam
        nonlocal curr_dept


        nonlocal t_h_artikel
        nonlocal t_h_artikel_data

        return {"p_855": p_855, "t-h-artikel": t_h_artikel_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 855)]})
    p_855 = htparam.finteger

    h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, htparam.finteger)]})
    t_h_artikel = T_h_artikel()
    t_h_artikel_data.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    return generate_output()