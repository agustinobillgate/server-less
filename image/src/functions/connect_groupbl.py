from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Reservation, Guest, Zimkateg

def connect_groupbl(case_type:int, resno:int, reslinno:int, gastno:int, grpname:str, gname:str, sorttype:int):
    res_list_list = []
    mainres_list_list = []
    guest_list_list = []
    ci_date:date = None
    co_date:date = None
    res_line = reservation = guest = zimkateg = None

    guest_list = res_list = mainres_list = mainbuff = gast = mainres = rline = None

    guest_list_list, Guest_list = create_model("Guest_list", {"gastnr":int, "name":str, "anredefirma":str, "wohnort":str, "karteityp":int})
    res_list_list, Res_list = create_model_like(Res_line, {"kurzbez":str, "groupname":str, "join_flag":bool, "mbill_flag":bool, "prev_join":bool, "prev_mbill":bool})
    mainres_list_list, Mainres_list = create_model("Mainres_list", {"gastnr":int, "resnr":int, "actflag":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":decimal, "until":date, "paid":decimal, "id1":str, "id2":str, "id2_date":date, "groupname":str, "grpflag":bool, "bemerk":str, "arrival":bool, "resident":bool, "arr_today":bool})

    Mainbuff = Reservation
    Gast = Guest
    Mainres = Reservation
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_list_list, mainres_list_list, guest_list_list, ci_date, co_date, res_line, reservation, guest, zimkateg
        nonlocal mainbuff, gast, mainres, rline


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres, rline
        nonlocal guest_list_list, res_list_list, mainres_list_list
        return {"res-list": res_list_list, "mainres-list": mainres_list_list, "guest-list": guest_list_list}

    def create_res():

        nonlocal res_list_list, mainres_list_list, guest_list_list, ci_date, co_date, res_line, reservation, guest, zimkateg
        nonlocal mainbuff, gast, mainres, rline


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres, rline
        nonlocal guest_list_list, res_list_list, mainres_list_list


        fill_mainres()

    def fill_mainres():

        nonlocal res_list_list, mainres_list_list, guest_list_list, ci_date, co_date, res_line, reservation, guest, zimkateg
        nonlocal mainbuff, gast, mainres, rline


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres, rline
        nonlocal guest_list_list, res_list_list, mainres_list_list

        do_it:bool = False
        Rline = Res_line

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastno)).first()

        for reservation in db_session.query(Reservation).filter(
                (Reservation.gastnr == gastno) &  (Reservation.resnr != resno) &  (Reservation.activeflag == 0) &  (Reservation.groupname != "")).all():

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reservation.resnr) &  (Res_line.active_flag == 1)).first()
            do_it = None != res_line

            if not do_it:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == reservation.resnr) &  (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (Res_line.ankunft <= co_date)).first()
                do_it = None != res_line

            if do_it:

                mainres_list = query(mainres_list_list, filters=(lambda mainres_list :mainres_list.resnr == reservation.resnr), first=True)

                if not mainres_list:
                    mainres_list = Mainres_list()
                    mainres_list_list.append(mainres_list)

                    mainres_list.resnr = reservation.resnr
                    mainres_list.deposit = reservation.depositgef
                    mainres_list.until = reservation.limitdate
                    mainres_list.paid = depositbez + depositbez2
                    mainres_list.segm = reservation.segmentcode
                    mainres_list.groupname = reservation.groupname
                    mainres_list.bemerk = reservation.bemerk
                    mainres_list.id1 = reservation.useridanlage
                    mainres_list.id2 = reservation.useridmutat
                    mainres_list.id2_date = reservation.mutdat
                    mainres_list.grpflag = reservation.grpflag


                    update_mainres()

    def update_mainres():

        nonlocal res_list_list, mainres_list_list, guest_list_list, ci_date, co_date, res_line, reservation, guest, zimkateg
        nonlocal mainbuff, gast, mainres, rline


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres, rline
        nonlocal guest_list_list, res_list_list, mainres_list_list


        mainres_list.ankunft = 01/01/2099
        mainres_list.abreise = 01/01/1998
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == mainres_list.resnr) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12)).all():

            if res_line.resstatus <= 6:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if mainres_list.ankunft > res_line.ankunft:
                mainres_list.ankunft = res_line.ankunft

            if mainres_list.abreise < res_line.abreise:
                mainres_list.abreise = res_line.abreise

            if (res_line.resstatus <= 5 or res_line.resstatus == 11):
                mainres_list.arrival = True

            if mainres_list.arrival  and res_line.ankunft == ci_date:
                mainres_list.arr_today = True

            if res_line.resstatus == 6 or res_line.resstatus == 13:
                mainres_list.resident = True

        for mainres_list in query(mainres_list_list, filters=(lambda mainres_list :mainres_list.zimanz == 0)):
            mainres_list_list.remove(mainres_list)

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

    if res_line:
        co_date = res_line.abreise

    if case_type == 1:

        res_line_obj_list = []
        for res_line, zimkateg, mainbuff in db_session.query(Res_line, Zimkateg, Mainbuff).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Mainbuff,(Mainbuff.resnr == Res_line.resnr)).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 12) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            res_list = Res_list()
            res_list_list.append(res_list)

            buffer_copy(res_line, res_list)

            if res_list.l_zuordnung[1] == 0 and res_list.l_zuordnung[4] == 0:
                res_list.join_flag = True
                res_list.mbill_flag = True
                res_list.prev_join = False
                res_list.prev_mbill = res_list.mbill_flag


            else:
                res_list.join_flag = res_list.l_zuordnung[4] != 0
                res_list.mbill_flag = res_list.l_zuordnung[1] == 0
                res_list.prev_join = res_list.join_flag
                res_list.prev_mbill = res_list.mbill_flag

            if res_line.l_zuordnung[4] != 0:

                mainres_obj_list = []
                for mainres, guest in db_session.query(Mainres, Guest).join(Guest,(Guest.gastnr == Mainres.gastnr)).filter(
                        (Mainres.resnr == res_line.l_zuordnung[4])).all():
                    if mainres._recid in mainres_obj_list:
                        continue
                    else:
                        mainres_obj_list.append(mainres._recid)

                    guest_list = query(guest_list_list, filters=(lambda guest_list :guest_list.gastnr == guest.gastnr), first=True)

                    if not guest_list:
                        gastno = guest.gastnr


                        guest_list = Guest_list()
                        guest_list_list.append(guest_list)

                        guest_list.gastnr = guest.gastnr
                        guest_list.name = guest.name
                        guest_list.anredefirma = guest.anredefirma
                        guest_list.wohnort = guest.wohnort
                        guest_list.karteityp = guest.karteityp


                    create_res()

    elif case_type == 2:

        reservation_obj_list = []
        for reservation, gast in db_session.query(Reservation, Gast).join(Gast,(Gast.gastnr == Reservation.gastnr)).filter(
                (Reservation.activeflag == 0) &  (func.lower(Reservation.groupname) == (grpname).lower())).all():
            if reservation._recid in reservation_obj_list:
                continue
            else:
                reservation_obj_list.append(reservation._recid)

            if gast:
                guest_list = Guest_list()
                guest_list_list.append(guest_list)

                guest_list.gastnr = gast.gastnr
                guest_list.name = gast.name
                guest_list.anredefirma = gast.anredefirma
                guest_list.wohnort = gast.wohnort
                guest_list.karteityp = gast.karteityp

    elif case_type == 22:

        reservation_obj_list = []
        for reservation, gast in db_session.query(Reservation, Gast).join(Gast,(Gast.gastnr == Reservation.gastnr) &  (func.lower(Gast.name) >= (gname).lower()) &  (Gast.gastnr > 0) &  (Gast.karteityp == sorttype)).filter(
                (Reservation.activeflag == 0) &  (Reservation.groupname != "")).all():
            if reservation._recid in reservation_obj_list:
                continue
            else:
                reservation_obj_list.append(reservation._recid)

            if gast:
                guest_list = Guest_list()
                guest_list_list.append(guest_list)

                guest_list.gastnr = gast.gastnr
                guest_list.name = gast.name
                guest_list.anredefirma = gast.anredefirma
                guest_list.wohnort = gast.wohnort
                guest_list.karteityp = gast.karteityp

    elif case_type == 23:

        reservation_obj_list = []
        for reservation, gast in db_session.query(Reservation, Gast).join(Gast,(Gast.gastnr == Reservation.gastnr) &  (func.lower(Gast.name) >= (gname).lower()) &  (Gast.gastnr > 0) &  (Gast.karteityp == sorttype)).filter(
                (Reservation.activeflag == 0)).all():
            if reservation._recid in reservation_obj_list:
                continue
            else:
                reservation_obj_list.append(reservation._recid)

            if gast:

                guest_list = query(guest_list_list, filters=(lambda guest_list :guest_list.gastnr == gast.gastnr), first=True)

                if not guest_list:
                    guest_list = Guest_list()
                    guest_list_list.append(guest_list)

                    guest_list.gastnr = gast.gastnr
                    guest_list.name = gast.name
                    guest_list.anredefirma = gast.anredefirma
                    guest_list.wohnort = gast.wohnort
                    guest_list.karteityp = gast.karteityp

    elif case_type == 3:
        create_res()

    return generate_output()