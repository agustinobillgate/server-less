#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill_line, Htparam, Waehrung, H_bill

def prepare_ts_disc1_1bl(dept:int, tischnr:int):

    prepare_cache ([Htparam, Waehrung, H_bill])

    price_decimal = 0
    exchg_rate = to_decimal("0.0")
    p_134 = False
    p_135 = False
    p_479 = False
    t_h_bill_line_data = []
    h_bill_line = htparam = waehrung = h_bill = None

    t_h_bill_line = None

    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, exchg_rate, p_134, p_135, p_479, t_h_bill_line_data, h_bill_line, htparam, waehrung, h_bill
        nonlocal dept, tischnr


        nonlocal t_h_bill_line
        nonlocal t_h_bill_line_data

        return {"price_decimal": price_decimal, "exchg_rate": exchg_rate, "p_134": p_134, "p_135": p_135, "p_479": p_479, "t-h-bill-line": t_h_bill_line_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam:

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


        else:
            exchg_rate =  to_decimal("1")

    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"tischnr": [(eq, tischnr)],"flag": [(eq, 0)]})

    if h_bill:

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == dept)).order_by(H_bill_line.bezeich).all():
            t_h_bill_line = T_h_bill_line()
            t_h_bill_line_data.append(t_h_bill_line)

            buffer_copy(h_bill_line, t_h_bill_line)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})

    if htparam:
        p_134 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})

    if htparam:
        p_135 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})

    if htparam:
        p_479 = htparam.flogical

    return generate_output()