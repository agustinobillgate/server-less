#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd 3/8/2025
# if not availble -> return

# yusufwijasena, 24/12/2025
# - add validation for balance_foreign and balance
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, H_bill_line, H_bill, Htparam

from functions import log_program as log

def ts_restinv_pay_cash3bl(pvilanguage:int, curr_dept:int, do_it:bool, rec_id:int, balance_foreign:Decimal, balance:Decimal, double_currency:bool):

    prepare_cache ([H_bill, Htparam])

    exrate = to_decimal("0.0")
    msg_str = ""
    t_h_artikel_data = []
    lvcarea:string = "TS-restinv"
    h_artikel = h_bill_line = h_bill = htparam = None

    t_h_artikel = h_bline = h_art = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    H_bline = create_buffer("H_bline",H_bill_line)
    H_art = create_buffer("H_art",H_artikel)
    
    # add validation for balance_foreign and balance
    if balance_foreign is None:
        balance_foreign = 0
    if balance is None:
        balance = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate, msg_str, t_h_artikel_data, lvcarea, h_artikel, h_bill_line, h_bill, htparam
        nonlocal pvilanguage, curr_dept, do_it, rec_id, balance_foreign, balance, double_currency
        nonlocal h_bline, h_art
        nonlocal t_h_artikel, h_bline, h_art
        nonlocal t_h_artikel_data

        return {
            "exrate": exrate, 
            "msg_str": msg_str, 
            "t-h-artikel": t_h_artikel_data
            }

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})
    # Rd 3/8/2025
    # if not avail return
    if h_bill is None:
        return generate_output()
    
    htparam = get_cache (Htparam, {"paramnr": [(eq, 855)]})

    h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, htparam.finteger)]})

    if not h_artikel or h_artikel.artart != 6:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Cash Payment Article not defined. (Param 855 / Grp 19).", lvcarea, "")

        return generate_output()

    if do_it:

        h_bline = db_session.query(H_bline).filter(
                 (H_bline.rechnr == h_bill.rechnr) & 
                 (H_bline.departement == h_bill.departement) & 
                 (H_bline.waehrungsnr > 0)).first()

        if h_bline:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Bill has been splitted, use Split Bill's Cash Payment", lvcarea, "")

            return generate_output()

        if balance_foreign != 0:
            # log.write_log ("TS-Restinv-Pay-Cash3BL", f"[LOG] balance_foreign: {balance_foreign}, balance: {balance}")
            exrate =  to_decimal(balance) / to_decimal(balance_foreign)
    t_h_artikel = T_h_artikel()
    t_h_artikel_data.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    return generate_output()