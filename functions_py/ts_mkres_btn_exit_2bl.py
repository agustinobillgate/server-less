#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def ts_mkres_btn_exit_2bl(pvilanguage:int, moved_tisch:int, s_recid:int, curr_dept:int, curr_date:date, von_zeit:string, bis_zeit:string, pax:int, telefon:string, gname:string, user_init:string, comments:string, selected_gastnr:int, depo_amount:Decimal, ns_billno:int, move_date:date):

    prepare_cache ([Queasy])

    msg_str = ""
    done = False
    lvcarea:string = "TS-mkres"
    queasy = None

    qsy = None

    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, done, lvcarea, queasy
        nonlocal pvilanguage, moved_tisch, s_recid, curr_dept, curr_date, von_zeit, bis_zeit, pax, telefon, gname, user_init, comments, selected_gastnr, depo_amount, ns_billno, move_date
        nonlocal qsy


        nonlocal qsy

        return {"moved_tisch": moved_tisch, "msg_str": msg_str, "done": done}


    if s_recid == 0:

        qsy = db_session.query(Qsy).filter(
                 (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (von_zeit >= substring(Qsy.char1, 0, 4)) & (von_zeit <= substring(Qsy.char1, 4, 4))).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                     (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (bis_zeit >= substring(Qsy.char1, 0, 4)) & (bis_zeit <= substring(Qsy.char1, 4, 4))).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                     (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (substring(Qsy.char1, 0, 4) >= (von_zeit).lower()) & (substring(Qsy.char1, 0, 4) <= (bis_zeit).lower())).first()

        if not qsy:

            qsy = db_session.query(Qsy).filter(
                     (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (substring(Qsy.char1, 4, 4) >= (von_zeit).lower()) & (substring(Qsy.char1, 4, 4) <= (bis_zeit).lower())).first()
    else:

        if move_date == curr_date:

            qsy = db_session.query(Qsy).filter(
                     (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (von_zeit >= substring(Qsy.char1, 0, 4)) & (von_zeit <= substring(Qsy.char1, 4, 4)) & (Qsy._recid != s_recid)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (bis_zeit >= substring(Qsy.char1, 0, 4)) & (bis_zeit <= substring(Qsy.char1, 4, 4)) & (Qsy._recid != s_recid)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (substring(Qsy.char1, 0, 4) >= (von_zeit).lower()) & (substring(Qsy.char1, 0, 4) <= (bis_zeit).lower()) & (Qsy._recid != s_recid)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == curr_date) & (Qsy.logi3) & (substring(Qsy.char1, 4, 4) >= (von_zeit).lower()) & (substring(Qsy.char1, 4, 4) <= (bis_zeit).lower()) & (Qsy._recid != s_recid)).first()
        else:

            qsy = db_session.query(Qsy).filter(
                     (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == move_date) & (Qsy.logi3) & (von_zeit >= substring(Qsy.char1, 0, 4)) & (von_zeit <= substring(Qsy.char1, 4, 4)) & (Qsy._recid != s_recid)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == move_date) & (Qsy.logi3) & (bis_zeit >= substring(Qsy.char1, 0, 4)) & (bis_zeit <= substring(Qsy.char1, 4, 4)) & (Qsy._recid != s_recid)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == move_date) & (Qsy.logi3) & (substring(Qsy.char1, 0, 4) >= (von_zeit).lower()) & (substring(Qsy.char1, 0, 4) <= (bis_zeit).lower()) & (Qsy._recid != s_recid)).first()

            if not qsy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 33) & (Qsy.number1 == curr_dept) & (Qsy.number2 == moved_tisch) & (Qsy.date1 == move_date) & (Qsy.logi3) & (substring(Qsy.char1, 4, 4) >= (von_zeit).lower()) & (substring(Qsy.char1, 4, 4) <= (bis_zeit).lower()) & (Qsy._recid != s_recid)).first()

            if qsy:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Overlapping Reservation time found:", lvcarea, "") + chr_unicode(10) + to_string(move_date) + "=> " + entry(0, qsy.char2, "&&") + " " + to_string(substring(qsy.char1, 0, 4) , "99:99") + " - " + to_string(substring(qsy.char1, 4, 4) , "99:99")

                return generate_output()

    if qsy:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Overlapping Reservation time found:", lvcarea, "") + chr_unicode(10) + entry(0, qsy.char2, "&&") + " " + to_string(substring(qsy.char1, 0, 4) , "99:99") + " - " + to_string(substring(qsy.char1, 4, 4) , "99:99")

        return generate_output()

    if matches(gname,r"*&*"):
        gname = replace_str(gname, "&", "")

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
        queasy.char2 = gname + "&&" + to_string(selected_gastnr)
        queasy.char3 = user_init + ";" + replace_str(comments, ";", ",") + ";"
        queasy.deci1 =  to_decimal(depo_amount)
        queasy.deci2 =  to_decimal(ns_billno)
        queasy.logi3 = True


        pass
        done = True
    else:

        # queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})
        queasy = db_session.query(Queasy).filter(Queasy._recid == s_recid).with_for_update().first()

        queasy.number2 = moved_tisch
        queasy.number3 = pax
        queasy.date3 = get_current_date()
        queasy.char1 = von_zeit + bis_zeit + ";" + telefon
        queasy.char2 = gname + "&&" + to_string(selected_gastnr)
        queasy.char3 = user_init + ";" + replace_str(comments, ";", ",") + ";"
        queasy.deci1 =  to_decimal(depo_amount)
        queasy.deci2 =  to_decimal(ns_billno)

        if move_date != curr_date:
            queasy.date1 = move_date
        pass
        pass
        done = True

    return generate_output()