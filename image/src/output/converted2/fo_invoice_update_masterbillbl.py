#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.i_inv_ar import *
from functions.i_update_masterbl import *
from functions.i_master_taxserv import *
from models import Bill, Artikel

def fo_invoice_update_masterbillbl(pvilanguage:int, bil_recid:int, curr_department:int, currzeit:int, amount:Decimal, amount_foreign:Decimal, billart:int, description:string, qty:int, curr_room:string, user_init:string, artnr:int, price:Decimal, cancel_str:string, exchg_rate:Decimal, price_decimal:int, double_currency:bool, master_flag:bool):
    ex_rate = to_decimal("0.0")
    mess_str = ""
    master_str = ""
    master_rechnr = ""
    bill_date:date = None
    na_running:bool = False
    gastnrmember:int = 0
    lvcarea:string = "fo-invoice"
    bill = artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ex_rate, mess_str, master_str, master_rechnr, bill_date, na_running, gastnrmember, lvcarea, bill, artikel
        nonlocal pvilanguage, bil_recid, curr_department, currzeit, amount, amount_foreign, billart, description, qty, curr_room, user_init, artnr, price, cancel_str, exchg_rate, price_decimal, double_currency, master_flag

        return {"ex_rate": ex_rate, "mess_str": mess_str, "master_str": master_str, "master_rechnr": master_rechnr, "master_flag": master_flag}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, artnr)],"departement": [(eq, curr_department)]})

    if artikel:
        master_flag = update_masterbill(currzeit)


    return generate_output()