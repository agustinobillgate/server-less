from functions.additional_functions import *
import decimal
from datetime import date
from functions.stock_movelist_btn_gobl import stock_movelist_btn_gobl

def stock_movelist_btn_go1bl(pvilanguage:int, s_artnr:int, show_price:bool, from_lager:int, to_lager:int):
    stock_movelist_list = []

    str_list = stock_movelist = None

    str_list_list, Str_list = create_model("Str_list", {"s":str, "id":str})
    stock_movelist_list, Stock_movelist = create_model("Stock_movelist", {"datum":date, "lscheinnr":str, "init_qty":decimal, "init_val":decimal, "in_qty":decimal, "in_val":decimal, "out_qty":decimal, "out_val":decimal, "note":str, "id":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_movelist_list


        nonlocal str_list, stock_movelist
        nonlocal str_list_list, stock_movelist_list
        return {"stock-movelist": stock_movelist_list}

    str_list_list = get_output(stock_movelist_btn_gobl(pvilanguage, s_artnr, show_price, from_lager, to_lager))
    stock_movelist_list.clear()

    for str_list in query(str_list_list):
        stock_movelist = Stock_movelist()
        stock_movelist_list.append(stock_movelist)

        stock_movelist.datum = date_mdy(substring(s, 0, 8))
        stock_movelist.lscheinnr = substring(s, 8, 16)
        stock_movelist.init_qty = decimal.Decimal(substring(s, 24, 11))
        stock_movelist.init_val = decimal.Decimal(substring(s, 35, 15))
        stock_movelist.in_qty = decimal.Decimal(substring(s, 50, 13))
        stock_movelist.in_val = decimal.Decimal(substring(s, 63, 14))
        stock_movelist.out_qty = decimal.Decimal(substring(s, 77, 13))
        stock_movelist.out_val = decimal.Decimal(substring(s, 90, 14))
        stock_movelist.note = substring(s, 115, 13)
        stock_movelist.id = str_list.id

    return generate_output()