#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Zimkateg, Guest, Guest_pr, Bediener, Res_history

def update_restriction_update_queasy_1bl(from_date:date, to_date:date, inp_str:string, rmtype:string, ota:string, restriction:int, flag:int):

    prepare_cache ([Queasy, Htparam, Zimkateg, Guest, Guest_pr, Bediener, Res_history])

    i:int = 0
    cat_flag:bool = False
    datum:date = None
    ci_date:date = None
    otanr:int = 0
    roomno:int = 0
    rcode:string = ""
    user_init:string = ""
    stat:string = ""
    str:string = ""
    progavail:string = ""
    queasy = htparam = zimkateg = guest = guest_pr = bediener = res_history = None

    room_list = rcode_list = qsy = buffqsy = qsy160 = checkqsy = None

    room_list_list, Room_list = create_model("Room_list", {"bezeich":string})
    rcode_list_list, Rcode_list = create_model("Rcode_list", {"bezeich":string})

    Qsy = create_buffer("Qsy",Queasy)
    Buffqsy = create_buffer("Buffqsy",Queasy)
    Qsy160 = create_buffer("Qsy160",Queasy)
    Checkqsy = create_buffer("Checkqsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, cat_flag, datum, ci_date, otanr, roomno, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal from_date, to_date, inp_str, rmtype, ota, restriction, flag
        nonlocal qsy, buffqsy, qsy160, checkqsy


        nonlocal room_list, rcode_list, qsy, buffqsy, qsy160, checkqsy
        nonlocal room_list_list, rcode_list_list

        return {}

    def rmstr2int(roomstr:string):

        nonlocal i, cat_flag, datum, ci_date, otanr, roomno, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal from_date, to_date, inp_str, rmtype, ota, restriction, flag
        nonlocal qsy, buffqsy, qsy160, checkqsy


        nonlocal room_list, rcode_list, qsy, buffqsy, qsy160, checkqsy
        nonlocal room_list_list, rcode_list_list

        roomnr:int = 0

        if cat_flag:

            buffqsy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, roomstr)]})

            if buffqsy:
                roomnr = buffqsy.number1
        else:

            zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, roomstr)]})

            if zimkateg:
                roomnr = zimkateg.zikatnr
        return roomnr


    def create_new_queasy(rate_code:string, roomno:int):

        nonlocal i, cat_flag, datum, ci_date, otanr, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal from_date, to_date, inp_str, rmtype, ota, restriction, flag
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

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
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


    def update_queasy(rate_code:string, roomno:int):

        nonlocal i, cat_flag, datum, ci_date, otanr, rcode, user_init, stat, str, progavail, queasy, htparam, zimkateg, guest, guest_pr, bediener, res_history
        nonlocal from_date, to_date, inp_str, rmtype, ota, restriction, flag
        nonlocal qsy, buffqsy, qsy160, checkqsy


        nonlocal room_list, rcode_list, qsy, buffqsy, qsy160, checkqsy
        nonlocal room_list_list, rcode_list_list

        curr_anz:int = 0
        old_status:string = ""
        new_status:string = ""
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
            pass

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

            if user_init != "":

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
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
            pass
            pass

            qsy = get_cache (Queasy, {"key": [(eq, 175)],"char1": [(eq, rate_code)],"number1": [(eq, roomno)],"number3": [(eq, otanr)],"date1": [(eq, datum)],"char2": [(eq, stat)]})

            if qsy and qsy.number2 != flag:
                pass
                qsy.number2 = flag
                qsy.logi3 = True


                pass
                pass

            elif not qsy:
                qsy = Queasy()
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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 152)]})

    if queasy:
        cat_flag = True

    if ota.lower()  != "" and ota.lower()  != ("*").lower() :

        guest = db_session.query(Guest).filter(
                 (Guest.karteityp == 2) & (Guest.steuernr != "") & (trim(entry(0, Guest.steuernr, "|")) == (ota).lower())).first()

        if guest:
            otanr = guest.gastnr

    if rmtype.lower()  == ("*").lower() :

        if cat_flag:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 152)).order_by(Queasy._recid).all():

                room_list = query(room_list_list, filters=(lambda room_list: room_list.bezeich == queasy.char1), first=True)

                if not room_list:
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.bezeich = queasy.char1


        else:

            for zimkateg in db_session.query(Zimkateg).order_by(Zimkateg._recid).all():

                room_list = query(room_list_list, filters=(lambda room_list: room_list.bezeich == zimkateg.kurzbez), first=True)

                if not room_list:
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.bezeich = zimkateg.kurzbez

    if rcode.lower()  == ("*").lower() :

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 159)).order_by(Queasy._recid).all():

            for guest_pr in db_session.query(Guest_pr).filter(
                     (Guest_pr.gastnr == queasy.number2)).order_by(Guest_pr._recid).all():

                qsy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

                if qsy:

                    rcode_list = query(rcode_list_list, filters=(lambda rcode_list: rcode_list.bezeich == qsy.char1), first=True)

                    if not rcode_list:
                        rcode_list = Rcode_list()
                        rcode_list_list.append(rcode_list)

                        rcode_list.bezeich = qsy.char1

    if rmtype.lower()  != ("*").lower()  and rcode.lower()  != ("*").lower() :
        roomno = rmstr2int (rmtype)
        for datum in date_range(from_date,to_date) :

            queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode)],"date1": [(eq, datum)],"number1": [(eq, roomno)],"number3": [(eq, otanr)]})

            if not queasy:
                create_new_queasy(rcode, roomno)
            else:
                update_queasy(rcode, roomno)

            if ota.lower()  == ("*").lower() :

                queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode)],"date1": [(eq, datum)],"number1": [(eq, roomno)],"number3": [(ne, 0)]})
                while None != queasy:
                    update_queasy(rcode, roomno)

                    curr_recid = queasy._recid
                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 174) & (Queasy.char1 == (rcode).lower()) & (Queasy.date1 == datum) & (Queasy.number1 == roomno) & (Queasy.number3 != 0) & (Queasy._recid > curr_recid)).first()

    elif rmtype.lower()  == ("*").lower()  and rcode.lower()  != ("*").lower() :

        for room_list in query(room_list_list):
            roomno = rmstr2int (room_list.bezeich)
            for datum in date_range(from_date,to_date) :

                queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode)],"number1": [(eq, roomno)],"date1": [(eq, datum)],"number3": [(eq, otanr)]})

                if not queasy:
                    create_new_queasy(rcode, roomno)

                elif queasy:
                    update_queasy(rcode, roomno)

                if ota.lower()  == ("*").lower() :

                    queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode)],"number1": [(eq, roomno)],"date1": [(eq, datum)],"number3": [(ne, 0)]})
                    while None != queasy:
                        update_queasy(rcode, roomno)

                        curr_recid = queasy._recid
                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 174) & (Queasy.char1 == (rcode).lower()) & (Queasy.number1 == roomno) & (Queasy.date1 == datum) & (Queasy.number3 != 0) & (Queasy._recid > curr_recid)).first()

    elif rmtype.lower()  != ("*").lower()  and rcode.lower()  == ("*").lower() :
        roomno = rmstr2int (rmtype)

        for rcode_list in query(rcode_list_list):
            for datum in date_range(from_date,to_date) :

                queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode_list.bezeich)],"number1": [(eq, roomno)],"date1": [(eq, datum)],"number3": [(eq, otanr)]})

                if not queasy:
                    create_new_queasy(rcode_list.bezeich, roomno)

                elif queasy:
                    update_queasy(rcode_list.bezeich, roomno)

                if ota.lower()  == ("*").lower() :

                    queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode_list.bezeich)],"number1": [(eq, roomno)],"date1": [(eq, datum)],"number3": [(ne, 0)]})
                    while None != queasy:
                        update_queasy(rcode_list.bezeich, roomno)

                        curr_recid = queasy._recid
                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 174) & (Queasy.char1 == rcode_list.bezeich) & (Queasy.number1 == roomno) & (Queasy.date1 == datum) & (Queasy.number3 != 0) & (Queasy._recid > curr_recid)).first()

    elif rmtype.lower()  == ("*").lower()  and rcode.lower()  == ("*").lower() :

        for rcode_list in query(rcode_list_list):

            for room_list in query(room_list_list):
                for datum in date_range(from_date,to_date) :
                    roomno = rmstr2int (room_list.bezeich)

                    queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode_list.bezeich)],"number1": [(eq, roomno)],"date1": [(eq, datum)],"number3": [(eq, otanr)]})

                    if not queasy:
                        create_new_queasy(rcode_list.bezeich, roomno)

                    elif queasy:
                        update_queasy(rcode_list.bezeich, roomno)

                    if ota.lower()  == ("*").lower() :

                        queasy = get_cache (Queasy, {"key": [(eq, 174)],"char1": [(eq, rcode_list.bezeich)],"number1": [(eq, roomno)],"date1": [(eq, datum)],"number3": [(ne, 0)]})
                        while None != queasy:
                            update_queasy(rcode_list.bezeich, roomno)

                            curr_recid = queasy._recid
                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 174) & (Queasy.char1 == rcode_list.bezeich) & (Queasy.number1 == roomno) & (Queasy.date1 == datum) & (Queasy.number3 != 0) & (Queasy._recid > curr_recid)).first()

    for qsy160 in db_session.query(Qsy160).filter(
             (Qsy160.key == 160)).order_by(Qsy160._recid).all():
        for i in range(1,num_entries(qsy160.char1, ";")  + 1) :
            str = entry(i - 1, qsy160.char1, ";")

            if substring(str, 0, 10) == ("$progname$").lower() :
                progavail = substring(str, 10)

                if num_entries(progavail, "=") >= 10:
                    progavail = entry(9, progavail, "=", "yes")
                    qsy160.char1 = entry(i - 1, qsy160.char1, ";", "$progname$" + progavail)

    return generate_output()