from functions.additional_functions import *
import decimal
from datetime import date
from models import Outorder

ooo_list2_list, Ooo_list2 = create_model("Ooo_list2", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int, "selected_om":bool})

def hk_ooo_remove_selected_databl(case_type:int, user_nr:int, ci_date:date, ooo_list2_list:[Ooo_list2]):
    success_flag = False
    outorder = None

    om_list = ooo_list2 = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "userinit":str, "ind":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, outorder
        nonlocal case_type, user_nr, ci_date, ooo_list2_list


        nonlocal om_list, ooo_list2
        nonlocal om_list_list, ooo_list2_list
        return {"success_flag": success_flag}


    if case_type == 1:

        for ooo_list2 in query(ooo_list2_list, filters=(lambda ooo_list2: ooo_list2.selected_om)):

            outorder = db_session.query(Outorder).filter(
                     (Outorder.zinr == ooo_list2.zinr) & (Outorder.gespstart == ooo_list2.gespstart) & (Outorder.gespende == ooo_list2.gespende) & (Outorder.betriebsnr == ooo_list2.betriebsnr)).with_for_update().first()

            if outorder:
                db_session.delete(outorder)
                
        success_flag = True

    return generate_output()