from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Zimkateg, Res_line, Bediener, Paramtext, Reservation, Waehrung, Fixleist, Queasy, Akt_kont, Reslin_queasy

def get_data_print_confirmletter_webbl(resnumber:int, user_init:str):
    print_list_list = []
    room:int = 0
    rmtype:str = ""
    pricerm:str = ""
    tot_rm:str = ""
    allgst:str = ""
    all_total:decimal = to_decimal("0.0")
    night:int = 0
    co:int = 0
    guest = zimkateg = res_line = bediener = paramtext = reservation = waehrung = fixleist = queasy = akt_kont = reslin_queasy = None

    print_list = setup_list = t_guest = t_zim = t_res = None

    print_list_list, Print_list = create_model("Print_list", {"resnr":int, "reslinnr":int, "gastnr":int, "resname":str, "guesttitle":str, "guestfname":str, "guestlname":str, "guestemail":str, "guesttelp":str, "checkin":date, "checkout":date, "roomtype":str, "roomtypebez":str, "roomrate":decimal, "currency":str, "username":str, "rescomment":str, "maincomment":str, "contactname":str, "contacttelp":str, "contactemail":str, "totalroom":int, "pax":int, "checkintime":str, "checkouttime":str, "billinstuct":str, "creditcard":str, "total_rate":decimal, "room_night":int, "argt":str, "tot_pay":decimal, "flight_nr":str, "kind1":int, "depositgef":decimal, "depositbez":decimal, "address":str, "bedsetup":str, "all_rmtype":str, "all_rmrate":str, "all_totrate":str, "bedsetup_rate":decimal, "all_guest":str, "cutoff_days":int, "all_total":decimal})
    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str, "ptexte":str})

    T_guest = create_buffer("T_guest",Guest)
    T_zim = create_buffer("T_zim",Zimkateg)
    T_res = create_buffer("T_res",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal print_list_list, room, rmtype, pricerm, tot_rm, allgst, all_total, night, co, guest, zimkateg, res_line, bediener, paramtext, reservation, waehrung, fixleist, queasy, akt_kont, reslin_queasy
        nonlocal resnumber, user_init
        nonlocal t_guest, t_zim, t_res


        nonlocal print_list, setup_list, t_guest, t_zim, t_res
        nonlocal print_list_list, setup_list_list
        return {"print-list": print_list_list}


    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = paramtext.txtnr - 9199
        setup_list.char = substring(paramtext.notes, 0, 1)
        setup_list.ptexte = paramtext.ptexte

    for res_line in db_session.query(Res_line).filter(
             (Res_line.resnr == resnumber) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 11)).order_by(Res_line._recid).all():

        setup_list = query(setup_list_list, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrmember)).first()

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == res_line.zikatnr)).first()

        waehrung = db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

        if waehrung:
            print_list = Print_list()
            print_list_list.append(print_list)

            print_list.resnr = res_line.resnr
            print_list.reslinnr = res_line.reslinnr
            print_list.gastnr = res_line.gastnrmember
            print_list.resname = res_line.resname
            print_list.guesttitle = guest.anrede1
            print_list.guestfname = guest.vorname1
            print_list.guestlname = guest.name
            print_list.guestemail = guest.email_adr
            print_list.guesttelp = guest.mobil_telefon
            print_list.checkin = res_line.ankunft
            print_list.checkout = res_line.abreise
            print_list.roomtype = zimkateg.kurzbez
            print_list.roomtypebez = zimkateg.bezeichnung
            print_list.currency = waehrung.wabkurz
            print_list.username = bediener.username
            print_list.rescomment = res_line.bemerk
            print_list.maincomment = reservation.bemerk
            print_list.totalroom = res_line.zimmeranz
            print_list.pax = res_line.erwachs + res_line.gratis + res_line.kind1 +\
                    res_line.kind2 + res_line.l_zuordnung[3]
            print_list.checkintime = to_string(res_line.ankzeit, "HH:MM")
            print_list.checkouttime = to_string(res_line.abreisezeit, "HH:MM")
            print_list.creditcard = guest.ausweis_nr2
            print_list.room_night = (res_line.abreise - res_line.ankunft) * res_line.zimmeranz
            print_list.argt = res_line.arrangement
            print_list.flight_nr = res_line.flight_nr
            print_list.kind1 = res_line.kind1
            print_list.depositgef =  to_decimal(reservation.depositgef)
            print_list.depositbez =  to_decimal(reservation.depositbez) + to_decimal(reservation.depositbez2)
            print_list.address = guest.adresse1 + guest.adresse2
            print_list.bedsetup = setup_list.ptexte
            print_list.cutoff_days = reservation.point

            fixleist = db_session.query(Fixleist).filter(
                     (Fixleist.resnr == res_line.resnr)).first()

            if fixleist:
                print_list.bedsetup_rate =  to_decimal(fixleist.betrag)
            else:
                print_list.bedsetup_rate =  to_decimal("0")

            t_guest = db_session.query(T_guest).filter(
                     (T_guest.gastnr == res_line.gastnr)).first()

            if t_guest.karteityp == 2:
                print_list.roomrate =  to_decimal("0")
                print_list.total_rate =  to_decimal("0")
            else:
                print_list.roomrate =  to_decimal(res_line.zipreis)
                print_list.total_rate = ( to_decimal(res_line.zipreis) * to_decimal(print_list.room_night)) + to_decimal(print_list.bedsetup_rate)

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

            if queasy:
                print_list.billinstuct = queasy.char1

            akt_kont = db_session.query(Akt_kont).filter(
                     (Akt_kont.gastnr == res_line.gastnr)).first()

            if akt_kont:
                print_list.contactname = akt_kont.name
                print_list.contacttelp = akt_kont.telefon
                print_list.contactemail = akt_kont.email_adr
            else:
                print_list.contactname = ""
                print_list.contacttelp = ""
                print_list.contactemail = ""

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.deci1 != 0)).order_by(Reslin_queasy._recid).all():
            print_list.tot_pay =  to_decimal(print_list.tot_pay) + to_decimal(reslin_queasy.deci1)

            if (reslin_queasy.date2 - reslin_queasy.date1) == 0:
                night = 1
            else:
                night = (reslin_queasy.date2 - reslin_queasy.date1) + 1
            pricerm = pricerm + to_string(to_decimal(reslin_queasy.deci1) , "->,>>>,>>>,>>>,>>9.99") + ":"
            tot_rm = tot_rm + to_string(to_decimal(reslin_queasy.deci1 * night) , "->,>>>,>>>,>>>,>>9.99") + ":"
            all_total =  to_decimal(all_total) + to_decimal((reslin_queasy.deci1) * to_decimal(night))

        for t_zim in db_session.query(T_zim).filter(
                 (T_zim.zikatnr == res_line.zikatnr)).order_by(T_zim._recid).all():
            rmtype = rmtype + t_zim.bezeichnung + ":"

        for t_guest in db_session.query(T_guest).filter(
                 (T_guest.gastnr == res_line.gastnr)).order_by(T_guest._recid).all():

            if t_guest.karteityp == 2:
                pricerm = ""
                tot_rm = ""

        for t_res in db_session.query(T_res).filter(
                 (T_res.resnr == res_line.resnr)).order_by(T_res._recid).all():
            allgst = allgst + t_res.name + " : "

        if pricerm != "":
            print_list.all_rmrate = pricerm
        else:
            print_list.all_rmrate = to_string(to_decimal(print_list.roomrate) , "->,>>>,>>>,>>>,>>9.99")

        if tot_rm != "":
            print_list.all_totrate = tot_rm
        else:
            print_list.all_totrate = to_string(to_decimal(print_list.total_rate) , "->,>>>,>>>,>>>,>>9.99")
        print_list.all_total =  to_decimal(all_total)
        print_list.all_rmtype = rmtype
        print_list.all_guest = allgst

    return generate_output()