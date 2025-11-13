# using conversion tools version: 1.0.0.117
"""_yusufwijasena_30/10/2025
    updated_07/11/2025

    Ticket ID: BA6AB0
        _remark_:   - fix var declaratiom
                    - fix python indentation
                    - fix long string spacing
                    - import from function_py
    Ticket ID: F6D79E
        _remark_:   - update ITA: 1812DE [BUGS], ITA: DD5979 [BUGS]
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.htpchar import htpchar
from functions_py.htpchar import htpchar
import re
from models import Waehrung, Guest, Billjournal, Artikel, Hoteldpt, Bill, H_bill, Bk_veran, Reservation


def fo_usrjournal_cld_1bl(mi_incl: bool, mi_excl: bool, mi_tran: bool, from_date: date, to_date: date, from_dept: int, to_dept: int, from_art: int, to_art: int, usr_init: str, long_digit: bool, foreign_flag: bool, sort_type: int):

    prepare_cache([Waehrung, Guest, Billjournal, Artikel, Hoteldpt, Bill, H_bill, Bk_veran, Reservation])

    output_list_data = []
    def_rate = ""
    x_rate = to_decimal("0.0")
    waehrung = guest = billjournal = artikel = hoteldpt = bill = h_bill = bk_veran = reservation = None

    output_list = None

    output_list_data, Output_list = create_model(
        "Output_list",
        {
            "str": str,
            "gname": str
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        return {
            "output-list": output_list_data
        }

    def journal_list1():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():
                artikel = get_cache(
                    Artikel, {"artnr": [(eq, billjournal.artnr)], "departement": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:
                    hoteldpt = get_cache(
                        Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)
                output_list = Output_list()

                output_list_data.append(output_list)
                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:

                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot =  to_decimal(sub_tot) + to_decimal(amount)
                tot =  to_decimal(tot) + to_decimal(amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list2():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():
                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:
                    hoteldpt = get_cache(
                        Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)
                output_list = Output_list()

                output_list_data.append(output_list)
                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()

        output_list_data.append(output_list)
        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list3():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:
                    hoteldpt = get_cache(
                        Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)
                output_list = Output_list()

                output_list_data.append(output_list)
                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {
                                "rechnr": [(eq, billjournal.rechnr)],
                                "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:

                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list11():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_date: date = None
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.bill_datum, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_date != None and last_date != billjournal.bill_datum:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_date = billjournal.bill_datum
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()

                output_list_data.append(output_list)
                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()

        output_list_data.append(output_list)
        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list21():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_date: date = None
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_date != None and last_date != billjournal.bill_datum:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_date = billjournal.bill_datum
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {
                                "rechnr": [(eq, billjournal.rechnr)],
                                "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:

                            bk_veran = get_cache (
                                Bk_veran, {"veran_nr": [(eq, to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5  - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list31():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_date: date = None
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_date != None and last_date != billjournal.bill_datum:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_date = billjournal.bill_datum
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()

                output_list_data.append(output_list)
                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {
                                "rechnr": [(eq, billjournal.rechnr)],
                                "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list12():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_room = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.zinr, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_room != billjournal.zinr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_room = billjournal.zinr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)
                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {
                                "rechnr": [(eq, billjournal.rechnr)],
                                "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)

        output_list = Output_list()
        output_list_data.append(output_list)
        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list22():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_room = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.zinr, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {"artnr": [(eq, billjournal.artnr)], "departement": [
                                    (eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_room != billjournal.zinr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_room = billjournal.zinr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)
                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {
                                "rechnr": [(eq, billjournal.rechnr)],
                                "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)

        output_list = Output_list()
        output_list_data.append(output_list)
        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list32():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_room = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.zinr, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_room != billjournal.zinr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_room = billjournal.zinr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:

                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list13():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_billno: int = 0
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.rechnr, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_billno != billjournal.rechnr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_billno = billjournal.rechnr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list23():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_billno: int = 0
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.zinr, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_billno != billjournal.rechnr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_billno = billjournal.rechnr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list33():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        last_billno: int = 0
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.rechnr, Billjournal.artnr, Billjournal.zeit).all():
                artikel = get_cache(Artikel, {"artnr": [(eq, billjournal.artnr)], "departement": [
                                    (eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_billno != billjournal.rechnr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_billno = billjournal.rechnr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(60)") + to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit,
                                                                                                                    "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list14():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = 0
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {"artnr": [(eq, billjournal.artnr)], "departement": [
                                    (eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_artnr != 0 and last_artnr != billjournal.artnr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_artnr = billjournal.artnr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list24():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = 0
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.artnr, Billjournal.zeit).all():
                artikel = get_cache(Artikel, {"artnr": [(eq, billjournal.artnr)], "departement": [
                                    (eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_artnr != 0 and last_artnr != billjournal.artnr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_artnr = billjournal.artnr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {
                                "rechnr": [(eq, billjournal.rechnr)],
                                "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list34():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = 0
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_artnr != 0 and last_artnr != billjournal.artnr:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_artnr = billjournal.artnr
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(
                                H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list15():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.bezeich, Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():
                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:
                    hoteldpt = get_cache(
                        Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)
                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(
                                H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list25():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.bezeich, Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:
                    hoteldpt = get_cache(
                        Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)
                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {
                                "rechnr": [(eq, billjournal.rechnr)],
                                "departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list35():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.bezeich, Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:

                    hoteldpt = get_cache(
                        Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)
                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list16():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache(Artikel, {"artnr": [(eq, billjournal.artnr)], "departement": [
                                    (eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_dept >= 0 and last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_dept = billjournal.departement
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list26():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():
                artikel = get_cache(Artikel, {
                    "artnr": [(eq, billjournal.artnr)],
                    "departement": [(eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_dept >= 0 and last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + to_string("T O T A L  ", "x(22)") + to_string(
                            a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_dept = billjournal.departement
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list36():
        nonlocal output_list_data, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag, sort_type
        nonlocal output_list
        nonlocal output_list_data

        qty: int = 0
        sub_tot: Decimal = to_decimal("0.0")
        tot: Decimal = to_decimal("0.0")
        curr_date: date = None
        last_dept: int = -1
        last_artnr: int = -1
        a_qty: int = 0
        a_tot: Decimal = to_decimal("0.0")
        lviresnr: int = -1
        lvcs = ""
        gbuff = None
        amount: Decimal = to_decimal("0.0")
        Gbuff = create_buffer("Gbuff", Guest)
        output_list_data.clear()
        for curr_date in date_range(from_date, to_date):
            for billjournal in db_session.query(Billjournal).filter(
                    (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():
                artikel = get_cache(Artikel, {"artnr": [(eq, billjournal.artnr)], "departement": [
                                    (eq, billjournal.departement)]})

                hoteldpt = get_cache(
                    Hoteldpt, {"num": [(eq, billjournal.departement)]})

                if last_dept >= 0 and last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    if not long_digit:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(87)") + \
                            to_string("T O T A L  ", "x(22)") + \
                            to_string(a_qty, "-9999") + \
                            to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = to_decimal("0")

                if foreign_flag:
                    amount = to_decimal(billjournal.betrag / x_rate)
                else:
                    amount = to_decimal(billjournal.betrag)
                last_dept = billjournal.departement
                a_qty = a_qty + billjournal.anzahl
                a_tot = to_decimal(a_tot + amount)

                output_list = Output_list()
                output_list_data.append(output_list)

                if not long_digit:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, "->,>>>,>>>,>>9.99") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + \
                        to_string(billjournal.zinr, "x(6)") + \
                        to_string(billjournal.rechnr, "9,999,999") + \
                        to_string(billjournal.artnr, "9999") + \
                        to_string(billjournal.bezeich, "x(60)") + \
                        to_string(hoteldpt.depart, "x(22)") + \
                        to_string(billjournal.anzahl, "-9999") + \
                        to_string(amount, " ->>>,>>>,>>>,>>9") + \
                        to_string(billjournal.zeit, "HH:MM:SS") + \
                        to_string(billjournal.userinit, "x(4)") + \
                        to_string(billjournal.sysdate) + \
                        to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):
                    if billjournal.rechnr > 0:
                        if billjournal.bediener_nr == 0:
                            bill = get_cache(
                                Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:
                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:
                            h_bill = get_cache(H_bill, {"rechnr": [(eq, billjournal.rechnr)], "departement": [
                                               (eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:
                        if get_index(billjournal.bezeich, " *BQT") > 0:
                            bk_veran = get_cache(Bk_veran, {"veran_nr": [(eq, to_int(substring(
                                billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5 - 1)))]})

                            if bk_veran:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(
                                billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache(
                                Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:
                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache(
                                    Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                        " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache(
                                    Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:
                                    gbuff = get_cache(
                                        Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + \
                                            " " + gbuff.anrede1 + gbuff.anredefirma
                # else:
                #     pass
                qty = qty + billjournal.anzahl
                sub_tot = to_decimal(sub_tot + amount)
                tot = to_decimal(tot + amount)
        output_list = Output_list()
        output_list_data.append(output_list)

        if not long_digit:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(87)") + \
                to_string("T O T A L  ", "x(22)") + \
                to_string(a_qty, "-9999") + \
                to_string(a_tot, "->,>>>,>>>,>>9.99")

    if foreign_flag:
        def_rate = get_output(htpchar(144))

        if def_rate == "":
            return generate_output()

        waehrung = get_cache(Waehrung, {"wabkurz": [(eq, def_rate)]})

        if waehrung:
            x_rate = to_decimal(waehrung.ankauf)

            if x_rate <= 0:
                return generate_output()
        else:
            return generate_output()

    if sort_type == 0:
        if mi_incl:
            journal_list1()

        elif mi_excl:
            journal_list2()

        elif mi_tran:
            journal_list3()

    elif sort_type == 1:
        if mi_incl:
            journal_list11()

        elif mi_excl:
            journal_list21()

        elif mi_tran:
            journal_list31()

    elif sort_type == 2:
        if mi_incl:
            journal_list12()

        elif mi_excl:
            journal_list22()

        elif mi_tran:
            journal_list32()

    elif sort_type == 3:
        if mi_incl:
            journal_list13()

        elif mi_excl:
            journal_list23()

        elif mi_tran:
            journal_list33()

    elif sort_type == 4:
        if mi_incl:
            journal_list14()

        elif mi_excl:
            journal_list24()

        elif mi_tran:
            journal_list34()

    elif sort_type == 5:
        if mi_incl:
            journal_list15()

        elif mi_excl:
            journal_list25()

        elif mi_tran:
            journal_list35()

    elif sort_type == 6:
        if mi_incl:
            journal_list16()

        elif mi_excl:
            journal_list26()

        elif mi_tran:
            journal_list36()

    return generate_output()
