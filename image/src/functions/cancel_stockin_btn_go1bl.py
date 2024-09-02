from functions.additional_functions import *
import decimal
from datetime import date
from functions.cancel_stockin_btn_gobl import cancel_stockin_btn_gobl

def cancel_stockin_btn_go1bl(pvilanguage:int, all_supp:bool, sorttype:int, from_grp:int, store:int, from_date:date, to_date:date, show_price:bool, from_supp:str):
    cancel_stockin_list_list = []

    str_list = cancel_stockin_list = None

    str_list_list, Str_list = create_model("Str_list", {"h_recid":int, "l_recid":int, "lief_nr":int, "billdate":date, "artnr":int, "lager_nr":int, "docu_nr":str, "lscheinnr":str, "invoice_nr":str, "qty":decimal, "epreis":decimal, "warenwert":decimal, "deci1_3":decimal, "s":str}, {"lscheinnr": ""})
    cancel_stockin_list_list, Cancel_stockin_list = create_model("Cancel_stockin_list", {"datum":date, "lager":str, "lief_nr":int, "lief":str, "art":str, "bezeich":str, "unit":str, "epreis":decimal, "in_qty":decimal, "amount":decimal, "docunr":str, "dlvnote":str, "note":str, "reason":str, "invnr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancel_stockin_list_list


        nonlocal str_list, cancel_stockin_list
        nonlocal str_list_list, cancel_stockin_list_list
        return {"cancel-stockin-list": cancel_stockin_list_list}

    str_list_list = get_output(cancel_stockin_btn_gobl(pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp))
    cancel_stockin_list_list.clear()

    for str_list in query(str_list_list):
        cancel_stockin_list = Cancel_stockin_list()
        cancel_stockin_list_list.append(cancel_stockin_list)

        cancel_stockin_list.datum = date_mdy(substring(str_list.s, 0, 8))
        cancel_stockin_list.lager = substring(str_list.s, 8, 2)
        cancel_stockin_list.lief_nr = str_list.lief_nr
        cancel_stockin_list.lief = substring(str_list.s, 83, 18)
        cancel_stockin_list.art = substring(str_list.s, 10, 7)
        cancel_stockin_list.bezeich = substring(str_list.s, 17, 32)
        cancel_stockin_list.unit = substring(str_list.s, 49, 6)
        cancel_stockin_list.epreis = decimal.Decimal(substring(str_list.s, 143, 14))
        cancel_stockin_list.in_qty = decimal.Decimal(substring(str_list.s, 55, 13))
        cancel_stockin_list.amount = decimal.Decimal(substring(str_list.s, 68, 15))
        cancel_stockin_list.docunr = substring(str_list.s, 107, 16)
        cancel_stockin_list.dlvnote = substring(str_list.s, 123, 20)
        cancel_stockin_list.note = substring(str_list.s, 157, 26)
        cancel_stockin_list.reason = substring(str_list.s, 183, 24)
        cancel_stockin_list.invnr = str_list.invoice_nr

    return generate_output()