#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Zimmer, Outorder, Bediener, Res_history, Queasy, Zimkateg

bline_list_list, Bline_list = create_model("Bline_list", {"zinr":string, "selected":bool, "bl_recid":int})
om_list_list, Om_list = create_model("Om_list", {"zinr":string, "ind":int})

def hk_statadmin_chk_btn_exit1bl(bline_list_list:[Bline_list], om_list_list:[Om_list], pvilanguage:int, resflag:bool, dept:int, zinr:string, user_nr:int, from_date:date, to_date:date, ci_date:date, reason:string):

    prepare_cache ([Res_line, Outorder, Bediener, Res_history, Queasy, Zimkateg])

    msg_str = ""
    z_list_list = []
    return_flag:bool = False
    from_stat:string = ""
    to_stat:string = ""
    curr_date:date = None
    lvcarea:string = "hk-statadmin"
    stat_list:List[string] = create_empty_list(10,"")
    res_line = zimmer = outorder = bediener = res_history = queasy = zimkateg = None

    z_list = om_list = bline_list = resline = None

    z_list_list, Z_list = create_model("Z_list", {"zinr":string, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":string, "bediener_nr_stat":int, "checkout":bool, "str_reason":string})

    Resline = create_buffer("Resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, z_list_list, return_flag, from_stat, to_stat, curr_date, lvcarea, stat_list, res_line, zimmer, outorder, bediener, res_history, queasy, zimkateg
        nonlocal pvilanguage, resflag, dept, zinr, user_nr, from_date, to_date, ci_date, reason
        nonlocal resline


        nonlocal z_list, om_list, bline_list, resline
        nonlocal z_list_list

        return {"bline-list": bline_list_list, "om-list": om_list_list, "msg_str": msg_str, "z-list": z_list_list}

    def update_queasy(zikatnr:int):

        nonlocal msg_str, z_list_list, return_flag, from_stat, to_stat, curr_date, lvcarea, stat_list, res_line, zimmer, outorder, bediener, res_history, queasy, zimkateg
        nonlocal pvilanguage, resflag, dept, zinr, user_nr, from_date, to_date, ci_date, reason
        nonlocal resline


        nonlocal z_list, om_list, bline_list, resline
        nonlocal z_list_list

        cat_flag:bool = False
        z_nr:int = 0
        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zikatnr)]})

        if zimkateg:

            if cat_flag:
                z_nr = zimkateg.typ
            else:
                z_nr = zimkateg.zikatnr

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(ge, ci_date)],"number1": [(eq, z_nr)]})
        while None != queasy and queasy.logi1 == False and queasy.logi2 == False :

            qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

            if qsy:
                qsy.logi2 = True
                pass
                pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 >= ci_date) & (Queasy.number1 == z_nr) & (Queasy._recid > curr_recid)).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = user_nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Room " + zimmer.zinr +\
                " Status Changed From " + from_stat + " to " + to_stat
        res_history.action = "Log Availability"


        pass
        pass

    stat_list[0] = translateExtended ("Vacant Clean Checked", lvcarea, "")
    stat_list[1] = translateExtended ("Vacant Clean Unchecked", lvcarea, "")
    stat_list[2] = translateExtended ("Vacant Dirty", lvcarea, "")
    stat_list[3] = translateExtended ("Expected Departure", lvcarea, "")
    stat_list[4] = translateExtended ("Occupied Dirty", lvcarea, "")
    stat_list[5] = translateExtended ("Occupied Cleaned", lvcarea, "")
    stat_list[6] = translateExtended ("Out-of-Order", lvcarea, "")
    stat_list[7] = translateExtended ("Off-Market", lvcarea, "")
    stat_list[8] = translateExtended ("Do not Disturb", lvcarea, "")
    stat_list[9] = translateExtended ("Out-of-Service", lvcarea, "")

    res_line = get_cache (Res_line, {"resnr": [(eq, dept)],"zinr": [(eq, zinr)]})

    for bline_list in query(bline_list_list, filters=(lambda bline_list: bline_list.selected)):

        zimmer = get_cache (Zimmer, {"zinr": [(eq, bline_list.zinr)]})
        for curr_date in date_range(from_date,to_date) :

            outorder = db_session.query(Outorder).filter(
                     (Outorder.zinr == zimmer.zinr) & ((Outorder.gespstart >= curr_date) & (Outorder.gespstart <= curr_date) | (Outorder.gespstart <= curr_date) & (Outorder.gespende >= curr_date)) & (Outorder.betriebsnr == 2)).first()

            if outorder:
                msg_str = msg_str + translateExtended ("Overlapping Off-Market found:", lvcarea, "") + chr_unicode(10) + translateExtended ("Room No", lvcarea, "") + " " + outorder.zinr + " - " + to_string(outorder.gespstart) + " To " + to_string(outorder.gespende)

                return generate_output()

        if not resflag:

            resline = get_cache (Res_line, {"active_flag": [(le, 1)],"resnr": [(ne, res_line.resnr)],"resstatus": [(ne, 12)],"abreise": [(le, from_date)],"ankunft": [(gt, to_date)],"zinr": [(eq, zinr)]})
        else:

            resline = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(ne, 12)],"abreise": [(le, from_date)],"ankunft": [(gt, to_date)],"zinr": [(eq, zinr)]})

        if resline:
            msg_str = msg_str + translateExtended ("Reservation exists under ResNo", lvcarea, "") + " = " + to_string(resline.resnr) + chr_unicode(10) + translateExtended ("Guest Name", lvcarea, "") + " = " + resline.name + chr_unicode(10) + translateExtended ("Arrival :", lvcarea, "") + " " + to_string(resline.ankunft) + " " + translateExtended ("Departure :", lvcarea, "") + " " + to_string(resline.abreise)
            return_flag = True

            return generate_output()

    for bline_list in query(bline_list_list, filters=(lambda bline_list: bline_list.selected)):

        zimmer = get_cache (Zimmer, {"zinr": [(eq, bline_list.zinr)]})

        om_list = query(om_list_list, filters=(lambda om_list: om_list.zinr == bline_list.zinr), first=True)
        from_stat = to_string(zimmer.zistatus) + " " + stat_list[om_list.ind - 1]
        outorder = Outorder()
        db_session.add(outorder)

        outorder.zinr = bline_list.zinr
        outorder.gespstart = from_date
        outorder.gespende = to_date

        if resflag:
            outorder.betriebsnr = 2
        else:
            outorder.betriebsnr = dept
        outorder.gespgrund = reason + "$" + to_string(user_nr)
        pass

        if outorder.gespstart == ci_date:

            om_list = query(om_list_list, filters=(lambda om_list: om_list.zinr == outorder.zinr), first=True)
            om_list.ind = 8
            to_stat = to_string(zimmer.zistatus) + " " + stat_list[om_list.ind - 1]

            bediener = get_cache (Bediener, {"nr": [(eq, user_nr)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Room " + zimmer.zinr +\
                    " Status Changed From " +\
                    from_stat + " to " + to_stat
            res_history.action = "HouseKeeping"


            pass
            pass
        update_queasy(zimmer.zikatnr)
        pass
        zimmer.bediener_nr_stat = user_nr
        pass
        bline_list.selected = False

    if return_flag:

        return generate_output()
    z_list_list.clear()

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        z_list = Z_list()
        z_list_list.append(z_list)

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

    return generate_output()