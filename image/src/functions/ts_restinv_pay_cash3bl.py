from functions.additional_functions import *
import decimal
from models import H_artikel, H_bill_line, H_bill, Htparam

def ts_restinv_pay_cash3bl(pvilanguage:int, curr_dept:int, do_it:bool, rec_id:int, balance_foreign:decimal, balance:decimal, double_currency:bool):
    exrate = 0
    msg_str = ""
    t_h_artikel_list = []
    lvcarea:str = "TS_restinv"
    h_artikel = h_bill_line = h_bill = htparam = None

    t_h_artikel = h_bline = h_art = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    H_bline = H_bill_line
    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate, msg_str, t_h_artikel_list, lvcarea, h_artikel, h_bill_line, h_bill, htparam
        nonlocal h_bline, h_art


        nonlocal t_h_artikel, h_bline, h_art
        nonlocal t_h_artikel_list
        return {"exrate": exrate, "msg_str": msg_str, "t-h-artikel": t_h_artikel_list}

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 855)).first()

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept) &  (H_artikel.artnr == htparam.finteger)).first()

    if not h_artikel or h_artikel.artart != 6:
        msg_str = msg_str + chr(2) + translateExtended ("Cash Payment Article not defined. (Param 855 / Grp 19).", lvcarea, "")

        return generate_output()

    if do_it:

        h_bline = db_session.query(H_bline).filter(
                (H_bline.rechnr == h_bill.rechnr) &  (H_bline.departement == h_bill.departement) &  (H_bline.waehrungsnr > 0)).first()

        if h_bline:
            msg_str = msg_str + chr(2) + translateExtended ("Bill has been splitted, use Split Bill's Cash Payment", lvcarea, "")

            return generate_output()

        if balance_foreign != 0:
            exrate = balance / balance_foreign
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    return generate_output()