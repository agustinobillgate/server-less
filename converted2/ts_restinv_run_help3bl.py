#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ts_restinv_calculate_amountbl import ts_restinv_calculate_amountbl
from models import H_artikel

def ts_restinv_run_help3bl(menu_list_artnr:int, menu_list_bezeich:string, menu_list_anzahl:int, menu_list_price:Decimal, curr_dept:int, cancel_reason:string, double_currency:bool, exchg_rate:Decimal, price_decimal:int, transdate:date, cancel_flag:bool, foreign_rate:bool):
    description = ""
    qty = 0
    price = to_decimal("0.0")
    cancel_str = ""
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    fl_code = 0
    fl_code1 = 0
    t_h_artikel_data = []
    h_artikel = None

    t_h_artikel = None

    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal description, qty, price, cancel_str, amount_foreign, amount, fl_code, fl_code1, t_h_artikel_data, h_artikel
        nonlocal menu_list_artnr, menu_list_bezeich, menu_list_anzahl, menu_list_price, curr_dept, cancel_reason, double_currency, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate


        nonlocal t_h_artikel
        nonlocal t_h_artikel_data

        return {"description": description, "qty": qty, "price": price, "cancel_str": cancel_str, "amount_foreign": amount_foreign, "amount": amount, "fl_code": fl_code, "fl_code1": fl_code1, "t-h-artikel": t_h_artikel_data}

    h_artikel = get_cache (H_artikel, {"artnr": [(eq, menu_list_artnr)],"departement": [(eq, curr_dept)]})
    t_h_artikel = T_h_artikel()
    t_h_artikel_data.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid


    description = menu_list_bezeich
    qty = menu_list_anzahl
    price =  to_decimal(menu_list_price)

    if qty < 0:
        cancel_str = cancel_reason
    price, amount_foreign, amount, fl_code, fl_code1 = get_output(ts_restinv_calculate_amountbl(h_artikel._recid, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate))

    return generate_output()