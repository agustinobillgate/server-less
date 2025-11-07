# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - convert only
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Bediener, Res_line, Guest


def leasing_list_proforma_invoice_printedbl(fdate: date, tdate: date, sorttype: int, gname: string, proforma: bool, actual: bool):

    prepare_cache([Queasy, Bediener, Res_line, Guest])

    leasing_list_data = []
    doit: bool = False
    queasy = bediener = res_line = guest = None

    leasing_list = None

    leasing_list_data, Leasing_list = create_model(
        "Leasing_list",
        {
            "createcontract": date,
            "gastnr": int,
            "gastnrpay": int,
            "guestname": string,
            "billrcv": string,
            "amount": Decimal,
            "ankunft": date,
            "abreise": date,
            "recid_queasy": int,
            "pinvoice": string,
            "printed": string,
            "cancel": bool,
            "nr": int,
            "resnr": int,
            "proforma_user": string
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal leasing_list_data, doit, queasy, bediener, res_line, guest
        nonlocal fdate, tdate, sorttype, gname, proforma, actual
        nonlocal leasing_list
        nonlocal leasing_list_data

        return {
            "leasing-list": leasing_list_data
        }

    if sorttype == 1:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 329) & (Queasy.date2 >= fdate) & (Queasy.date2 <= tdate)).order_by(Queasy.date2).all():
            doit = True

            if proforma and ((queasy.char1 == "" and queasy.char2 == "") or (queasy.char1 != "" and queasy.char2 != "")):
                doit = False

            if doit and actual and queasy.char1 != "" and queasy.char2 == "":
                doit = False

            if doit:
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

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, leasing_list.gastnr)]})

                    if guest:
                        leasing_list.guestname = guest.name + "," + guest.vorname1

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, leasing_list.gastnrpay)]})

                    if guest:
                        leasing_list.billrcv = guest.name + "," + guest.vorname1

    elif sorttype == 2:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 329) & (Queasy.date3 >= fdate) & (Queasy.date3 <= tdate)).order_by(Queasy.date3).all():
            doit = True

            if proforma and ((queasy.char1 == "" and queasy.char2 == "") or (queasy.char1 != "" and queasy.char2 != "")):
                doit = False

            if doit and actual and queasy.char1 != "" and queasy.char2 == "":
                doit = False

            if doit:
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

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, leasing_list.gastnr)]})

                    if guest:
                        leasing_list.guestname = guest.name + "," + guest.vorname1

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, leasing_list.gastnrpay)]})

                    if guest:
                        leasing_list.billrcv = guest.name + "," + guest.vorname1

    elif sorttype == 3:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 329) & (Queasy.date1 >= fdate) & (Queasy.date1 <= tdate)).order_by(Queasy.date1).all():
            doit = True

            if proforma and ((queasy.char1 == "" and queasy.char2 == "") or (queasy.char1 != "" and queasy.char2 != "")):
                doit = False

            if doit and actual and queasy.char1 != "" and queasy.char2 == "":
                doit = False

            if doit:
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

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, leasing_list.gastnr)]})

                    if guest:
                        leasing_list.guestname = guest.name + "," + guest.vorname1

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, leasing_list.gastnrpay)]})

                    if guest:
                        leasing_list.billrcv = guest.name + "," + guest.vorname1

    if gname != "":
        for leasing_list in query(leasing_list_data, filters=(lambda leasing_list: not matches(leasing_list.guestName, r"*" + gname + r"*"))):
            leasing_list_data.remove(leasing_list)

    return generate_output()
