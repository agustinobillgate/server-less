#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.stock_hmovelist_create_listbl import stock_hmovelist_create_listbl

def stock_hmovelist_create_list_webbl(pvilanguage:int, s_artnr:int, mm:int, yy:int, from_lager:int, to_lager:int, show_price:bool):
    anfdate = None
    enddate = None
    art_list_list = []

    str_list = art_list = None

    str_list_list, Str_list = create_model("Str_list", {"s":string})
    art_list_list, Art_list = create_model("Art_list", {"datum":string, "devnote":string, "qty":string, "val":string, "in_qty":string, "in_val":string, "out_qty":string, "out_val":string, "note":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anfdate, enddate, art_list_list
        nonlocal pvilanguage, s_artnr, mm, yy, from_lager, to_lager, show_price


        nonlocal str_list, art_list
        nonlocal str_list_list, art_list_list

        return {"anfdate": anfdate, "enddate": enddate, "art-list": art_list_list}

    anfdate, enddate, str_list_list = get_output(stock_hmovelist_create_listbl(pvilanguage, s_artnr, mm, yy, from_lager, to_lager, show_price))

    for str_list in query(str_list_list):
        art_list = Art_list()
        art_list_list.append(art_list)

        art_list.datum = substring(str_list.s, 0, 8)
        art_list.devnote = substring(str_list.s, 8, 16)
        art_list.qty = substring(str_list.s, 24, 11)
        art_list.val = substring(str_list.s, 35, 15)
        art_list.in_qty = substring(str_list.s, 50, 13)
        art_list.in_val = substring(str_list.s, 63, 14)
        art_list.out_qty = substring(str_list.s, 77, 13)
        art_list.out_val = substring(str_list.s, 90, 14)
        art_list.note = substring(str_list.s, 115, 16)

    return generate_output()