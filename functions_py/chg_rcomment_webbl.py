#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 28/10/2025
# remark ke-4 blm muncul
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Res_line, Reservation, Guest, Reslin_queasy, Bediener, Res_history

def chg_rcomment_webbl(icase:int, resno:int, reslinno:int, user_init:string, res_com:string, resl_com:string, g_com:string, web_com:string):

    prepare_cache ([Queasy, Res_line, Reservation, Guest, Reslin_queasy, Bediener, Res_history])

    str1:string = ""
    str2:string = ""
    loopi:int = 0
    loopj:int = 0
    loopk:int = 0
    heute:date = None
    zeit:int = 0
    cid:string = " "
    cdate:string = " "
    queasy = res_line = reservation = guest = reslin_queasy = bediener = res_history = None

    buf_q = None

    Buf_q = create_buffer("Buf_q",Queasy)


    db_session = local_storage.db_session

    web_com = web_com.strip()
    res_com = res_com.strip()
    resl_com = resl_com.strip()
    g_com = g_com.strip()

    def generate_output():
        nonlocal str1, str2, loopi, loopj, loopk, heute, zeit, cid, cdate, queasy, res_line, reservation, guest, reslin_queasy, bediener, res_history
        nonlocal icase, resno, reslinno, user_init, res_com, resl_com, g_com, web_com
        nonlocal buf_q


        nonlocal buf_q

        return {"res_com": res_com, "resl_com": resl_com, "g_com": g_com, "web_com": web_com}

    def read_comment():

        nonlocal str1, str2, loopi, loopj, loopk, heute, zeit, cid, cdate, queasy, res_line, reservation, guest, reslin_queasy, bediener, res_history
        nonlocal icase, resno, reslinno, user_init, res_com, resl_com, g_com, web_com
        nonlocal buf_q


        nonlocal buf_q

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if not res_line:

            return

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        g_com = guest.bemerkung
        res_com = reservation.bemerk
        resl_com = res_line.bemerk


        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str1 = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if matches(str1,r"*WCI-req*"):
                str2 = entry(1, str1, "=")
                for loopj in range(1,num_entries(str2, ",")  + 1) :

                    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, to_int(entry(loopj - 1, str2, ",")))]})

                    if queasy:
                        for loopk in range(1,num_entries(queasy.char1, ";")  + 1) :

                            if matches(entry(loopk - 1, queasy.char1, ";"),r"*en*"):
                                web_com = entry(1, entry(loopk - 1, queasy.char1, ";") , "=") + ", " + web_com


                                return

            elif matches(str1,r"*PRCODE*"):
                web_com = web_com + "PromoCode: " + entry(2, str1, "$")

        # buf_q = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, resno)],"number2": [(eq, reslinno)]})
        buf_q = db_session.query(Queasy).filter((Queasy.key == 267) & (Queasy.number1 == resno) & (Queasy.number2 == reslinno)).first() 

        if buf_q:
            web_com = web_com + buf_q.char1


    def update_comment():

        nonlocal str1, str2, loopi, loopj, loopk, heute, zeit, cid, cdate, queasy, res_line, reservation, guest, reslin_queasy, bediener, res_history
        nonlocal icase, resno, reslinno, user_init, res_com, resl_com, g_com, web_com
        nonlocal buf_q


        nonlocal buf_q

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if not res_line:

            return
        pass

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if (res_com != reservation.bemerk) or (resl_com != res_line.bemerk):
            heute = get_current_date()
            zeit = get_current_time_in_seconds()

            if trim(res_line.changed_id) != "":
                cid = res_line.changed_id
                cdate = to_string(res_line.changed)

            elif length(res_line.reserve_char) >= 14:
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
            pass
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = res_line.resnr
            res_history.reslinnr = res_line.reslinnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Remark"


            res_history.aenderung = to_string(res_line.resnr) + "-" + reservation.bemerk + chr_unicode(10) + res_line.bemerk + chr_unicode(10) + chr_unicode(10) + "*** Changed to:" + chr_unicode(10) + chr_unicode(10) + res_com + chr_unicode(10) + resl_com

            if bediener:
                res_history.betriebsnr = bediener.nr
            pass
        guest.bemerkung = g_com
        reservation.bemerk = res_com
        res_line.bemerk = resl_com

        # buf_q = get_cache (Queasy, {"key": [(eq, 267)],"number1": [(eq, resno)],"number2": [(eq, reslinno)]})
        buf_q = db_session.query(Queasy).filter((Queasy.key == 267) & (Queasy.number1 == resno) & (Queasy.number2 == reslinno)).first()

        if not buf_q:
            buf_q = Queasy()
            buf_q.key = 267
            buf_q.number1 = resno
            buf_q.number2 = reslinno
            buf_q.char1 = web_com
            db_session.add(buf_q)

        else:
            pass
            buf_q.char1 = web_com

        db_session.commit()

    if icase == 1:
        read_comment()

    elif icase == 2:
        update_comment()

    return generate_output()