#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, H_bill_line

def ts_restinv_cancel_order2bl(rec_id_h_art:int, rec_id_hbline:int):

    prepare_cache ([H_bill_line])

    answer = False
    cancel_flag = False
    billart = 0
    description = ""
    price = to_decimal("0.0")
    t_h_artikel_data = []
    h_artikel = h_bill_line = None

    t_h_artikel = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal answer, cancel_flag, billart, description, price, t_h_artikel_data, h_artikel, h_bill_line
        nonlocal rec_id_h_art, rec_id_hbline


        nonlocal t_h_artikel
        nonlocal t_h_artikel_data

        return {"answer": answer, "cancel_flag": cancel_flag, "billart": billart, "description": description, "price": price, "t-h-artikel": t_h_artikel_data}

    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, rec_id_hbline)]})

    if not h_bill_line:

        return generate_output()
    answer = False
    cancel_flag = True

    h_artikel = get_cache (H_artikel, {"_recid": [(eq, rec_id_h_art)]})
    billart = h_bill_line.artnr
    description = h_bill_line.bezeich
    price =  to_decimal(h_bill_line.epreis)
    t_h_artikel = T_h_artikel()
    t_h_artikel_data.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid

    return generate_output()