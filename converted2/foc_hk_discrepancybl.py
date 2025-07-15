#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.hk_discrepancybl import hk_discrepancybl

def foc_hk_discrepancybl():
    hk_discrepancy_list_data = []
    msg_str:string = ""
    fo_stat:string = ""
    hk_stat:string = ""

    rmplan = hkdiscrepancy_list = hk_discrepancy_list = None

    rmplan_data, Rmplan = create_model("Rmplan", {"nr":int, "str":string})
    hkdiscrepancy_list_data, Hkdiscrepancy_list = create_model("Hkdiscrepancy_list", {"zinr":string, "features":string, "etage":int, "bezeich":string, "house_status":int, "zistatus":int, "userinit":string, "nr":int})
    hk_discrepancy_list_data, Hk_discrepancy_list = create_model("Hk_discrepancy_list", {"roomno":string, "fo_status":string, "fo_adult":int, "fo_child":int, "hk_status":string, "hk_adult":int, "hk_child":int, "explanation":string, "times":string, "id":string, "floor":int, "room_descr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hk_discrepancy_list_data, msg_str, fo_stat, hk_stat


        nonlocal rmplan, hkdiscrepancy_list, hk_discrepancy_list
        nonlocal rmplan_data, hkdiscrepancy_list_data, hk_discrepancy_list_data

        return {"hk-discrepancy-list": hk_discrepancy_list_data}


    msg_str, fo_stat, hk_stat, hkdiscrepancy_list_data, rmplan_data = get_output(hk_discrepancybl(0, "", "", 0, "", "", "", "", "", 0, 0, 0, 0))

    for hkdiscrepancy_list in query(hkdiscrepancy_list_data):
        hk_discrepancy_list = Hk_discrepancy_list()
        hk_discrepancy_list_data.append(hk_discrepancy_list)

        roomno = hkdiscrepancy_list.zinr
        fo_status = substring(hkdiscrepancy_list.features, 0, 12)
        fo_adult = to_int(substring(hkdiscrepancy_list.features, 63, 2))
        fo_child = to_int(substring(hkdiscrepancy_list.features, 65, 2))
        hk_status = substring(hkdiscrepancy_list.features, 12, 12)
        hk_adult = to_int(substring(hkdiscrepancy_list.features, 67, 2))
        hk_child = to_int(substring(hkdiscrepancy_list.features, 69, 2))
        explanation = substring(hkdiscrepancy_list.features, 31, 32)
        times = substring(hkdiscrepancy_list.features, 26, 5)
        id = substring(hkdiscrepancy_list.features, 24, 2)
        floor = hkdiscrepancy_list.etage
        room_descr = hkdiscrepancy_list.bezeich

    return generate_output()