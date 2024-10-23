from functions.additional_functions import *
import decimal
from functions.hk_discrepancybl import hk_discrepancybl

def foc_hk_discrepancybl():
    hk_discrepancy_list_list = []
    msg_str:str = ""
    fo_stat:str = ""
    hk_stat:str = ""

    rmplan = hkdiscrepancy_list = hk_discrepancy_list = None

    rmplan_list, Rmplan = create_model("Rmplan", {"nr":int, "str":str})
    hkdiscrepancy_list_list, Hkdiscrepancy_list = create_model("Hkdiscrepancy_list", {"zinr":str, "features":str, "etage":int, "bezeich":str, "house_status":int, "zistatus":int, "userinit":str, "nr":int})
    hk_discrepancy_list_list, Hk_discrepancy_list = create_model("Hk_discrepancy_list", {"roomno":str, "fo_status":str, "fo_adult":int, "fo_child":int, "hk_status":str, "hk_adult":int, "hk_child":int, "explanation":str, "times":str, "id":str, "floor":int, "room_descr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hk_discrepancy_list_list, msg_str, fo_stat, hk_stat


        nonlocal rmplan, hkdiscrepancy_list, hk_discrepancy_list
        nonlocal rmplan_list, hkdiscrepancy_list_list, hk_discrepancy_list_list
        return {"hk-discrepancy-list": hk_discrepancy_list_list}


    msg_str, fo_stat, hk_stat, hkdiscrepancy_list_list, rmplan_list = get_output(hk_discrepancybl(0, "", "", 0, "", "", "", "", "", 0, 0, 0, 0))

    for hkdiscrepancy_list in query(hkdiscrepancy_list_list):
        hk_discrepancy_list = Hk_discrepancy_list()
        hk_discrepancy_list_list.append(hk_discrepancy_list)

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