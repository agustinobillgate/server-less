#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 21/8/2025
# bill datum (fo_cashgjourn_cldbl)
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htplogic import htplogic
from functions.htpchar import htpchar
import re
from models import Bediener, Guest, Artikel, Billjournal, Hoteldpt, Bill, H_bill, Bk_veran, Reservation

bline_list_data, Bline_list = create_model("Bline_list", {"flag":int, "userinit":string, "selected":bool, "name":string, "bl_recid":int})

def fo_cashgjourn_cldbl(pvilanguage:int, case_type:int, curr_shift:int, summary_flag:bool, onlyjournal:bool, excljournal:bool, from_date:date, bline_list_data:[Bline_list]):

    prepare_cache ([Bediener, Guest, Artikel, Billjournal, Hoteldpt, Bill, H_bill, Bk_veran, Reservation])

    double_currency = False
    foreign_curr = ""
    output_list_data = []
    long_digit:bool = False
    lvcarea:string = "fo-cashgjourn"
    bediener = guest = artikel = billjournal = hoteldpt = bill = h_bill = bk_veran = reservation = None

    bline_list = sum_list = output_list = usr = None

    sum_list_data, Sum_list = create_model("Sum_list", {"artnr":int, "artart":int, "bezeich":string, "f_amt":Decimal, "amt":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"flag":string, "amt_foreign":Decimal, "str_foreign":string, "str":string, "gname":string})

    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal double_currency, foreign_curr, output_list_data, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal pvilanguage, case_type, curr_shift, summary_flag, onlyjournal, excljournal, from_date
        nonlocal usr


        nonlocal bline_list, sum_list, output_list, usr
        nonlocal sum_list_data, output_list_data

        return {"from_date": from_date, "double_currency": double_currency, "foreign_curr": foreign_curr, "bline-list": bline_list_data, "output-list": output_list_data}

    def cr_bline_list():

        nonlocal double_currency, foreign_curr, output_list_data, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal pvilanguage, case_type, curr_shift, summary_flag, onlyjournal, excljournal, from_date
        nonlocal usr


        nonlocal bline_list, sum_list, output_list, usr
        nonlocal sum_list_data, output_list_data

        for usr in db_session.query(Usr).filter(
                 (Usr.username != "") & (Usr.flag == 0)).order_by(Usr.username).all():
            bline_list = Bline_list()
            bline_list_data.append(bline_list)

            bline_list.userinit = usr.userinit
            bline_list.name = usr.username
            bline_list.bl_recid = usr._recid

            if substring(usr.permissions, 7, 1) >= ("2").lower() :
                bline_list.flag = 1


    def journal_list():

        nonlocal double_currency, foreign_curr, output_list_data, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal pvilanguage, case_type, curr_shift, summary_flag, onlyjournal, excljournal, from_date
        nonlocal usr


        nonlocal bline_list, sum_list, output_list, usr
        nonlocal sum_list_data, output_list_data

        qty:int = 0
        art_tot:Decimal = to_decimal("0.0")
        art_foreign:Decimal = to_decimal("0.0")
        sub_tot:Decimal = to_decimal("0.0")
        sub_foreign:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        tot_foreign:Decimal = to_decimal("0.0")
        curr_art:int = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        amt:Decimal = to_decimal("0.0")
        tot_cash:Decimal = to_decimal("0.0")
        lviresnr:int = -1
        lvcs:string = ""
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Guest)
        sum_list_data.clear()
        output_list_data.clear()

        for bline_list in query(bline_list_data, filters=(lambda bline_list: bline_list.selected), sort_by=[("name",False)]):

            bediener = get_cache (Bediener, {"_recid": [(eq, bline_list.bl_recid)]})
            it_exist = False

            if not summary_flag:

                if bediener:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = "*"
                    # Rd 21/8/2025, if bediener available
                    if bediener:
                        output_list.str = to_string("", "x(27)") + to_string((translateExtended ("User:", lvcarea, "") + " " + bediener.username) , "x(22)")
                else:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.flag = "*"
                    output_list.str = to_string("", "x(27)") + to_string((translateExtended ("User:", lvcarea, "") + " " + "") , "x(22)")
            sub_tot =  to_decimal("0")
            curr_art = 0
            art_tot =  to_decimal("0")
            art_foreign =  to_decimal("0")

            for artikel in db_session.query(Artikel).filter(
                     ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.departement == 0)).order_by(Artikel.bezeich).all():

                sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.artnr == artikel.artnr), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_data.append(sum_list)

                    sum_list.artnr = artikel.artnr
                    sum_list.artart = artikel.artart
                    sum_list.bezeich = artikel.bezeich

                if bediener:

                    for billjournal in db_session.query(Billjournal).filter(
                             (Billjournal.userinit == bediener.userinit) & (Billjournal.artnr == artikel.artnr) & (Billjournal.anzahl != 0) & (Billjournal.departement == artikel.departement) & (Billjournal.bill_datum == from_date) & (((Billjournal.bediener_nr == 0) & (onlyjournal == False)) | ((Billjournal.bediener_nr != 0) & (excljournal == False)))).order_by(Billjournal.zeit, Billjournal.rechnr).all():

                        if curr_art == 0:
                            curr_art = artikel.artnr

                        if curr_art != artikel.artnr:

                            if not summary_flag:
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                output_list.flag = "**"
                                output_list.amt_foreign =  to_decimal(art_foreign)

                                if not long_digit:
                                    output_list.str = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                                else:
                                    output_list.str = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr_unicode(10))
                            art_tot =  to_decimal("0")
                            art_foreign =  to_decimal("0")
                            curr_art = artikel.artnr

                        if artikel.pricetab or artikel.betriebsnr != 0:
                            art_foreign =  to_decimal(art_foreign) + to_decimal(billjournal.fremdwaehrng)
                            sum_list.f_amt =  to_decimal(sum_list.f_amt) + to_decimal(billjournal.fremdwaehrng)
                        else:
                            art_tot =  to_decimal(art_tot) + to_decimal(billjournal.betrag)
                            sum_list.amt =  to_decimal(sum_list.amt) + to_decimal(billjournal.betrag)
                        it_exist = True

                        if last_dept != billjournal.departement:

                            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})
                        last_dept = hoteldpt.num

                        if not summary_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)


                            if artikel.pricetab or artikel.betriebsnr != 0:
                                amt_foreign = billjournal.fremdwaehrng
                                amt =  to_decimal("0")
                            else:
                                amt =  to_decimal(billjournal.betrag)

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

                            if not long_digit:
                                output_list.str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                            else:
                                output_list.str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->>>>,>>>,>>>,>>9") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                        qty = qty + billjournal.anzahl

                        if artikel.pricetab or artikel.betriebsnr != 0:
                            sub_foreign =  to_decimal(sub_foreign) + to_decimal(billjournal.fremdwaehrng)
                        else:
                            sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)

            if it_exist and not summary_flag:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = "**"
                output_list.amt_foreign =  to_decimal(art_foreign)

                if not long_digit:
                    output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                else:
                    output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr_unicode(10))
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(sub_foreign)
                tot =  to_decimal(tot) + to_decimal(sub_tot)

            elif not it_exist and not summary_flag:
                output_list_data.remove(output_list)

        if not summary_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = "***"
            output_list.amt_foreign =  to_decimal("0")

            if not long_digit:
                output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->,>>>,>>>,>>9.99")
            else:
                output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->>>>,>>>,>>>,>>9")

        sum_list = query(sum_list_data, filters=(lambda sum_list:(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF CASH PAYMENT:", lvcarea, "") , "x(57)")
            output_list.flag = "#"
            tot_cash =  to_decimal("0")

            for sum_list in query(sum_list_data, filters=(lambda sum_list:(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6), sort_by=[("artnr",False)]):
                tot_cash =  to_decimal(tot_cash) + to_decimal(sum_list.amt)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = "SUM"

                if not long_digit:
                    output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)
                else:
                    output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = "SUM"
            output_list.flag = "***"

            if not long_digit:
                output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->,>>>,>>>,>>9.99")
                output_list.amt_foreign =  to_decimal("0")
            else:
                output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->>>>,>>>,>>>,>>9")
                output_list.amt_foreign =  to_decimal("0")

        sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.f_amt != 0 or sum_list.amt != 0), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF PAYMENT:", lvcarea, "") , "x(57)")
            output_list.flag = "#"

            for sum_list in query(sum_list_data, filters=(lambda sum_list: sum_list.f_amt != 0 or sum_list.amt != 0), sort_by=[("artnr",False)]):
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = "SUM"

                # Rd 21/8/2025
                # if not long_digit:
                #     output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                #     output_list.amt_foreign =  to_decimal(sum_list.f_amt)
                # else:
                #     output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                #     output_list.amt_foreign =  to_decimal(sum_list.f_amt)
                #  output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->,>>>,>>>,>>9.99")
                if not long_digit:

                    output_list.str = to_string("", "x(27)") + to_string(translateExtended (sum_list.bezeich, lvcarea, "") , "x(56)") + " " + to_string(sum_list.amt, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)
                else:
                #     output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(56)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.str = to_string("", "x(27)") + to_string(translateExtended (0, lvcarea, "") , "x(56)") + " " + to_string(0, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)

        for output_list in query(output_list_data, filters=(lambda output_list: output_list.amt_foreign != 0)):

            if (output_list.amt_foreign > 99999999) or (output_list.amt_foreign < -99999999):
                output_list.str_foreign = to_string(output_list.amt_foreign, "->>>,>>>,>>>,>>9")
            else:
                output_list.str_foreign = to_string(output_list.amt_foreign, "->,>>>,>>>,>>9.99")


    def journal_list1():

        nonlocal double_currency, foreign_curr, output_list_data, long_digit, lvcarea, bediener, guest, artikel, billjournal, hoteldpt, bill, h_bill, bk_veran, reservation
        nonlocal pvilanguage, case_type, curr_shift, summary_flag, onlyjournal, excljournal, from_date
        nonlocal usr


        nonlocal bline_list, sum_list, output_list, usr
        nonlocal sum_list_data, output_list_data

        qty:int = 0
        art_tot:Decimal = to_decimal("0.0")
        art_foreign:Decimal = to_decimal("0.0")
        sub_tot:Decimal = to_decimal("0.0")
        sub_foreign:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        tot_foreign:Decimal = to_decimal("0.0")
        curr_art:int = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        amt:Decimal = to_decimal("0.0")
        tot_cash:Decimal = to_decimal("0.0")
        lviresnr:int = -1
        lvcs:string = ""
        gbuff = None
        Gbuff =  create_buffer("Gbuff",Guest)
        sum_list_data.clear()
        output_list_data.clear()

        for bline_list in query(bline_list_data, filters=(lambda bline_list: bline_list.selected), sort_by=[("name",False)]):

            bediener = get_cache (Bediener, {"_recid": [(eq, bline_list.bl_recid)]})
            # Rd 21/8/2025
            if bediener is None:
                continue

            it_exist = False

            if not summary_flag:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = "*"
                # Rd 21/8/2025
                # if available bediener
                if bediener:
                    output_list.str = to_string("", "x(27)") + to_string((translateExtended ("User:", lvcarea, "") + " " + bediener.username) , "x(22)")
            sub_tot =  to_decimal("0")
            curr_art = 0
            art_tot =  to_decimal("0")
            art_foreign =  to_decimal("0")

            for artikel in db_session.query(Artikel).filter(
                     ((Artikel.artart == 2) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.departement == 0)).order_by(Artikel.bezeich).all():

                sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.artnr == artikel.artnr), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_data.append(sum_list)

                    sum_list.artnr = artikel.artnr
                    sum_list.artart = artikel.artart
                    sum_list.bezeich = artikel.bezeich

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.userinit == bediener.userinit) & (Billjournal.artnr == artikel.artnr) & 
                         (Billjournal.anzahl != 0) & (Billjournal.departement == artikel.departement) & 
                         (Billjournal.bill_datum == from_date) & (Billjournal.betriebsnr == curr_shift) & 
                         (((Billjournal.bediener_nr == 0) & (onlyjournal == False)) | ((Billjournal.bediener_nr != 0) & 
                                                                                       (excljournal == False)))).order_by(Billjournal.zeit, Billjournal.rechnr).all():

                    if curr_art == 0:
                        curr_art = artikel.artnr

                    if curr_art != artikel.artnr:

                        if not summary_flag:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.flag = "**"
                            output_list.amt_foreign =  to_decimal(art_foreign)

                            if not long_digit:
                                output_list.str = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                            else:
                                output_list.str = to_string("", "x(67)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(16)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr_unicode(10))
                        art_tot =  to_decimal("0")
                        art_foreign =  to_decimal("0")
                        curr_art = artikel.artnr

                    if artikel.pricetab or artikel.betriebsnr != 0:
                        art_foreign =  to_decimal(art_foreign) + to_decimal(billjournal.fremdwaehrng)
                        sum_list.f_amt =  to_decimal(sum_list.f_amt) + to_decimal(billjournal.fremdwaehrng)
                    else:
                        art_tot =  to_decimal(art_tot) + to_decimal(billjournal.betrag)
                        sum_list.amt =  to_decimal(sum_list.amt) + to_decimal(billjournal.betrag)
                    it_exist = True

                    if last_dept != billjournal.departement:

                        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, billjournal.departement)]})
                    last_dept = hoteldpt.num

                    if not summary_flag:
                        output_list = Output_list()
                        output_list_data.append(output_list)


                        if artikel.pricetab or artikel.betriebsnr != 0:
                            amt_foreign = billjournal.fremdwaehrng
                            amt =  to_decimal("0")
                        else:
                            amt =  to_decimal(billjournal.betrag)

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

                        if not long_digit:
                            # Rd 21/8/2025, bill-datum, zeit
                            # output_list.str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                            output_list.str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + \
                                            to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + \
                                                to_string(amt, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                        else:
                            # Rd 21/8/2025, bill-datum, zeit
                            # output_list.str = to_string(bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + to_string(amt, "->>>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")
                            output_list.str = to_string(billjournal.bill_datum) + to_string(billjournal.zinr, "x(6)") + to_string(billjournal.rechnr, ">>>>>>>>9") + \
                                                to_string(billjournal.artnr, "9999") + to_string(billjournal.bezeich, "x(40)") + to_string(hoteldpt.depart, "x(17)") + \
                                                to_string(amt, "->>>>,>>>,>>>,>>9") + to_string(billjournal.zeit, "HH:MM:SS") + to_string(bediener.userinit, "x(3)")

                    qty = qty + billjournal.anzahl

                    if artikel.pricetab or artikel.betriebsnr != 0:
                        sub_foreign =  to_decimal(sub_foreign) + to_decimal(billjournal.fremdwaehrng)
                    else:
                        sub_tot =  to_decimal(sub_tot) + to_decimal(billjournal.betrag)

            if it_exist and not summary_flag:
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = "**"
                output_list.amt_foreign =  to_decimal(art_foreign)

                if not long_digit:
                    output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                else:
                    output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Sub Total", lvcarea, "") , "x(56)") + " " + to_string(art_tot, " ->>>,>>>,>>>,>>9") + to_string(chr_unicode(10))
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(sub_foreign)
                tot =  to_decimal(tot) + to_decimal(sub_tot)

            elif not it_exist and not summary_flag:
                output_list_data.remove(output_list)

        if not summary_flag:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = "***"
            output_list.amt_foreign =  to_decimal("0")

            if not long_digit:
                output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->,>>>,>>>,>>9.99")
            else:
                output_list.str = to_string("", "x(27)") + to_string(translateExtended ("Grand TOTAL", lvcarea, "") , "x(56)") + " " + to_string(tot, "->>>>,>>>,>>>,>>9")

        sum_list = query(sum_list_data, filters=(lambda sum_list:(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF CASH PAYMENT:", lvcarea, "") , "x(57)")
            output_list.flag = "#"
            tot_cash =  to_decimal("0")

            for sum_list in query(sum_list_data, filters=(lambda sum_list:(sum_list.f_amt != 0 or sum_list.amt != 0) and sum_list.artart == 6), sort_by=[("artnr",False)]):
                tot_cash =  to_decimal(tot_cash) + to_decimal(sum_list.amt)
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = "SUM"
                if not long_digit:
                    output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)
                else:
                    output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + to_string(sum_list.bezeich, "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = "SUM"
            output_list.flag = "***"

            if not long_digit:
                # Rd 21/8/20225
                # output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->,>>>,>>>,>>9.99")
                output_list.str = to_string("", "x(27)") + to_string(translateExtended (sum_list.bezeich, lvcarea, "") , "x(56)") + " " + to_string(sum_list.amt, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))

                output_list.amt_foreign =  to_decimal("0")
            else:
                output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(0, ">>>>") + to_string("TOTAL", "x(40)") + to_string(" ", "x(17)") + to_string(tot_cash, "->>>>,>>>,>>>,>>9")
                output_list.amt_foreign =  to_decimal("0")

        sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.f_amt != 0 or sum_list.amt != 0), first=True)

        if sum_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.str = to_string("", "x(31)") + to_string(translateExtended ("SUMMARY OF PAYMENT:", lvcarea, "") , "x(47)")
            output_list.flag = "#"

            for sum_list in query(sum_list_data, filters=(lambda sum_list: sum_list.f_amt != 0 or sum_list.amt != 0), sort_by=[("artnr",False)]):
                output_list = Output_list()
                output_list_data.append(output_list)

                output_list.flag = "SUM"
                if not long_digit:
                    # output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + \
                    #     to_string(sum_list.bezeich.strip(), "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->,>>>,>>>,>>9.99")
                    # Rd 21/8/2025
                    output_list.str = to_string("", "x(27)") + to_string(translateExtended (sum_list.bezeich, lvcarea, "") , "x(56)") + " " + to_string(sum_list.amt, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)
                else:
                    # Rd 21/8/2025

                    # output_list.str = to_string(" ", "x(8)") + to_string(" ", "x(6)") + to_string(0, ">>>>>>>>>") + to_string(sum_list.artnr, "9999") + \
                    # to_string(sum_list.bezeich.strip(), "x(40)") + to_string(" ", "x(17)") + to_string(sum_list.amt, "->>>>,>>>,>>>,>>9")
                    output_list.str = to_string("", "x(27)") + to_string(translateExtended ("", lvcarea, "") , "x(56)") + " " + to_string(sum_list.amt, "->,>>>,>>>,>>9.99") + to_string(chr_unicode(10))
                    output_list.amt_foreign =  to_decimal(sum_list.f_amt)

        for output_list in query(output_list_data, filters=(lambda output_list: output_list.amt_foreign != 0)):

            if (output_list.amt_foreign > 99999999) or (output_list.amt_foreign < -99999999):
                output_list.str_foreign = to_string(output_list.amt_foreign, "->>>,>>>,>>>,>>9")
            else:
                output_list.str_foreign = to_string(output_list.amt_foreign, "->,>>>,>>>,>>9.99")


    #----------------------------------------------
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