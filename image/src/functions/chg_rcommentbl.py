from functions.additional_functions import *
import decimal
from datetime import date
import re
from sqlalchemy import func
from models import Res_line, Reservation, Guest, Queasy, Reslin_queasy, Bediener, Res_history

def chg_rcommentbl(icase:int, resno:int, reslinno:int, user_init:str, res_com:str, resl_com:str, g_com:str, web_com:str):
    str1:str = ""
    str2:str = ""
    loopi:int = 0
    loopj:int = 0
    loopk:int = 0
    heute:date = None
    zeit:int = 0
    cid:str = ""
    cdate:str = ""
    res_line = reservation = guest = queasy = reslin_queasy = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str1, str2, loopi, loopj, loopk, heute, zeit, cid, cdate, res_line, reservation, guest, queasy, reslin_queasy, bediener, res_history


        return {}

    def read_comment():

        nonlocal str1, str2, loopi, loopj, loopk, heute, zeit, cid, cdate, res_line, reservation, guest, queasy, reslin_queasy, bediener, res_history

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()
        g_com = guest.bemerk
        res_com = reservation.bemerk
        resl_com = res_line.bemerk


        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if re.match(".*WCI_req.*",str1):
                str2 = entry(1, str1, " == ")
                for loopj in range(1,num_entries(str2, ",")  + 1) :

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 160) &  (Queasy.number1 == to_int(entry(loopj - 1, str2, ",")))).first()

                    if queasy:
                        for loopk in range(1,num_entries(queasy.char1, ";")  + 1) :

                            if re.match(".*en.*",entry(loopk - 1, queasy.char1, ";")):
                                web_com = entry(1, entry(loopk - 1, queasy.char1, ";") , " == ") + ", " + web_com


                                return

            elif re.match(".*PRCODE.*",str1):
                web_com = web_com + "PromoCode: " + entry(2, str1, "$")

    def update_comment():

        nonlocal str1, str2, loopi, loopj, loopk, heute, zeit, cid, cdate, res_line, reservation, guest, queasy, reslin_queasy, bediener, res_history

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

        if (res_com != reservation.bemerk) or (resl_com != res_line.bemerk):
            heute = get_current_date()
            zeit = get_current_time_in_seconds()

            if trim(res_line.changed_id) != "":
                cid = res_line.changed_id
                cdate = to_string(res_line.changed)

            elif len(res_line.reserve_char) >= 14:
                cid = substring(res_line.reserve_char, 13)
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "ResChanges"
            reslin_queasy.resnr = resno
            reslin_queasy.reslinnr = reslinno
            reslin_queasy.date2 = heute
            reslin_queasy.number2 = zeit


            reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(res_line.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.zinr) + ";" + to_string(res_line.arrangement) + ";" + to_string(res_line.arrangement) + ";"
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.zipreis) + ";" + to_string(res_line.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(heute) + ";" + to_string(res_line.name) + ";" + to_string(res_line.name) + ";"

            if res_line.was_status == 0:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO", "x(3)") + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"

            if res_line.was_status == 0:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO", "x(3)") + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"

            reslin_queasy = db_session.query(Reslin_queasy).first()


            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = res_line.resnr
            res_history.reslinnr = res_line.reslinnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Remark"


            res_history.aenderung = to_string(res_line.resnr) + "-" + reservation.bemerk + chr(10) + res_line.bemerk + chr(10) + chr(10) + "*** Changed to:" + chr(10) + chr(10) + res_com + chr(10) + resl_com

            if bediener:
                res_history.betriebsnr = bediener.nr

        guest.bemerk = g_com
        reservation.bemerk = res_com
        res_line.bemerk = resl_com

        res_line = db_session.query(Res_line).first()

        reservation = db_session.query(Reservation).first()

        guest = db_session.query(Guest).first()


    if icase == 1:
        read_comment()

    elif icase == 2:
        update_comment()

    return generate_output()