#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Reservation, Guest, Zimkateg

def connect_groupbl(case_type:int, resno:int, reslinno:int, gastno:int, grpname:string, gname:string, sorttype:int):

    prepare_cache ([Reservation, Guest])

    res_list_list = []
    mainres_list_list = []
    guest_list_list = []
    ci_date:date = None
    co_date:date = None
    res_line = reservation = guest = zimkateg = None

    guest_list = res_list = mainres_list = mainbuff = gast = mainres = None

    guest_list_list, Guest_list = create_model("Guest_list", {"gastnr":int, "name":string, "anredefirma":string, "wohnort":string, "karteityp":int})
    res_list_list, Res_list = create_model_like(Res_line, {"kurzbez":string, "groupname":string, "join_flag":bool, "mbill_flag":bool, "prev_join":bool, "prev_mbill":bool})
    mainres_list_list, Mainres_list = create_model("Mainres_list", {"gastnr":int, "resnr":int, "actflag":int, "zimanz":int, "ankunft":date, "abreise":date, "segm":int, "deposit":Decimal, "until":date, "paid":Decimal, "id1":string, "id2":string, "id2_date":date, "groupname":string, "grpflag":bool, "bemerk":string, "arrival":bool, "resident":bool, "arr_today":bool})

    Mainbuff = create_buffer("Mainbuff",Reservation)
    Gast = create_buffer("Gast",Guest)
    Mainres = create_buffer("Mainres",Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_list_list, mainres_list_list, guest_list_list, ci_date, co_date, res_line, reservation, guest, zimkateg
        nonlocal case_type, resno, reslinno, gastno, grpname, gname, sorttype
        nonlocal mainbuff, gast, mainres


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres
        nonlocal guest_list_list, res_list_list, mainres_list_list

        return {"res-list": res_list_list, "mainres-list": mainres_list_list, "guest-list": guest_list_list}

    def create_res():

        nonlocal res_list_list, mainres_list_list, guest_list_list, ci_date, co_date, res_line, reservation, guest, zimkateg
        nonlocal case_type, resno, reslinno, gastno, grpname, gname, sorttype
        nonlocal mainbuff, gast, mainres


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres
        nonlocal guest_list_list, res_list_list, mainres_list_list


        fill_mainres()


    def fill_mainres():

        nonlocal res_list_list, mainres_list_list, guest_list_list, ci_date, co_date, res_line, reservation, guest, zimkateg
        nonlocal case_type, resno, reslinno, gastno, grpname, gname, sorttype
        nonlocal mainbuff, gast, mainres


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres
        nonlocal guest_list_list, res_list_list, mainres_list_list

        do_it:bool = False
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.gastnr == gastno) & (Reservation.resnr != resno) & (Reservation.activeflag == 0) & (Reservation.groupname != "")).order_by(Reservation._recid).all():

            res_line = get_cache (Res_line, {"resnr": [(eq, reservation.resnr)],"active_flag": [(eq, 1)]})
            do_it = None != res_line

            if not do_it:

                res_line = db_session.query(Res_line).filter(
                         (Res_line.resnr == reservation.resnr) & (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.ankunft <= co_date)).first()
                do_it = None != res_line

            if do_it:

                mainres_list = query(mainres_list_list, filters=(lambda mainres_list: mainres_list.resnr == reservation.resnr), first=True)

                if not mainres_list:
                    mainres_list = Mainres_list()
                    mainres_list_list.append(mainres_list)

                    mainres_list.resnr = reservation.resnr
                    mainres_list.deposit =  to_decimal(reservation.depositgef)
                    mainres_list.until = reservation.limitdate
                    mainres_list.paid =  to_decimal(depositbez) + to_decimal(depositbez2)
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
        nonlocal case_type, resno, reslinno, gastno, grpname, gname, sorttype
        nonlocal mainbuff, gast, mainres


        nonlocal guest_list, res_list, mainres_list, mainbuff, gast, mainres
        nonlocal guest_list_list, res_list_list, mainres_list_list


        mainres_list.ankunft = date_mdy(1, 1, 2099)
        mainres_list.abreise = date_mdy(1, 1, 1998)
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == mainres_list.resnr) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12)).order_by(Res_line._recid).all():

            if res_line.resstatus <= 6:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if mainres_list.ankunft > res_line.ankunft:
                mainres_list.ankunft = res_line.ankunft

            if mainres_list.abreise < res_line.abreise:
                mainres_list.abreise = res_line.abreise

            if (resstatus <= 5 or resstatus == 11):
                mainres_list.arrival = True

            if mainres_list.arrival  and res_line.ankunft == ci_date:
                mainres_list.arr_today = True

            if res_line.resstatus == 6 or res_line.resstatus == 13:
                mainres_list.resident = True

        for mainres_list in query(mainres_list_list, filters=(lambda mainres_list: mainres_list.zimanz == 0)):
            mainres_list_list.remove(mainres_list)


    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

    if res_line:
        co_date = res_line.abreise

    if case_type == 1:

        res_line_obj_list = {}
        for res_line, zimkateg, mainbuff in db_session.query(Res_line, Zimkateg, Mainbuff).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Mainbuff,(Mainbuff.resnr == Res_line.resnr)).filter(
                 (Res_line.resnr == resno) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


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

                mainres_obj_list = {}
                mainres = Reservation()
                guest = Guest()
                for mainres.resnr, mainres.depositgef, mainres.limitdate, mainres.segmentcode, mainres.groupname, mainres.bemerk, mainres.useridanlage, mainres.useridmutat, mainres.mutdat, mainres.grpflag, mainres._recid, guest.gastnr, guest.name, guest.anredefirma, guest.wohnort, guest.karteityp, guest._recid in db_session.query(Mainres.resnr, Mainres.depositgef, Mainres.limitdate, Mainres.segmentcode, Mainres.groupname, Mainres.bemerk, Mainres.useridanlage, Mainres.useridmutat, Mainres.mutdat, Mainres.grpflag, Mainres._recid, Guest.gastnr, Guest.name, Guest.anredefirma, Guest.wohnort, Guest.karteityp, Guest._recid).join(Guest,(Guest.gastnr == Mainres.gastnr)).filter(
                         (Mainres.resnr == res_line.l_zuordnung[4])).order_by(Mainres._recid).all():
                    if mainres_obj_list.get(mainres._recid):
                        continue
                    else:
                        mainres_obj_list[mainres._recid] = True

                    guest_list = query(guest_list_list, filters=(lambda guest_list: guest_list.gastnr == guest.gastnr), first=True)

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

        reservation_obj_list = {}
        reservation = Reservation()
        gast = Guest()
        for reservation.resnr, reservation.depositgef, reservation.limitdate, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation.useridanlage, reservation.useridmutat, reservation.mutdat, reservation.grpflag, reservation._recid, gast.gastnr, gast.name, gast.anredefirma, gast.wohnort, gast.karteityp, gast._recid in db_session.query(Reservation.resnr, Reservation.depositgef, Reservation.limitdate, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation.useridanlage, Reservation.useridmutat, Reservation.mutdat, Reservation.grpflag, Reservation._recid, Gast.gastnr, Gast.name, Gast.anredefirma, Gast.wohnort, Gast.karteityp, Gast._recid).join(Gast,(Gast.gastnr == Reservation.gastnr)).filter(
                 (Reservation.activeflag == 0) & (Reservation.groupname == (grpname).lower())).order_by(Gast.name).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True

            if gast:
                guest_list = Guest_list()
                guest_list_list.append(guest_list)

                guest_list.gastnr = gast.gastnr
                guest_list.name = gast.name
                guest_list.anredefirma = gast.anredefirma
                guest_list.wohnort = gast.wohnort
                guest_list.karteityp = gast.karteityp

    elif case_type == 22:

        reservation_obj_list = {}
        reservation = Reservation()
        gast = Guest()
        for reservation.resnr, reservation.depositgef, reservation.limitdate, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation.useridanlage, reservation.useridmutat, reservation.mutdat, reservation.grpflag, reservation._recid, gast.gastnr, gast.name, gast.anredefirma, gast.wohnort, gast.karteityp, gast._recid in db_session.query(Reservation.resnr, Reservation.depositgef, Reservation.limitdate, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation.useridanlage, Reservation.useridmutat, Reservation.mutdat, Reservation.grpflag, Reservation._recid, Gast.gastnr, Gast.name, Gast.anredefirma, Gast.wohnort, Gast.karteityp, Gast._recid).join(Gast,(Gast.gastnr == Reservation.gastnr) & (Gast.name >= (gname).lower()) & (Gast.gastnr > 0) & (Gast.karteityp == sorttype)).filter(
                 (Reservation.activeflag == 0) & (Reservation.groupname != "")).order_by(Gast.name).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True

            if gast:
                guest_list = Guest_list()
                guest_list_list.append(guest_list)

                guest_list.gastnr = gast.gastnr
                guest_list.name = gast.name
                guest_list.anredefirma = gast.anredefirma
                guest_list.wohnort = gast.wohnort
                guest_list.karteityp = gast.karteityp

    elif case_type == 23:

        reservation_obj_list = {}
        reservation = Reservation()
        gast = Guest()
        for reservation.resnr, reservation.depositgef, reservation.limitdate, reservation.segmentcode, reservation.groupname, reservation.bemerk, reservation.useridanlage, reservation.useridmutat, reservation.mutdat, reservation.grpflag, reservation._recid, gast.gastnr, gast.name, gast.anredefirma, gast.wohnort, gast.karteityp, gast._recid in db_session.query(Reservation.resnr, Reservation.depositgef, Reservation.limitdate, Reservation.segmentcode, Reservation.groupname, Reservation.bemerk, Reservation.useridanlage, Reservation.useridmutat, Reservation.mutdat, Reservation.grpflag, Reservation._recid, Gast.gastnr, Gast.name, Gast.anredefirma, Gast.wohnort, Gast.karteityp, Gast._recid).join(Gast,(Gast.gastnr == Reservation.gastnr) & (Gast.name >= (gname).lower()) & (Gast.gastnr > 0) & (Gast.karteityp == sorttype)).filter(
                 (Reservation.activeflag == 0)).order_by(Reservation.gastnr, Gast.name).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True

            if gast:

                guest_list = query(guest_list_list, filters=(lambda guest_list: guest_list.gastnr == gast.gastnr), first=True)

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