#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Zimkateg, Zimmer, Bediener, Res_history, Htparam, Queasy

def del_room_admin_1bl(pvilanguage:int, zinr:string, zikatnr:int, user_init:string):

    prepare_cache ([Zimkateg, Bediener, Res_history, Htparam, Queasy])

    msg_str = ""
    room_limit = 0
    curr_anz = 0
    lvcarea:string = "del-room-admin"
    res_line = zimkateg = zimmer = bediener = res_history = htparam = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_limit, curr_anz, lvcarea, res_line, zimkateg, zimmer, bediener, res_history, htparam, queasy
        nonlocal pvilanguage, zinr, zikatnr, user_init

        return {"msg_str": msg_str, "room_limit": room_limit, "curr_anz": curr_anz}

    def check_rm_limit():

        nonlocal msg_str, room_limit, curr_anz, lvcarea, res_line, zimkateg, zimmer, bediener, res_history, htparam, queasy
        nonlocal pvilanguage, zinr, zikatnr, user_init

        rbuff = None
        Rbuff =  create_buffer("Rbuff",Zimmer)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

        if htparam.finteger > 0:
            room_limit = htparam.finteger
        curr_anz = 0

        for rbuff in db_session.query(Rbuff).order_by(Rbuff._recid).all():
            curr_anz = curr_anz + 1


    def update_queasy():

        nonlocal msg_str, room_limit, curr_anz, lvcarea, res_line, zimkateg, zimmer, bediener, res_history, htparam, queasy
        nonlocal pvilanguage, zinr, zikatnr, user_init

        cat_flag:bool = False
        z_nr:int = 0
        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zikatnr)]})

        if zimkateg:

            if cat_flag:
                z_nr = zimkateg.typ
            else:
                z_nr = zimkateg.zikatnr

        queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(ge, get_current_date())],"number1": [(eq, z_nr)]})
        while None != queasy :

            if queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

            curr_recid = queasy._recid
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) & (Queasy.date1 >= get_current_date()) & (Queasy.number1 == z_nr) & (Queasy._recid > curr_recid)).first()

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Delete Room Number " + zimmer.zinr
        res_history.action = "Log Availability"


        pass
        pass

    res_line = get_cache (Res_line, {"zinr": [(eq, zinr)]})

    if res_line:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")
    else:

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zikatnr)]})
        zimkateg.maxzimanz = zimkateg.maxzimanz - 1
        pass

        zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

        if zimmer:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete Room Number " + zimmer.zinr


            res_history.action = "Room Admin"
            pass
            pass
            pass
            db_session.delete(zimmer)
            pass
        check_rm_limit()
        update_queasy()

    return generate_output()