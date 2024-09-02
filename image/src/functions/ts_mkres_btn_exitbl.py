from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy

def ts_mkres_btn_exitbl(pvilanguage:int, moved_tisch:int, s_recid:int, curr_dept:int, curr_date:date, von_zeit:str, bis_zeit:str, pax:int, telefon:str, gname:str, user_init:str, comments:str):
    msg_str = ""
    done = False
    lvcarea:str = "TS_mkres"
    queasy = None

    qsy = None

    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, done, lvcarea, queasy
        nonlocal qsy


        nonlocal qsy
        return {"msg_str": msg_str, "done": done}


    if s_recid == 0:

        qsy = db_session.query(Qsy).filter(
                (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (Qsy.von_zeit >= substring(Qsy.char1, 0, 4)) &  (Qsy.von_zeit <= substring(Qsy.char1, 4, 4))).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (Qsy.bis_zeit >= substring(Qsy.char1, 0, 4)) &  (Qsy.bis_zeit <= substring(Qsy.char1, 4, 4))).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (substring(Qsy.char1, 0, 4) >= (von_zeit).lower()) &  (substring(Qsy.char1, 0, 4) <= (bis_zeit).lower())).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (substring(Qsy.char1, 4, 4) >= (von_zeit).lower()) &  (substring(Qsy.char1, 4, 4) <= (bis_zeit).lower())).first()
    else:

        qsy = db_session.query(Qsy).filter(
                (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (Qsy.von_zeit >= substring(Qsy.char1, 0, 4)) &  (Qsy.von_zeit <= substring(Qsy.char1, 4, 4)) &  (Qsy._recid != s_recid)).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (Qsy.bis_zeit >= substring(Qsy.char1, 0, 4)) &  (Qsy.bis_zeit <= substring(Qsy.char1, 4, 4)) &  (Qsy._recid != s_recid)).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (substring(Qsy.char1, 0, 4) >= (von_zeit).lower()) &  (substring(Qsy.char1, 0, 4) <= (bis_zeit).lower()) &  (Qsy._recid != s_recid)).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 33) &  (Qsy.number1 == curr_dept) &  (Qsy.number2 == moved_tisch) &  (Qsy.date1 == curr_date) &  (Qsy.logi3) &  (substring(Qsy.char1, 4, 4) >= (von_zeit).lower()) &  (substring(Qsy.char1, 4, 4) <= (bis_zeit).lower()) &  (Qsy._recid != s_recid)).first()

    if qsy:
        msg_str = msg_str + chr(2) + translateExtended ("Overlapping Reservation time found:", lvcarea, "") + chr(10) + entry(0, qsy.char2, "&&") + " " + to_string(substring(qsy.char1, 0, 4) , "99:99") + " - " + to_string(substring(qsy.char1, 4, 4) , "99:99")

        return generate_output()

    if s_recid == 0:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 33
        queasy.number1 = curr_dept
        queasy.number2 = moved_tisch
        queasy.number3 = pax
        queasy.date1 = curr_date
        queasy.date2 = get_current_date()
        queasy.char1 = von_zeit + bis_zeit + ";" + telefon
        queasy.char2 = gname + "&&"
        queasy.char3 = user_init + ";" + replace_str(comments, ";", ",") + ";"
        queasy.logi3 = True

        queasy = db_session.query(Queasy).first()
        done = True
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == s_recid)).first()
        queasy.number2 = moved_tisch
        queasy.number3 = pax
        queasy.date3 = get_current_date()
        queasy.char1 = von_zeit + bis_zeit + ";" + telefon
        queasy.char2 = gname + "&&"
        queasy.char3 = user_init + ";" + replace_str(comments, ";", ",") + ";"

        queasy = db_session.query(Queasy).first()
        done = True

    return generate_output()