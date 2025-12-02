#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_newresnobl import get_newresnobl
from models import Guest, Res_line, Reservation, Resplan, Zimkateg, Reslin_queasy

s_list_data, S_list = create_model("S_list", {"grpname":string, "ankunft":date, "abreise":date, "anzahl":int})

def create_group_seriesbl(pvilanguage:int, resno:int, user_init:string, s_list_data:[S_list]):

    prepare_cache ([Res_line, Reservation, Resplan, Zimkateg])

    created = False
    msg_str = ""
    new_resnr:int = 0
    lvcarea:string = "reservation"
    guest = res_line = reservation = resplan = zimkateg = reslin_queasy = None

    s_list = bguest = rline1 = rline2 = reser1 = reser2 = None

    Bguest = create_buffer("Bguest",Guest)
    Rline1 = create_buffer("Rline1",Res_line)
    Rline2 = create_buffer("Rline2",Res_line)
    Reser1 = create_buffer("Reser1",Reservation)
    Reser2 = create_buffer("Reser2",Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal pvilanguage, resno, user_init
        nonlocal bguest, rline1, rline2, reser1, reser2


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2

        return {"created": created, "msg_str": msg_str}

    def get_newresno():

        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal pvilanguage, resno, user_init
        nonlocal bguest, rline1, rline2, reser1, reser2


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2

        resno = 0

        def generate_inner_output():
            return (resno)

        resno = get_output(get_newresnobl())

        return generate_inner_output()


    def add_resplan(resnr:int, reslinnr:int):

        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal pvilanguage, resno, user_init
        nonlocal bguest, rline1, rline2, reser1, reser2


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2

        curr_date:date = None
        beg_datum:date = None
        end_datum:date = None
        i:int = 0
        rline = None
        rbuff = None
        Rline =  create_buffer("Rline",Res_line)
        Rbuff =  create_buffer("Rbuff",Resplan)

        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
        i = rline.resstatus

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rline.zikatnr)]})
        beg_datum = rline.ankunft
        end_datum = rline.abreise - timedelta(days=1)
        curr_date = beg_datum


        for curr_date in date_range(beg_datum,end_datum) :

            # resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})
            resplan = db_session.query(Resplan).filter((Resplan.zikatnr == zimkateg.zikatnr) & (Resplan.datum == curr_date)).with_for_update().first()

            if not resplan:
                resplan = Resplan()
                db_session.add(resplan)

                resplan.datum = curr_date
                resplan.zikatnr = zimkateg.zikatnr
                resplan.anzzim[i - 1] = resplan.anzzim[i - 1] + rline.zimmeranz


            else:

                # rbuff = get_cache (Resplan, {"_recid": [(eq, resplan._recid)]})
                rbuff = db_session.query(Resplan).filter(Resplan._recid == resplan._recid).with_for_update().first()
                rbuff.anzzim[i - 1] = rbuff.anzzim[i - 1] + rline.zimmeranz
                pass
                pass


    def check_fixedrate(resnr:int, reslinnr:int, new_resnr:int):

        nonlocal created, msg_str, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal pvilanguage, resno, user_init
        nonlocal bguest, rline1, rline2, reser1, reser2


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2

        found:bool = False
        rqsy = None
        rline1 = None
        rline2 = None
        Rqsy =  create_buffer("Rqsy",Reslin_queasy)
        Rline1 =  create_buffer("Rline1",Res_line)
        Rline2 =  create_buffer("Rline2",Res_line)

        rline1 = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        rline2 = get_cache (Res_line, {"resnr": [(eq, new_resnr)],"reslinnr": [(eq, reslinnr)]})

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr)).order_by(Reslin_queasy._recid).all():
            rqsy = Reslin_queasy()
            db_session.add(rqsy)

            buffer_copy(reslin_queasy, rqsy,except_fields=["resnr"])
            rqsy.resnr = new_resnr

            if reslin_queasy.date1 == rline1.ankunft:
                rqsy.date1 = rline2.ankunft
            else:
                found = True

            if reslin_queasy.date2 == rline1.abreise:
                rqsy.date2 = rline2.abreise
            else:
                found = True

        if found and msg_str == "":
            msg_str = "&W" + translateExtended ("Wrong date in fixed-rate setup. Re-check it.", lvcarea, "")


    def create_logfile(resnr:int, reslinnr:int):

        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal pvilanguage, resno, user_init
        nonlocal bguest, rline1, rline2, reser1, reser2


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2

        fixed_rate:bool = False
        rline = None
        guest1 = None
        Rline =  create_buffer("Rline",Res_line)
        Guest1 =  create_buffer("Guest1",Guest)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
        fixed_rate = None != reslin_queasy

        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = rline.resnr
        reslin_queasy.reslinnr = rline.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(rline.ankunft) + ";" + to_string(rline.ankunft) + ";" + to_string(rline.abreise) + ";" + to_string(rline.abreise) + ";" + to_string(rline.zimmeranz) + ";" + to_string(rline.zimmeranz) + ";" + to_string(rline.erwachs) + ";" + to_string(rline.erwachs) + ";" + to_string(rline.kind1) + ";" + to_string(rline.kind1) + ";" + to_string(rline.gratis) + ";" + to_string(rline.gratis) + ";" + to_string(rline.zikatnr) + ";" + to_string(rline.zikatnr) + ";" + to_string(rline.zinr) + ";" + to_string(rline.zinr) + ";" + to_string(rline.arrangement) + ";" + to_string(rline.arrangement) + ";" + to_string(rline.zipreis) + ";" + to_string(rline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(rline.name) + ";" + to_string("New Reservation") + ";"

        if rline.was_status == 0:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"

        if not fixed_rate:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"
        pass
        pass


    rline1_obj_list = {}
    for rline1, bguest in db_session.query(Rline1, Bguest).join(Bguest,(Bguest.gastnr == rline1.gastnr) & (Bguest.karteityp == 0)).filter(
             (Rline1.resnr == resno)).order_by(Rline1._recid).all():
        if rline1_obj_list.get(rline1._recid):
            continue
        else:
            rline1_obj_list[rline1._recid] = True


        msg_str = translateExtended ("One of this line has been modified to individual guest! Changed not possible!", lvcarea, "")

        return generate_output()

    if msg_str != "":

        return generate_output()

    reser1 = get_cache (Reservation, {"resnr": [(eq, resno)]})

    for s_list in query(s_list_data):
        new_resnr = get_newresno()
        reser2 = Reservation()
        db_session.add(reser2)

        buffer_copy(reser1, reser2,except_fields=["resnr","useridmutat","mutdat","depositbez","zahldatum","zahlkonto","depositbez2","zahldatum2","zahlkonto2"])
        reser2.resnr = new_resnr
        reser2.groupname = s_list.grpname
        reser2.useridanlage = user_init
        created = True


        pass
        pass

        for rline1 in db_session.query(Rline1).filter(
                 (Rline1.resnr == resno) & (Rline1.active_flag <= 1) & (Rline1.resstatus != 12)).order_by(Rline1._recid).all():
            rline2 = Res_line()
            db_session.add(rline2)

            buffer_copy(rline1, rline2,except_fields=["resnr","betrieb_gast","zinr","flight_nr","kontignr"])
            rline2.resnr = new_resnr
            rline2.active_flag = 0
            rline2.resstatus = 3
            rline2.ankunft = s_list.ankunft
            rline2.abreise = s_list.abreise
            rline2.anztage = (s_list.abreise - s_list.ankunft).days
            rline2.zimmeranz = s_list.anzahl
            rline2.reserve_char = to_string(get_current_date()) + to_string(get_current_time_in_seconds(), "HH:MM") + user_init


            pass
            pass
            add_resplan(new_resnr, rline1.reslinnr)
            check_fixedrate(rline1.resnr, rline1.reslinnr, new_resnr)
            create_logfile(new_resnr, rline1.reslinnr)

    return generate_output()
