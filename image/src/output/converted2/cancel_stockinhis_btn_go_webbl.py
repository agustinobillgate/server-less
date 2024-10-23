from functions.additional_functions import *
import decimal
from datetime import date
from functions.cancel_stockinhis_btn_go_cldbl import cancel_stockinhis_btn_go_cldbl

def cancel_stockinhis_btn_go_webbl(pvilanguage:int, all_supp:bool, sorttype:int, from_grp:int, store:int, from_date:date, to_date:date, show_price:bool, from_supp:str):
    cancel_stockinhis_list_list = []

    str_list = cancel_stockinhis_list = None

    str_list_list, Str_list = create_model("Str_list", {"h_recid":int, "l_recid":int, "lief_nr":int, "billdate":date, "artnr":int, "lager_nr":int, "docu_nr":str, "lscheinnr":str, "invoice_nr":str, "qty":decimal, "epreis":decimal, "warenwert":decimal, "deci1_3":decimal, "s":str}, {"lscheinnr": ""})
    cancel_stockinhis_list_list, Cancel_stockinhis_list = create_model("Cancel_stockinhis_list", {"datum":date, "lager":str, "lief_nr":int, "lief":str, "art":str, "bezeich":str, "unit":str, "epreis":decimal, "in_qty":decimal, "amount":decimal, "docunr":str, "dlvnote":str, "note":str, "reason":str, "invnr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancel_stockinhis_list_list
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list, cancel_stockinhis_list
        nonlocal str_list_list, cancel_stockinhis_list_list
        return {"cancel-stockinhis-list": cancel_stockinhis_list_list}

    str_list_list = get_output(cancel_stockinhis_btn_go_cldbl(pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp))
    cancel_stockinhis_list_list.clear()

    for str_list in query(str_list_list):
        cancel_stockinhis_list = Cancel_stockinhis_list()
        cancel_stockinhis_list_list.append(cancel_stockinhis_list)

        cancel_stockinhis_list.datum = date_mdy(substring(str_list.s, 0, 8))
        cancel_stockinhis_list.lager = substring(str_list.s, 8, 2)
        cancel_stockinhis_list.lief_nr = str_list.lief_nr
        cancel_stockinhis_list.lief = substring(str_list.s, 83, 18)
        cancel_stockinhis_list.art = substring(str_list.s, 10, 7)
        cancel_stockinhis_list.bezeich = substring(str_list.s, 17, 32)
        cancel_stockinhis_list.unit = substring(str_list.s, 49, 6)
        cancel_stockinhis_list.epreis = to_decimal(substring(str_list.s, 143, 14))
        cancel_stockinhis_list.in_qty = to_decimal(substring(str_list.s, 55, 13))
        cancel_stockinhis_list.amount = to_decimal(substring(str_list.s, 68, 15))
        cancel_stockinhis_list.docunr = substring(str_list.s, 107, 16)
        cancel_stockinhis_list.dlvnote = substring(str_list.s, 123, 20)
        cancel_stockinhis_list.note = substring(str_list.s, 157, 26)
        cancel_stockinhis_list.reason = substring(str_list.s, 183, 24)
        cancel_stockinhis_list.invnr = str_list.invoice_nr

    return generate_output()