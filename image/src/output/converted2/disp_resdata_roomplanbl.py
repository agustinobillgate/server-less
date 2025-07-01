#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Reservation, Waehrung, Outorder, Zimkateg

def disp_resdata_roomplanbl(pvilanguage:int, curr_date:date, i:int, zinr:string, gstatus:int, recid1:int):

    prepare_cache ([Res_line, Reservation, Waehrung, Outorder, Zimkateg])

    n_edit = ""
    c_edit = ""
    fg_col = 0
    flag_res_line = False
    flag_outorder = False
    last_zinr = ""
    buf_res_line_list = []
    buf_reservation_list = []
    lvcarea:string = "disp-resdata-roomplan"
    res_line = reservation = waehrung = outorder = zimkateg = None

    buf_res_line = buf_reservation = None

    buf_res_line_list, Buf_res_line = create_model("Buf_res_line", {"gastnr":int, "resnr":int, "reslinnr":int, "active_flag":int, "zinr":string, "kurzbez":string, "resstatus":int, "ankunft":date, "abreise":date, "betrieb_gast":int, "zipreis":Decimal, "was_status":int, "name":string, "ziwech_zeit":int, "recid1":int})
    buf_reservation_list, Buf_reservation = create_model("Buf_reservation", {"gastnr":int, "resnr":int, "grpflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n_edit, c_edit, fg_col, flag_res_line, flag_outorder, last_zinr, buf_res_line_list, buf_reservation_list, lvcarea, res_line, reservation, waehrung, outorder, zimkateg
        nonlocal pvilanguage, curr_date, i, zinr, gstatus, recid1


        nonlocal buf_res_line, buf_reservation
        nonlocal buf_res_line_list, buf_reservation_list

        return {"n_edit": n_edit, "c_edit": c_edit, "fg_col": fg_col, "flag_res_line": flag_res_line, "flag_outorder": flag_outorder, "last_zinr": last_zinr, "buf-res-line": buf_res_line_list, "buf-reservation": buf_reservation_list}

    def disp_res_data():

        nonlocal n_edit, c_edit, fg_col, flag_res_line, flag_outorder, last_zinr, buf_res_line_list, buf_reservation_list, lvcarea, res_line, reservation, waehrung, outorder, zimkateg
        nonlocal pvilanguage, curr_date, i, zinr, gstatus, recid1


        nonlocal buf_res_line, buf_reservation
        nonlocal buf_res_line_list, buf_reservation_list

        resline = None

        if i == 0:

            res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"abreise": [(eq, curr_date)],"zinr": [(eq, zinr)],"resstatus": [(ne, 12)]})

            if res_line:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                n_edit = "ResNo: " + to_string(res_line.resnr) + " " + translateExtended ("Room:", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + translateExtended ("Guest:", lvcarea, "") + " " + res_line.name + chr_unicode(10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(res_line.ankunft) + chr_unicode(10) + translateExtended ("Depart:", lvcarea, "") + " " + to_string(res_line.abreise) + chr_unicode(10) + translateExtended ("RmRate:", lvcarea, "") + " " + to_string(res_line.zipreis)

                if res_line.betriebsnr > 0:

                    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                    if waehrung:
                        n_edit = n_edit + " " + waehrung.wabkurz
                c_edit = translateExtended ("Reservation Comment:", lvcarea, "") + chr_unicode(10) + reservation.bemerk + chr_unicode(10) + res_line.bemerk
                fg_col = 0
            else:
                n_edit = ""
                c_edit = ""

        elif gstatus == 9:

            outorder = get_cache (Outorder, {"_recid": [(eq, recid1)]})
            n_edit = ""
            c_edit = translateExtended ("Out-of-order Reason:", lvcarea, "") + chr_unicode(10)

            if outorder:
                c_edit = c_edit + outorder.gespgrund
            fg_col = 12
            pass

        elif gstatus == 12:

            outorder = get_cache (Outorder, {"_recid": [(eq, recid1)]})
            n_edit = ""
            c_edit = translateExtended ("Out-of-Service Reason:", lvcarea, "") + chr_unicode(10)

            if outorder:
                c_edit = c_edit + outorder.gespgrund
            fg_col = 12
            pass

        elif gstatus == 10:
            Resline =  create_buffer("Resline",Res_line)

            outorder = get_cache (Outorder, {"_recid": [(eq, recid1)]})

            if outorder:

                resline = get_cache (Res_line, {"resnr": [(eq, outorder.betriebsnr)],"zinr": [(eq, outorder.zinr)],"resstatus": [(eq, 1)]})
                n_edit = ""
                c_edit = translateExtended ("Off-Market Reason:", lvcarea, "") + chr_unicode(10) + outorder.gespgrund + chr_unicode(10)

                if resline:
                    c_edit = c_edit + translateExtended ("ResNo:", lvcarea, "") + " " + to_string(resline.resnr) + chr_unicode(10) + translateExtended ("Guest:", lvcarea, "") + " " + resline.name + chr_unicode(10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(resline.ankunft) + chr_unicode(10) + translateExtended ("Departure:", lvcarea, "") + " " + to_string(resline.abreise)
                fg_col = 4
                pass

        elif recid1 != 0:

            res_line = get_cache (Res_line, {"_recid": [(eq, recid1)]})

            if not res_line:

                return

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
            n_edit = translateExtended ("ResNo:", lvcarea, "") + " " + to_string(res_line.resnr) + " " + translateExtended ("Room:", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + translateExtended ("Guest:", lvcarea, "") + " " + res_line.name + chr_unicode(10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(res_line.ankunft) + chr_unicode(10) + translateExtended ("Depart:", lvcarea, "") + " " + to_string(res_line.abreise) + chr_unicode(10) + translateExtended ("RmRate:", lvcarea, "") + " " + to_string(res_line.zipreis)

            if res_line.betriebsnr > 0:

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    n_edit = n_edit + " " + waehrung.wabkurz
            c_edit = translateExtended ("Reservation Comment:", lvcarea, "") + chr_unicode(10) + reservation.bemerk + chr_unicode(10) + res_line.bemerk

            if gstatus == 1:
                fg_col = 2

            elif gstatus == 2:
                fg_col = 1

            elif gstatus == 3:
                fg_col = 9

        if res_line:

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
            buf_res_line = Buf_res_line()
            buf_res_line_list.append(buf_res_line)

            buf_res_line.gastnr = res_line.gastnr
            buf_res_line.resnr = res_line.resnr
            buf_res_line.reslinnr = res_line.reslinnr
            buf_res_line.active_flag = res_line.active_flag
            buf_res_line.zinr = res_line.zinr
            buf_res_line.kurzbez = zimkateg.kurzbez
            buf_res_line.resstatus = res_line.resstatus
            buf_res_line.ankunft = res_line.ankunft
            buf_res_line.abreise = res_line.abreise
            buf_res_line.betrieb_gast = res_line.betrieb_gast
            buf_res_line.zipreis =  to_decimal(res_line.zipreis)
            buf_res_line.was_status = res_line.was_status
            buf_res_line.name = res_line.name
            buf_res_line.ziwech_zeit = res_line.ziwech_zeit
            buf_res_line.recid1 = res_line._recid


            flag_res_line = True

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            if reservation:
                buf_reservation = Buf_reservation()
                buf_reservation_list.append(buf_reservation)

                buf_reservation.gastnr = reservation.gastnr
                buf_reservation.resnr = reservation.resnr
                buf_reservation.grpflag = reservation.grpflag

            if res_line.active_flag == 0:

                outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"betriebsnr": [(eq, res_line.resnr)]})

                if outorder:
                    flag_outorder = True
            last_zinr = res_line.zinr


    disp_res_data()

    return generate_output()