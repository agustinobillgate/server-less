#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.cancel_stockout_btn_gobl import cancel_stockout_btn_gobl

def cancel_stockout_btn_go1bl(from_grp:int, mi_alloc_chk:bool, mi_article_chk:bool, mi_docu_chk:bool, mi_date_chk:bool, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, show_price:bool, cost_acct:string, mattype:int):
    it_exist = False
    cancel_stockout_data = []

    str_list = cancel_stockout = None

    str_list_data, Str_list = create_model("Str_list", {"fibu":string, "other_fibu":bool, "op_recid":int, "lscheinnr":string, "s":string})
    cancel_stockout_data, Cancel_stockout = create_model("Cancel_stockout", {"datum":date, "lager":string, "lscheinnr":string, "artnr":int, "bezeich":string, "out_qty":Decimal, "avrg_price":Decimal, "amount":Decimal, "id":string, "reason":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, cancel_stockout_data
        nonlocal from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, mattype


        nonlocal str_list, cancel_stockout
        nonlocal str_list_data, cancel_stockout_data

        return {"it_exist": it_exist, "cancel-stockout": cancel_stockout_data}
    
    def reformat_date_if_valid(date_str):
        try:
            date_obj = datetime.strptime(date_str, '%m/%d/%y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return date_str

    it_exist, str_list_data = get_output(cancel_stockout_btn_gobl(from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, mattype))
    cancel_stockout_data.clear()

    for str_list in query(str_list_data):
        cancel_stockout = Cancel_stockout()
        cancel_stockout_data.append(cancel_stockout)

        date_str = substring(str_list.s, 0, 8)
        date_formatted = reformat_date_if_valid(date_str)

        cancel_stockout.datum = date_formatted
        cancel_stockout.lager = substring(str_list.s, 8, 30)
        cancel_stockout.artnr = to_int(substring(str_list.s, 38, 7))
        cancel_stockout.bezeich = substring(str_list.s, 45, 32)
        cancel_stockout.out_qty = to_decimal(substring(str_list.s, 77, 14))
        cancel_stockout.avrg_price = to_decimal(substring(str_list.s, 91, 14))
        cancel_stockout.amount = to_decimal(substring(str_list.s, 105, 14))
        cancel_stockout.id = substring(str_list.s, 131, 2)
        cancel_stockout.reason = substring(str_list.s, 141, 24)

        if substring(str_list.s, 119, 12) == "0":
            cancel_stockout.lscheinnr = ""
        else: 
            cancel_stockout.lscheinnr = substring(str_list.s, 119, 12)

    return generate_output()