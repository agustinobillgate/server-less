from functions.additional_functions import *
import decimal
from models import H_artikel, Htparam

def ts_closeinv_prepare_pay_cashbl(curr_dept:int, cash_foreign:bool, pay_voucher:bool):
    cash_artnr = 0
    p_854:int = 0
    p_855:int = 0
    p_1001:int = 0
    h_artikel = htparam = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cash_artnr, p_854, p_855, p_1001, h_artikel, htparam


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list
        return {"cash_artnr": cash_artnr}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 854)).first()
    p_854 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 855)).first()
    p_855 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1001)).first()
    p_1001 = htparam.finteger

    if cash_foreign:
        cash_artnr = p_854
    else:

        if not pay_voucher:
            cash_artnr = p_855
        else:
            cash_artnr = p_1001

    return generate_output()