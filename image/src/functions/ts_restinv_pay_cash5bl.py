from functions.additional_functions import *
import decimal
from models import H_artikel, Htparam

def ts_restinv_pay_cash5bl(multi_cash:bool, cash_artno:int, cash_foreign:bool, pay_voucher:bool, curr_dept:int, voucher_nr:str, amount:decimal):
    billart = 0
    qty = 0
    description = ""
    p_88 = False
    t_h_artikel_list = []
    h_artikel = htparam = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, p_88, t_h_artikel_list, h_artikel, htparam


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list
        return {"billart": billart, "qty": qty, "description": description, "p_88": p_88, "t-h-artikel": t_h_artikel_list}

    if multi_cash and cash_artno != 0:
        billart = cash_artno
    else:

        if cash_foreign:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 854)).first()
        else:

            if not pay_voucher:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 855)).first()
            else:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 1001)).first()
        billart = htparam.finteger

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept) &  (H_artikel.artnr == billart)).first()
    qty = 1
    description = h_artikel.bezeich

    if voucher_nr != "":
        description = description + " " + voucher_nr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 88)).first()
    p_88 = htparam.flogical
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    return generate_output()