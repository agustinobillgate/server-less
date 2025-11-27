#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.genoooroom_dailybl import genoooroom_dailybl
from functions.deactivate_ooo2_cldbl import deactivate_ooo2_cldbl
from models import Outorder, Zimmer, Bediener, Res_history

ooo_list_data, Ooo_list = create_model("Ooo_list", {"zinr":string, "gespgrund":string, "gespstart":date, "gespende":date, "userinit":string, "etage":int, "ind":int, "bezeich":string, "betriebsnr":int, "selected_om":bool, "rec_id":int})

def hk_ooo_remove_selected_data_webbl(case_type:int, user_init:string, ci_date:date, ooo_list_data:[Ooo_list]):

    prepare_cache ([Zimmer, Bediener, Res_history])

    success_flag = False
    oos_flag:bool = False
    user_nr:int = 0
    stat_list:List[string] = create_empty_list(10,"")
    outorder = zimmer = bediener = res_history = None

    om_list = ooo_list = ooo_list2 = None

    om_list_data, Om_list = create_model("Om_list", {"zinr":string, "userinit":string, "ind":int})
    ooo_list2_data, Ooo_list2 = create_model("Ooo_list2", {"zinr":string, "gespgrund":string, "gespstart":date, "gespende":date, "userinit":string, "etage":int, "ind":int, "bezeich":string, "betriebsnr":int, "selected_om":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, oos_flag, user_nr, stat_list, outorder, zimmer, bediener, res_history
        nonlocal case_type, user_init, ci_date


        nonlocal om_list, ooo_list, ooo_list2
        nonlocal om_list_data, ooo_list2_data

        return {"success_flag": success_flag}


    stat_list[0] = "Vacant Clean Checked"
    stat_list[1] = "Vacant Clean Unchecked"
    stat_list[2] = "Vacant Dirty"
    stat_list[3] = "Expected Departure"
    stat_list[4] = "Occupied Dirty"
    stat_list[5] = "Occupied Cleaned"
    stat_list[6] = "Out-of-Order"
    stat_list[7] = "Off-Market"
    stat_list[8] = "Do not Disturb"
    stat_list[9] = "Out-of-Service"

    if case_type == 1:

        for ooo_list in query(ooo_list_data):

            outorder = get_cache (Outorder, {"_recid": [(eq, ooo_list.rec_id)]})

            zimmer = get_cache (Zimmer, {"zinr": [(eq, outorder.zinr)]})

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if outorder:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Room " + zimmer.zinr +\
                        " Status Changed From " +\
                        to_string(zimmer.zistatus) + " Off-Market" + " to " + to_string(zimmer.zistatus) + " " + stat_list[zimmer.zistatus + 1 - 1]
                res_history.action = "HouseKeeping"


                pass
                pass
                pass
                db_session.delete(outorder)
                pass
        success_flag = True

    elif case_type == 2:
        ooo_list2_data.clear()

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            user_nr = bediener.nr

        for ooo_list in query(ooo_list_data):
            get_output(genoooroom_dailybl(ooo_list.zinr, user_init))
            oos_flag = (ooo_list.betriebsnr == 3 or ooo_list.betriebsnr == 4)
            ooo_list2 = Ooo_list2()
            ooo_list2_data.append(ooo_list2)

            ooo_list2.zinr = ooo_list.zinr
            ooo_list2.betriebsnr = ooo_list.betriebsnr
            ooo_list2.gespstart = ooo_list.gespstart
            ooo_list2.gespende = ooo_list.gespende
            get_output(deactivate_ooo2_cldbl(user_nr, oos_flag, ci_date, ooo_list2_data))
        success_flag = True

    return generate_output()