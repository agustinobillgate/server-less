from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Htparam, Zimkateg, Guest, Guest_pr, Bediener, Res_history

def update_restriction_update_queasy_1bl(from_date:date, to_date:date, inp_str:str, rmtype:str, ota:str, restriction:int, flag:int):
    i:int = 0
    cat_flag:bool = False
    datum:date = None
    ci_date:date = None
    otanr:int = 0
    roomno:int = 0
    rcode:str = ""
    user_init:str = ""
    stat:str = ""
    str:str = ""
    progavail:str = ""
    queasy = htparam = zimkateg = guest = guest_pr = bediener = res_history = None

    room_list = rcode_list = qsy = buffqsy = qsy160 = checkqsy = None

    room_list_list, Room_list = create_model("Room_list", {"bezeich":str})
    rcode_list_list, Rcode_list = create_model("Rcode_list", {"bezeich":str})

    Qsy = Queasy
    Buffqsy = Queasy
    Qsy160 = Queasy
    Checkqsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, cat_flag, datum, ci_date, otanr, roomno, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal qsy, buffqsy, qsy160, checkqsy


        nonlocal room_list, rcode_list, qsy, buffqsy, qsy160, checkqsy
        nonlocal room_list_list, rcode_list_list
        return {}

    def rmstr2int(roomstr:str):

        nonlocal i, cat_flag, datum, ci_date, otanr, roomno, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal qsy, buffqsy, qsy160, checkqsy


        nonlocal room_list, rcode_list, qsy, buffqsy, qsy160, checkqsy
        nonlocal room_list_list, rcode_list_list

        roomnr:int = 0

        if cat_flag:

            buffqsy = db_session.query(Buffqsy).filter(
                    (Buffqsy.key == 152) &  (func.lower(Buffqsy.char1) == (roomstr).lower())).first()

            if buffqsy:
                roomnr = buffqsy.number1
        else:

            zimkateg = db_session.query(Zimkateg).filter(
                    (func.lower(Zimkateg.kurzbez) == (roomstr).lower())).first()

            if zimkateg:
                roomnr = zimkateg.zikatnr
        return roomnr

    def create_new_queasy(rate_code:str, roomno:int):

        nonlocal i, cat_flag, datum, ci_date, otanr, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal qsy, buffqsy, qsy160, checkqsy


        nonlocal room_list, rcode_list, qsy, buffqsy, qsy160, checkqsy
        nonlocal room_list_list, rcode_list_list

        j:int = 0
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 174
        queasy.char1 = rate_code
        queasy.number1 = roomno
        queasy.number3 = otanr
        queasy.date1 = datum
        queasy.logi1 = True

        if restriction == 0:
            queasy.char2 = to_string(flag) + ";0;0"

        elif restriction == 1:
            queasy.char2 = "0;" + to_string(flag) + ";0"

        elif restriction == 2:
            queasy.char2 = "0;0;" + to_string(flag)
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 175
        queasy.char1 = rate_code
        queasy.char2 = stat
        queasy.number1 = roomno
        queasy.number2 = flag
        queasy.number3 = otanr
        queasy.date1 = datum
        queasy.date2 = ci_date
        queasy.logi3 = True

        if user_init != "":

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "restriction"


            res_history.aenderung = "rcode:" + rcode + ",rmtype:" + rmtype + "ota:" + ota + ",Date:" + to_string(datum, "99/99/99") + ","

            if restriction == 0:
                res_history.aenderung = res_history.aenderung + "CLOSE: 0 ChangeTo " + to_string(flag)

            elif restriction == 1:
                res_history.aenderung = res_history.aenderung + "CTA: 0 ChangeTo " + to_string(flag)

            elif restriction == 2:
                res_history.aenderung = res_history.aenderung + "CTD: 0 ChangeTo " + to_string(flag)

    def update_queasy(rate_code:str, roomno:int):

        nonlocal i, cat_flag, datum, ci_date, otanr, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal qsy, buffqsy, qsy160, checkqsy


        nonlocal room_list, rcode_list, qsy, buffqsy, qsy160, checkqsy
        nonlocal room_list_list, rcode_list_list

        curr_anz:int = 0
        old_status:str = ""
        new_status:str = ""
        do_it:bool = False

        if restriction == 0:

            if entry(0, queasy.char2, ";") != to_string(flag):
                do_it = True

        elif restriction == 1:

            if entry(1, queasy.char2, ";") != to_string(flag):
                do_it = True

        elif restriction == 2:

            if entry(2, queasy.char2, ";") != to_string(flag):
                do_it = True

        if do_it:

            queasy = db_session.query(Queasy).first()

            if user_init != "":

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "restriction"


                res_history.aenderung = "rcode:" + rcode + ",rmtype:" + rmtype + "ota:" + ota + ",Date:" + to_string(datum, "99/99/99") + ","

                if restriction == 0:
                    res_history.aenderung = res_history.aenderung + "CLOSE: " + entry(0, queasy.char2, ";") + "ChangeTo" + to_string(flag)

                elif restriction == 1:
                    res_history.aenderung = res_history.aenderung + "CTA: " + entry(0, queasy.char2, ";") + "ChangeTo" + to_string(flag)

                elif restriction == 2:
                    res_history.aenderung = res_history.aenderung + "CTD: " + entry(0, queasy.char2, ";") + "ChangeTo" + to_string(flag)

            if restriction == 0:
                queasy.char2 = entry(0, queasy.char2, ";", to_string(flag))
                queasy.char2 = entry(1, queasy.char2, ";", "0")
                queasy.char2 = entry(2, queasy.char2, ";", "0")

            elif restriction == 1:
                queasy.char2 = entry(0, queasy.char2, ";", "0")
                queasy.char2 = entry(1, queasy.char2, ";", to_string(flag))

            elif restriction == 2:
                queasy.char2 = entry(0, queasy.char2, ";", "0")
                queasy.char2 = entry(2, queasy.char2, ";", to_string(flag))

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 175) &  (func.lower(Qsy.char1) == (rate_code).lower()) &  (Qsy.number1 == roomno) &  (Qsy.number3 == otanr) &  (Qsy.date1 == datum) &  (func.lower(Qsy.char2) == (stat).lower())).first()

            if qsy and qsy.number2 != flag:

                qsy = db_session.query(Qsy).first()
                qsy.number2 = flag
                qsy.logi3 = True

                qsy = db_session.query(Qsy).first()


            elif not qsy:
                qsy = Qsy()
                db_session.add(qsy)

                qsy.key = 175
                qsy.char1 = rate_code
                qsy.char2 = stat
                qsy.number1 = roomno
                qsy.number2 = flag
                qsy.number3 = otanr
                qsy.date1 = datum
                qsy.date2 = ci_date
                qsy.logi3 = True

            queasy = db_session.query(Queasy).first()

    if restriction == 0:
        stat = "CLOSE"

    elif restriction == 1:
        stat = "CTA"

    if restriction == 2:
        stat = "CTD"

    if num_entries(inp_str, ";") > 1:
        rcode = entry(0, inp_str, ";")
        user_init = entry(1, inp_str, ";")


    else:
        rcode = inp_str

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 152)).first()

    if queasy:
        cat_flag = True

    if ota.lower()  != "" and ota.lower()  != "*":

        guest = db_session.query(Guest).filter(
                (Guest.karteityp == 2) &  (Guest.steuernr != "") &  (trim(entry(0, Guest.steuernr, "|Guest.")) == (ota).lower())).first()

        if guest:
            otanr = guest.gastnr

    if rmtype.lower()  == "*":

        if cat_flag:

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 152)).all():

                room_list = query(room_list_list, filters=(lambda room_list :room_list.bezeich == queasy.char1), first=True)

                if not room_list:
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.bezeich = queasy.char1


        else:

            for zimkateg in db_session.query(Zimkateg).all():

                room_list = query(room_list_list, filters=(lambda room_list :room_list.bezeich == zimkateg.kurzbez), first=True)

                if not room_list:
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.bezeich = zimkateg.kurzbez

    if rcode.lower()  == "*":

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 159)).all():

            for guest_pr in db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == queasy.number2)).all():

                qsy = db_session.query(Qsy).filter(
                        (Qsy.key == 2) &  (Qsy.char1 == guest_pr.CODE)).first()

                if qsy:

                    rcode_list = query(rcode_list_list, filters=(lambda rcode_list :rcode_list.bezeich == qsy.char1), first=True)

                    if not rcode_list:
                        rcode_list = Rcode_list()
                        rcode_list_list.append(rcode_list)

                        rcode_list.bezeich = qsy.char1

    if rmtype.lower()  != "*" and rcode.lower()  != "*":
        roomno = rmstr2int (rmtype)
        for datum in range(from_date,to_date + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomno) &  (Queasy.number3 == otanr)).first()

            if not queasy:
                create_new_queasy(rcode, roomno)
            else:
                update_queasy(rcode, roomno)

            if ota.lower()  == "*":

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomno) &  (Queasy.number3 != 0)).first()
                while None != queasy:
                    update_queasy(rcode, roomno)

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomno) &  (Queasy.number3 != 0)).first()

    elif rmtype.lower()  == "*" and rcode.lower()  != "*":

        for room_list in query(room_list_list):
            roomno = rmstr2int (room_list.bezeich)
            for datum in range(from_date,to_date + 1) :

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 == otanr)).first()

                if not queasy:
                    create_new_queasy(rcode, roomno)

                elif queasy:
                    update_queasy(rcode, roomno)

                if ota.lower()  == "*":

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 != 0)).first()
                    while None != queasy:
                        update_queasy(rcode, roomno)

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 174) &  (func.lower(Queasy.char1) == (rcode).lower()) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 != 0)).first()

    elif rmtype.lower()  != "*" and rcode.lower()  == "*":
        roomno = rmstr2int (rmtype)

        for rcode_list in query(rcode_list_list):
            for datum in range(from_date,to_date + 1) :

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 174) &  (Queasy.char1 == rcode_list.bezeich) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 == otanr)).first()

                if not queasy:
                    create_new_queasy(rcode_list.bezeich, roomno)

                elif queasy:
                    update_queasy(rcode_list.bezeich, roomno)

                if ota.lower()  == "*":

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 174) &  (Queasy.char1 == rcode_list.bezeich) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 != 0)).first()
                    while None != queasy:
                        update_queasy(rcode_list.bezeich, roomno)

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 174) &  (Queasy.char1 == rcode_list.bezeich) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 != 0)).first()

    elif rmtype.lower()  == "*" and rcode.lower()  == "*":

        for rcode_list in query(rcode_list_list):

            for room_list in query(room_list_list):
                for datum in range(from_date,to_date + 1) :
                    roomno = rmstr2int (room_list.bezeich)

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 174) &  (Queasy.char1 == rcode_list.bezeich) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 == otanr)).first()

                    if not queasy:
                        create_new_queasy(rcode_list.bezeich, roomno)

                    elif queasy:
                        update_queasy(rcode_list.bezeich, roomno)

                    if ota.lower()  == "*":

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 174) &  (Queasy.char1 == rcode_list.bezeich) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 != 0)).first()
                        while None != queasy:
                            update_queasy(rcode_list.bezeich, roomno)

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 174) &  (Queasy.char1 == rcode_list.bezeich) &  (Queasy.number1 == roomno) &  (Queasy.date1 == datum) &  (Queasy.number3 != 0)).first()

    for qsy160 in db_session.query(Qsy160).filter(
            (Qsy160.key == 160)).all():
        for i in range(1,num_entries(qsy160.char1, ";")  + 1) :
            str = entry(i - 1, qsy160.char1, ";")

            if substring(str, 0, 10) == "$progname$":
                progavail = substring(str, 10)

                if num_entries(progavail, " == ") >= 10:
                    progavail = entry(9, progavail, "=", "yes")
                    qsy160.char1 = entry(i - 1, qsy160.char1, ";", "$progname$" + progavail)

    return generate_output()