#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext, Res_line, Guest, Zimkateg, Reservation

def print_letter_disp_arlistbl(last_sort:int, fdate:date, lname:string):

    prepare_cache ([Paramtext, Res_line, Guest, Zimkateg, Reservation])

    q1_list_data = []
    paramtext = res_line = guest = zimkateg = reservation = None

    setup_list = q1_list = None

    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string, "ptexte":string})
    q1_list_data, Q1_list = create_model("Q1_list", {"resnr":int, "grpflag":bool, "gastnr":int, "name":string, "vorname1":string, "anrede1":string, "anredefirma":string, "briefnr":int, "ankunft":date, "anztage":int, "abreise":date, "kurzbez":string, "resstatus":int, "groupname":string, "activeflag":int, "roomrate":Decimal, "room_night":int, "bedsetup":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, paramtext, res_line, guest, zimkateg, reservation
        nonlocal last_sort, fdate, lname


        nonlocal setup_list, q1_list
        nonlocal setup_list_data, q1_list_data

        return {"q1-list": q1_list_data}

    def disp_arlist():

        nonlocal q1_list_data, paramtext, res_line, guest, zimkateg, reservation
        nonlocal last_sort, fdate, lname


        nonlocal setup_list, q1_list
        nonlocal setup_list_data, q1_list_data

        if last_sort == 1:

            if fdate == None:

                reservation_obj_list = {}
                for reservation, res_line, guest, zimkateg in db_session.query(Reservation, Res_line, Guest, Zimkateg).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.active_flag == 0)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Reservation.activeflag == 0) & (Reservation.name >= (lname).lower())).order_by(Reservation.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    assign_it()

                    if reservation.resnr == 80:
                        pass

            else:

                reservation_obj_list = {}
                for reservation, res_line, guest, zimkateg in db_session.query(Reservation, Res_line, Guest, Zimkateg).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Reservation.activeflag == 0) & (Reservation.name >= (lname).lower())).order_by(Reservation.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    assign_it()


        elif last_sort == 2:

            if fdate == None:

                reservation_obj_list = {}
                for reservation, res_line, guest, zimkateg in db_session.query(Reservation, Res_line, Guest, Zimkateg).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.active_flag == 0)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Reservation.activeflag == 0) & (Reservation.name >= (lname).lower())).order_by(Res_line.ankunft).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    assign_it()

            else:

                reservation_obj_list = {}
                for reservation, res_line, guest, zimkateg in db_session.query(Reservation, Res_line, Guest, Zimkateg).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Reservation.activeflag == 0) & (Reservation.name >= (lname).lower())).order_by(Res_line.ankunft).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    assign_it()


        elif last_sort == 3:

            reservation_obj_list = {}
            for reservation, res_line, guest, zimkateg in db_session.query(Reservation, Res_line, Guest, Zimkateg).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.active_flag == 0)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Reservation.activeflag == 0) & (Reservation.name >= (lname).lower())).order_by(Reservation.resnr).all():
                setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                if not setup_list:
                    continue

                if reservation_obj_list.get(reservation._recid):
                    continue
                else:
                    reservation_obj_list[reservation._recid] = True


                assign_it()

    def assign_it():

        nonlocal q1_list_data, paramtext, res_line, guest, zimkateg, reservation
        nonlocal last_sort, fdate, lname


        nonlocal setup_list, q1_list
        nonlocal setup_list_data, q1_list_data


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

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
        q1_list.roomrate =  to_decimal(res_line.zipreis)
        q1_list.room_night = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz
        q1_list.bedsetup = setup_list.ptexte

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = paramtext.txtnr - 9199
        setup_list.char = substring(paramtext.notes, 0, 1)
        setup_list.ptexte = paramtext.ptexte
    disp_arlist()

    return generate_output()