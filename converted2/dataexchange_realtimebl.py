from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Interface, Reslin_queasy, Res_line, Guest, Zimkateg, Reservation, Sourccod, Kontline, Zimmer, Outorder, Segment

def dataexchange_realtimebl(ci_date:date):
    last_date = None
    last_time = 0
    occupancies_list = []
    guestinhouse_list = []
    inhouse_guest:bool = False
    send_occ:bool = False
    cat_flag:bool = False
    counter:int = 0
    curr_rmtype:str = ""
    curr_qty:int = 0
    curr_recid:int = 0
    catnr:int = 0
    i:int = 0
    guest_mail:str = ""
    datum:date = None
    fdate:date = None
    tdate:date = None
    end_date:date = None
    start_date:date = None
    rm_occ:int = 0
    rm_ooo:int = 0
    room:int = 0
    rm_kontline:int = 0
    vhp_limited:bool = False
    do_it:bool = False
    queasy = interface = reslin_queasy = res_line = guest = zimkateg = reservation = sourccod = kontline = zimmer = outorder = segment = None

    guestinhouse = headerinhouse = header2 = occupancies = occ_list = rmcat_list = occ_room = ooo_list = t_kontline = qbuff = bocc = None

    guestinhouse_list, Guestinhouse = create_model("Guestinhouse", {"name":str, "email":str, "checkindate":str, "checkoutdate":str, "roomtype":str, "roomnumber":str, "reservationsource":str})
    headerinhouse_list, Headerinhouse = create_model("Headerinhouse", {"datatype":str, "vhphotelid":str, "timestampofinsertion":str, "occupanciesdate":str})
    header2_list, Header2 = create_model("Header2", {"datatype":str, "vhphotelid":str, "timestampofinsertion":str})
    occupancies_list, Occupancies = create_model("Occupancies", {"startdate":str, "enddate":str, "roomtype":str, "qty":str})
    occ_list_list, Occ_list = create_model("Occ_list", {"date1":date, "date2":date, "rmtype":str, "qty":int, "zikatnr":int, "counter":int})
    rmcat_list_list, Rmcat_list = create_model("Rmcat_list", {"zikatnr":int, "anzahl":int, "typ":int, "sleeping":bool}, {"sleeping": True})
    occ_room_list, Occ_room = create_model("Occ_room", {"datum":date, "zikatnr":int, "anzahl":int})
    ooo_list_list, Ooo_list = create_model("Ooo_list", {"datum":date, "zikatnr":int, "anzahl":int})
    t_kontline_list, T_kontline = create_model("T_kontline", {"datum":date, "zikatnr":int, "anzahl":int})

    Qbuff = create_buffer("Qbuff",Queasy)
    Bocc = Occ_list
    bocc_list = occ_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal last_date, last_time, occupancies_list, guestinhouse_list, inhouse_guest, send_occ, cat_flag, counter, curr_rmtype, curr_qty, curr_recid, catnr, i, guest_mail, datum, fdate, tdate, end_date, start_date, rm_occ, rm_ooo, room, rm_kontline, vhp_limited, do_it, queasy, interface, reslin_queasy, res_line, guest, zimkateg, reservation, sourccod, kontline, zimmer, outorder, segment
        nonlocal ci_date
        nonlocal qbuff, bocc


        nonlocal guestinhouse, headerinhouse, header2, occupancies, occ_list, rmcat_list, occ_room, ooo_list, t_kontline, qbuff, bocc
        nonlocal guestinhouse_list, headerinhouse_list, header2_list, occupancies_list, occ_list_list, rmcat_list_list, occ_room_list, ooo_list_list, t_kontline_list

        return {"last_date": last_date, "last_time": last_time, "occupancies": occupancies_list, "guestInhouse": guestinhouse_list}

    def count_rmcateg():

        nonlocal last_date, last_time, occupancies_list, guestinhouse_list, inhouse_guest, send_occ, cat_flag, counter, curr_rmtype, curr_qty, curr_recid, catnr, i, guest_mail, datum, fdate, tdate, end_date, start_date, rm_occ, rm_ooo, room, rm_kontline, vhp_limited, do_it, queasy, interface, reslin_queasy, res_line, guest, zimkateg, reservation, sourccod, kontline, zimmer, outorder, segment
        nonlocal ci_date
        nonlocal qbuff, bocc


        nonlocal guestinhouse, headerinhouse, header2, occupancies, occ_list, rmcat_list, occ_room, ooo_list, t_kontline, qbuff, bocc
        nonlocal guestinhouse_list, headerinhouse_list, header2_list, occupancies_list, occ_list_list, rmcat_list_list, occ_room_list, ooo_list_list, t_kontline_list

        zikatnr:int = 0
        rmcat_list_list.clear()

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer.zikatnr).all():

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.zikatnr == zimmer.zikatnr)).first()

            if zimkateg and zimkateg.verfuegbarkeit:

                if cat_flag and zimkateg.typ != 0:
                    zikatnr = zimkateg.typ
                else:
                    zikatnr = zimkateg.zikatnr

                rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list: rmcat_list.typ == zikatnr), first=True)

                if not rmcat_list:
                    rmcat_list = Rmcat_list()
                    rmcat_list_list.append(rmcat_list)

                    rmcat_list.typ = zikatnr


                    rmcat_list.anzahl = 1
                else:
                    rmcat_list.anzahl = rmcat_list.anzahl + 1

    occupancies_list.clear()
    guestInhouse_list.clear()
    guestInhouse_list.clear()
    headerInhouse_list.clear()
    header2_list.clear()
    occupancies_list.clear()
    occ_list_list.clear()
    rmcat_list_list.clear()
    occ_room_list.clear()
    ooo_list_list.clear()
    t_kontline_list.clear()
    fdate = ci_date
    tdate = fdate + timedelta(days=365)

    for interface in db_session.query(Interface).filter(
             (Interface.key == 10) & (func.lower(not Interface.nebenstelle).op("~")(("*DtExc*".lower().replace("*",".*")))) & (Interface.decfield != 13) & (Interface.intdate == ci_date)).order_by(intdate, int_time).all():
        last_date = interface.intdate
        last_time = interface.int_time

        if interface.decfield != 1 and interface.decfield != 2 and interface.decfield != 10 and interface.decfield != 9:
            send_occ = True

        if interface.decfield == 9:

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                     (func.lower(Reslin_queasy.key) == ("ResChanges").lower()) & (Reslin_queasy.resnr == interface.resnr) & (Reslin_queasy.reslinnr == interface.reslinnr) & (Reslin_queasy.date2 == interface.intdate) & (interface.int_time - Reslin_queasy.number2 <= 10) & ((entry(0, Reslin_queasy.char3, ";") != entry(1, Reslin_queasy.char3, ";")) | (entry(2, Reslin_queasy.char3, ";") != entry(3, Reslin_queasy.char3, ";")) | (entry(4, Reslin_queasy.char3, ";") != entry(5, Reslin_queasy.char3, ";")) | (entry(12, Reslin_queasy.char3, ";") != entry(13, Reslin_queasy.char3, ";")))).first()

            if reslin_queasy:
                send_occ = True

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == interface.resnr) & (Res_line.reslinnr == interface.reslinnr) & (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).first()

        if res_line:
            inhouse_guest = True

    if get_current_time_in_seconds() >= 21600:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 172) & (func.lower(Queasy.char2) == ("dataExchange").lower())).first()

        if not queasy:
            inhouse_guest = True
            send_occ = True


            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 172
            queasy.date1 = ci_date
            queasy.char2 = "dataExchange"

        elif queasy and queasy.date1 != ci_date:
            inhouse_guest = True
            send_occ = True


            queasy.date1 = ci_date
            pass
    guestInhouse_list.clear()

    if inhouse_guest:

        res_line_obj_list = []
        for res_line, guest, zimkateg, reservation in db_session.query(Res_line, Guest, Zimkateg, Reservation).join(Guest,(Guest.gastnr == Res_line.gastnrmember)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                 (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.zinr != "")).order_by(Res_line._recid).all():
            sourccod = query(sourccod_list, (lambda sourccod: Sourccod.source_code == reservation.resart), first=True)
            if not sourccod:
                continue

            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if guest.email_adr == "":
                guest_mail = "N/A"

            elif guest.email_adr != "":
                guest_mail = guest.email_adr
            guestinhouse = Guestinhouse()
            guestinhouse_list.append(guestinhouse)

            guestinhouse.name = guest.vorname1 + " " + guest.name + "," + guest.anrede1
            guestinhouse.email = guest_mail
            guestinhouse.checkindate = to_string(get_year(res_line.ankunft) , "9999") + "-" +\
                    to_string(get_month(res_line.ankunft) , "99") + "-" +\
                    to_string(get_day(res_line.ankunft) , "99")
            guestinhouse.checkoutdate = to_string(get_year(res_line.abreise) , "9999") + "-" +\
                    to_string(get_month(res_line.abreise) , "99") + "-" +\
                    to_string(get_day(res_line.abreise) , "99")
            guestinhouse.roomtype = zimkateg.bezeichnung
            guestinhouse.roomnumber = res_line.zinr
            guestinhouse.reservationsource = Sourccod.bezeich

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    if send_occ:

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 171)).first()

        if queasy:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.char1 == "")).order_by(Queasy._recid).all():
                occ_list = Occ_list()
                occ_list_list.append(occ_list)

                counter = counter + 1
                occ_list.date1 = queasy.date1
                occ_list.date2 = queasy.date1
                occ_list.qty = queasy.number2


                occ_list.counter = counter

                if not cat_flag:

                    zimkateg = db_session.query(Zimkateg).filter(
                             (Zimkateg.zikatnr == queasy.number1)).first()

                    if zimkateg:
                        occ_list.rmtype = zimkateg.kurzbez
                else:

                    qbuff = db_session.query(Qbuff).filter(
                             (Qbuff.key == 152) & (Qbuff.number1 == queasy.number1)).first()

                    if qbuff:
                        occ_list.rmtype = qbuff.char1
        else:
            count_rmcateg()
            counter = 0

            if cat_flag:
                for datum in date_range(fdate,tdate) :

                    for queasy in db_session.query(Queasy).filter(
                             (Queasy.key == 152)).order_by(Queasy._recid).all():
                        occ_list = Occ_list()
                        occ_list_list.append(occ_list)

                        counter = counter + 1
                        occ_list.date1 = datum
                        occ_list.date2 = datum
                        occ_list.counter = counter
                        occ_list.zikatnr = queasy.number1
                        occ_list.rmtype = queasy.char1


            else:
                for datum in date_range(fdate,tdate) :

                    for zimkateg in db_session.query(Zimkateg).filter(
                             (Zimkateg.verfuegbarkeit)).order_by(Zimkateg._recid).all():
                        occ_list = Occ_list()
                        occ_list_list.append(occ_list)

                        counter = counter + 1
                        occ_list.date1 = datum
                        occ_list.date2 = datum
                        occ_list.counter = counter
                        occ_list.zikatnr = zimkateg.zikatnr
                        occ_list.rmtype = zimkateg.kurzbez

            kontline_obj_list = []
            for kontline, zimkateg in db_session.query(Kontline, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Kontline.zikatnr)).filter(
                     (Kontline.ankunft <= tdate) & (Kontline.abreise >= fdate) & (Kontline.betriebsnr == 1) & (Kontline.kontstat == 1)).order_by(Kontline._recid).all():
                if kontline._recid in kontline_obj_list:
                    continue
                else:
                    kontline_obj_list.append(kontline._recid)

                if cat_flag:
                    catnr = zimkateg.typ
                else:
                    catnr = zimkateg.zikatnr
                for datum in date_range(kontline.ankunft,kontline.abreise) :

                    t_kontline = query(t_kontline_list, filters=(lambda t_kontline: t_kontline.datum == datum and t_kontline.zikatnr == catnr), first=True)

                    if not t_kontline:
                        t_kontline = T_kontline()
                        t_kontline_list.append(t_kontline)

                        t_kontline.datum = datum
                        t_kontline.zikatnr = catnr


                    t_kontline.anzahl = t_kontline.anzahl + kontline.zimmeranz

            outorder_obj_list = []
            for outorder, zimmer, zimkateg in db_session.query(Outorder, Zimmer, Zimkateg).join(Zimmer,(Zimmer.zinr == Outorder.zinr) & (Zimmer.sleeping)).join(Zimkateg,(Zimkateg.zikatnr == Zimmer.zikatnr)).filter(
                     (Outorder.betriebsnr <= 1) & (Outorder.gespstart <= tdate) & (Outorder.gespende >= fdate)).order_by(Outorder._recid).all():
                if outorder._recid in outorder_obj_list:
                    continue
                else:
                    outorder_obj_list.append(outorder._recid)

                if cat_flag:
                    catnr = zimkateg.typ
                else:
                    catnr = zimkateg.zikatnr
                for datum in date_range(outorder.gespstart,outorder.gespende) :

                    ooo_list = query(ooo_list_list, filters=(lambda ooo_list: ooo_list.zikatnr == catnr and ooo_list.datum == datum), first=True)

                    if not occ_list:
                        ooo_list = Ooo_list()
                        ooo_list_list.append(ooo_list)

                        ooo_list.zikatnr = catnr
                        ooo_list.datum = datum


                    ooo_list.anzahl = ooo_list.anzahl + 1

            res_line_obj_list = []
            for res_line, zimkateg in db_session.query(Res_line, Zimkateg).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.ankunft <= tdate) & (Res_line.abreise >= fdate)).order_by(Res_line._recid).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = db_session.query(Reservation).filter(
                             (Reservation.resnr == res_line.resnr)).first()

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0

                if do_it:

                    if res_line.ankunft == res_line.abreise:
                        end_date = res_line.abreise
                    else:
                        end_date = res_line.abreise - timedelta(days=1)

                    if cat_flag:
                        catnr = zimkateg.typ
                    else:
                        catnr = zimkateg.zikatnr

                    if res_line.ankunft <= fdate:
                        start_date = fdate
                    else:
                        start_date = res_line.ankunft

                    if end_date >= tdate:
                        end_date = tdate
                    for datum in date_range(start_date,end_date) :

                        occ_room = query(occ_room_list, filters=(lambda occ_room: occ_room.zikatnr == catnr and occ_room.datum == datum), first=True)

                        if not occ_room:
                            occ_room = Occ_room()
                            occ_room_list.append(occ_room)

                            occ_room.zikatnr = catnr
                            occ_room.datum = datum


                        occ_room.anzahl = occ_room.anzahl + res_line.zimmeranz

            for occ_list in query(occ_list_list):
                rm_ooo = 0
                rm_occ = 0
                rm_kontline = 0
                room = 0

                occ_room = query(occ_room_list, filters=(lambda occ_room: occ_room.zikatnr == occ_list.zikatnr and occ_room.datum == occ_list.date1), first=True)

                if occ_room:
                    rm_occ = occ_room.anzahl

                ooo_list = query(ooo_list_list, filters=(lambda ooo_list: ooo_list.zikatnr == occ_list.zikatnr and ooo_list.datum == occ_list.date1), first=True)

                if ooo_list:
                    rm_ooo = ooo_list.anzahl

                t_kontline = query(t_kontline_list, filters=(lambda t_kontline: t_kontline.zikatnr == occ_list.zikatnr and t_kontline.datum == occ_list.date1), first=True)

                if t_kontline:
                    rm_kontline = t_kontline.anzahl

                rmcat_list = query(rmcat_list_list, filters=(lambda rmcat_list: rmcat_list.typ == occ_list.zikatnr), first=True)

                if rmcat_list:
                    room = rmcat_list.anzahl
                occ_list.qty = room - rm_occ - rm_ooo - rm_kontline

    for occ_list in query(occ_list_list, sort_by=[("rmtype",False),("date1",False)]):

        if curr_qty != occ_list.qty:
            curr_rmtype = occ_list.rmtype
            curr_qty = occ_list.qty
            curr_recid = occ_list.counter

        elif curr_qty == occ_list.qty and curr_rmtype != occ_list.rmtype:
            curr_rmtype = occ_list.rmtype
            curr_qty = occ_list.qty
            curr_recid = occ_list.counter

        elif curr_qty == occ_list.qty and curr_rmtype == occ_list.rmtype:

            bocc = query(bocc_list, filters=(lambda bocc: bocc.counter == curr_recid), first=True)

            if bocc and (bocc.date2 == occ_list.date1 - 1 or bocc.date2 >= occ_list.date1) and bocc.rmtype == occ_list.rmtyp:

                if bocc.date2 > occ_list.date1:
                    pass
                else:
                    bocc.date2 = occ_list.date2
                occ_list_list.remove(occ_list)
                pass
                pass

    for occ_list in query(occ_list_list, sort_by=[("rmtype",False),("date1",False)]):
        occupancies = Occupancies()
        occupancies_list.append(occupancies)

        occupancies.roomtype = occ_list.rmtype
        occupancies.qty = to_string(occ_list.qty)
        occupancies.startdate = to_string(get_year(occ_list.date1) , "9999") + "-" +\
                to_string(get_month(occ_list.date1) , "99") + "-" +\
                to_string(get_day(occ_list.date1) , "99")
        occupancies.enddate = to_string(get_year(occ_list.date2) , "9999") + "-" +\
                to_string(get_month(occ_list.date2) , "99") + "-" +\
                to_string(get_day(occ_list.date2) , "99")


    occ_list_list.clear()

    return generate_output()