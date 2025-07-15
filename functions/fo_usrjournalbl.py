from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpchar import htpchar
from sqlalchemy import func
import re
from models import Waehrung, Guest, Billjournal, Artikel, Hoteldpt, Bill, Reservation

def fo_usrjournalbl(mi_incl:bool, mi_excl:bool, mi_tran:bool, from_date:date, to_date:date, from_dept:int, to_dept:int, from_art:int, to_art:int, usr_init:str, long_digit:bool, foreign_flag:bool):
    output_list_list = []
    def_rate:str = ""
    x_rate:decimal = 0
    waehrung = guest = billjournal = artikel = hoteldpt = bill = reservation = None

    output_list = gbuff = None

    output_list_list, Output_list = create_model("Output_list", {"str":str, "gname":str})

    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, reservation
        nonlocal gbuff


        nonlocal output_list, gbuff
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def journal_list1():

        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, reservation
        nonlocal gbuff


        nonlocal output_list, gbuff
        nonlocal output_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        last_dept:int = -1
        last_artnr:int = -1
        a_qty:int = 0
        a_tot:decimal = 0
        lviresnr:int = -1
        lvcs:str = ""
        amount:decimal = 0
        Gbuff = Guest
        output_list_list.clear()
        for curr_date in range(from_date,to_date + 1) :

            for billjournal in db_session.query(Billjournal).filter(
                    (func.lower(Billjournal.userinit) == (usr_init).lower()) &  (Billjournal.bill_datum == curr_date) &  (Billjournal.departement >= from_dept) &  (Billjournal.departement <= to_dept) &  (Billjournal.artnr >= from_art) &  (Billjournal.artnr <= to_art)).all():

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == billjournal.artnr) &  (Artikel.departement == billjournal.departement)).first()

                if last_dept != billjournal.departement:

                    hoteldpt = db_session.query(Hoteldpt).filter(
                            (Hoteldpt.num == billjournal.departement)).first()

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
                        STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = 0

                if foreign_flag:
                    amount = billjournal.betrag / x_rate
                else:
                    amount = billjournal.betrag
                a_qty = a_qty + billjournal.anzahl
                a_tot = a_tot + amount
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    STR = to_string(bill_datum) + to_string(zinr, "x(6)") + to_string(rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                else:
                    STR = to_string(bill_datum) + to_string(zinr, "x(6)") + to_string(rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)

                if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                    if billjournal.rechnr > 0:

                        bill = db_session.query(Bill).filter(
                                (Bill.rechnr == billjournal.rechnr)).first()

                        if bill:

                            if bill.resnr == 0 and bill.bilname != "":
                                output_list.gname = bill.bilname
                            else:

                                gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == bill.gastnr)).first()

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                    else:

                        if artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, "[#") + 2)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == lviresnr)).first()

                            if reservation:

                                gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == reservation.gastnr)).first()

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                        ELSE IF1 + get_index(billjournal.bezeich, " #") > 0 and billjournal.departement = 0 THEN
                        lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " #") + 2)
                        lviresnr = to_int(entry(0, lvcs, "]"))

                        reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == lviresnr)).first()

                        if reservation:

                            gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == reservation.gastnr)).first()

                            if gbuff:
                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot = sub_tot + amount
                tot = tot + amount
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            STR = to_string("", "x(55)") + to_string("T O T A L   ", "x(13)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list2():

        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, reservation
        nonlocal gbuff


        nonlocal output_list, gbuff
        nonlocal output_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        last_dept:int = -1
        last_artnr:int = -1
        a_qty:int = 0
        a_tot:decimal = 0
        lviresnr:int = -1
        lvcs:str = ""
        amount:decimal = 0
        Gbuff = Guest
        output_list_list.clear()
        for curr_date in range(from_date,to_date + 1) :

            for billjournal in db_session.query(Billjournal).filter(
                    (func.lower(Billjournal.userinit) == (usr_init).lower()) &  (Billjournal.bill_datum == curr_date) &  (Billjournal.departement >= from_dept) &  (Billjournal.departement <= to_dept) &  (Billjournal.artnr >= from_art) &  (Billjournal.artnr <= to_art) &  (Billjournal.anzahl != 0)).all():

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == billjournal.artnr) &  (Artikel.departement == billjournal.departement)).first()

                if last_dept != billjournal.departement:

                    hoteldpt = db_session.query(Hoteldpt).filter(
                            (Hoteldpt.num == billjournal.departement)).first()

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
                        STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = 0

                if foreign_flag:
                    amount = billjournal.betrag / x_rate
                else:
                    amount = billjournal.betrag
                a_qty = a_qty + billjournal.anzahl
                a_tot = a_tot + amount
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    STR = to_string(bill_datum) + to_string(zinr, "x(6)") + to_string(rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                else:
                    STR = to_string(bill_datum) + to_string(zinr, "x(6)") + to_string(rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)

                if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                    if billjournal.rechnr > 0:

                        bill = db_session.query(Bill).filter(
                                (Bill.rechnr == billjournal.rechnr)).first()

                        if bill:

                            if bill.resnr == 0 and bill.bilname != "":
                                output_list.gname = bill.bilname
                            else:

                                gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == bill.gastnr)).first()

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                    else:

                        if artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, "[#") + 2)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == lviresnr)).first()

                            if reservation:

                                gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == reservation.gastnr)).first()

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                        ELSE IF1 + get_index(billjournal.bezeich, " #") > 0 and billjournal.departement = 0 THEN
                        lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " #") + 2)
                        lviresnr = to_int(entry(0, lvcs, "]"))

                        reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == lviresnr)).first()

                        if reservation:

                            gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == reservation.gastnr)).first()

                            if gbuff:
                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot = sub_tot + amount
                tot = tot + amount
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")

    def journal_list3():

        nonlocal output_list_list, def_rate, x_rate, waehrung, guest, billjournal, artikel, hoteldpt, bill, reservation
        nonlocal gbuff


        nonlocal output_list, gbuff
        nonlocal output_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        last_dept:int = -1
        last_artnr:int = -1
        a_qty:int = 0
        a_tot:decimal = 0
        lviresnr:int = -1
        lvcs:str = ""
        amount:decimal = 0
        Gbuff = Guest
        output_list_list.clear()
        for curr_date in range(from_date,to_date + 1) :

            for billjournal in db_session.query(Billjournal).filter(
                    (func.lower(Billjournal.userinit) == (usr_init).lower()) &  (Billjournal.bill_datum == curr_date) &  (Billjournal.departement >= from_dept) &  (Billjournal.departement <= to_dept) &  (Billjournal.artnr >= from_art) &  (Billjournal.artnr <= to_art) &  (Billjournal.anzahl == 0)).all():

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == billjournal.artnr) &  (Artikel.departement == billjournal.departement)).first()

                if last_dept != billjournal.departement:

                    hoteldpt = db_session.query(Hoteldpt).filter(
                            (Hoteldpt.num == billjournal.departement)).first()

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
                        STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    else:
                        STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
                    a_qty = 0
                    a_tot = 0

                if foreign_flag:
                    amount = billjournal.betrag / x_rate
                else:
                    amount = billjournal.betrag
                a_qty = a_qty + billjournal.anzahl
                a_tot = a_tot + amount
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    STR = to_string(bill_datum) + to_string(zinr, "x(6)") + to_string(rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)
                else:
                    STR = to_string(bill_datum) + to_string(zinr, "x(6)") + to_string(rechnr, "9,999,999") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(30)") + to_string(hoteldpt.depart, "x(12)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(billjournal.userinit, "x(4)") + to_string(billjournal.sysdate)

                if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                    if billjournal.rechnr > 0:

                        bill = db_session.query(Bill).filter(
                                (Bill.rechnr == billjournal.rechnr)).first()

                        if bill:

                            if bill.resnr == 0 and bill.bilname != "":
                                output_list.gname = bill.bilname
                            else:

                                gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == bill.gastnr)).first()

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                    else:

                        if artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
                            lviresnr = -1
                            lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, "[#") + 2)
                            lviresnr = to_int(entry(0, lvcs, " "))

                            reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == lviresnr)).first()

                            if reservation:

                                gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == reservation.gastnr)).first()

                                if gbuff:
                                    output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                        ELSE IF1 + get_index(billjournal.bezeich, " #") > 0 and billjournal.departement = 0 THEN
                        lvcs = substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " #") + 2)
                        lviresnr = to_int(entry(0, lvcs, "]"))

                        reservation = db_session.query(Reservation).filter(
                                    (Reservation.resnr == lviresnr)).first()

                        if reservation:

                            gbuff = db_session.query(Gbuff).filter(
                                        (Gbuff.gastnr == reservation.gastnr)).first()

                            if gbuff:
                                output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma
                else:
                    pass
                qty = qty + billjournal.anzahl
                sub_tot = sub_tot + amount
                tot = tot + amount
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")
        else:
            STR = to_string("", "x(57)") + to_string("T O T A L   ", "x(11)") + to_string(a_qty, "-9999") + to_string(a_tot, "->,>>>,>>>,>>9.99")

    if foreign_flag:
        def_rate = get_output(htpchar(144))

        if def_rate == "":

            return generate_output()

        waehrung = db_session.query(Waehrung).filter(
                (func.lower(Waehrung.wabkurz) == (def_rate).lower())).first()

        if waehrung:
            x_rate = waehrung.ankauf

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