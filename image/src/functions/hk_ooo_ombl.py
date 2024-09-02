from functions.additional_functions import *
import decimal
from datetime import date
from functions.create_om_list_cldbl import create_om_list_cldbl
from functions.hk_ooo_1_cldbl import hk_ooo_1_cldbl
from models import Bediener, Outorder

def hk_ooo_ombl(fdate:date, tdate:date, disptype:int, sorttype:int):
    ci_date = None
    om_list_list = []
    ooo_list_list = []
    user_init:str = ""
    bediener = outorder = None

    om_list2 = om_list = ooo_list = t_ooo_list = None

    om_list2_list, Om_list2 = create_model("Om_list2", {"zinr":str, "userinit":str, "ind":int, "reason":str, "gespstart":date, "gespende":date})
    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "userinit":str, "ind":int, "reason":str, "gespstart":date, "gespende":date, "rec_id":int})
    ooo_list_list, Ooo_list = create_model("Ooo_list", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int, "selected_om":bool, "rec_id":int})
    t_ooo_list_list, T_ooo_list = create_model("T_ooo_list", {"zinr":str, "gespgrund":str, "gespstart":date, "gespende":date, "userinit":str, "etage":int, "ind":int, "bezeich":str, "betriebsnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, om_list_list, ooo_list_list, user_init, bediener, outorder


        nonlocal om_list2, om_list, ooo_list, t_ooo_list
        nonlocal om_list2_list, om_list_list, ooo_list_list, t_ooo_list_list
        return {"ci_date": ci_date, "om-list": om_list_list, "ooo-list": ooo_list_list}


    bediener = db_session.query(Bediener).first()
    user_init = bediener.userinit
    om_list2_list.clear()
    om_list_list.clear()
    om_list2_list = get_output(create_om_list_cldbl(fdate, tdate))
    # for om in om_list2_list:
    #     print("OMList2:", om)
    ci_date, ooo_list_list = get_output(hk_ooo_1_cldbl(om_list2, fdate, tdate, disptype, sorttype, user_init))
    # ci_date, ooo_list_list = get_output(hk_ooo_1_cldbl(om_list2_list, fdate, tdate, disptype, sorttype, user_init))

    for om_list2 in query(om_list2_list):
        om_list = Om_list()
        om_list_list.append(om_list)

        om_list.zinr = om_list2.zinr
        om_list.userinit = om_list2.userinit
        om_list.ind = om_list2.ind
        om_list.reason = om_list2.reason
        om_list.gespstart = om_list2.gespstart
        om_list.gespende = om_list2.gespende

    for om_list in query(om_list_list):

        outorder = db_session.query(Outorder).filter(
                (Outorder.zinr == om_list.zinr) &  (Outorder.gespstart == om_list.gespstart) &  (Outorder.gespende == om_list.gespende)).first()

        if outorder:
            om_list.rec_id = outorder._recid

    return generate_output()