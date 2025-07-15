#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.prepare_stock_onhandbl import prepare_stock_onhandbl

def prepare_stock_onhand1bl(s_artnr:int):
    price_decimal = 0
    artnr = 0
    bezeich = ""
    soh_list_data = []

    str_list = soh_list = None

    str_list_data, Str_list = create_model("Str_list", {"l_bezeich":string, "str":string})
    soh_list_data, Soh_list = create_model("Soh_list", {"store":int, "bezeich":string, "from_date":string, "init_stock":Decimal, "init_value":Decimal, "in_qty":Decimal, "in_amount":Decimal, "out_qty":Decimal, "out_amount":Decimal, "adjustment":Decimal, "end_qty":Decimal, "end_value":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, artnr, bezeich, soh_list_data
        nonlocal s_artnr


        nonlocal str_list, soh_list
        nonlocal str_list_data, soh_list_data

        return {"price_decimal": price_decimal, "artnr": artnr, "bezeich": bezeich, "soh-list": soh_list_data}

    price_decimal, artnr, bezeich, str_list_data = get_output(prepare_stock_onhandbl(s_artnr))
    soh_list_data.clear()

    for str_list in query(str_list_data):
        soh_list = Soh_list()
        soh_list_data.append(soh_list)

        soh_list.store = to_int(substring(str_list.str, 0, 2))
        soh_list.bezeich = str_list.l_bezeich
        soh_list.from_date = substring(str_list.str, 2, 8)
        soh_list.init_stock = to_decimal(substring(str_list.str, 10, 13))
        soh_list.init_value = to_decimal(substring(str_list.str, 23, 14))
        soh_list.in_qty = to_decimal(substring(str_list.str, 37, 13))
        soh_list.in_amount = to_decimal(substring(str_list.str, 50, 14))
        soh_list.out_qty = to_decimal(substring(str_list.str, 64, 13))
        soh_list.out_amount = to_decimal(substring(str_list.str, 77, 14))
        soh_list.adjustment = to_decimal(substring(str_list.str, 91, 13))
        soh_list.end_qty = to_decimal(substring(str_list.str, 104, 13))
        soh_list.end_value = to_decimal(substring(str_list.str, 117, 14))

    return generate_output()