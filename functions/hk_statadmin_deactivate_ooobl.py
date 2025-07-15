#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimkateg, Queasy, Zimmer, Outorder, Zinrstat, Res_history, Res_line

bline_list_data, Bline_list = create_model("Bline_list", {"zinr":string, "selected":bool, "bl_recid":int})
om_list_data, Om_list = create_model("Om_list", {"zinr":string, "ind":int})

def hk_statadmin_deactivate_ooobl(bline_list_data:[Bline_list], om_list_data:[Om_list], ci_date:date, user_nr:int, chgsort:int):

    prepare_cache ([Zimkateg, Queasy, Zinrstat, Res_history])

    z_list_data = []
    datum:date = None
    cat_flag:bool = False
    roomnr:int = 0
    zimkateg = queasy = zimmer = outorder = zinrstat = res_history = res_line = None

    z_list = om_list = bline_list = zbuff = qsy = None

    z_list_data, Z_list = create_model("Z_list", {"zinr":string, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":string, "bediener_nr_stat":int, "checkout":bool, "str_reason":string})

    Zbuff = create_buffer("Zbuff",Zimkateg)
    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal z_list_data, datum, cat_flag, roomnr, zimkateg, queasy, zimmer, outorder, zinrstat, res_history, res_line
        nonlocal ci_date, user_nr, chgsort
        nonlocal zbuff, qsy


        nonlocal z_list, om_list, bline_list, zbuff, qsy
        nonlocal z_list_data

        return {"bline-list": bline_list_data, "om-list": om_list_data, "z-list": z_list_data}

    def deactivate_ooo():

        nonlocal z_list_data, datum, cat_flag, roomnr, zimkateg, queasy, zimmer, outorder, zinrstat, res_history, res_line
        nonlocal ci_date, user_nr, chgsort
        nonlocal zbuff, qsy


        nonlocal z_list, om_list, bline_list, zbuff, qsy
        nonlocal z_list_data

        answer:bool = False
        result:bool = False
        oos_flag:bool = False
        ooo_flag:bool = False

        for bline_list in query(bline_list_data, filters=(lambda bline_list: bline_list.selected)):

            zimmer = get_cache (Zimmer, {"zinr": [(eq, bline_list.zinr)]})

            for outorder in db_session.query(Outorder).filter(
                     (Outorder.zinr == bline_list.zinr)).order_by(Outorder._recid).all():
                oos_flag = (outorder.betriebsnr == 3 or outorder.betriebsnr == 4)
                ooo_flag = (outorder.betriebsnr <= 1 and ci_date >= outorder.gespstart and ci_date <= outorder.gespende)

                if oos_flag and (outorder.gespstart == outorder.gespende):

                    zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "oos")],"datum": [(eq, ci_date)]})

                    if not zinrstat:
                        zinrstat = Zinrstat()
                        db_session.add(zinrstat)

                        zinrstat.datum = ci_date
                        zinrstat.zinr = "oos"


                    zinrstat.zimmeranz = zinrstat.zimmeranz + 1
                    db_session.delete(outorder)
                    pass

                elif ooo_flag:

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
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = user_nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Remove O-O-O Record of Room " + outorder.zinr +\
                            " " + to_string(outorder.gespstart) + "-" + to_string(outorder.gespende)
                    res_history.action = "Log Availability"


                    pass
                    pass
                    db_session.delete(outorder)
                    pass
            pass
            zimmer.bediener_nr_stat = user_nr

            if zimmer.zistatus >= 6:
                zimmer.zistatus = chgsort - 1

                om_list = query(om_list_data, filters=(lambda om_list: om_list.zinr == zimmer.zinr), first=True)
                om_list.ind = zimmer.zistatus + 1
            pass
            bline_list.selected = False
        z_list_data.clear()

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            z_list = Z_list()
            z_list_data.append(z_list)

            buffer_copy(zimmer, z_list)

            if zimmer.zistatus == 2:

                res_line = get_cache (Res_line, {"resstatus": [(eq, 8)],"zinr": [(eq, zimmer.zinr)],"abreise": [(eq, ci_date)]})

                if res_line:
                    z_list.checkout = True

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"betriebsnr": [(le, 2)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)]})

            if outorder:
                z_list.str_reason = entry(0, outorder.gespgrund, "$")


            else:
                z_list.str_reason = " "

    deactivate_ooo()

    return generate_output()