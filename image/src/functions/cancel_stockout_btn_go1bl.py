from functions.additional_functions import *
import decimal
from datetime import date
from functions.cancel_stockout_btn_gobl import cancel_stockout_btn_gobl

def cancel_stockout_btn_go1bl(from_grp:int, mi_alloc_chk:bool, mi_article_chk:bool, mi_docu_chk:bool, mi_date_chk:bool, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, show_price:bool, cost_acct:str, mattype:int):
    it_exist = False
    cancel_stockout_list = []

    str_list = cancel_stockout = None

    str_list_list, Str_list = create_model("Str_list", {"fibu":str, "other_fibu":bool, "op_recid":int, "lscheinnr":str, "s":str})
    cancel_stockout_list, Cancel_stockout = create_model("Cancel_stockout", {"datum":date, "lager":str, "lscheinnr":str, "artnr":int, "bezeich":str, "out_qty":decimal, "avrg_price":decimal, "amount":decimal, "id":str, "reason":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, cancel_stockout_list


        nonlocal str_list, cancel_stockout
        nonlocal str_list_list, cancel_stockout_list
        return {"it_exist": it_exist, "cancel-stockout": cancel_stockout_list}

    it_exist, str_list_list = get_output(cancel_stockout_btn_gobl(from_grp, mi_alloc_chk, mi_article_chk, mi_docu_chk, mi_date_chk, from_lager, to_lager, from_date, to_date, from_art, to_art, show_price, cost_acct, mattype))
    cancel_stockout_list.clear()

    for str_list in query(str_list_list):
        cancel_stockout = Cancel_stockout()
        cancel_stockout_list.append(cancel_stockout)

        cancel_stockout.datum = date_mdy(substring(s, 0, 8))
        cancel_stockout.lager = substring(s, 8, 30)
        cancel_stockout.lscheinnr = substring(s, 119, 12)
        cancel_stockout.artnr = to_int(substring(s, 38, 7))
        cancel_stockout.bezeich = substring(s, 45, 32)
        cancel_stockout.out_qty = decimal.Decimal(substring(s, 77, 14))
        cancel_stockout.avrg_price = decimal.Decimal(substring(s, 91, 14))
        cancel_stockout.amount = decimal.Decimal(substring(s, 105, 14))
        cancel_stockout.id = substring(s, 131, 2)
        cancel_stockout.reason = substring(s, 141, 24)

    return generate_output()