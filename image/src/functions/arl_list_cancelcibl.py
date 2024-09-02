from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from functions.intevent_1 import intevent_1
from models import Res_line, Bill, Bediener, Bill_line, Reslin_queasy, Res_history, Resplan, Zimmer, Zimplan, Htparam

def arl_list_cancelcibl(recid_resline:int, user_init:str, t_ankunft:date):
    fl_ok = False
    fl_error = 0
    p_87:date = None
    orig_status:int = 1
    room_nr:str = ""
    priscilla_active:bool = True
    billnumber:str = ""
    res_number:int = 0
    count_i:int = 0
    res_line = bill = bediener = bill_line = reslin_queasy = res_history = resplan = zimmer = zimplan = htparam = None

    resline = buff_resline = mbill = None

    Resline = Res_line
    Buff_resline = Res_line
    Mbill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_ok, fl_error, p_87, orig_status, room_nr, priscilla_active, billnumber, res_number, count_i, res_line, bill, bediener, bill_line, reslin_queasy, res_history, resplan, zimmer, zimplan, htparam
        nonlocal resline, buff_resline, mbill


        nonlocal resline, buff_resline, mbill
        return {"fl_ok": fl_ok, "fl_error": fl_error}

    p_87 = get_output(htpdate(87))

    if t_ankunft < p_87:
        fl_ok = False

    if not fl_ok:

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == recid_resline)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    res_number = res_line.resnr
    room_nr = res_line.zinr

    for bill in db_session.query(Bill).filter(
            (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr)).all():

        if (bill.gesamtumsatz != 0 or bill.saldo != 0):
            fl_error = 1

            return generate_output()

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill.rechnr)).first()

        if bill_line:
            fl_error = 2

            return generate_output()
    billnumber = ""

    for bill in db_session.query(Bill).filter(
            (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr)).all():

        if bill.rechnr == 0:
            db_session.delete(bill)

        else:
            bill.flag = 1
            fl_error = 3
            billnumber = billnumber + ";" + to_string(bill.rechnr)

    for buff_resline in db_session.query(Buff_resline).filter(
            (Buff_resline.resnr == res_number) &  (Buff_resline.resstatus == 6)).all():
        count_i = count_i + 1

    if count_i == 1:

        mbill = db_session.query(Mbill).filter(
                (Mbill.resnr == res_number) &  (Mbill.reslinnr == 0) &  (Mbill.saldo != 0) &  (Mbill.zinr == "") &  (Mbill.flag == 0)).first()

        if mbill:
            fl_error = 1
    reslin_queasy = Reslin_queasy()
    db_session.add(reslin_queasy)

    reslin_queasy.key = "ResChanges"
    reslin_queasy.resnr = res_line.resnr
    reslin_queasy.reslinnr = res_line.reslinnr
    reslin_queasy.date2 = get_current_date()
    reslin_queasy.number2 = get_current_time_in_seconds()
    reslin_queasy.char3 = to_string(res_line.ankunft) + ";" +\
            to_string(res_line.ankunft) + ";" +\
            to_string(res_line.abreise) + ";" +\
            to_string(res_line.abreise) + ";" +\
            to_string(res_line.zimmeranz) + ";" +\
            to_string(res_line.zimmeranz) + ";" +\
            to_string(res_line.erwachs) + ";" +\
            to_string(res_line.erwachs) + ";" +\
            to_string(res_line.kind1) + ";" +\
            to_string(res_line.kind1) + ";" +\
            to_string(res_line.gratis) + ";" +\
            to_string(res_line.gratis) + ";" +\
            to_string(res_line.zikatnr) + ";" +\
            to_string(res_line.zikatnr) + ";" +\
            to_string(res_line.zinr) + ";" +\
            to_string(res_line.zinr) + ";" +\
            to_string(res_line.arrangement) + ";" +\
            to_string(res_line.arrangement) + ";" +\
            to_string(res_line.zipreis) + ";" +\
            to_string(res_line.zipreis) + ";" +\
            to_string(user_init) + ";" +\
            to_string(user_init) + ";" +\
            to_string(get_current_date()) + ";" +\
            to_string(get_current_date()) + ";" +\
            to_string(res_line.name) + ";" +\
            to_string("CANCEL CHECK_IN") + ";" +\
            to_string(" ") + ";" +\
            to_string(" ") + ";"

    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.resnr = res_line.resnr
    res_history.reslinnr = res_line.reslinnr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Cancel C/I Room " + res_line.zinr +\
            " ResNo " + to_string(res_line.resnr) + " billnumber " + billnumber
    res_history.action = "Cancel C/I"

    res_history = db_session.query(Res_history).first()

    get_output(intevent_1(2, res_line.zinr, "Deactivate!;PABX", res_line.resnr, res_line.reslinnr))

    for resplan in db_session.query(Resplan).filter(
            (Resplan.zikatnr == res_line.zikatnr) &  (Resplan.datum >= res_line.ankunft) &  (Resplan.datum < res_line.abreise)).all():
        resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] - 1
        resplan.anzzim[0] = resplan.anzzim[0] + 1


    resline = db_session.query(Resline).filter(
            (Resline.active_flag == 1) &  (Resline.zinr == res_line.zinr) &  (Resline.reslinnr != res_line.reslinnr)).first()

    if not resline:

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == res_line.zinr)).first()

        if zimmer:

            zimmer = db_session.query(Zimmer).first()
            zimmer.zistatus = 2

            zimmer = db_session.query(Zimmer).first()

        for zimplan in db_session.query(Zimplan).filter(
                (Zimplan.zinr == res_line.zinr) &  (Zimplan.gastnrmember == res_line.gastnrmember) &  (Zimplan.datum >= res_line.ankunft) &  (Zimplan.datum <= (res_line.abreise - 1))).all():
            db_session.delete(zimplan)


    resline = db_session.query(Resline).filter(
            (Resline._recid == res_line._recid)).first()

    if resline.resstatus == 13:
        orig_status = 11
    resline.zinr = ""
    resline.resstatus = orig_status
    resline.ankzeit = 0
    resline.active_flag = 0

    resline = db_session.query(Resline).first()

    for resline in db_session.query(Resline).filter(
            (Resline.resnr == res_line.resnr) &  (Resline.active_flag == 1) &  (Resline.l_zuordnung[2] == 1) &  (Resline.kontakt_nr == res_line.reslinnr)).all():
        resline.zinr = ""
        resline.resstatus = 11
        resline.ankzeit = 0
        resline.active_flag = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 341)).first()

    if htparam.fchar != "":
        get_output(intevent_1(2, room_nr, "My Checkout!", res_line.resnr, res_line.reslinnr))

    if priscilla_active:
        get_output(intevent_1(9, room_nr, "Priscilla", res_line.resnr, res_line.reslinnr))

    return generate_output()