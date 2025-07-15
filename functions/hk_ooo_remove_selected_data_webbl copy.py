from functions.additional_functions import *
import decimal
from datetime import date
from functions.genoooroom_dailybl import genoooroom_dailybl
from functions.deactivate_ooo2_cldbl import deactivate_ooo2_cldbl
from models import Outorder, Bediener

ooo_list_list, Ooo_list = create_model("Ooo_list", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int, "selected_om":bool, "rec_id":int})

def hk_ooo_remove_selected_data_webbl(case_type:int, user_init:str, ci_date:date, ooo_list_list:[Ooo_list]):
    success_flag = False
    oos_flag:bool = False
    user_nr:int = 0
    outorder = bediener = None

    om_list = ooo_list = ooo_list2 = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "userinit":str, "ind":int})
    ooo_list2_list, Ooo_list2 = create_model("Ooo_list2", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int, "selected_om":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, oos_flag, user_nr, outorder, bediener
        nonlocal case_type, user_init, ci_date


        nonlocal om_list, ooo_list, ooo_list2
        nonlocal om_list_list, ooo_list_list, ooo_list2_list
        return {"success_flag": success_flag}

    if case_type == 1:

        for ooo_list in query(ooo_list_list):

            if not outorder or not(outorder._recid == ooo_list.rec_id):
                outorder = db_session.query(Outorder).filter(
                    (Outorder._recid == ooo_list.rec_id)).first()

            if outorder:
                db_session.delete(outorder)
                pass
        success_flag = True

    elif case_type == 2:
        ooo_list2_list.clear()

        if not bediener or not(bediener.userinit == userinit):
            bediener = db_session.query(Bediener).filter(
                (Bediener.userinit == userinit)).first()

        if bediener:
            user_nr = bediener.nr

        for ooo_list in query(ooo_list_list):
            get_output(genoooroom_dailybl(ooo_list.zinr, user_init))
            oos_flag = (ooo_list.betriebsnr == 3 or ooo_list.betriebsnr == 4)
            ooo_list2 = Ooo_list2()
            ooo_list2_list.append(ooo_list2)

            ooo_list2.zinr = ooo_list.zinr
            ooo_list2.betriebsnr = ooo_list.betriebsnr
            ooo_list2.gespstart = ooo_list.gespstart
            ooo_list2.gespende = ooo_list.gespende
            get_output(deactivate_ooo2_cldbl(user_nr, oos_flag, ci_date, ooo_list2_list))
        success_flag = True

    return generate_output()