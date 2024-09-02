from functions.additional_functions import *
import decimal
from functions.sall_onhand_btn_gobl import sall_onhand_btn_gobl

def sall_onhand_btn_go1bl(all_flag:bool, show_price:bool, zero_flag:bool, from_grp:int, sub_grp:int, from_lager:int, to_lager:int, sorttype:int, mattype:int):
    soh_list_list = []

    str_list = soh_list = None

    str_list_list, Str_list = create_model("Str_list", {"flag":int, "s":str})
    soh_list_list, Soh_list = create_model("Soh_list", {"artnr":int, "bezeich":str, "unit":str, "act_qty":decimal, "act_val":decimal, "cont1":str, "d_unit":str, "cont2":str, "last_price":decimal, "act_price":decimal, "avrg_price":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal soh_list_list


        nonlocal str_list, soh_list
        nonlocal str_list_list, soh_list_list
        return {"soh-list": soh_list_list}

    str_list_list = get_output(sall_onhand_btn_gobl(all_flag, show_price, zero_flag, from_grp, sub_grp, from_lager, to_lager, sorttype, mattype))
    soh_list_list.clear()

    for str_list in query(str_list_list):
        soh_list = Soh_list()
        soh_list_list.append(soh_list)

        soh_list.artnr = to_int(substring(str_list.s, 0, 7))
        soh_list.bezeich = substring(str_list.s, 7, 30)
        soh_list.unit = substring(str_list.s, 37, 3)
        soh_list.act_qty = decimal.Decimal(substring(str_list.s, 108, 13))
        soh_list.act_val = decimal.Decimal(substring(str_list.s, 121, 15))
        soh_list.cont1 = substring(str_list.s, 40, 9)
        soh_list.d_unit = substring(str_list.s, 49, 8)
        soh_list.cont2 = substring(str_list.s, 57, 9)
        soh_list.last_price = decimal.Decimal(substring(str_list.s, 66, 14))
        soh_list.act_price = decimal.Decimal(substring(str_list.s, 80, 14))
        soh_list.avrg_price = decimal.Decimal(substring(str_list.s, 94, 14))

    return generate_output()