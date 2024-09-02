from functions.additional_functions import *
import decimal
from datetime import date
from functions.discrepancy_inlistbl import discrepancy_inlistbl
from models import L_lager

def discrepancy_inlist_1bl(sorttype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, mi_rec_chk:bool, mi_ord_chk:bool, mi_all_chk:bool):
    discrepancy_inlist_list = []
    lager_bezeich:str = ""
    l_lager = None

    str_list = discrepancy_inlist = None

    str_list_list, Str_list = create_model("Str_list", {"s":str})
    discrepancy_inlist_list, Discrepancy_inlist = create_model("Discrepancy_inlist", {"datum":date, "lager":str, "docunr":str, "art":str, "bezeich":str, "in_qty":decimal, "amount":decimal, "epreis1":decimal, "epreis2":decimal, "lief":str, "dlvnote":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal discrepancy_inlist_list, lager_bezeich, l_lager


        nonlocal str_list, discrepancy_inlist
        nonlocal str_list_list, discrepancy_inlist_list
        return {"discrepancy-inlist": discrepancy_inlist_list}

    str_list_list = get_output(discrepancy_inlistbl(sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, mi_rec_chk, mi_ord_chk, mi_all_chk))
    discrepancy_inlist_list.clear()

    for str_list in query(str_list_list):
        discrepancy_inlist = Discrepancy_inlist()
        discrepancy_inlist_list.append(discrepancy_inlist)


        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == to_int(substring(str_list.s, 8, 2)))).first()

        if l_lager:
            lager_bezeich = l_lager.bezeich


        discrepancy_inlist.datum = date_mdy(substring(str_list.s, 0, 8))
        discrepancy_inlist.lager = lager_bezeich
        discrepancy_inlist.docunr = substring(str_list.s, 106, 12)
        discrepancy_inlist.art = substring(str_list.s, 10, 7)
        discrepancy_inlist.bezeich = substring(str_list.s, 17, 36)
        discrepancy_inlist.in_qty = decimal.Decimal(substring(str_list.s, 53, 11))
        discrepancy_inlist.amount = decimal.Decimal(substring(str_list.s, 64, 14))
        discrepancy_inlist.epreis1 = decimal.Decimal(substring(str_list.s, 134, 14))
        discrepancy_inlist.epreis2 = decimal.Decimal(substring(str_list.s, 148, 14))
        discrepancy_inlist.lief = substring(str_list.s, 86, 20)
        discrepancy_inlist.dlvnote = substring(str_list.s, 118, 16)

    return generate_output()