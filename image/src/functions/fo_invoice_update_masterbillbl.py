from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Artikel

def fo_invoice_update_masterbillbl(pvilanguage:int, bil_recid:int, curr_department:int, currzeit:int, amount:decimal, amount_foreign:decimal, billart:int, description:str, qty:int, curr_room:str, user_init:str, artnr:int, price:decimal, cancel_str:str, exchg_rate:decimal, price_decimal:int, double_currency:bool, master_flag:bool):
    ex_rate = 0
    mess_str = ""
    master_str = ""
    master_rechnr = ""
    bill_date:date = None
    na_running:bool = False
    gastnrmember:int = 0
    lvcarea:str = "fo_invoice"
    bill = artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ex_rate, mess_str, master_str, master_rechnr, bill_date, na_running, gastnrmember, lvcarea, bill, artikel


        return {"ex_rate": ex_rate, "mess_str": mess_str, "master_str": master_str, "master_rechnr": master_rechnr}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == artnr) &  (Artikel.departement == curr_department)).first()

    if artikel:
        master_flag = update_masterbill(currzeit)

    return generate_output()