from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Queasy, Guest, Guest_pr, Bediener, Res_history, Waehrung

def ratecode_adm_prcodebl(curr_select:str, prcode:str, bezeich:str, segmentcode:str, minstay:int, maxstay:int, minadvance:int, maxadvance:int, frdate:date, todate:date, user_init:str, foreign_rate:bool, local_flag:bool, drate_flag:bool, gastnr:int, local_nr:int, foreign_nr:int):
    tb1_list = []
    ct:str = ""
    queasy = guest = guest_pr = bediener = res_history = waehrung = None

    tb1 = None

    tb1_list, Tb1 = create_model_like(Queasy, {"waehrungsnr":int, "wabkurz":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tb1_list, ct, queasy, guest, guest_pr, bediener, res_history, waehrung


        nonlocal tb1
        nonlocal tb1_list
        return {"tb1": tb1_list}

    if curr_select.lower()  == "add":
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 2
        queasy.char1 = prcode
        queasy.char2 = bezeich
        queasy.char3 = segmentcode + ";"
        queasy.number2 = minstay
        queasy.deci2 = maxstay
        queasy.number3 = minadvance
        queasy.deci3 = maxadvance
        queasy.date1 = frdate
        queasy.date2 = todate
        queasy.logi1 = local_flag
        queasy.logi2 = drate_flag

        if (not foreign_rate) or queasy.logi1:
            queasy.number1 = local_nr
        else:
            queasy.number1 = foreign_nr

        queasy = db_session.query(Queasy).first()

        if gastnr == 0:

            guest = db_session.query(Guest).first()

            if guest and guest.gastnr > 0:
                gastnr = guest.gastnr + 1
            else:
                gastnr = 1
            guest = Guest()
            db_session.add(guest)

            guest.gastnr = gastnr
            guest.name = prcode
            guest.karteityp = 9
            guest.anlage_datum = get_current_date()
            guest.char1 = user_init

            guest = db_session.query(Guest).first()
        guest_pr = Guest_pr()
        db_session.add(guest_pr)

        guest_pr.gastnr = gastnr
        guest_pr.code = prcode

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Add Contract Rate, Code: " + prcode + " segmentcode: " + segmentcode + " Description: " + bezeich


            res_history.action = "RateCode"

            res_history = db_session.query(Res_history).first()

    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (func.lower(Queasy.char1) == (prcode).lower())).first()
        queasy.char2 = bezeich
        queasy.logi1 = local_flag
        queasy.number2 = minstay
        queasy.deci2 = maxstay
        queasy.number3 = minadvance
        queasy.deci3 = maxadvance
        queasy.date1 = frdate
        queasy.date2 = todate

        if not re.match(".*;.*",queasy.char3):
            queasy.char3 = segmentcode + ";"
        else:
            ct = entry(0, queasy.char3, ";") + ";"
            queasy.char3 = segmentcode + ";" +\
                substring(queasy.char3, len(ct) + 1 - 1)

        queasy = db_session.query(Queasy).first()

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Contract Rate, Code: " + prcode + " segmentcode: " + segmentcode + " Description: " + bezeich


            res_history.action = "RateCode"

            res_history = db_session.query(Res_history).first()

    tb1 = Tb1()
    tb1_list.append(tb1)

    buffer_copy(queasy, tb1)

    waehrung = db_session.query(Waehrung).filter(
            (Waehrungsnr == queasy.number1)).first()

    if waehrung:
        tb1.waehrungsnr = waehrungsnr
        tb1.wabkurz = waehrung.wabkurz

    return generate_output()