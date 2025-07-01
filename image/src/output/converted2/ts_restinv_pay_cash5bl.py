#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Htparam

def ts_restinv_pay_cash5bl(multi_cash:bool, cash_artno:int, cash_foreign:bool, pay_voucher:bool, curr_dept:int, voucher_nr:string, amount:Decimal):

    prepare_cache ([Htparam])

    billart = 0
    qty = to_decimal("0.0")
    description = ""
    p_88 = False
    t_h_artikel_list = []
    local_curr_code:string = ""
    h_artikel = htparam = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billart, qty, description, p_88, t_h_artikel_list, local_curr_code, h_artikel, htparam
        nonlocal multi_cash, cash_artno, cash_foreign, pay_voucher, curr_dept, voucher_nr, amount


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        return {"billart": billart, "qty": qty, "description": description, "p_88": p_88, "t-h-artikel": t_h_artikel_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    if htparam:
        local_curr_code = htparam.fchar

    if multi_cash and cash_artno != 0:
        billart = cash_artno
    else:

        if cash_foreign:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 854)]})
        else:

            if not pay_voucher:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 855)]})
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})
        billart = htparam.finteger

    h_artikel = get_cache (H_artikel, {"departement": [(eq, curr_dept)],"artnr": [(eq, billart)]})
    qty =  to_decimal("1")
    description = h_artikel.bezeich

    if voucher_nr.lower()  != "" and voucher_nr.lower()  != ("0").lower() :
        description = description + " " + voucher_nr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 88)]})
    p_88 = htparam.flogical
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    if local_curr_code.lower()  != ("Rp").lower() :
        description = "Cash" + " " + local_curr_code

        if voucher_nr.lower()  != "" and voucher_nr.lower()  != ("0").lower() :
            description = description + " " + voucher_nr
        t_h_artikel.bezeich = "Cash" + " " + local_curr_code

    return generate_output()