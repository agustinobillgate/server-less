from functions.additional_functions import *
import decimal
from datetime import date
from functions.ts_restinv_calculate_amountbl import ts_restinv_calculate_amountbl
from models import H_artikel

def ts_restinv_run_help3bl(menu_list_artnr:int, menu_list_bezeich:str, menu_list_anzahl:int, menu_list_price:decimal, curr_dept:int, cancel_reason:str, double_currency:bool, exchg_rate:decimal, price_decimal:int, transdate:date, cancel_flag:bool, foreign_rate:bool):
    description = ""
    qty = 0
    price = 0
    cancel_str = ""
    amount_foreign = 0
    amount = 0
    fl_code = 0
    fl_code1 = 0
    t_h_artikel_list = []
    h_artikel = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal description, qty, price, cancel_str, amount_foreign, amount, fl_code, fl_code1, t_h_artikel_list, h_artikel


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list
        return {"description": description, "qty": qty, "price": price, "cancel_str": cancel_str, "amount_foreign": amount_foreign, "amount": amount, "fl_code": fl_code, "fl_code1": fl_code1, "t-h-artikel": t_h_artikel_list}

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == menu_list_artnr) &  (H_artikel.departement == curr_dept)).first()
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    buffer_copy(h_artikel, t_h_artikel)
    t_h_artikel.rec_id = h_artikel._recid


    description = menu_list_bezeich
    qty = menu_list_anzahl
    price = menu_list_price

    if qty < 0:
        cancel_str = cancel_reason
    price, amount_foreign, amount, fl_code, fl_code1 = get_output(ts_restinv_calculate_amountbl(h_artikel._recid, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate))

    return generate_output()