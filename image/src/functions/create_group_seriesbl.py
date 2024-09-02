from functions.additional_functions import *
import decimal
from datetime import date
from functions.get_newresnobl import get_newresnobl
from sqlalchemy import func
from models import Guest, Res_line, Reservation, Resplan, Zimkateg, Reslin_queasy

def create_group_seriesbl(pvilanguage:int, resno:int, user_init:str, s_list:[S_list]):
    created = False
    msg_str = ""
    new_resnr:int = 0
    lvcarea:str = "reservation"
    guest = res_line = reservation = resplan = zimkateg = reslin_queasy = None

    s_list = bguest = rline1 = rline2 = reser1 = reser2 = rline = rbuff = rqsy = guest1 = None

    s_list_list, S_list = create_model("S_list", {"grpname":str, "ankunft":date, "abreise":date, "anzahl":int})

    Bguest = Guest
    Rline1 = Res_line
    Rline2 = Res_line
    Reser1 = Reservation
    Reser2 = Reservation
    Rline = Res_line
    Rbuff = Resplan
    Rqsy = Reslin_queasy
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1
        nonlocal s_list_list
        return {"created": created, "msg_str": msg_str}

    def get_newresno():

        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1
        nonlocal s_list_list

        resno = 0

        def generate_inner_output():
            return resno
        resno = get_output(get_newresnobl())


        return generate_inner_output()

    def add_resplan(resnr:int, reslinnr:int):

        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1
        nonlocal s_list_list

        curr_date:date = None
        beg_datum:date = None
        end_datum:date = None
        i:int = 0
        Rline = Res_line
        Rbuff = Resplan

        rline = db_session.query(Rline).filter(
                (Rline.resnr == resnr) &  (Rline.reslinnr == reslinnr)).first()
        i = rline.resstatus

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == rline.zikatnr)).first()
        beg_datum = rline.ankunft
        end_datum = rline.abreise - 1
        curr_date = beg_datum


        for curr_date in range(beg_datum,end_datum + 1) :

            resplan = db_session.query(Resplan).filter(
                    (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

            if not resplan:
                resplan = Resplan()
                db_session.add(resplan)

                resplan.datum = curr_date
                resplan.zikatnr = zimkateg.zikatnr
                resplan.anzzim[i - 1] = resplan.anzzim[i - 1] + rline.zimmeranz


            else:

                rbuff = db_session.query(Rbuff).filter(
                        (Rbuff._recid == resplan._recid)).first()
                rbuff.anzzim[i - 1] = rbuff.anzzim[i - 1] + rline.zimmeranz

                rbuff = db_session.query(Rbuff).first()


    def check_fixedrate(resnr:int, reslinnr:int, new_resnr:int):

        nonlocal created, msg_str, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1
        nonlocal s_list_list

        found:bool = False
        Rqsy = Reslin_queasy
        Rline1 = Res_line
        Rline2 = Res_line

        rline1 = db_session.query(Rline1).filter(
                (Rline1.resnr == resnr) &  (Rline1.reslinnr == reslinnr)).first()

        rline2 = db_session.query(Rline2).filter(
                (Rline2.resnr == new_resnr) &  (Rline2.reslinnr == reslinnr)).first()

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr)).all():
            rqsy = Rqsy()
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
            msg_str = "&W" + translateExtended ("Wrong date in fixed_rate setup. Re_check it.", lvcarea, "")

    def create_logfile(resnr:int, reslinnr:int):

        nonlocal created, msg_str, new_resnr, lvcarea, guest, res_line, reservation, resplan, zimkateg, reslin_queasy
        nonlocal bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1


        nonlocal s_list, bguest, rline1, rline2, reser1, reser2, rline, rbuff, rqsy, guest1
        nonlocal s_list_list

        fixed_rate:bool = False
        Rline = Res_line
        Guest1 = Guest

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resnr) &  (Reslin_queasy.reslinnr == reslinnr)).first()
        fixed_rate = None != reslin_queasy

        rline = db_session.query(Rline).filter(
                (Rline.resnr == resnr) &  (Rline.reslinnr == reslinnr)).first()
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

        reslin_queasy = db_session.query(Reslin_queasy).first()


    rline1_obj_list = []
    for rline1, bguest in db_session.query(Rline1, Bguest).join(Bguest,(Bguest.gastnr == rLine1.gastnr) &  (Bguest.karteityp == 0)).filter(
            (Rline1.resnr == resno)).all():
        if rline1._recid in rline1_obj_list:
            continue
        else:
            rline1_obj_list.append(rline1._recid)


        msg_str = translateExtended ("One of this line has been modified to individual guest! return

    if msg_str != "":

        return generate_output()

    reser1 = db_session.query(Reser1).filter(
            (Reser1.resnr == resno)).first()

    for s_list in query(s_list_list):
        new_resnr = get_newresno()
        reser2 = Reser2()
        db_session.add(reser2)

        buffer_copy(reser1, reser2,except_fields=["resnr","useridmutat","mutdat","depositbez","zahldatum","zahlkonto","depositbez2","zahldatum2","zahlkonto2"])
        reser2.resnr = new_resnr
        reser2.groupname = s_list.grpname
        reser2.useridanlage = user_init
        created = True

        reser2 = db_session.query(Reser2).first()


        for rline1 in db_session.query(Rline1).filter(
                (Rline1.resnr == resno) &  (Rline1.active_flag <= 1) &  (Rline1.resstatus != 12)).all():
            rline2 = Rline2()
            db_session.add(rline2)

            buffer_copy(rline1, rline2,except_fields=["resnr","betrieb_gast","zinr","flight_nr","kontignr"])
            rline2.resnr = new_resnr
            rline2.active_flag = 0
            rline2.resstatus = 3
            rline2.ankunft = s_list.ankunft
            rline2.abreise = s_list.abreise
            rline2.anztage = s_list.abreise - s_list.ankunft
            rline2.zimmeranz = s_list.anzahl
            rline2.reserve_char = to_string(get_current_date()) + to_string(get_current_time_in_seconds(), "HH:MM") + user_init

            rline2 = db_session.query(Rline2).first()

            add_resplan(new_resnr, rline1.reslinnr)
            check_fixedrate(rline1.resnr, rline1.reslinnr, new_resnr)
            create_logfile(new_resnr, rline1.reslinnr)

    return generate_output()