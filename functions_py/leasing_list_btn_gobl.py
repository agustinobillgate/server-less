# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - convert only
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Bediener, Res_line, Guest


def leasing_list_btn_gobl(fdate: date, tdate: date, sorttype: int, gname: str):

    prepare_cache([Queasy, Htparam, Bediener, Res_line, Guest])

    leasing_list_data = []
    ar_ledger: int = 0
    tot_amount: Decimal = to_decimal("0.0")
    queasy = htparam = bediener = res_line = guest = None

    leasing_list = bqueasy = None

    leasing_list_data, Leasing_list = create_model(
        "Leasing_list",
        {
            "createcontract": date,
            "gastnr": int,
            "gastnrpay": int,
            "guestname": str,
            "billrcv": str,
            "amount": Decimal,
            "ankunft": date,
            "abreise": date,
            "recid_queasy": int,
            "pinvoice": str,
            "printed": str,
            "cancel": bool,
            "nr": int,
            "resnr": int,
            "reslinnr": int,
            "proforma_user": str,
            "payment": bool,
            "full_payment": bool,
            "pay_amount": Decimal,
            "rstatus": str,
            "rmrate_chg": Decimal,
            "extend": bool
        })

    Bqueasy = create_buffer("Bqueasy", Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal leasing_list_data, ar_ledger, tot_amount, queasy, htparam, bediener, res_line, guest
        nonlocal fdate, tdate, sorttype, gname
        nonlocal bqueasy
        nonlocal leasing_list, bqueasy
        nonlocal leasing_list_data

        return {
            "leasing-list": leasing_list_data
        }

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1051)]})

    if htparam:
        ar_ledger = htparam.finteger

    if sorttype == 1:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 329) & (Queasy.date2 >= fdate) & (Queasy.date2 <= tdate) & (Queasy.deci1 != 0)).order_by(Queasy.date2).all():
            leasing_list = Leasing_list()
            leasing_list_data.append(leasing_list)

            leasing_list.createcontract = queasy.date1
            leasing_list.ankunft = queasy.date2
            leasing_list.abreise = queasy.date3
            leasing_list.amount = to_decimal(round(queasy.deci1, 0))
            leasing_list.recid_queasy = queasy._recid
            leasing_list.pinvoice = queasy.char2
            leasing_list.cancel = queasy.logi1
            leasing_list.nr = queasy.number3
            leasing_list.payment = queasy.logi2
            leasing_list.pay_amount = to_decimal(queasy.deci2)
            leasing_list.extend = queasy.logi3
            tot_amount = to_decimal(tot_amount + round(queasy.deci1, 0))

            if queasy.deci1 == queasy.deci2:
                leasing_list.full_payment = True

            if queasy.char1 != "" and num_entries(queasy.char1, "|") > 1:
                leasing_list.printed = entry(0, queasy.char1, "|")

                bediener = get_cache(
                    Bediener, {"userinit": [(eq, entry(3, queasy.char1, "|"))]})

                if bediener:
                    leasing_list.proforma_user = bediener.username

            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                leasing_list.gastnr = res_line.gastnrmember
                leasing_list.gastnrpay = res_line.gastnr
                leasing_list.resnr = res_line.resnr
                leasing_list.reslinnr = res_line.reslinnr

                guest = get_cache(
                    Guest, {"gastnr": [(eq, leasing_list.gastnr)]})

                if guest:
                    leasing_list.guestname = guest.name + "," + guest.vorname1

                guest = get_cache(
                    Guest, {"gastnr": [(eq, leasing_list.gastnrpay)]})

                if guest:
                    leasing_list.billrcv = guest.name + "," + guest.vorname1

                if res_line.resstatus == 9 or res_line.resstatus == 99:
                    leasing_list.rstatus = "Cancel"

                elif res_line.resstatus == 6:
                    leasing_list.rstatus = "Arrived"

                elif res_line.resstatus == 8:
                    leasing_list.rstatus = "CheckOut"

                else:
                    leasing_list.rstatus = "Reservation"

            bqueasy = get_cache(
                Queasy, {"key": [(eq, 356)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

            if bqueasy:
                for bqueasy in db_session.query(Bqueasy).filter(
                        (Bqueasy.key == 356) & (Bqueasy.number1 == queasy.number1) & (Bqueasy.number2 == queasy.number2)).order_by(Bqueasy.date1.desc(), Bqueasy.number3.desc()).all():
                    leasing_list.rmrate_chg = to_decimal(bqueasy.deci1)

                    break

    elif sorttype == 2:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 329) & (Queasy.date3 >= fdate) & (Queasy.date3 <= tdate) & (Queasy.deci1 != 0)).order_by(Queasy.date3).all():
            leasing_list = Leasing_list()
            leasing_list_data.append(leasing_list)

            leasing_list.createcontract = queasy.date1
            leasing_list.ankunft = queasy.date2
            leasing_list.abreise = queasy.date3
            leasing_list.amount = to_decimal(round(queasy.deci1, 0))
            leasing_list.recid_queasy = queasy._recid
            leasing_list.pinvoice = queasy.char2
            leasing_list.cancel = queasy.logi1
            leasing_list.nr = queasy.number3
            leasing_list.payment = queasy.logi1
            leasing_list.pay_amount = to_decimal(queasy.deci2)
            leasing_list.extend = queasy.logi3
            tot_amount = to_decimal(tot_amount + round(queasy.deci1, 0))

            if queasy.deci1 == queasy.deci2:
                leasing_list.full_payment = True

            if queasy.char1 != "" and num_entries(queasy.char1, "|") > 1:
                leasing_list.printed = entry(0, queasy.char1, "|")

                bediener = get_cache(
                    Bediener, {"userinit": [(eq, entry(3, queasy.char1, "|"))]})

                if bediener:
                    leasing_list.proforma_user = bediener.username

            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                leasing_list.gastnr = res_line.gastnrmember
                leasing_list.gastnrpay = res_line.gastnr
                leasing_list.resnr = res_line.resnr
                leasing_list.reslinnr = res_line.reslinnr

                guest = get_cache(
                    Guest, {"gastnr": [(eq, leasing_list.gastnr)]})

                if guest:
                    leasing_list.guestname = guest.name + "," + guest.vorname1

                guest = get_cache(
                    Guest, {"gastnr": [(eq, leasing_list.gastnrpay)]})

                if guest:
                    leasing_list.billrcv = guest.name + "," + guest.vorname1

                if res_line.resstatus == 9 or res_line.resstatus == 99:
                    leasing_list.rstatus = "Cancel"

                elif res_line.resstatus == 6:
                    leasing_list.rstatus = "Arrived"

                elif res_line.resstatus == 8:
                    leasing_list.rstatus = "CheckOut"

                else:
                    leasing_list.rstatus = "Reservation"

            bqueasy = get_cache(
                Queasy, {"key": [(eq, 356)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

            if bqueasy:
                for bqueasy in db_session.query(Bqueasy).filter(
                        (Bqueasy.key == 356) & (Bqueasy.number1 == queasy.number1) & (Bqueasy.number2 == queasy.number2)).order_by(Bqueasy.date1.desc(), Bqueasy.number3.desc()).all():
                    leasing_list.rmrate_chg = to_decimal(bqueasy.deci1)

                    break

    elif sorttype == 3:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 329) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate) & (Queasy.deci1 != 0)).order_by(Queasy.date1).all():
            leasing_list = Leasing_list()
            leasing_list_data.append(leasing_list)

            leasing_list.createcontract = queasy.date1
            leasing_list.ankunft = queasy.date2
            leasing_list.abreise = queasy.date3
            leasing_list.amount = to_decimal(round(queasy.deci1, 0))
            leasing_list.recid_queasy = queasy._recid
            leasing_list.pinvoice = queasy.char2
            leasing_list.cancel = queasy.logi1
            leasing_list.nr = queasy.number3
            leasing_list.payment = queasy.logi1
            leasing_list.pay_amount = to_decimal(queasy.deci2)
            leasing_list.extend = queasy.logi3
            tot_amount = to_decimal(tot_amount + round(queasy.deci1, 0))

            if queasy.deci1 == queasy.deci2:
                leasing_list.full_payment = True

            if queasy.char1 != "" and num_entries(queasy.char1, "|") > 1:
                leasing_list.printed = entry(0, queasy.char1, "|")

                bediener = get_cache(
                    Bediener, {"userinit": [(eq, entry(3, queasy.char1, "|"))]})

                if bediener:
                    leasing_list.proforma_user = bediener.username

            res_line = get_cache(
                Res_line, {"resnr": [(eq, queasy.number1)], "reslinnr": [(eq, queasy.number2)]})

            if res_line:
                leasing_list.gastnr = res_line.gastnrmember
                leasing_list.gastnrpay = res_line.gastnr
                leasing_list.resnr = res_line.resnr
                leasing_list.reslinnr = res_line.reslinnr

                guest = get_cache(
                    Guest, {"gastnr": [(eq, leasing_list.gastnr)]})

                if guest:
                    leasing_list.guestname = guest.name + "," + guest.vorname1

                guest = get_cache(
                    Guest, {"gastnr": [(eq, leasing_list.gastnrpay)]})

                if guest:
                    leasing_list.billrcv = guest.name + "," + guest.vorname1

                if res_line.resstatus == 9 or res_line.resstatus == 99:
                    leasing_list.rstatus = "Cancel"

                elif res_line.resstatus == 6:
                    leasing_list.rstatus = "Arrived"

                elif res_line.resstatus == 8:
                    leasing_list.rstatus = "CheckOut"

                else:
                    leasing_list.rstatus = "Reservation"

            bqueasy = get_cache(
                Queasy, {"key": [(eq, 356)], "number1": [(eq, queasy.number1)], "number2": [(eq, queasy.number2)]})

            if bqueasy:
                for bqueasy in db_session.query(Bqueasy).filter(
                        (Bqueasy.key == 356) & (Bqueasy.number1 == queasy.number1) & (Bqueasy.number2 == queasy.number2)).order_by(Bqueasy.date1.desc(), Bqueasy.number3.desc()).all():
                    leasing_list.rmrate_chg = to_decimal(bqueasy.deci1)

                    break

    if gname != "":
        for leasing_list in query(leasing_list_data, filters=(lambda leasing_list: not matches(leasing_list.guestName, r"*" + gname + r"*"))):
            tot_amount = to_decimal(tot_amount - leasing_list.amount)

            leasing_list_data.remove(leasing_list)
    leasing_list = Leasing_list()
    leasing_list_data.append(leasing_list)

    leasing_list.guestname = "TOTAL"
    leasing_list.amount = to_decimal(tot_amount)

    return generate_output()
