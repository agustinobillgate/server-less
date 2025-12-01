# using conversion tools version: 1.0.0.117
# -----------------------------------------
# Rd 21/7/2025
# Ticket #716
# validasi sanitize_bill_line, validasi anzhal , int + str

# yusufwijasena, 13/11/2025 (F6D79E)
# - last update from ITA: Program terkait feature service apartement
# - fix python indentation
# - fix run inv-ar.p to call function from i_inv_ar
# -----------------------------------------
# ============================
# Rd, 24/11/2025, update last_count for counter update
# ============================
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.i_inv_ar import *
from models import Res_line, Queasy, Bill, Artikel, Counters, Htparam, Bill_line, Umsatz, Billjournal, Master, Mast_art
from functions.next_counter_for_update import next_counter_for_update


s_list_data, S_list = create_model(
    "S_list",
    {
        "zeit": int,
        "dept": int,
        "artnr": int,
        "bezeich": string,
        "zinr": string,
        "anzahl": int,
        "preis": Decimal,
        "betrag": Decimal,
        "l_betrag": Decimal,
        "f_betrag": Decimal,
        "resnr": int,
        "reslinnr": int
    })


def sanitize_bill_line(b):
    if isinstance(b.zeit, str) and b.zeit.strip() == "":
        b.zeit = None
    if isinstance(b.arrangement, str) and b.arrangement.strip() == "":
        b.arrangement = None
    if isinstance(b.origin_id, str) and b.origin_id.strip() == "":
        b.origin_id = None
    return b


def quick_post_create_billbl(s_list_data: list[S_list], pvilanguage: int, billart: int, curr_dept: int, amount: Decimal, 
                             double_currency: bool, foreign_rate: bool, user_init: string, voucher_nr: string):

    prepare_cache([Res_line, Bill, Artikel, Counters, Htparam, Bill_line, Umsatz, Billjournal, Master])

    msg_str = ""
    msg_str2 = ""
    lvcarea: string = "quick-post"
    res_line = queasy = bill = artikel = counters = htparam = bill_line = umsatz = billjournal = master = mast_art = None

    s_list = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock = ""


    def generate_output():
        nonlocal msg_str, msg_str2, lvcarea, res_line, queasy, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal pvilanguage, billart, curr_dept, amount, double_currency, foreign_rate, user_init, voucher_nr
        nonlocal s_list

        return {
            "s-list": s_list_data,
            "msg_str": msg_str,
            "msg_str2": msg_str2
        }

    def create_bill():
        nonlocal msg_str, msg_str2, lvcarea, res_line, queasy, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal pvilanguage, billart, curr_dept, amount, double_currency, foreign_rate, user_init, voucher_nr
        nonlocal s_list

        for s_list in query(s_list_data):
            res_line = get_cache(
                Res_line, {"resnr": [(eq, s_list.resnr)], "reslinnr": [(eq, s_list.reslinnr)]})

            if res_line:
                # ITA: Program terkait feature service apartement
                queasy = get_cache(
                    Queasy, {"key": [(eq, 329)], "number1": [(eq, res_line.resnr)]})

                if queasy:

                    bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &
                        (Bill.reslinnr == res_line.reslinnr) &
                        (Bill.zinr == res_line.zinr) &
                        (Bill.billnr == 2)).first()

                    if bill:
                        if bill.flag == 1:
                            msg_str = msg_str + chr_unicode(2) + "&W" + \
                                translateExtended("Bill Number", lvcarea, "") + " " + to_string(bill.rechnr) + " " + translateExtended("RmNo", lvcarea, "") + " " + s_list.zinr + \
                                " : " + translateExtended("Status closed, Posting not possible.", lvcarea, "")
                        else:

                            if res_line.l_zuordnung[1] != 1:
                                check_mbill(s_list.dept, s_list.artnr)
                            update_bill()
                else:
                    bill = get_cache(
                        Bill, {"resnr": [(eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "zinr": [(eq, res_line.zinr)]})

                    if bill:
                        if bill.flag == 1:
                            msg_str = msg_str + chr_unicode(2) + "&W" + \
                                translateExtended("Bill Number", lvcarea, "") + " " + to_string(bill.rechnr) + " " + translateExtended("RmNo", lvcarea, "") + " " + s_list.zinr + \
                                " : " + translateExtended("Status closed, Posting not possible.", lvcarea, "")
                        else:

                            if res_line.l_zuordnung[1] != 1:
                                check_mbill(s_list.dept, s_list.artnr)
                            update_bill()
                # end ITA: Program terkait feature service apartement
            s_list_data.remove(s_list)


    def update_bill():

        nonlocal msg_str, msg_str2, lvcarea, res_line, queasy, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal pvilanguage, billart, curr_dept, amount, double_currency, foreign_rate, user_init, voucher_nr


        nonlocal s_list

        bil_flag:int = 0
        master_flag:bool = False
        bill_date:date = None
        na_running:bool = False

        db_session.refresh(bill, with_for_update=True)

        artikel = get_cache(
            Artikel, {"artnr": [(eq, billart)], "departement": [(eq, curr_dept)]})

        if artikel:
            if artikel.umsatzart == 1:
                bill.logisumsatz = to_decimal(
                    bill.logisumsatz) + to_decimal(amount)

            elif artikel.umsatzart == 2:
                bill.argtumsatz = to_decimal(
                    bill.argtumsatz) + to_decimal(amount)

            elif (artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6):
                bill.f_b_umsatz = to_decimal(
                    bill.f_b_umsatz) + to_decimal(amount)

            elif artikel.umsatzart == 4:
                bill.sonst_umsatz = to_decimal(
                    bill.sonst_umsatz) + to_decimal(amount)

            if artikel.umsatzart >= 1 and artikel.umsatzart <= 4:
                bill.gesamtumsatz = to_decimal(
                    bill.gesamtumsatz) + to_decimal(amount)
        bill.rgdruck = 0
        bill.saldo = to_decimal(bill.saldo) + to_decimal(s_list.l_betrag)

        if double_currency or foreign_rate:
            bill.mwst[98] = bill.mwst[98] + s_list.f_betrag

        if bill.rechnr == 0:
            # counters = get_cache(Counters, {"counter_no": [(eq, 3)]})
            # counters.counter = counters.counter + 1
            # bill.rechnr = counters.counter
            last_count, error_lock = get_output(next_counter_for_update(3))
            bill.rechnr = last_count
            

        htparam = get_cache(Htparam, {"paramnr": [(eq, 253)]})

        if htparam:
            na_running = htparam.flogical

        htparam = get_cache(Htparam, {"paramnr": [(eq, 110)]})

        if htparam:
            bill_date = htparam.fdate

            if na_running and bill_date == htparam.fdate:
                bill_date = bill_date + timedelta(days=1)

        if bill.datum < bill_date or bill.datum is None:
            bill.datum = bill_date
        bill_line = Bill_line()

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = s_list.artnr
        bill_line.bezeich = s_list.bezeich
        bill_line.anzahl = s_list.anzahl
        bill_line.betrag = to_decimal(s_list.l_betrag)
        bill_line.fremdwbetrag = to_decimal(s_list.f_betrag)
        bill_line.zinr = s_list.zinr
        bill_line.departement = s_list.dept
        bill_line.epreis = to_decimal(s_list.preis)
        bill_line.zeit = s_list.zeit
        bill_line.userinit = user_init
        bill_line.bill_datum = bill_date

        # Rd 221/7/2025
        # validasi isi data sblm insert
        sanitize_bill_line(bill_line)
        db_session.add(bill_line)

        # Rd 21/7/2025
        # possible int err
        dept = s_list.dept
        if isinstance(dept, str) and dept.strip() == "":
            dept = None
        else:
            try:
                dept = int(dept)
            except ValueError:
                dept = None
        # umsatz = get_cache (Umsatz, {"artnr": [(eq, s_list.artnr)],"departement": [(eq, s_list.dept)],"datum": [(eq, bill_date)]})
        umsatz = db_session.query(Umsatz).filter(
            (Umsatz.artnr == s_list.artnr) & 
            (Umsatz.departement == s_list.dept) & 
            (Umsatz.datum == bill_date)).with_for_update().first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = s_list.artnr
            umsatz.datum = bill_date
            umsatz.departement = s_list.dept
        umsatz.betrag = to_decimal(umsatz.betrag) + to_decimal(s_list.l_betrag)
        # Rd 21/7/2025
        # validasi err int + str
        # umsatz.anzahl = umsatz.anzahl + s_list.anzahl
        try:
            umsatz.anzahl += int(s_list.anzahl)
        except (ValueError, TypeError):
            umsatz.anzahl += 0
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = s_list.artnr
        billjournal.anzahl = s_list.anzahl
        billjournal.fremdwaehrng = to_decimal(s_list.f_betrag)
        billjournal.betrag = to_decimal(s_list.l_betrag)
        billjournal.bezeich = s_list.bezeich
        billjournal.zinr = s_list.zinr
        billjournal.departement = s_list.dept
        billjournal.epreis = to_decimal(s_list.preis)
        billjournal.zeit = s_list.zeit
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_date


        if artikel.artart == 2 or artikel.artart == 7:
            # inv_ar(artikel.artnr, res_line.zinr, bill.gastnr, res_line.gastnrmember, bill.rechnr, s_list.betrag, s_list.f_betrag, bill_date, bill.name, user_init, voucher_nr)
            i_inv_ar(artikel.artnr, res_line.zinr, bill.gastnr, res_line.gastnrmember, bill.rechnr, s_list.betrag, s_list.f_betrag, bill_date, bill.name, user_init, voucher_nr)

    def check_mbill(slist_dept: int, slist_artnr: int):
        nonlocal msg_str, msg_str2, lvcarea, res_line, bill, artikel, counters, htparam, bill_line, umsatz, billjournal, master, mast_art
        nonlocal pvilanguage, billart, curr_dept, amount, double_currency, foreign_rate, user_init, voucher_nr
        nonlocal s_list

        master_flag: bool = False
        resline = None
        Resline = create_buffer("Resline", Res_line)

        artikel = get_cache(
            Artikel, {"departement": [(eq, slist_dept)], "artnr": [(eq, slist_artnr)]})

        master = get_cache(
            Master, {"resnr": [(eq, bill.resnr)], "active": [(eq, True)], "flag": [(eq, 0)]})

        if master:
            if (master.umsatzart[0] and artikel.artart == 8) or (master.umsatzart[1] and artikel.artart == 9 and artikel.artgrp == 0) or (master.umsatzart[2] and artikel.umsatzart == 3) or (master.umsatzart[3] and artikel.umsatzart == 4):
                master_flag = True

            if not master_flag:
                mast_art = get_cache(
                    Mast_art, {"resnr": [(eq, master.resnr)], "departement": [(eq, artikel.departement)], "artnr": [(eq, artikel.artnr)]})

                if mast_art:
                    master_flag = True

        if master_flag:
            bill = get_cache(
                Bill, {"resnr": [(eq, res_line.resnr)], "reslinnr": [(eq, 0)]})
            msg_str2 = translateExtended("RmNo", lvcarea, "") + " " + res_line.zinr + " " + \
                translateExtended("transfered to Master Bill No.", lvcarea, "") + \
                " " + to_string(bill.rechnr)

            return

        if res_line.memozinr != "" and res_line.memozinr != res_line.zinr:
            resline = get_cache(
                Res_line, {"zinr": [(eq, res_line.memozinr)], "resstatus": [(eq, 6)]})

            if resline:
                bill = get_cache(
                    Bill, {"resnr": [(eq, resline.resnr)], "reslinnr": [(eq, resline.reslinnr)]})
            msg_str2 = translateExtended("RmNo", lvcarea, "") + " " + res_line.zinr + " " + \
                translateExtended("transfered to Bill No.", lvcarea, "") + \
                " " + to_string(bill.rechnr)

    create_bill()

    return generate_output()
