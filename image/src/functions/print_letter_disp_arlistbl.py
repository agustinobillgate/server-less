from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Paramtext, Res_line, Guest, Zimkateg, Reservation

def print_letter_disp_arlistbl(last_sort:int, fdate:date, lname:str):
    q1_list_list = []
    paramtext = res_line = guest = zimkateg = reservation = None

    setup_list = q1_list = None

    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str, "ptexte":str})
    q1_list_list, Q1_list = create_model("Q1_list", {"resnr":int, "grpflag":bool, "gastnr":int, "name":str, "vorname1":str, "anrede1":str, "anredefirma":str, "briefnr":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":str, "resstatus":int, "groupname":str, "activeflag":int, "roomrate":decimal, "room_night":int, "bedsetup":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, paramtext, res_line, guest, zimkateg, reservation


        nonlocal setup_list, q1_list
        nonlocal setup_list_list, q1_list_list
        return {"q1-list": q1_list_list}

    def assign_it():

        nonlocal q1_list_list, paramtext, res_line, guest, zimkateg, reservation


        nonlocal setup_list, q1_list
        nonlocal setup_list_list, q1_list_list

        if last_sort == 1:

            if fdate == None:

                reservation_obj_list = []
                for reservation, res_line, guest, zimkateg, setup_list in db_session.query(Reservation, Res_line, Guest, Zimkateg, Setup_list).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.active_flag == 0)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Setup_list,(Setup_list.nr == res_line.setup + 1)).filter(
                            (Reservation.activeflag == 0) &  (func.lower(Reservation.name) >= (lname).lower())).all():
                    if reservation._recid in reservation_obj_list:
                        continue
                    else:
                        reservation_obj_list.append(reservation._recid)


                    assign_it()

                    if reservation.resnr == 80:
                    else:

                        reservation_obj_list = []
                    for reservation, res_line, guest, zimkateg, setup_list in db_session.query(Reservation, Res_line, Guest, Zimkateg, Setup_list).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= fdate)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Setup_list,(Setup_list.nr == res_line.setup + 1)).filter(
                                (Reservation.activeflag == 0) &  (func.lower(Reservation.name) >= (lname).lower())).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        assign_it()


            elif last_sort == 2:

                if fdate == None:

                    reservation_obj_list = []
                    for reservation, res_line, guest, zimkateg, setup_list in db_session.query(Reservation, Res_line, Guest, Zimkateg, Setup_list).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.active_flag == 0)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Setup_list,(Setup_list.nr == res_line.setup + 1)).filter(
                                (Reservation.activeflag == 0) &  (func.lower(Reservation.name) >= (lname).lower())).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        assign_it()

                else:

                    reservation_obj_list = []
                    for reservation, res_line, guest, zimkateg, setup_list in db_session.query(Reservation, Res_line, Guest, Zimkateg, Setup_list).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.active_flag == 0) &  (Res_line.ankunft >= fdate)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Setup_list,(Setup_list.nr == res_line.setup + 1)).filter(
                                (Reservation.activeflag == 0) &  (func.lower(Reservation.name) >= (lname).lower())).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        assign_it()


            elif last_sort == 3:

                reservation_obj_list = []
                for reservation, res_line, guest, zimkateg, setup_list in db_session.query(Reservation, Res_line, Guest, Zimkateg, Setup_list).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.active_flag == 0)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == res_line.zikatnr)).join(Setup_list,(Setup_list.nr == res_line.setup + 1)).filter(
                            (Reservation.activeflag == 0) &  (func.lower(Reservation.name) >= (lname).lower())).all():
                    if reservation._recid in reservation_obj_list:
                        continue
                    else:
                        reservation_obj_list.append(reservation._recid)


                    assign_it()

            q1_list = Q1_list()
            q1_list_list.append(q1_list)

            q1_list.resnr = reservation.resnr
            q1_list.grpflag = reservation.grpflag
            q1_list.gastnr = reservation.gastnr
            q1_list.name = guest.name
            q1_list.vorname1 = guest.vorname1
            q1_list.anrede1 = guest.anrede1
            q1_list.anredefirma = guest.anredefirma
            q1_list.briefnr = reservation.briefnr
            q1_list.ankunft = res_line.ankunft
            q1_list.anztage = res_line.anztage
            q1_list.abreise = res_line.abreise
            q1_list.kurzbez = zimkateg.kurzbez
            q1_list.resstatus = res_line.resstatus
            q1_list.groupname = reservation.groupname
            q1_list.activeflag = reservation.activeflag
            q1_list.roomrate = res_line.zipreis
            q1_list.room_night = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz
            q1_list.bedsetup = setup_list.ptexte


    for paramtext in db_session.query(Paramtext).filter(
            (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = paramtext.txtnr - 9199
        setup_list.char = substring(paramtext.notes, 0, 1)
        setup_list.ptexte = paramtext.ptexte
    disp_arlist()

    return generate_output()