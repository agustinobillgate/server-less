from functions.additional_functions import *
import decimal
from functions.prepare_stock_onhandbl import prepare_stock_onhandbl

def prepare_stock_onhand1bl(s_artnr:int):
    price_decimal = 0
    artnr = 0
    bezeich = ""
    soh_list_list = []

    str_list = soh_list = None

    str_list_list, Str_list = create_model("Str_list", {"l_bezeich":str, "str":str})
    soh_list_list, Soh_list = create_model("Soh_list", {"store":int, "bezeich":str, "from_date":str, "init_stock":decimal, "init_value":decimal, "in_qty":decimal, "in_amount":decimal, "out_qty":decimal, "out_amount":decimal, "adjustment":decimal, "end_qty":decimal, "end_value":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, artnr, bezeich, soh_list_list


        nonlocal str_list, soh_list
        nonlocal str_list_list, soh_list_list
        return {"price_decimal": price_decimal, "artnr": artnr, "bezeich": bezeich, "soh-list": soh_list_list}

    price_decimal, artnr, bezeich, str_list_list = get_output(prepare_stock_onhandbl(s_artnr))
    soh_list_list.clear()

    for str_list in query(str_list_list):
        soh_list = Soh_list()
        soh_list_list.append(soh_list)

        soh_list.store = to_int(substring(str_list.s, 0, 2))
        soh_list.bezeich = str_list.l_bezeich
        soh_list.from_date = substring(str_list.s, 2, 8)
        soh_list.init_stock = decimal.Decimal(substring(str_list.s, 10, 13))
        soh_list.init_value = decimal.Decimal(substring(str_list.s, 23, 14))
        soh_list.in_qty = decimal.Decimal(substring(str_list.s, 37, 13))
        soh_list.in_amount = decimal.Decimal(substring(str_list.s, 50, 14))
        soh_list.out_qty = decimal.Decimal(substring(str_list.s, 64, 13))
        soh_list.out_amount = decimal.Decimal(substring(str_list.s, 77, 14))
        soh_list.adjustment = decimal.Decimal(substring(str_list.s, 91, 13))
        soh_list.end_qty = decimal.Decimal(substring(str_list.s, 104, 13))
        soh_list.end_value = decimal.Decimal(substring(str_list.s, 117, 14))

    return generate_output()