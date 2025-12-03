# using conversion tools version: 1.0.0.117
# ------------------------------------------
# Rulita, 15/8/2025
# Modify input param intevent_1 cancelCI roomnr
# ticket: 1957FB
# --------------------------------------------

# ==========================================
# Rulita, 25-11-2025
# - Added with_for_update all query

# yusufwijasena, 03/12/2025
# - fix position db_session.refresh()
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.intevent_1 import intevent_1
from models import Res_line, Bill, Bediener, Bill_line, Reslin_queasy, Res_history, Resplan, Zimmer, Zimplan, Htparam


def arl_list_cancelcibl(recid_resline: int, user_init: string, t_ankunft: date):

    prepare_cache([Res_line, Bill, Bediener, Reslin_queasy, Res_history, Resplan, Zimmer, Htparam])

    fl_ok = True
    fl_error = 0
    p_87: date = None
    orig_status: int = 1
    room_nr: string = ""
    priscilla_active: bool = True
    billnumber: string = ""
    res_number: int = 0
    count_i: int = 0
    res_line = bill = bediener = bill_line = reslin_queasy = res_history = resplan = zimmer = zimplan = htparam = None

    resline = buff_resline = mbill = None

    Resline = create_buffer("Resline", Res_line)
    Buff_resline = create_buffer("Buff_resline", Res_line)
    Mbill = create_buffer("Mbill", Bill)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_ok, fl_error, p_87, orig_status, room_nr, priscilla_active, billnumber, res_number, count_i, res_line, bill, bediener, bill_line, reslin_queasy, res_history, resplan, zimmer, zimplan, htparam
        nonlocal recid_resline, user_init, t_ankunft
        nonlocal resline, buff_resline, mbill
        nonlocal resline, buff_resline, mbill

        return {
            "fl_ok": fl_ok,
            "fl_error": fl_error
        }

    p_87 = get_output(htpdate(87))

    if t_ankunft < p_87:
        fl_ok = False

    if not fl_ok:
        return generate_output()

    res_line = get_cache(Res_line, {"_recid": [(eq, recid_resline)]})

    if not res_line:
        return generate_output()

    bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
    res_number = res_line.resnr
    room_nr = res_line.zinr

    for bill in db_session.query(Bill).filter(
            (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr)).order_by(Bill._recid).all():

        if (bill.gesamtumsatz != 0 or bill.saldo != 0):
            fl_error = 1

            return generate_output()

        bill_line = get_cache(Bill_line, {"rechnr": [(eq, bill.rechnr)]})

        if bill_line:
            fl_error = 2

            return generate_output()

    billnumber = ""
    for bill in db_session.query(Bill).filter(
            (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr)).order_by(Bill._recid).with_for_update().all():

        if bill.rechnr == 0:
            db_session.delete(bill)
            pass
        else:
            bill.flag = 1
            fl_error = 3
            billnumber = billnumber + ";" + to_string(bill.rechnr)

        db_session.refresh(bill, with_for_update=True)

    for buff_resline in db_session.query(Buff_resline).filter(
            (Buff_resline.resnr == res_number) & (Buff_resline.resstatus == 6)).order_by(Buff_resline._recid).all():
        count_i = count_i + 1

    if count_i == 1:
        mbill = get_cache(
            Bill, {"resnr": [(eq, res_number)], "reslinnr": [(eq, 0)], "saldo": [(ne, 0)], "zinr": [(eq, "")], "flag": [(eq, 0)]})

        if mbill:
            fl_error = 1

            return generate_output()

    elif count_i == 0:

        # mbill = get_cache (Bill, {"resnr": [(eq, res_number)],"reslinnr": [(eq, 0)],"saldo": [(eq, 0)],"zinr": [(eq, "")],"flag": [(eq, 0)]})
        mbill = db_session.query(Bill).filter((Bill.resnr == res_number) & (Bill.reslinnr == 0) & (
            Bill.saldo == 0) & (Bill.zinr == "") & (Bill.flag == 0)).with_for_update().first()

        if mbill:
            mbill.flag = 1
            fl_error = 3
            billnumber = billnumber + ";" + to_string(mbill.rechnr)
        else:
            fl_error = 1
            return generate_output()

        db_session.refresh(mbill, with_for_update=True)

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
        to_string("CANCEL CHECK-IN") + ";" +\
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

    get_output(intevent_1(2, res_line.zinr, "Deactivate!;PABX", res_line.resnr, res_line.reslinnr))

    for resplan in db_session.query(Resplan).filter(
            (Resplan.zikatnr == res_line.zikatnr) & (Resplan.datum >= res_line.ankunft) & (Resplan.datum < res_line.abreise)).order_by(Resplan._recid).with_for_update().all():
        resplan.anzzim[res_line.resstatus - 1] = resplan.anzzim[res_line.resstatus - 1] - 1
        resplan.anzzim[0] = resplan.anzzim[0] + 1
        db_session.refresh(resplan, with_for_update=True)

    resline = get_cache(
        Res_line, {"active_flag": [(eq, 1)], "zinr": [(eq, res_line.zinr)], "reslinnr": [(ne, res_line.reslinnr)]})

    if not resline:
        zimmer = get_cache(Zimmer, {"zinr": [(eq, res_line.zinr)]})

        if zimmer:
            zimmer.zistatus = 2

        for zimplan in db_session.query(Zimplan).filter(
                (Zimplan.zinr == res_line.zinr) & (Zimplan.gastnrmember == res_line.gastnrmember) & (Zimplan.datum >= res_line.ankunft) & (Zimplan.datum <= (res_line.abreise - timedelta(days=1)))).order_by(Zimplan._recid).with_for_update().all():
            db_session.refresh(zimplan, with_for_update=True)
            db_session.delete(zimplan)

    resline = get_cache(Res_line, {"_recid": [(eq, res_line._recid)]})

    if resline.resstatus == 13:
        orig_status = 11
    resline.zinr = ""
    resline.resstatus = orig_status
    resline.ankzeit = 0
    resline.active_flag = 0

    for resline in db_session.query(Resline).filter(
            (Resline.resnr == res_line.resnr) & (Resline.active_flag == 1) & (Resline.l_zuordnung[inc_value(2)] == 1) & (Resline.kontakt_nr == res_line.reslinnr)).order_by(Resline._recid).all():
        resline.zinr = ""
        resline.resstatus = 11
        resline.ankzeit = 0
        resline.active_flag = 0

    count_i = 0

    for buff_resline in db_session.query(Buff_resline).filter(
            (Buff_resline.resnr == res_number) & (Buff_resline.resstatus == 6)).order_by(Buff_resline._recid).all():
        count_i = count_i + 1

    if count_i == 0:

        # mbill = get_cache (Bill, {"resnr": [(eq, res_number)],"reslinnr": [(eq, 0)],"saldo": [(eq, 0)],"zinr": [(eq, "")],"flag": [(eq, 0)]})
        mbill = db_session.query(Bill).filter((Bill.resnr == res_number) & (Bill.reslinnr == 0) & (
            Bill.saldo == 0) & (Bill.zinr == "") & (Bill.flag == 0)).with_for_update().first()

        if mbill:
            db_session.refresh(mbill, with_for_update=True)
            mbill.flag = 1
            fl_error = 3
            billnumber = billnumber + ";" + to_string(mbill.rechnr)

            db_session.flush()

    htparam = get_cache(Htparam, {"paramnr": [(eq, 341)]})

    if htparam.fchar != "":
        get_output(intevent_1(2, room_nr, "My Checkout!", res_line.resnr, res_line.reslinnr))

    if priscilla_active:
        get_output(intevent_1(9, room_nr, "Priscilla", res_line.resnr, res_line.reslinnr))

    htparam = get_cache(Htparam, {"paramnr": [(eq, 359)]})

    if htparam.flogical:
        # Rulita 150825 | Modify cancelCI roomnr
        get_output(intevent_1(1, room_nr, "CancelCI", res_line.resnr, res_line.reslinnr))

    return generate_output()
