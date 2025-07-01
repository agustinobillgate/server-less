#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Reservation, Outorder

def hk_roomplan_disp_resdatabl(i:int, curr_date:date, zinr:string, gstatus:int, recid1:int):

    prepare_cache ([Res_line, Reservation, Outorder])

    n_edit = ""
    c_edit = ""
    fgcol_n = 0
    fgcol_c = 0
    t_res_line_list = []
    res_line = reservation = outorder = None

    t_res_line = resline = None

    t_res_line_list, T_res_line = create_model("T_res_line", {"rec_id":int, "ziwech_zeit":int})

    Resline = create_buffer("Resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal n_edit, c_edit, fgcol_n, fgcol_c, t_res_line_list, res_line, reservation, outorder
        nonlocal i, curr_date, zinr, gstatus, recid1
        nonlocal resline


        nonlocal t_res_line, resline
        nonlocal t_res_line_list

        return {"n_edit": n_edit, "c_edit": c_edit, "fgcol_n": fgcol_n, "fgcol_c": fgcol_c, "t-res-line": t_res_line_list}

    if i == 0:

        res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"abreise": [(eq, curr_date)],"zinr": [(eq, zinr)],"resstatus": [(ne, 12)]})

        if res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
            n_edit = "ResNo: " + to_string(res_line.resnr) + " " + "Room: " + res_line.zinr + chr_unicode(10) + "Guest: " + res_line.name + chr_unicode(10) + "Arrival: " + to_string(res_line.ankunft) + chr_unicode(10) + "Depart: " + to_string(res_line.abreise)
            c_edit = "Reservation Comment:" + chr_unicode(10) + reservation.bemerk + chr_unicode(10) + res_line.bemerk
            fgcol_n = 0
            fgcol_c = 0
        else:
            n_edit = ""
            c_edit = ""

    elif gstatus == 9:

        outorder = get_cache (Outorder, {"_recid": [(eq, recid1)]})
        n_edit = ""
        c_edit = "Out-of-order Reason:" + chr_unicode(10) + outorder.gespgrund
        fgcol_c = 12
        pass

    elif gstatus == 10:

        outorder = get_cache (Outorder, {"_recid": [(eq, recid1)]})

        resline = get_cache (Res_line, {"resnr": [(eq, outorder.betriebsnr)],"zinr": [(eq, outorder.zinr)],"resstatus": [(eq, 1)]})
        n_edit = ""
        c_edit = "Off-Market Reason:" + chr_unicode(10) + outorder.gespgrund + chr_unicode(10)

        if resline:
            c_edit = c_edit + "ResNo: " + to_string(resline.resnr) + chr_unicode(10) + "Guest: " + resline.name + chr_unicode(10) + "Arrival: " + to_string(resline.ankunft) + chr_unicode(10) + "Departure: " + to_string(resline.abreise)
        fgcol_c = 4
        pass

    elif recid1 != 0:

        res_line = get_cache (Res_line, {"_recid": [(eq, recid1)]})

        reservation = get_cache (Reservation, {"gastnr": [(eq, res_line.gastnr)],"resnr": [(eq, res_line.resnr)]})
        n_edit = "ResNo: " + to_string(res_line.resnr) + " " + "Room: " + res_line.zinr + chr_unicode(10) + "Guest: " + res_line.name + chr_unicode(10) + "Arrival: " + to_string(res_line.ankunft) + chr_unicode(10) + "Depart: " + to_string(res_line.abreise)
        c_edit = "Reservation Comment:" + chr_unicode(10) + reservation.bemerk + chr_unicode(10) + res_line.bemerk

        if gstatus == 1:
            fgcol_n = 2
            fgcol_c = 2

        elif gstatus == 2:
            fgcol_n = 1
            fgcol_c = 1

        elif gstatus == 3:
            fgcol_n = 9
            fgcol_c = 9
    else:
        pass

    if res_line:
        t_res_line = T_res_line()
        t_res_line_list.append(t_res_line)

        t_res_line.rec_id = res_line._recid
        t_res_line.ziwech_zeit = res_line.ziwech_zeit

    return generate_output()