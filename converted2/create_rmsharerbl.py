#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.intevent_1 import intevent_1
from models import Res_line, Reservation, Guest, Guestseg

s_list_data, S_list = create_model("S_list", {"name":string, "nat":string, "ankunft":date, "abreise":date, "sharerflag":bool, "accompflag":bool, "added":bool, "gastnr":int})

def create_rmsharerbl(s_list_data:[S_list], user_init:string, lname:string, fname:string, ftitle:string, mresnr:int, mreslinnr:int):

    prepare_cache ([Res_line, Reservation, Guestseg])

    sh_created = False
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    room_qty:int = 0
    priscilla_active:bool = True
    res_line = reservation = guest = guestseg = None

    s_list = resline = None

    Resline = create_buffer("Resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sh_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, room_qty, priscilla_active, res_line, reservation, guest, guestseg
        nonlocal user_init, lname, fname, ftitle, mresnr, mreslinnr
        nonlocal resline


        nonlocal s_list, resline

        return {"sh_created": sh_created}

    def create_rmsharer():

        nonlocal sh_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, room_qty, priscilla_active, res_line, reservation, guest, guestseg
        nonlocal user_init, lname, fname, ftitle, mresnr, mreslinnr
        nonlocal resline


        nonlocal s_list, resline

        gcf_found:bool = False
        created:bool = False

        for s_list in query(s_list_data):

            if room_qty > 1 or substring(s_list.name, 0, 11) != ("Room Sharer").lower() :
                check_name(s_list.name)

                guest = get_cache (Guest, {"gastnr": [(eq, s_list.gastnr)]})
                gcf_found = (None != guest)

                if guest and s_list.nat != guest.nation1 and s_list.nat != "":
                    pass
                    guest.nation1 = s_list.nat
                    guest.land = s_list.nat
                    guest.char2 = user_init


                    pass

                if not guest:
                    create_gcf()
                create_resline()
                created = True

        if created:
            pass
            res_line.kontakt_nr = res_line.reslinnr
            pass


    def check_name(inp_name:string):

        nonlocal sh_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, room_qty, priscilla_active, res_line, reservation, guest, guestseg
        nonlocal user_init, lname, fname, ftitle, mresnr, mreslinnr
        nonlocal resline


        nonlocal s_list, resline

        i:int = 0
        n:int = 1
        m:int = 0
        len_:int = 0

        if room_qty > 1:

            guest = get_cache (Guest, {"gastnr": [(eq, s_list.gastnr)]})
            lname = guest.name
            fname = guest.vorname1
            ftitle = guest.anrede1

            return
        lname = ""
        fname = ""
        ftitle = ""


        for i in range(1,num_entries(inp_name, ",")  + 1) :

            if i == 1:
                lname = trim(entry(0, inp_name, ","))
            elif i == 2:
                fname = trim(entry(1, inp_name, ","))
            elif i == 3:
                ftitle = trim(entry(2, inp_name, ","))


    def create_gcf():

        nonlocal sh_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, room_qty, priscilla_active, res_line, reservation, guest, guestseg
        nonlocal user_init, lname, fname, ftitle, mresnr, mreslinnr
        nonlocal resline


        nonlocal s_list, resline

        curr_gastnr:int = 0

        guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()

        if guest:
            curr_gastnr = guest.gastnr + 1
        else:
            curr_gastnr = 1
        guest = Guest()
        db_session.add(guest)

        guest.gastnr = curr_gastnr
        guest.karteityp = 0
        guest.nation1 = s_list.nat
        guest.land = s_list.nat
        guest.name = lname
        guest.vorname1 = fname
        guest.anrede1 = ftitle
        guest.char1 = user_init


        pass
        guestseg = Guestseg()
        db_session.add(guestseg)

        guestseg.gastnr = guest.gastnr
        guestseg.reihenfolge = 1
        guestseg.segmentcode = reservation.segmentcode


        pass
        pass


    def create_resline():

        nonlocal sh_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, room_qty, priscilla_active, res_line, reservation, guest, guestseg
        nonlocal user_init, lname, fname, ftitle, mresnr, mreslinnr
        nonlocal resline


        nonlocal s_list, resline

        reslinnr:int = 0

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == res_line.resnr)).order_by(Resline.reslinnr.desc()).yield_per(100):
            reslinnr = resline.reslinnr + 1
            break
        resline = Res_line()
        db_session.add(resline)

        resline.resnr = res_line.resnr
        resline.reslinnr = reslinnr
        resline.name = s_list.name
        resline.gastnr = res_line.gastnr
        resline.gastnrpay = guest.gastnr
        resline.gastnrmember = guest.gastnr
        resline.ankunft = s_list.ankunft
        resline.abreise = s_list.abreise
        resline.l_zuordnung[2] = to_int(not s_list.sharerflag)
        resline.anztage = (resline.abreise - resline.ankunft).days
        resline.erwachs = 0
        resline.zimmeranz = room_qty
        resline.zikatnr = res_line.zikatnr
        resline.zinr = res_line.zinr
        resline.arrangement = res_line.arrangement
        resline.grpflag = res_line.grpflag
        resline.kontignr = 0
        resline.reserve_int = res_line.reserve_int
        resline.setup = res_line.setup
        resline.adrflag = res_line.adrflag
        resline.was_status = res_line.was_status
        resline.kontakt_nr = res_line.reslinnr
        resline.betriebsnr = res_line.betriebsnr
        resline.reserve_char = to_string(get_current_date()) + to_string(get_current_time_in_seconds(), "HH:MM") + user_init
        resline.resstatus = 11

        if not s_list.sharerflag:

            if res_line.active_flag == 1:
                resline.resstatus = 13
                resline.active_flag = 1
                resline.ankzeit = get_current_time_in_seconds()

        if priscilla_active:
            get_output(intevent_1(11, resline.zinr, "Priscilla", resline.resnr, resline.reslinnr))
        store_vip()
        pass
        sh_created = True


    def store_vip():

        nonlocal sh_created, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, room_qty, priscilla_active, res_line, reservation, guest, guestseg
        nonlocal user_init, lname, fname, ftitle, mresnr, mreslinnr
        nonlocal resline


        nonlocal s_list, resline

        if guest.karteityp != 0:

            return

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == guest.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:
            resline.betrieb_gastmem = guestseg.segmentcode


    res_line = get_cache (Res_line, {"resnr": [(eq, mresnr)],"reslinnr": [(eq, mreslinnr)],"active_flag": [(le, 1)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
    room_qty = res_line.zimmeranz


    create_rmsharer()

    return generate_output()