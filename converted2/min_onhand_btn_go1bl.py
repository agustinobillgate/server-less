from functions.additional_functions import *
import decimal
from datetime import date
from functions.min_onhand_btn_gobl import min_onhand_btn_gobl

def min_onhand_btn_go1bl(sorttype:int, main_grp:int, from_store3:int, to_store3:int, show_price:bool):
    min_onhand_list_list = []

    s_list = min_onhand_list = None

    s_list_list, S_list = create_model("S_list", {"s":str, "s2":str})
    min_onhand_list_list, Min_onhand_list = create_model("Min_onhand_list", {"artnr":int, "name":str, "min_oh":decimal, "curr_oh":decimal, "avrgprice":decimal, "ek_aktuell":str, "datum":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal min_onhand_list_list
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal s_list, min_onhand_list
        nonlocal s_list_list, min_onhand_list_list
        return {"min-onhand-list": min_onhand_list_list}

    s_list_list = get_output(min_onhand_btn_gobl(sorttype, main_grp, from_store3, to_store3, show_price))
    min_onhand_list_list.clear()

    for s_list in query(s_list_list):
        min_onhand_list = Min_onhand_list()
        min_onhand_list_list.append(min_onhand_list)

        min_onhand_list.artnr = to_int(substring(s, 0, 7))


        min_onhand_list.name = substring(s, 7, 36)


        min_onhand_list.min_oh = to_decimal(substring(s, 43, 11))


        min_onhand_list.curr_oh = to_decimal(substring(s, 54, 11))


        min_onhand_list.avrgprice = to_decimal(substring(s, 65, 16))


        min_onhand_list.ek_aktuell = substring(s, 81, 16)


        min_onhand_list.datum = date_mdy(substring(s, 97, 8))

    return generate_output()