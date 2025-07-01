#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimkateg, Queasy, Outorder, Res_history, Zimmer, Zinrstat

ooo_list2_list, Ooo_list2 = create_model("Ooo_list2", {"zinr":string, "gespgrund":string, "gespstart":date, "gespende":date, "userinit":string, "etage":int, "ind":int, "bezeich":string, "betriebsnr":int, "selected_om":bool})

def deactivate_ooo2_1_cldbl(user_nr:int, oos_flag:bool, ci_date:date, ooo_list2_list:[Ooo_list2]):

    prepare_cache ([Zimkateg, Queasy, Res_history, Zimmer, Zinrstat])

    datum:date = None
    cat_flag:bool = False
    roomnr:int = 0
    zimkateg = queasy = outorder = res_history = zimmer = zinrstat = None

    om_list = ooo_list2 = zbuff = qsy = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":string, "userinit":string, "ind":int})

    Zbuff = create_buffer("Zbuff",Zimkateg)
    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, cat_flag, roomnr, zimkateg, queasy, outorder, res_history, zimmer, zinrstat
        nonlocal user_nr, oos_flag, ci_date, ooo_list2_list
        nonlocal zbuff, qsy


        nonlocal om_list, ooo_list2, zbuff, qsy
        nonlocal om_list_list

        return {}


    ooo_list2 = query(ooo_list2_list, first=True)

    outorder = get_cache (Outorder, {"zinr": [(eq, ooo_list2.zinr)],"betriebsnr": [(eq, ooo_list2.betriebsnr)],"gespstart": [(eq, ooo_list2.gespstart)],"gespende": [(eq, ooo_list2.gespende)]})

    if outorder.betriebsnr <= 1:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = user_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Remove O-O-O Record of Room " + outorder.zinr +\
                " " + to_string(outorder.gespstart) + "-" + to_string(outorder.gespende)
        res_history.action = "HouseKeeping"


        pass
        pass

        zimmer = get_cache (Zimmer, {"zinr": [(eq, ooo_list2.zinr)]})

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        if zbuff:

            if cat_flag:
                roomnr = zbuff.typ
            else:
                roomnr = zbuff.zikatnr
        for datum in date_range(outorder.gespstart,outorder.gespende) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

    if outorder.betriebsnr == 2:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = user_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Remove Off Market Record of Room " + outorder.zinr +\
                " " + to_string(outorder.gespstart) + "-" + to_string(outorder.gespende)
        res_history.action = "HouseKeeping"


        pass
        pass

        zimmer = get_cache (Zimmer, {"zinr": [(eq, ooo_list2.zinr)]})

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

        if zbuff:

            if cat_flag:
                roomnr = zbuff.typ
            else:
                roomnr = zbuff.zikatnr
        for datum in date_range(outorder.gespstart,outorder.gespende) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

    if oos_flag and (outorder.gespstart == outorder.gespende):

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "oos")],"datum": [(eq, ci_date)]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = ci_date
            zinrstat.zinr = "oos"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1
    pass
    db_session.delete(outorder)

    zimmer = get_cache (Zimmer, {"zinr": [(eq, ooo_list2.zinr)]})

    if zimmer.zistatus == 6:
        zimmer.zistatus = 2
    zimmer.bediener_nr_stat = user_nr
    pass

    return generate_output()