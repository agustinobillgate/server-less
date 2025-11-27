# using conversion tools version: 1.0.0.119
"""_yusufwijasena_03/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix var declaration
                    - fix python indentation
                    - add import from function_py
                    - changed string to str
                    - fix string.lower() 
"""

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.htpdate import htpdate
from functions.htpdate import htpdate
from models import Res_line, Queasy, Htparam, Reservation, Bill, Bill_line, Zimkateg, Guest, Kontline


def reservation_webbl(case_type: int, gastno: int, resno: int):

    prepare_cache([Queasy, Htparam, Reservation, Bill, Bill_line, Zimkateg, Guest, Kontline])

    mainres_list_data = []
    res_list_data = []
    ci_date: date = None
    i: int = 0
    str = ""
    res_bemerk = ""
    loopk: int = 0
    art_security: int = 0
    main_security = to_decimal("0.0")
    res_security = to_decimal("0.0")
    res_line = queasy = htparam = reservation = bill = bill_line = zimkateg = guest = kontline = None

    mainres_list = res_list = bresline = bqueasy = None

    mainres_list_data, Mainres_list = create_model(
        "Mainres_list",
        {
            "resnr": int,
            "zimanz": int,
            "ankunft": date,
            "abreise": date,
            "segm": int,
            "deposit": Decimal,
            "until": date,
            "paid": Decimal,
            "id1": str,
            "id2": str,
            "id2_date": date,
            "groupname": str,
            "grpflag": bool,
            "bemerk": str,
            "voucher": str,
            "vesrdepot2": str,
            "arrival": bool,
            "resident": bool,
            "arr_today": bool,
            "last_reslinnr": int,
            "avail_pay": bool,
            "deposit_security": bool
        },
        {
            "ankunft": date_mdy(1,1,2099),
            "abreise": date_mdy(1,1,1998)
        })
    res_list_data, Res_list = create_model(
        "Res_list",
        {
            "name": str,
            "abreise": date,
            "zinr": str,
            "kurzbez": str,
            "zipreis": Decimal,
            "arrangement": str,
            "erwachs": int,
            "gratis": int,
            "kind1": int,
            "kind2": int,
            "ankunft": date,
            "resstatus": int,
            "kontakt_nr": int,
            "zimmeranz": int,
            "anztage": int,
            "changed_id": str,
            "changed": date,
            "ratecode": str,
            "bemerk": str,
            "l_zuord3": int,
            "resnr": int,
            "reslinnr": int,
            "gastnrmember": int,
            "betrieb_gast": int,
            "zikatnr": int,
            "reserve_int": int,
            "kontignr": int,
            "karteityp": int,
            "allot_flag": int,
            "kontcode": str,
            "avail_pay": bool,
            "deposit_security": bool
        })

    Bresline = create_buffer("Bresline", Res_line)
    Bqueasy = create_buffer("Bqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_list_data, res_list_data, ci_date, i, str, res_bemerk, loopk, art_security, main_security, res_security, res_line, queasy, htparam, reservation, bill, bill_line, zimkateg, guest, kontline
        nonlocal case_type, gastno, resno
        nonlocal bresline, bqueasy
        nonlocal mainres_list, res_list, bresline, bqueasy
        nonlocal mainres_list_data, res_list_data

        return {
            "mainres-list": mainres_list_data,
            "res-list": res_list_data
        }

    def update_mainres():
        nonlocal mainres_list_data, res_list_data, ci_date, i, str, res_bemerk, loopk, art_security, main_security, res_security, res_line, queasy, htparam, reservation, bill, bill_line, zimkateg, guest, kontline
        nonlocal case_type, gastno, resno
        nonlocal bresline, bqueasy
        nonlocal mainres_list, res_list, bresline, bqueasy
        nonlocal mainres_list_data, res_list_data

        mainres_list.ankunft = date_mdy(1, 1, 2099)
        mainres_list.abreise = date_mdy(1, 1, 1998)
        mainres_list.zimanz = 0
        mainres_list.arrival = False
        mainres_list.arr_today = False
        mainres_list.resident = False

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == mainres_list.resnr) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line._recid).all():

            if res_line.resstatus <= 6:
                mainres_list.zimanz = mainres_list.zimanz + res_line.zimmeranz

            if mainres_list.ankunft > res_line.ankunft:
                mainres_list.ankunft = res_line.ankunft

            if mainres_list.abreise < res_line.abreise:
                mainres_list.abreise = res_line.abreise

            if res_line.resstatus <= 5 or res_line.resstatus == 11:
                mainres_list.arrival = True

            if mainres_list.arrival and res_line.ankunft == ci_date:
                mainres_list.arr_today = True

            if res_line.resstatus == 6 or res_line.resstatus == 13:
                mainres_list.resident = True

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == mainres_list.resnr)).order_by(Res_line.reslinnr.desc()).all():
            mainres_list.last_reslinnr = res_line.reslinnr
            break

    def update_gcfinfo():
        nonlocal mainres_list_data, res_list_data, i, str, res_bemerk, loopk, art_security, main_security, res_security, res_line, queasy, htparam, reservation, bill, bill_line, zimkateg, guest, kontline
        nonlocal case_type, gastno, resno
        nonlocal bresline, bqueasy
        nonlocal mainres_list, res_list, bresline, bqueasy
        nonlocal mainres_list_data, res_list_data

        ci_date: date = None
        ci_date = get_output(htpdate(87))

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) & (Res_line.gastnr == gastno) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line._recid).all():

            # guest = get_cache(Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            guest = db_session.query(Guest).filter(Guest.gastnr == res_line.gastnrmember).with_for_update().first()

            if guest.erste_res == None:
                guest.erste_res = ci_date

            if guest.naechste_res == None or guest.naechste_res < res_line.ankunft:
                guest.naechste_res = res_line.ankunft
            guest.letzte_res = ci_date
            pass

    ci_date = get_output(htpdate(87))

    htparam = get_cache(
        Htparam, {"paramnr": [(eq, 1053)]})

    if htparam:
        art_security = htparam.finteger

    if case_type == 1:

        if resno == 0:

            reservation_obj_list = {}
            for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line, (Res_line.resnr == Reservation.resnr) & (Res_line.active_flag <= 1)).filter(
                    (Reservation.gastnr == gastno) & (Reservation.activeflag == 0)).order_by(Reservation.resnr).all():
                if reservation_obj_list.get(reservation._recid):
                    continue
                else:
                    reservation_obj_list[reservation._recid] = True

                mainres_list = Mainres_list()
                mainres_list_data.append(mainres_list)

                mainres_list.resnr = reservation.resnr
                mainres_list.deposit = to_decimal(reservation.depositgef)
                mainres_list.until = reservation.limitdate
                mainres_list.paid = to_decimal(reservation.depositbez + reservation.depositbez2)
                mainres_list.segm = reservation.segmentcode
                mainres_list.groupname = reservation.groupname
                mainres_list.bemerk = reservation.bemerk
                mainres_list.id1 = reservation.useridanlage
                mainres_list.id2 = reservation.useridmutat
                mainres_list.id2_date = reservation.mutdat
                mainres_list.grpflag = reservation.grpflag
                mainres_list.voucher = reservation.vesrdepot

                update_mainres()

                queasy = get_cache(
                    Queasy, {"key": [(eq, 329)], "number1": [(eq, res_line.resnr)]})

                if queasy:
                    if queasy.logi2:
                        mainres_list.avail_pay = True

                    bqueasy = get_cache(
                        Queasy, {"key": [(eq, 349)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

                    if bqueasy:
                        bill = get_cache(
                            Bill, {"resnr": [(eq, bqueasy.number1)], "billnr": [(eq, 4)]})

                        if bill:
                            for bill_line in db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == bill.rechnr) & (Bill_line.artnr == art_security)).order_by(Bill_line._recid).all():
                                main_security = to_decimal(
                                    main_security + bill_line.betrag)

                            if main_security != 0:
                                mainres_list.deposit_security = True

                        elif bqueasy.deci1 != 0:
                            mainres_list.deposit_security = True

        else:

            reservation = get_cache(
                Reservation, {"gastnr": [(eq, gastno)], "resnr": [(eq, resno)], "activeflag": [(eq, 0)]})

            if reservation:
                mainres_list = Mainres_list()
                mainres_list_data.append(mainres_list)

                mainres_list.resnr = reservation.resnr
                mainres_list.deposit = to_decimal(reservation.depositgef)
                mainres_list.until = reservation.limitdate
                mainres_list.paid = to_decimal(reservation.depositbez + reservation.depositbez2)
                mainres_list.segm = reservation.segmentcode
                mainres_list.groupname = reservation.groupname
                mainres_list.bemerk = reservation.bemerk
                mainres_list.id1 = reservation.useridanlage
                mainres_list.id2 = reservation.useridmutat
                mainres_list.id2_date = reservation.mutdat
                mainres_list.grpflag = reservation.grpflag
                mainres_list.voucher = reservation.vesrdepot

                update_mainres()

                queasy = get_cache(
                    Queasy, {"key": [(eq, 329)], "number1": [(eq, reservation.resnr)]})

                if queasy:
                    if queasy.logi2:
                        mainres_list.avail_pay = True

                    bqueasy = get_cache(
                        Queasy, {"key": [(eq, 349)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

                    if bqueasy:
                        bill = get_cache(
                            Bill, {"resnr": [(eq, bqueasy.number1)], "billnr": [(eq, 4)]})

                        if bill:
                            for bill_line in db_session.query(Bill_line).filter(
                                    (Bill_line.rechnr == bill.rechnr) & (Bill_line.artnr == art_security)).order_by(Bill_line._recid).all():
                                main_security = to_decimal(main_security + bill_line.betrag)

                            if main_security != 0:
                                mainres_list.deposit_security = True

                        elif bqueasy.deci1 != 0:
                            mainres_list.deposit_security = True

    elif case_type == 2:
        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resno) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line._recid).all():

            zimkateg = get_cache(
                Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            guest = get_cache(
                Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            res_list = Res_list()
            res_list_data.append(res_list)

            buffer_copy(res_line, res_list)
            res_list.bemerk = replace_str(res_list.bemerk, chr_unicode(10), "")
            res_list.bemerk = replace_str(res_list.bemerk, chr_unicode(13), "")
            res_list.bemerk = replace_str(res_list.bemerk, "~n", "")
            res_list.bemerk = replace_str(res_list.bemerk, "\\n", "")
            res_list.bemerk = replace_str(res_list.bemerk, "~r", "")
            res_list.bemerk = replace_str(res_list.bemerk, "~r~n", "")
            res_list.bemerk = replace_str(res_list.bemerk, chr_unicode(10) + chr_unicode(13), "")
            res_bemerk = ""
            for loopk in range(1, length(res_list.bemerk) + 1):
                if asc(substring(res_list.bemerk, loopk - 1, 1)) == 0:
                    pass
                else:
                    res_bemerk = res_bemerk + substring(res_list.bemerk, loopk - 1, 1)
            res_list.bemerk = res_bemerk

            if length(res_list.bemerk) < 3:
                res_list.bemerk = replace_str(
                    res_list.bemerk, chr_unicode(32), "")

            if length(res_list.bemerk) == None:
                res_list.bemerk = ""
            for i in range(1, num_entries(res_line.zimmer_wunsch, ";")):
                str = entry(i - 1, res_line.zimmer_wunsch, ";")

                if substring(str, 0, 6) == "$code$":
                    res_list.ratecode = substring(str, 6)
            res_list.karteityp = guest.karteityp
            res_list.l_zuord3 = res_line.l_zuordnung[2]
            res_list.kurzbez = zimkateg.kurzbez

            queasy = get_cache(
                Queasy, {"key": [(eq, 329)], "number1": [(eq, res_line.resnr)]})

            if queasy:
                if queasy.logi2:
                    res_list.avail_pay = True

                bqueasy = get_cache(
                    Queasy, {"key": [(eq, 349)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

                if bqueasy:
                    bill = get_cache(
                        Bill, {"resnr": [(eq, bqueasy.number1)], "billnr": [(eq, 4)]})

                    if bill:
                        res_security = to_decimal("0")

                        for bill_line in db_session.query(Bill_line).filter(
                                (Bill_line.rechnr == bill.rechnr) & (Bill_line.artnr == art_security)).order_by(Bill_line._recid).all():
                            res_security = to_decimal(
                                res_security) + to_decimal(bill_line.betrag)

                        if res_security != 0:
                            res_list.deposit_security = True

                    elif bqueasy.deci1 != 0:
                        res_list.deposit_security = True

            kontline = get_cache(
                Kontline, {"kontignr": [(eq, res_line.kontignr)], "betriebsnr": [(eq, 0)], "kontstatus": [(eq, 1)]})

            if kontline:
                res_list.allot_flag = 1
                res_list.kontcode = kontline.kontcode

            else:
                kontline = get_cache(
                    Kontline, {"kontignr": [(eq, - res_line.kontignr)], "betriebsnr": [(eq, 1)], "kontstatus": [(eq, 1)]})

                if kontline:
                    res_list.allot_flag = -1
                    res_list.kontcode = kontline.kontcode

    elif case_type == 3:
        update_gcfinfo()

    return generate_output()
