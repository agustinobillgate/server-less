#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, Htparam

def prepare_ts_splititembl(h_recid:int):

    prepare_cache ([Htparam])

    price_decimal = 0
    double_currency = False
    curr_qty = 0
    t_h_bill_line_list = []
    h_bill_line = htparam = None

    t_h_bill_line = None

    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, double_currency, curr_qty, t_h_bill_line_list, h_bill_line, htparam
        nonlocal h_recid


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_list

        return {"price_decimal": price_decimal, "double_currency": double_currency, "curr_qty": curr_qty, "t-h-bill-line": t_h_bill_line_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, h_recid)]})
    curr_qty = h_bill_line.anzahl
    t_h_bill_line = T_h_bill_line()
    t_h_bill_line_list.append(t_h_bill_line)

    buffer_copy(h_bill_line, t_h_bill_line)
    t_h_bill_line.rec_id = h_bill_line._recid

    return generate_output()