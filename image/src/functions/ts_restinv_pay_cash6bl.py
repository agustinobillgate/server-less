from functions.additional_functions import *
import decimal
from models import H_artikel, Htparam

def ts_restinv_pay_cash6bl(curr_dept:int):
    p_855 = 0
    t_h_artikel_list = []
    h_artikel = htparam = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_855, t_h_artikel_list, h_artikel, htparam


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list
        return {"p_855": p_855, "t-h-artikel": t_h_artikel_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 855)).first()
    p_855 = htparam.finteger

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept) &  (H_artikel.artnr == htparam.finteger)).first()
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    return generate_output()