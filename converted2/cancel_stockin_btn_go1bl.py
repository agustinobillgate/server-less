#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.cancel_stockin_btn_go_cldbl import cancel_stockin_btn_go_cldbl

def cancel_stockin_btn_go1bl(pvilanguage:int, all_supp:bool, sorttype:int, from_grp:int, store:int, from_date:date, to_date:date, show_price:bool, from_supp:string):
    cancel_stockin_list_data = []

    str_list = cancel_stockin_list = None

    str_list_data, Str_list = create_model("Str_list", {"h_recid":int, "l_recid":int, "lief_nr":int, "billdate":date, "artnr":int, "lager_nr":int, "docu_nr":string, "lscheinnr":string, "invoice_nr":string, "qty":Decimal, "epreis":Decimal, "warenwert":Decimal, "deci1_3":Decimal, "s":string}, {"lscheinnr": ""})
    cancel_stockin_list_data, Cancel_stockin_list = create_model("Cancel_stockin_list", {"datum":date, "lager":string, "lief_nr":int, "lief":string, "art":string, "bezeich":string, "unit":string, "epreis":Decimal, "in_qty":Decimal, "amount":Decimal, "docunr":string, "dlvnote":string, "note":string, "reason":string, "invnr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancel_stockin_list_data
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list, cancel_stockin_list
        nonlocal str_list_data, cancel_stockin_list_data

        return {"cancel-stockin-list": cancel_stockin_list_data}

    str_list_data = get_output(cancel_stockin_btn_go_cldbl(pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp))
    cancel_stockin_list_data.clear()

    for str_list in query(str_list_data):
        cancel_stockin_list = Cancel_stockin_list()
        cancel_stockin_list_data.append(cancel_stockin_list)

        cancel_stockin_list.datum = date_mdy(substring(str_list.s, 0, 8))
        cancel_stockin_list.lager = substring(str_list.s, 8, 2)
        cancel_stockin_list.lief_nr = str_list.lief_nr
        cancel_stockin_list.lief = substring(str_list.s, 83, 24)
        cancel_stockin_list.art = substring(str_list.s, 10, 7)
        cancel_stockin_list.bezeich = substring(str_list.s, 17, 32)
        cancel_stockin_list.unit = substring(str_list.s, 49, 6)
        cancel_stockin_list.epreis = to_decimal(substring(str_list.s, 143, 14))
        cancel_stockin_list.in_qty = to_decimal(substring(str_list.s, 55, 13))
        cancel_stockin_list.amount = to_decimal(substring(str_list.s, 68, 15))
        cancel_stockin_list.docunr = substring(str_list.s, 107, 16)
        cancel_stockin_list.dlvnote = substring(str_list.s, 123, 20)
        cancel_stockin_list.note = substring(str_list.s, 157, 26)
        cancel_stockin_list.reason = substring(str_list.s, 183, 24)
        cancel_stockin_list.invnr = str_list.invoice_nr

    return generate_output()