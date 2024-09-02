from functions.additional_functions import *
import decimal
from datetime import date
from functions.stock_retourlist_create_listbl import stock_retourlist_create_listbl

def stock_retourlist_create_list1bl(from_date:date, to_date:date, from_supp:str, to_supp:str, show_price:bool):
    stock_retour_list_list = []

    str_list = stock_retour_list = None

    str_list_list, Str_list = create_model("Str_list", {"s":str})
    stock_retour_list_list, Stock_retour_list = create_model("Stock_retour_list", {"datum":date, "lief":str, "art":str, "bezeich":str, "qty":decimal, "epreis":decimal, "amount":decimal, "reason":str, "id":str, "dlvnote":str, "lager":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal stock_retour_list_list


        nonlocal str_list, stock_retour_list
        nonlocal str_list_list, stock_retour_list_list
        return {"stock-retour-list": stock_retour_list_list}

    str_list_list = get_output(stock_retourlist_create_listbl(from_date, to_date, from_supp, to_supp, show_price))
    stock_retour_list_list.clear()

    for str_list in query(str_list_list):
        stock_retour_list = Stock_retour_list()
        stock_retour_list_list.append(stock_retour_list)

        stock_retour_list.datum = date_mdy(substring(str_list.s, 0, 8))
        stock_retour_list.lief = substring(str_list.s, 8, 24)
        stock_retour_list.art = substring(str_list.s, 32, 7)
        stock_retour_list.bezeich = substring(str_list.s, 39, 36)
        stock_retour_list.qty = decimal.Decimal(substring(str_list.s, 75, 10))
        stock_retour_list.epreis = decimal.Decimal(substring(str_list.s, 85, 13))
        stock_retour_list.amount = decimal.Decimal(substring(str_list.s, 98, 13))
        stock_retour_list.reason = substring(str_list.s, 111, 16)
        stock_retour_list.id = substring(str_list.s, 127, 2)
        stock_retour_list.dlvnote = substring(str_list.s, 129, 20)
        stock_retour_list.lager = substring(str_list.s, 149, 2)

    return generate_output()