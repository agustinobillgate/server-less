from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Zimkateg, Zimmer, Bediener, Res_history, Htparam, Queasy

def del_room_admin_1bl(pvilanguage:int, zinr:str, zikatnr:int, user_init:str):
    msg_str = ""
    room_limit = 0
    curr_anz = 0
    lvcarea:str = "del_room_admin"
    res_line = zimkateg = zimmer = bediener = res_history = htparam = queasy = None

    rbuff = qsy = None

    Rbuff = Zimmer
    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, room_limit, curr_anz, lvcarea, res_line, zimkateg, zimmer, bediener, res_history, htparam, queasy
        nonlocal rbuff, qsy


        nonlocal rbuff, qsy
        return {"msg_str": msg_str, "room_limit": room_limit, "curr_anz": curr_anz}

    def check_rm_limit():

        nonlocal msg_str, room_limit, curr_anz, lvcarea, res_line, zimkateg, zimmer, bediener, res_history, htparam, queasy
        nonlocal rbuff, qsy


        nonlocal rbuff, qsy


        Rbuff = Zimmer

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 975)).first()

        if htparam.finteger > 0:
            room_limit = htparam.finteger
        curr_anz = 0

        for rbuff in db_session.query(Rbuff).all():
            curr_anz = curr_anz + 1

    def update_queasy():

        nonlocal msg_str, room_limit, curr_anz, lvcarea, res_line, zimkateg, zimmer, bediener, res_history, htparam, queasy
        nonlocal rbuff, qsy


        nonlocal rbuff, qsy

        cat_flag:bool = False
        z_nr:int = 0
        Qsy = Queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 152)).first()

        if queasy:
            cat_flag = True

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zikatnr)).first()

        if zimkateg:

            if cat_flag:
                z_nr = zimkateg.typ
            else:
                z_nr = zimkateg.zikatnr

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 171) &  (Queasy.date1 >= get_current_date()) &  (Queasy.number1 == z_nr)).first()
        while None != queasy and queasy.logi1 == False and queasy.logi2 == False :

            qsy = db_session.query(Qsy).filter(
                    (Qsy._recid == queasy._recid)).first()

            if qsy:
                qsy.logi2 = True

                qsy = db_session.query(Qsy).first()


            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 >= get_current_date()) &  (Queasy.number1 == z_nr)).first()


    res_line = db_session.query(Res_line).filter(
            (func.lower(Res_line.(zinr).lower()) == (zinr).lower())).first()

    if res_line:
        msg_str = msg_str + chr(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")
    else:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zikatnr)).first()
        zimkateg.maxzimanz = zimkateg.maxzimanz - 1

        zimkateg = db_session.query(Zimkateg).first()

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

        if zimmer:

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete Room Number " + zimmer.zinr


            res_history.action = "Room Admin"

            res_history = db_session.query(Res_history).first()


            zimmer = db_session.query(Zimmer).first()
            db_session.delete(zimmer)

        check_rm_limit()
        update_queasy()

    return generate_output()