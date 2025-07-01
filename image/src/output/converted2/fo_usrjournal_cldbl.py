#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpchar import htpchar
import re
from models import Waehrung, Guest, Billjournal, Artikel, Hoteldpt, Bill, H_bill, Bk_veran, Reservation

def fo_usrjournal_cldbl(mi_incl:bool, mi_excl:bool, mi_tran:bool, from_date:date, to_date:date, from_dept:int, to_dept:int, from_art:int, to_art:int, usr_init:string, long_digit:bool, foreign_flag:bool):

    prepare_cache ([Waehrung, Guest, Billjournal, Artikel, Hoteldpt, Bill, H_bill, Bk_veran, Reservation])

    output_list_list = []
    def_rate:string = ""
    x_rate:Decimal = to_decimal("0.0")
    waehrung = guest = billjournal = artikel = hoteldpt = bill = h_bill = bk_veran = reservation = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":string, "gname":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag


        nonlocal output_list
        nonlocal output_list_list

        return {"output-list": output_list_list}

    def journal_list1():

        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag


        nonlocal output_list
        nonlocal output_list_list

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        last_artnr:int = -1
        a_qty:int = 0
        a_tot:Decimal = to_decimal("0.0")
        lviresnr:int = -1
        lvcs:string = ""
        gbuff = None
        amount:Decimal = to_decimal("0.0")
        Gbuff =  create_buffer("Gbuff",Guest)
        output_list_list.clear()
        for curr_date in date_range(from_date,to_date) :

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if not long_digit:
                        str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot =  to_decimal("0")

                if foreign_flag:
                    amount =  to_decimal(billjournal.betrag) / to_decimal(x_rate)
                else:
                    amount =  to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot =  to_decimal(a_tot) + to_decimal(amount)
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                    if billjournal.rechnr > 0:

                        if billjournal.bediener_nr == 0:

                            bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:

                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:

                                    gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:

                        if get_index(billjournal.bezeich, " *BQT") > 0:

                            bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5  - 1)))]})

                            if bk_veran:

                                gbuff = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:

                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache (Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:

                                    gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot =  to_decimal(sub_tot) + to_decimal(amount)
                tot =  to_decimal(tot) + to_decimal(amount)
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")


    def journal_list2():

        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag


        nonlocal output_list
        nonlocal output_list_list

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        last_artnr:int = -1
        a_qty:int = 0
        a_tot:Decimal = to_decimal("0.0")
        lviresnr:int = -1
        lvcs:string = ""
        gbuff = None
        amount:Decimal = to_decimal("0.0")
        Gbuff =  create_buffer("Gbuff",Guest)
        output_list_list.clear()
        for curr_date in date_range(from_date,to_date) :

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl != 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if not long_digit:
                        str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot =  to_decimal("0")

                if foreign_flag:
                    amount =  to_decimal(billjournal.betrag) / to_decimal(x_rate)
                else:
                    amount =  to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot =  to_decimal(a_tot) + to_decimal(amount)
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                    if billjournal.rechnr > 0:

                        if billjournal.bediener_nr == 0:

                            bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:

                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:

                                    gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:

                        if get_index(billjournal.bezeich, " *BQT") > 0:

                            bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5  - 1)))]})

                            if bk_veran:

                                gbuff = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:

                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache (Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:

                                    gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot =  to_decimal(sub_tot) + to_decimal(amount)
                tot =  to_decimal(tot) + to_decimal(amount)
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")


    def journal_list3():

        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal mi_incl, mi_excl, mi_tran, from_date, to_date, from_dept, to_dept, from_art, to_art, usr_init, long_digit, foreign_flag


        nonlocal output_list
        nonlocal output_list_list

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        last_artnr:int = -1
        a_qty:int = 0
        a_tot:Decimal = to_decimal("0.0")
        lviresnr:int = -1
        lvcs:string = ""
        gbuff = None
        amount:Decimal = to_decimal("0.0")
        Gbuff =  create_buffer("Gbuff",Guest)
        output_list_list.clear()
        for curr_date in date_range(from_date,to_date) :

            for billjournal in db_session.query(Billjournal).filter(
                     (Billjournal.userinit == (usr_init).lower()) & (Billjournal.bill_datum == curr_date) & (Billjournal.departement >= from_dept) & (Billjournal.departement <= to_dept) & (Billjournal.artnr >= from_art) & (Billjournal.artnr <= to_art) & (Billjournal.anzahl == 0)).order_by(Billjournal.departement, Billjournal.artnr, Billjournal.zeit).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, billjournal.departement)]})

                if last_dept != billjournal.departement:

                    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})

                    if last_dept == -1:
                        last_dept = billjournal.departement

                if last_artnr == -1:
                    last_artnr = billjournal.artnr

                if last_artnr != billjournal.artnr or last_dept != billjournal.departement:
                    last_dept = hoteldpt.num
                    last_artnr = billjournal.artnr
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if not long_digit:
                        str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot =  to_decimal("0")

                if foreign_flag:
                    amount =  to_decimal(billjournal.betrag) / to_decimal(x_rate)
                else:
                    amount =  to_decimal(billjournal.betrag)
                a_qty = a_qty + billjournal.anzahl
                a_tot =  to_decimal(a_tot) + to_decimal(amount)
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)
                else:
                    str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate) + to_string(billjournal._recid)

                if not matches(billjournal.bezeich, ("*<*")) and not matches(billjournal.bezeich, ("*>*")):

                    if billjournal.rechnr > 0:

                        if billjournal.bediener_nr == 0:

                            bill = get_cache (Bill, {"rechnr": [(eq, billjournal.rechnr)]})

                            if bill:

                                if bill.resnr == 0 and bill.bilname != "":
                                    output_list.gname = bill.bilname
                                else:

                                    gbuff = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif billjournal.bediener_nr != 0:

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, billjournal.rechnr)],"departement": [(eq, billjournal.betriebsnr)]})

                            if h_bill:
                                output_list.gname = h_bill.bilname
                    else:

                        if get_index(billjournal.bezeich, " *BQT") > 0:

                            bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, to_int(substring(billjournal.bezeich, get_index(billjournal.bezeich, " *bqt") + 5  - 1)))]})

                            if bk_veran:

                                gbuff = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif artikel.artart == 5 and get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich, get_index(billjournal.bezeich, "[#") + 2 - 1)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                            if reservation:

                                gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                        elif num_entries(billjournal.bezeich, "#") > 1 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = entry(1, billjournal.bezeich, "#")

                            if get_index(billjournal.bezeich, "Guest") > 0:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                gbuff = get_cache (Guest, {"gastnr": [(eq, lviresnr)]})

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                            else:
                                lviresnr = to_int(entry(0, lvcs, "]"))

                                reservation = get_cache (Reservation, {"resnr": [(eq, lviresnr)]})

                                if reservation:

                                    gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot =  to_decimal(sub_tot) + to_decimal(amount)
                tot =  to_decimal(tot) + to_decimal(amount)
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(57)") + to_string("T O T A L ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")


    if foreign_flag:
        def_rate = get_output(htpchar(144))

        if def_rate == "":

            return generate_output()

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, def_rate)]})

        if waehrung:
            x_rate =  to_decimal(waehrung.ankauf)

            if x_rate <= 0:

                return generate_output()
        else:

            return generate_output()

    if mi_incl :
        journal_list1()

    elif mi_excl :
        journal_list2()

    elif mi_tran :
        journal_list3()

    return generate_output()