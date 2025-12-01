#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 18/7/25
# ooo tidak masuk
#-----------------------------------------
# Rd, 27/11/2025, with_for_update added
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Outorder, Zimkateg, Queasy, Zimmer, Res_line, Res_history

bline_list_data, Bline_list = create_model("Bline_list", {"zinr":string, "selected":bool, "bl_recid":int})
om_list_data, Om_list = create_model("Om_list", {"zinr":string, "ind":int})

def hk_statadmin_activate_ooobl(bline_list_data:[Bline_list], om_list_data:[Om_list], pvilanguage:int, from_date:date, 
                                to_date:date, ci_date:date, dept:int, reason:string, service_flag:bool, user_nr:int):

    prepare_cache ([Outorder, Zimkateg, Queasy, Res_line, Res_history])

    flag = 0
    msg_str = ""
    z_list_data = []
    lvcarea:string = "hk-statadmin"
    datum:date = None
    cat_flag:bool = False
    roomnr:int = 0
    outorder = zimkateg = queasy = zimmer = res_line = res_history = None

    z_list = om_list = bline_list = obuff = zbuff = qsy = None

    z_list_data, Z_list = create_model("Z_list", {"zinr":string, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":string, "bediener_nr_stat":int, "checkout":bool, "str_reason":string})

    Obuff = create_buffer("Obuff",Outorder)
    Zbuff = create_buffer("Zbuff",Zimkateg)
    Qsy = create_buffer("Qsy",Queasy)

    db_session = local_storage.db_session
    reason = reason.strip()

    def generate_output():
        nonlocal flag, msg_str, z_list_data, lvcarea, datum, cat_flag, roomnr, outorder, zimkateg, queasy, zimmer, res_line, res_history
        nonlocal pvilanguage, from_date, to_date, ci_date, dept, reason, service_flag, user_nr
        nonlocal obuff, zbuff, qsy


        nonlocal z_list, om_list, bline_list, obuff, zbuff, qsy
        nonlocal z_list_data

        return {"bline-list": bline_list_data, "om-list": om_list_data, "flag": flag, "msg_str": msg_str, "z-list": z_list_data}

    for bline_list in query(bline_list_data, filters=(lambda bline_list: bline_list.selected)):

        obuff = db_session.query(Obuff).filter(
                 (Obuff.zinr == bline_list.zinr) & (((Obuff.gespstart >= from_date) & (Obuff.gespstart <= to_date)) | ((Obuff.gespende >= from_date) & (Obuff.gespende <= to_date)) | ((from_date >= Obuff.gespstart) & (from_date <= Obuff.gespende)) | ((to_date >= Obuff.gespstart) & (to_date <= Obuff.gespende)))).first()

        if obuff:
            msg_str = translateExtended ("Overlapping O-O-O or O-M record found!", lvcarea, "") + " " + to_string(bline_list.zinr)
            flag = 1


            break

    if flag == 1:

        return generate_output()

    for bline_list in query(bline_list_data, filters=(lambda bline_list: bline_list.selected)):

        # zimmer = get_cache (Zimmer, {"zinr": [(eq, bline_list.zinr)]})
        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == bline_list.zinr)).with_for_update().first()

        res_line = db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (((Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)) | ((Res_line.abreise > from_date) & (Res_line.abreise <= to_date)) | ((from_date >= Res_line.ankunft) & (from_date < Res_line.abreise))) & (Res_line.zinr == bline_list.zinr)).first()

        if res_line:
            msg_str = translateExtended ("Attention: Room Number", lvcarea, "") + " " + to_string(bline_list.zinr) + chr_unicode(10) + translateExtended ("Reservation exists under ResNo", lvcarea, "") + " = " + to_string(res_line.resnr) + chr_unicode(10) + translateExtended ("Guest Name", lvcarea, "") + " = " + res_line.name + chr_unicode(10) + translateExtended ("Arrival :", lvcarea, "") + " " + to_string(res_line.ankunft) + " " + translateExtended ("Departure :", lvcarea, "") + " " + to_string(res_line.abreise)
            flag = 2
            break
        else:
            # Rd 18/7/25
            # add commit()->dihandle di main.py
            outorder = Outorder()
            db_session.add(outorder)

            outorder.zinr = bline_list.zinr
            outorder.gespstart = from_date
            outorder.gespende = to_date
            outorder.betriebsnr = dept
            outorder.gespgrund = reason + "$" + to_string(user_nr)
            if service_flag:
                outorder.betriebsnr = outorder.betriebsnr + 3
            pass

            queasy = get_cache (Queasy, {"key": [(eq, 152)]})

            if queasy:
                cat_flag = True

            zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

            if zbuff:

                if cat_flag:
                    roomnr = zbuff.typ
                else:
                    roomnr = zbuff.zikatnr
            for datum in date_range(from_date,to_date) :

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    # qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
                    qsy = db_session.query(Qsy).filter(
                             (Qsy._recid == queasy._recid)).with_for_update().first()

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = user_nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Change to OOO - Room : " + bline_list.zinr
            res_history.action = "Log Availability"


            pass
            pass

            if not service_flag:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = user_nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Set O-O-O to Room " + bline_list.zinr +\
                        " " + to_string(from_date) + " - " + to_string(to_date) +\
                        "; " + reason
                res_history.action = "HouseKeeping"


                pass
                pass

            if from_date == ci_date:
                pass
                zimmer.bediener_nr_stat = user_nr

                res_line = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, zimmer.zinr)]})

                if not res_line:
                    zimmer.zistatus = 6

                    om_list = query(om_list_data, filters=(lambda om_list: om_list.zinr == zimmer.zinr), first=True)

                    if outorder.betriebsnr == 3 or outorder.betriebsnr == 4:
                        om_list.ind = 10
                    else:
                        om_list.ind = 7
                pass
            bline_list.selected = False
            pass

    if flag == 2:

        return generate_output()
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

    return generate_output()