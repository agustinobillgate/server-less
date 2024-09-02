from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Reservation, Waehrung, Outorder, Zimkateg

def disp_resdata_roomplanbl(pvilanguage:int, curr_date:date, i:int, zinr:str, gstatus:int, recid1:int):
    n_edit = ""
    c_edit = ""
    fg_col = 0
    flag_res_line = False
    flag_outorder = False
    last_zinr = ""
    buf_res_line_list = []
    buf_reservation_list = []
    lvcarea:str = "disp_resdata_roomplan"
    res_line = reservation = waehrung = outorder = zimkateg = None

    buf_res_line = buf_reservation = resline = None

    buf_res_line_list, Buf_res_line = create_model("Buf_res_line", {"gastnr":int, "resnr":int, "reslinnr":int, "active_flag":int, "zinr":str, "kurzbez":str, "resstatus":int, "ankunft":date, "abreise":date, "betrieb_gast":int, "zipreis":decimal, "was_status":int, "name":str, "ziwech_zeit":int, "recid1":int})
    buf_reservation_list, Buf_reservation = create_model("Buf_reservation", {"gastnr":int, "resnr":int, "grpflag":bool})

    Resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n_edit, c_edit, fg_col, flag_res_line, flag_outorder, last_zinr, buf_res_line_list, buf_reservation_list, lvcarea, res_line, reservation, waehrung, outorder, zimkateg
        nonlocal resline


        nonlocal buf_res_line, buf_reservation, resline
        nonlocal buf_res_line_list, buf_reservation_list
        return {"n_edit": n_edit, "c_edit": c_edit, "fg_col": fg_col, "flag_res_line": flag_res_line, "flag_outorder": flag_outorder, "last_zinr": last_zinr, "buf-res-line": buf_res_line_list, "buf-reservation": buf_reservation_list}

    def disp_res_data():

        nonlocal n_edit, c_edit, fg_col, flag_res_line, flag_outorder, last_zinr, buf_res_line_list, buf_reservation_list, lvcarea, res_line, reservation, waehrung, outorder, zimkateg
        nonlocal resline


        nonlocal buf_res_line, buf_reservation, resline
        nonlocal buf_res_line_list, buf_reservation_list

        if i == 0:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 1) &  (Res_line.abreise == curr_date) &  (func.lower(Res_line.zinr) == (zinr).lower()) &  (Res_line.resstatus != 12)).first()

            if res_line:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()
                n_edit = "ResNo: " + to_string(res_line.resnr) + "   " + translateExtended ("Room:", lvcarea, "") + " " + res_line.zinr + chr (10) + translateExtended ("Guest:", lvcarea, "") + " " + res_line.name + chr (10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(res_line.ankunft) + chr (10) + translateExtended ("Depart:", lvcarea, "") + " " + to_string(res_line.abreise) + chr (10) + translateExtended ("RmRate:", lvcarea, "") + " " + to_string(res_line.zipreis)

                if res_line.betriebsnr > 0:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                    if waehrung:
                        n_edit = n_edit + " " + waehrung.wabkurz
                c_edit = translateExtended ("Reservation Comment:", lvcarea, "") + chr (10) + reservation.bemerk + chr (10) + res_line.bemerk
                fg_col = 0
            else:
                n_edit = ""
                c_edit = ""

        elif gstatus == 9:

            outorder = db_session.query(Outorder).filter(
                    (Outorder._recid == recid1)).first()
            n_edit = ""
            c_edit = translateExtended ("Out_of_order Reason:", lvcarea, "") + chr (10)

            if outorder:
                c_edit = c_edit + outorder.gespgrund
            fg_col = 12


        elif gstatus == 12:

            outorder = db_session.query(Outorder).filter(
                    (Outorder._recid == recid1)).first()
            n_edit = ""
            c_edit = translateExtended ("Out_of_Service Reason:", lvcarea, "") + chr (10)

            if outorder:
                c_edit = c_edit + outorder.gespgrund
            fg_col = 12


        elif gstatus == 10:
            Resline = Res_line

            outorder = db_session.query(Outorder).filter(
                    (Outorder._recid == recid1)).first()

            if outorder:

                resline = db_session.query(Resline).filter(
                        (Resline.resnr == outorder.betriebsnr) &  (Resline.zinr == outorder.zinr) &  (Resline.resstatus == 1)).first()
                n_edit = ""
                c_edit = translateExtended ("Off_Market Reason:", lvcarea, "") + chr (10) + outorder.gespgrund + chr (10)

                if resline:
                    c_edit = c_edit + translateExtended ("ResNo:", lvcarea, "") + " " + to_string(resline.resnr) + chr (10) + translateExtended ("Guest:", lvcarea, "") + " " + resline.name + chr (10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(resline.ankunft) + chr (10) + translateExtended ("Departure:", lvcarea, "") + " " + to_string(resline.abreise)
                fg_col = 4


        elif recid1 != 0:

            res_line = db_session.query(Res_line).filter(
                    (Res_line._recid == recid1)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()
            n_edit = translateExtended ("ResNo:", lvcarea, "") + " " + to_string(res_line.resnr) + "   " + translateExtended ("Room:", lvcarea, "") + " " + res_line.zinr + chr (10) + translateExtended ("Guest:", lvcarea, "") + " " + res_line.name + chr (10) + translateExtended ("Arrival:", lvcarea, "") + " " + to_string(res_line.ankunft) + chr (10) + translateExtended ("Depart:", lvcarea, "") + " " + to_string(res_line.abreise) + chr (10) + translateExtended ("RmRate:", lvcarea, "") + " " + to_string(res_line.zipreis)

            if res_line.betriebsnr > 0:

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    n_edit = n_edit + " " + waehrung.wabkurz
            c_edit = translateExtended ("Reservation Comment:", lvcarea, "") + chr (10) + reservation.bemerk + chr (10) + res_line.bemerk

            if gstatus == 1:
                fg_col = 2

            elif gstatus == 2:
                fg_col = 1

            elif gstatus == 3:
                fg_col = 9

        if res_line:

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()
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
            buf_res_line.zipreis = res_line.zipreis
            buf_res_line.was_status = res_line.was_status
            buf_res_line.name = res_line.name
            buf_res_line.ziwech_zeit = res_line.ziwech_zeit
            buf_res_line.recid1 = res_line._recid


            flag_res_line = True

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            if reservation:
                buf_reservation = Buf_reservation()
                buf_reservation_list.append(buf_reservation)

                buf_reservation.gastnr = reservation.gastnr
                buf_reservation.resnr = reservation.resnr
                buf_reservation.grpflag = reservation.grpflag

            if res_line.active_flag == 0:

                outorder = db_session.query(Outorder).filter(
                        (Outorder.zinr == res_line.zinr) &  (Outorder.betriebsnr == res_line.resnr)).first()

                if outorder:
                    flag_outorder = True
            last_zinr = res_line.zinr

    disp_res_data()

    return generate_output()