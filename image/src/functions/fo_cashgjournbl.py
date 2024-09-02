from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from functions.htpchar import htpchar
import re
from models import Bediener, Guest, Artikel, Billjournal, Hoteldpt, Bill, H_bill, Bk_veran, Reservation

def fo_cashgjournbl(pvilanguage:int, case_type:int, curr_shift:int, summary_flag:bool, from_date:date, bline_list:[Bline_list]):
    double_currency = False
    foreign_curr = ""
    output_list_list = []
    long_digit:bool = False
    lvcarea:str = "fo_cashgjourn"
    bediener = guest = artikel = billjournal = hoteldpt = bill = h_bill = bk_veran = reservation = None

    bline_list = sum_list = output_list = usr = gbuff = None

    bline_list_list, Bline_list = create_model("Bline_list", {"flag":int, "userinit":str, "selected":bool, "name":str, "bl_recid":int})
    sum_list_list, Sum_list = create_model("Sum_list", {"artnr":int, "artart":int, "bezeich":str, "f_amt":decimal, "amt":decimal})
    output_list_list, Output_list = create_model("Output_list", {"flag":str, "amt_foreign":decimal, "str_foreign":str, "str":str, "gname":str})

    Usr = Bediener
    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal double_currency, foreign_curr, output_list_list, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal usr, gbuff


        nonlocal bline_list, sum_list, output_list, usr, gbuff
        nonlocal bline_list_list, sum_list_list, output_list_list
        return {"double_currency": double_currency, "foreign_curr": foreign_curr, "output-list": output_list_list}

    def cr_bline_list():

        nonlocal double_currency, foreign_curr, output_list_list, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal usr, gbuff


        nonlocal bline_list, sum_list, output_list, usr, gbuff
        nonlocal bline_list_list, sum_list_list, output_list_list

        for usr in db_session.query(Usr).filter(
                (Usr.username != "") &  (Usr.flag == 0)).all():
            bline_list = Bline_list()
            bline_list_list.append(bline_list)

            bline_list.userinit = usr.userinit
            bline_list.name = usr.username
            bline_list.bl_recid = usr._recid

            if substring(usr.perm, 7, 1) >= "2":
                bline_list.flag = 1

    def journal_list():

        nonlocal double_currency, foreign_curr, output_list_list, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal usr, gbuff


        nonlocal bline_list, sum_list, output_list, usr, gbuff
        nonlocal bline_list_list, sum_list_list, output_list_list

        qty:int = 0
        art_tot:decimal = 0
        art_foreign:decimal = 0
        sub_tot:decimal = 0
        sub_foreign:decimal = 0
        tot:decimal = 0
        tot_foreign:decimal = 0
        curr_art:int = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        amt:decimal = 0
        tot_cash:decimal = 0
        lviresnr:int = -1
        lvcs:str = ""
        Gbuff = Guest
        sum_list_list.clear()
        output_list_list.clear()

        for bline_list in query(bline_list_list, filters=(lambda bline_list :bline_list.selected)):

            bediener = db_session.query(Bediener).filter(
                    (Bediener._recid == bline_list.bl_recid)).first()
            it_exist = False

            if not summary_flag:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "*"
                output_list.STR = to_string("", "x(27)") + to_string((translateExtended ("User:", lvcarea, "") + " " + bediener.username) , "x(22)")
            sub_tot = 0
            curr_art = 0
            art_tot = 0
            art_foreign = 0

            for artikel in db_session.query(Artikel).filter(
                    ((Artikel.artart == 2) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.departement == 0)).all():

                sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.artnr == artikel.artnr), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_list.append(sum_list)

                    sum_list.artnr = artikel.artnr
                    sum_list.artart = artikel.artart
                    sum_list.bezeich = artikel.bezeich

                for billjournal in db_session.query(Billjournal).filter(
                        (Billjournal.userinit == bediener.userinit) &  (Billjournal.artnr == artikel.artnr) &  (Billjournal.anzahl != 0) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == from_date)).all():

                    if curr_art == 0:
                        curr_art = artikel.artnr

                    if curr_art != artikel.artnr:

                        if not summary_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.flag = "**"
                            output_list.amt_foreign = art_foreign

                            if not long_digit:
                                output_list.STR = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr(10))
                            else:
                                STR = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr(10))
                        art_tot = 0
                        art_foreign = 0
                        curr_art = artikel.artnr

                    if artikel.pricetab or artikel.betriebsnr != 0:
                        art_foreign = art_foreign + billjournal.fremdwaehrng
                        sum_list.f_amt = sum_list.f_amt + billjournal.fremdwaehrng
                    else:
                        art_tot = art_tot + billjournal.betrag
                        sum_list.amt = sum_list.amt + billjournal.betrag
                    it_exist = True

                    if last_dept != billjournal.departement:

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                (Hoteldpt.num == billjournal.departement)).first()
                    last_dept = hoteldpt.num

                    if not summary_flag:
                        output_list = Output_list()
                        output_list_list.append(output_list)


                        if artikel.pricetab or artikel.betriebsnr != 0:
                            amt_foreign = billjournal.fremdwaehrng
                            amt = 0
                        else:
                            amt = billjournal.betrag

                        if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                            if billjournal.rechnr > 0:

                                if billjournal.bediener_nr == 0:

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

                                elif billjournal.bediener_nr != 0:

                                    h_bill = db_session.query(H_bill).filter(
                                            (H_bill.rechnr == billjournal.rechnr) &  (H_bill.departement == billjournal.betriebsnr)).first()

                                    if h_bill:
                                        output_list.gname = h_bill.bilname
                            else:
                                IF1 + get_index(billjournal.bezeich, " *BQT") > 0 THEN

                                bk_veran = db_session.query(Bk_veran).filter(
                                            (Bk_veran.veran_nr == to_int(substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " *BQT") + 5)))).first()

                                if bk_veran:

                                    gbuff = db_session.query(Gbuff).filter(
                                                (Gbuff.gastnr == bk_veran.gastnr)).first()

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                elif artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
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

                        if not long_digit:
                            output_list.STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                        else:
                            output_list.STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                    qty = qty + billjournal.anzahl

                    if artikel.pricetab or artikel.betriebsnr != 0:
                        sub_foreign = sub_foreign + billjournal.fremdwaehrng
                    else:
                        sub_tot = sub_tot + billjournal.betrag

            if it_exist and not summary_flag:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "**"
                output_list.amt_foreign = art_foreign

                if not long_digit:
                    output_list.STR = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr(10))
                else:
                    STR = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr(10))
                tot_foreign = tot_foreign + sub_foreign
                tot = tot + sub_tot

            elif not it_exist and not summary_flag:
                output_list_list.remove(output_list)

        if not summary_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = "***"
            output_list.amt_foreign = 0

            if not long_digit:
                STR = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->,>>>,>>>,>>9.99")
            else:
                STR = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->>>>,>>>,>>>,>>9")

        sum_list = query(sum_list_list, filters=(lambda sum_list :(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF CASH PAYMENT:", lvcarea, "") , "x(57)")
            output_list.flag = "#"
            tot_cash = 0

            for sum_list in query(sum_list_list, filters=(lambda sum_list :(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6)):
                tot_cash = tot_cash + sum_list.amt
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "SUM"

                if not long_digit:
                    output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                    output_list.amt_foreign = sum_list.f_amt
                else:
                    STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.amt_foreign = sum_list.f_amt
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = "SUM"
            output_list.flag = "***"

            if not long_digit:
                output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->,>>>,>>>,>>9.99")
                output_list.amt_foreign = 0
            else:
                output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->>>>,>>>,>>>,>>9")
                output_list.amt_foreign = 0

        sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.f_amt != 0 or sum_list.amt != 0), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF PAYMENT:", lvcarea, "") , "x(57)")
            output_list.flag = "#"

            for sum_list in query(sum_list_list, filters=(lambda sum_list :sum_list.f_amt != 0 or sum_list.amt != 0)):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "SUM"

                if not long_digit:
                    output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                    output_list.amt_foreign = sum_list.f_amt
                else:
                    output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.amt_foreign = sum_list.f_amt

        for output_list in query(output_list_list, filters=(lambda output_list :output_list.amt_foreign != 0)):

            if (output_list.amt_foreign > 99999999) or (output_list.amt_foreign < -99999999):
                output_list.str_foreign = to_string(output_list.amt_foreign, "->>>,>>>,>>>,>>9")
            else:
                output_list.str_foreign = to_string(output_list.amt_foreign, "->,>>>,>>>,>>9.99")

    def journal_list1():

        nonlocal double_currency, foreign_curr, output_list_list, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal usr, gbuff


        nonlocal bline_list, sum_list, output_list, usr, gbuff
        nonlocal bline_list_list, sum_list_list, output_list_list

        qty:int = 0
        art_tot:decimal = 0
        art_foreign:decimal = 0
        sub_tot:decimal = 0
        sub_foreign:decimal = 0
        tot:decimal = 0
        tot_foreign:decimal = 0
        curr_art:int = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        amt:decimal = 0
        tot_cash:decimal = 0
        lviresnr:int = -1
        lvcs:str = ""
        Gbuff = Guest
        sum_list_list.clear()
        output_list_list.clear()

        for bline_list in query(bline_list_list, filters=(lambda bline_list :bline_list.selected)):

            bediener = db_session.query(Bediener).filter(
                    (Bediener._recid == bline_list.bl_recid)).first()
            it_exist = False

            if not summary_flag:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "*"
                STR = to_string("", "x(27)") + to_string((translateExtended ("User:", lvcarea, "") + " " + bediener.username) , "x(22)")
            sub_tot = 0
            curr_art = 0
            art_tot = 0
            art_foreign = 0

            for artikel in db_session.query(Artikel).filter(
                    ((Artikel.artart == 2) |  (Artikel.artart == 6) |  (Artikel.artart == 7)) &  (Artikel.departement == 0)).all():

                sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.artnr == artikel.artnr), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_list.append(sum_list)

                    sum_list.artnr = artikel.artnr
                    sum_list.artart = artikel.artart
                    sum_list.bezeich = artikel.bezeich

                for billjournal in db_session.query(Billjournal).filter(
                        (Billjournal.userinit == bediener.userinit) &  (Billjournal.artnr == artikel.artnr) &  (Billjournal.anzahl != 0) &  (Billjournal.departement == artikel.departement) &  (Billjournal.bill_datum == from_date) &  (Billjournal.betriebsnr == curr_shift)).all():

                    if curr_art == 0:
                        curr_art = artikel.artnr

                    if curr_art != artikel.artnr:

                        if not summary_flag:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.flag = "**"
                            output_list.amt_foreign = art_foreign

                            if not long_digit:
                                STR = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr(10))
                            else:
                                STR = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr(10))
                        art_tot = 0
                        art_foreign = 0
                        curr_art = artikel.artnr

                    if artikel.pricetab or artikel.betriebsnr != 0:
                        art_foreign = art_foreign + billjournal.fremdwaehrng
                        sum_list.f_amt = sum_list.f_amt + billjournal.fremdwaehrng
                    else:
                        art_tot = art_tot + billjournal.betrag
                        sum_list.amt = sum_list.amt + billjournal.betrag
                    it_exist = True

                    if last_dept != billjournal.departement:

                        hoteldpt = db_session.query(Hoteldpt).filter(
                                (Hoteldpt.num == billjournal.departement)).first()
                    last_dept = hoteldpt.num

                    if not summary_flag:
                        output_list = Output_list()
                        output_list_list.append(output_list)


                        if artikel.pricetab or artikel.betriebsnr != 0:
                            amt_foreign = billjournal.fremdwaehrng
                            amt = 0
                        else:
                            amt = billjournal.betrag

                        if not re.match(".*<.*",billjournal.bezeich) and not re.match(".*>.*",billjournal.bezeich):

                            if billjournal.rechnr > 0:

                                if billjournal.bediener_nr == 0:

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

                                elif billjournal.bediener_nr != 0:

                                    h_bill = db_session.query(H_bill).filter(
                                            (H_bill.rechnr == billjournal.rechnr) &  (H_bill.departement == billjournal.betriebsnr)).first()

                                    if h_bill:
                                        output_list.gname = h_bill.bilname
                            else:
                                IF1 + get_index(billjournal.bezeich, " *BQT") > 0 THEN

                                bk_veran = db_session.query(Bk_veran).filter(
                                            (Bk_veran.veran_nr == to_int(substring(billjournal.bezeich,0 + get_index(billjournal.bezeich, " *BQT") + 5)))).first()

                                if bk_veran:

                                    gbuff = db_session.query(Gbuff).filter(
                                                (Gbuff.gastnr == bk_veran.gastnr)).first()

                                    if gbuff:
                                        output_list.gname = gbuff.name + ", " + gbuff.vorname1 + " " + gbuff.anrede1 + gbuff.anredefirma

                                elif artikel.artart == 5 AND1 + get_index(billjournal.bezeich, " [#") > 0 and billjournal.departement == 0:
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

                        if not long_digit:
                            output_list.STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                        else:
                            output_list.STR = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                    qty = qty + billjournal.anzahl

                    if artikel.pricetab or artikel.betriebsnr != 0:
                        sub_foreign = sub_foreign + billjournal.fremdwaehrng
                    else:
                        sub_tot = sub_tot + billjournal.betrag

            if it_exist and not summary_flag:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "**"
                output_list.amt_foreign = art_foreign

                if not long_digit:
                    output_list.STR = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr(10))
                else:
                    output_list.STR = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr(10))
                tot_foreign = tot_foreign + sub_foreign
                tot = tot + sub_tot

            elif not it_exist and not summary_flag:
                output_list_list.remove(output_list)

        if not summary_flag:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = "***"
            output_list.amt_foreign = 0

            if not long_digit:
                STR = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->,>>>,>>>,>>9.99")
            else:
                STR = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->>>>,>>>,>>>,>>9")

        sum_list = query(sum_list_list, filters=(lambda sum_list :(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF CASH PAYMENT:", lvcarea, "") , "x(57)")
            output_list.flag = "#"
            tot_cash = 0

            for sum_list in query(sum_list_list, filters=(lambda sum_list :(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6)):
                tot_cash = tot_cash + sum_list.amt
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "SUM"

                if not long_digit:
                    output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                    output_list.amt_foreign = sum_list.f_amt
                else:
                    output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.amt_foreign = sum_list.f_amt
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = "SUM"
            output_list.flag = "***"

            if not long_digit:
                output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->,>>>,>>>,>>9.99")
                output_list.amt_foreign = 0
            else:
                output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->>>>,>>>,>>>,>>9")
                output_list.amt_foreign = 0

        sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.f_amt != 0 or sum_list.amt != 0), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF PAYMENT:", lvcarea, "") , "x(47)")
            output_list.flag = "#"

            for sum_list in query(sum_list_list, filters=(lambda sum_list :sum_list.f_amt != 0 or sum_list.amt != 0)):
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = "SUM"

                if not long_digit:
                    output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                    output_list.amt_foreign = sum_list.f_amt
                else:
                    output_list.STR = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.amt_foreign = sum_list.f_amt

        for output_list in query(output_list_list, filters=(lambda output_list :output_list.amt_foreign != 0)):

            if (output_list.amt_foreign > 99999999) or (output_list.amt_foreign < -99999999):
                output_list.str_foreign = to_string(output_list.amt_foreign, "->>>,>>>,>>>,>>9")
            else:
                output_list.str_foreign = to_string(output_list.amt_foreign, "->,>>>,>>>,>>9.99")

    if from_date == None:
        from_date = get_output(htpdate(110))
    double_currency = get_output(htplogic(240))

    if double_currency:
        foreign_curr = get_output(htpchar(144))

    if case_type == 1:
        cr_bline_list()

    elif case_type == 2:

        if curr_shift == 0:
            journal_list()
        else:
            journal_list1()

    return generate_output()