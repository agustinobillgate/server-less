#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.create_om_list_cldbl import create_om_list_cldbl
from functions.hk_ooo_1_cldbl import hk_ooo_1_cldbl
from models import Outorder

def hk_ooo_ombl(fdate:date, tdate:date, disptype:int, sorttype:int):

    prepare_cache ([Outorder])

    ci_date = None
    om_list_data = []
    ooo_list_data = []
    user_init:string = ""
    outorder = None

    om_list2 = om_list = ooo_list = t_ooo_list = None

    om_list2_data, Om_list2 = create_model("Om_list2", {"zinr":string, "userinit":string, "ind":int, "reason":string, "gespstart":date, "gespende":date})
    om_list_data, Om_list = create_model("Om_list", {"zinr":string, "userinit":string, "ind":int, "reason":string, "gespstart":date, "gespende":date, "rec_id":int})
    ooo_list_data, Ooo_list = create_model("Ooo_list", {"zinr":string, "gespgrund":string, "gespstart":date, "gespende":date, "userinit":string, "etage":int, "ind":int, "bezeich":string, "betriebsnr":int, "selected_om":bool, "rec_id":int})
    t_ooo_list_data, T_ooo_list = create_model("T_ooo_list", {"zinr":string, "gespgrund":string, "gespstart":date, "gespende":date, "userinit":string, "etage":int, "ind":int, "bezeich":string, "betriebsnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, om_list_data, ooo_list_data, user_init, outorder
        nonlocal fdate, tdate, disptype, sorttype


        nonlocal om_list2, om_list, ooo_list, t_ooo_list
        nonlocal om_list2_data, om_list_data, ooo_list_data, t_ooo_list_data

        return {"ci_date": ci_date, "om-list": om_list_data, "ooo-list": ooo_list_data}

    user_init = ""
    om_list2_data.clear()
    om_list_data.clear()
    om_list2_data = get_output(create_om_list_cldbl(fdate, tdate))
    ci_date, ooo_list_data = get_output(hk_ooo_1_cldbl(om_list2_data, fdate, tdate, disptype, sorttype, user_init))

    for om_list2 in query(om_list2_data):
        om_list = Om_list()
        om_list_data.append(om_list)

        om_list.zinr = om_list2.zinr
        om_list.userinit = om_list2.userinit
        om_list.ind = om_list2.ind
        om_list.reason = om_list2.reason
        om_list.gespstart = om_list2.gespstart
        om_list.gespende = om_list2.gespende

    for om_list in query(om_list_data):

        outorder = get_cache (Outorder, {"zinr": [(eq, om_list.zinr)],"gespstart": [(eq, om_list.gespstart)],"gespende": [(eq, om_list.gespende)]})

        if outorder:
            om_list.rec_id = outorder._recid

    return generate_output()