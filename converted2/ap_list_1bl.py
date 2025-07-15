#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, L_lieferant, Queasy

def ap_list_1bl(from_date:date, to_date:date, lastname:string, sorttype:int, price_decimal:int, check_disp:int):

    prepare_cache ([L_kredit, L_lieferant, Queasy])

    output_list_data = []
    t_ap:Decimal = to_decimal("0.0")
    t_pay:Decimal = to_decimal("0.0")
    t_bal:Decimal = to_decimal("0.0")
    tot_ap:Decimal = to_decimal("0.0")
    tot_pay:Decimal = to_decimal("0.0")
    tot_bal:Decimal = to_decimal("0.0")
    i:int = 0
    l_kredit = l_lieferant = queasy = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"betriebsnr":int, "ap_recid":int, "curr_pay":Decimal, "lscheinnr":string, "str":string, "steuercode":int, "recv_date":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant, queasy
        nonlocal from_date, to_date, lastname, sorttype, price_decimal, check_disp


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def disp_it():

        nonlocal output_list_data, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant, queasy
        nonlocal from_date, to_date, lastname, sorttype, price_decimal, check_disp


        nonlocal output_list
        nonlocal output_list_data

        curr_firma:string = ""
        s2:string = ""
        d2:string = ""
        curr_pay:Decimal = to_decimal("0.0")
        do_it:bool = False
        l_ap = None
        L_ap =  create_buffer("L_ap",L_kredit)
        output_list_data.clear()
        t_ap =  to_decimal("0")
        t_pay =  to_decimal("0")
        t_bal =  to_decimal("0")
        tot_ap =  to_decimal("0")
        tot_pay =  to_decimal("0")
        tot_bal =  to_decimal("0")

        if lastname == "":

            if check_disp == 0:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,53 + 1) :
                                output_list.str = output_list.str + " "
                            output_list.str = output_list.str + "T O T A L "

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                            else:
                                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                            t_ap =  to_decimal("0")
                            t_pay =  to_decimal("0")
                            t_bal =  to_decimal("0")
                            curr_firma = l_lieferant.firma
                        curr_pay =  to_decimal("0")

                        if l_kredit.counter > 0:

                            for l_ap in db_session.query(L_ap).filter(
                                     (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                d2 = to_string(l_ap.rgdatum)

                        if curr_pay == 0:
                            d2 = ""
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.steuercode = l_kredit.steuercode
                        output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                        output_list.lscheinnr = l_kredit.lscheinnr

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        else:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                        tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1

            elif check_disp == 1:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.rechnr != 0000000)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,53 + 1) :
                                output_list.str = output_list.str + " "
                            output_list.str = output_list.str + "T O T A L "

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                            else:
                                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                            t_ap =  to_decimal("0")
                            t_pay =  to_decimal("0")
                            t_bal =  to_decimal("0")
                            curr_firma = l_lieferant.firma
                        curr_pay =  to_decimal("0")

                        if l_kredit.counter > 0:

                            for l_ap in db_session.query(L_ap).filter(
                                     (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                d2 = to_string(l_ap.rgdatum)

                        if curr_pay == 0:
                            d2 = ""
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.steuercode = l_kredit.steuercode
                        output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                        output_list.lscheinnr = l_kredit.lscheinnr

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        else:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                        tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1


            else:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True

                    queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                    if queasy:
                        do_it = True

                        if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                            do_it = False

                        if do_it:

                            if curr_firma == "":
                                curr_firma = l_lieferant.firma

                            if curr_firma != l_lieferant.firma:
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                for i in range(1,53 + 1) :
                                    output_list.str = output_list.str + " "
                                output_list.str = output_list.str + "T O T A L "

                                if price_decimal == 0:
                                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                                else:
                                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                                t_ap =  to_decimal("0")
                                t_pay =  to_decimal("0")
                                t_bal =  to_decimal("0")
                                curr_firma = l_lieferant.firma
                            curr_pay =  to_decimal("0")

                            if l_kredit.counter > 0:

                                for l_ap in db_session.query(L_ap).filter(
                                         (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                    curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                    d2 = to_string(l_ap.rgdatum)

                            if curr_pay == 0:
                                d2 = ""
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.betriebsnr = l_kredit.betriebsnr
                            output_list.ap_recid = l_kredit._recid
                            output_list.curr_pay =  to_decimal(curr_pay)
                            output_list.steuercode = l_kredit.steuercode
                            output_list.recv_date = queasy.date1
                            output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                            output_list.lscheinnr = l_kredit.lscheinnr

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                            else:
                                output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                            t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                            t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                            t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                            tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                            tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "T O T A L "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
            else:
                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "GRAND TOTAL "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(tot_ap, "->,>>>,>>>,>>>,>>9") + to_string(tot_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(tot_bal, "->,>>>,>>>,>>>,>>9")
            else:
                output_list.str = output_list.str + to_string(tot_ap, "->>,>>>,>>>,>>9.99") + to_string(tot_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(tot_bal, "->>,>>>,>>>,>>9.99") + " "
        else:
            do_it = False

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, lastname)]})

            if l_lieferant:

                if l_lieferant.segment1 == 0:
                    do_it = True
                else:
                    do_it = l_lieferant.segment1 == l_lieferant.segment1

            if do_it:

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.lief_nr == l_lieferant.lief_nr) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_kredit.rgdatum).all():
                    curr_pay =  to_decimal("0")

                    if l_kredit.counter > 0:

                        for l_ap in db_session.query(L_ap).filter(
                                 (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                            curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                            d2 = to_string(l_ap.rgdatum)

                    if curr_pay == 0:
                        d2 = ""
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.steuercode = l_kredit.steuercode
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                    queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                    if queasy:
                        output_list.recv_date = queasy.date1


                output_list = Output_list()
                output_list_data.append(output_list)

                for i in range(1,53 + 1) :
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + "T O T A L "

                if price_decimal == 0:
                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                else:
                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "


    def disp_it0():

        nonlocal output_list_data, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant, queasy
        nonlocal from_date, to_date, lastname, sorttype, price_decimal, check_disp


        nonlocal output_list
        nonlocal output_list_data

        curr_firma:string = ""
        s2:string = ""
        d2:string = ""
        curr_pay:Decimal = to_decimal("0.0")
        do_it:bool = False
        l_ap = None
        L_ap =  create_buffer("L_ap",L_kredit)
        output_list_data.clear()
        t_ap =  to_decimal("0")
        t_pay =  to_decimal("0")
        t_bal =  to_decimal("0")
        tot_ap =  to_decimal("0")
        tot_pay =  to_decimal("0")
        tot_bal =  to_decimal("0")

        if lastname == "":

            if check_disp == 0:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,53 + 1) :
                                output_list.str = output_list.str + " "
                            output_list.str = output_list.str + "T O T A L "

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                            else:
                                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                            t_ap =  to_decimal("0")
                            t_pay =  to_decimal("0")
                            t_bal =  to_decimal("0")
                            curr_firma = l_lieferant.firma
                        curr_pay =  to_decimal("0")

                        if l_kredit.counter > 0:

                            for l_ap in db_session.query(L_ap).filter(
                                     (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                d2 = to_string(l_ap.rgdatum)

                        if curr_pay == 0:
                            d2 = ""
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.steuercode = l_kredit.steuercode
                        output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                        output_list.lscheinnr = l_kredit.lscheinnr

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        else:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                        tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1

            elif check_disp == 1:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.rechnr != 0000000)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,53 + 1) :
                                output_list.str = output_list.str + " "
                            output_list.str = output_list.str + "T O T A L "

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                            else:
                                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                            t_ap =  to_decimal("0")
                            t_pay =  to_decimal("0")
                            t_bal =  to_decimal("0")
                            curr_firma = l_lieferant.firma
                        curr_pay =  to_decimal("0")

                        if l_kredit.counter > 0:

                            for l_ap in db_session.query(L_ap).filter(
                                     (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                d2 = to_string(l_ap.rgdatum)

                        if curr_pay == 0:
                            d2 = ""
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.steuercode = l_kredit.steuercode
                        output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                        output_list.lscheinnr = l_kredit.lscheinnr

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        else:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                        tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1


            else:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True

                    queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                    if queasy:
                        do_it = True

                        if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                            do_it = False

                        if do_it:

                            if curr_firma == "":
                                curr_firma = l_lieferant.firma

                            if curr_firma != l_lieferant.firma:
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                for i in range(1,53 + 1) :
                                    output_list.str = output_list.str + " "
                                output_list.str = output_list.str + "T O T A L "

                                if price_decimal == 0:
                                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                                else:
                                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                                t_ap =  to_decimal("0")
                                t_pay =  to_decimal("0")
                                t_bal =  to_decimal("0")
                                curr_firma = l_lieferant.firma
                            curr_pay =  to_decimal("0")

                            if l_kredit.counter > 0:

                                for l_ap in db_session.query(L_ap).filter(
                                         (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                    curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                    d2 = to_string(l_ap.rgdatum)

                            if curr_pay == 0:
                                d2 = ""
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.betriebsnr = l_kredit.betriebsnr
                            output_list.ap_recid = l_kredit._recid
                            output_list.curr_pay =  to_decimal(curr_pay)
                            output_list.steuercode = l_kredit.steuercode
                            output_list.recv_date = queasy.date1
                            output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                            output_list.lscheinnr = l_kredit.lscheinnr

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                            else:
                                output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                            t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                            t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                            t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                            tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                            tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "T O T A L "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
            else:
                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "GRAND TOTAL "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(tot_ap, "->,>>>,>>>,>>>,>>9") + to_string(tot_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(tot_bal, "->,>>>,>>>,>>>,>>9")
            else:
                output_list.str = output_list.str + to_string(tot_ap, "->>,>>>,>>>,>>9.99") + to_string(tot_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(tot_bal, "->>,>>>,>>>,>>9.99") + " "
        else:
            do_it = False

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, lastname)]})

            if l_lieferant:

                if l_lieferant.segment1 == 0:
                    do_it = True
                else:
                    do_it = l_lieferant.segment1 == l_lieferant.segment1

            if do_it:

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.lief_nr == l_lieferant.lief_nr) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.rgdatum <= to_date)).order_by(L_kredit.rgdatum).all():
                    curr_pay =  to_decimal("0")

                    if l_kredit.counter > 0:

                        for l_ap in db_session.query(L_ap).filter(
                                 (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                            curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                            d2 = to_string(l_ap.rgdatum)

                    if curr_pay == 0:
                        d2 = ""
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.steuercode = l_kredit.steuercode
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                    queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                    if queasy:
                        output_list.recv_date = queasy.date1


                output_list = Output_list()
                output_list_data.append(output_list)

                for i in range(1,53 + 1) :
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + "T O T A L "

                if price_decimal == 0:
                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                else:
                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "


    def disp_it1():

        nonlocal output_list_data, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant, queasy
        nonlocal from_date, to_date, lastname, sorttype, price_decimal, check_disp


        nonlocal output_list
        nonlocal output_list_data

        curr_firma:string = ""
        s2:string = ""
        d2:string = ""
        curr_pay:Decimal = to_decimal("0.0")
        do_it:bool = False
        l_ap = None
        L_ap =  create_buffer("L_ap",L_kredit)
        output_list_data.clear()
        t_ap =  to_decimal("0")
        t_pay =  to_decimal("0")
        t_bal =  to_decimal("0")
        tot_ap =  to_decimal("0")
        tot_pay =  to_decimal("0")
        tot_bal =  to_decimal("0")

        if lastname == "":

            if check_disp == 0:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,53 + 1) :
                                output_list.str = output_list.str + " "
                            output_list.str = output_list.str + "T O T A L "

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                            else:
                                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                            t_ap =  to_decimal("0")
                            t_pay =  to_decimal("0")
                            t_bal =  to_decimal("0")
                            curr_firma = l_lieferant.firma
                        curr_pay =  to_decimal("0")

                        if l_kredit.counter > 0:

                            for l_ap in db_session.query(L_ap).filter(
                                     (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                d2 = to_string(l_ap.rgdatum)

                        if curr_pay == 0:
                            d2 = ""
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.steuercode = l_kredit.steuercode
                        output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                        output_list.lscheinnr = l_kredit.lscheinnr

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        else:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                        tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1

            elif check_disp == 1:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.rechnr != 0000000)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            for i in range(1,53 + 1) :
                                output_list.str = output_list.str + " "
                            output_list.str = output_list.str + "T O T A L "

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                            else:
                                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                            t_ap =  to_decimal("0")
                            t_pay =  to_decimal("0")
                            t_bal =  to_decimal("0")
                            curr_firma = l_lieferant.firma
                        curr_pay =  to_decimal("0")

                        if l_kredit.counter > 0:

                            for l_ap in db_session.query(L_ap).filter(
                                     (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                d2 = to_string(l_ap.rgdatum)

                        if curr_pay == 0:
                            d2 = ""
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.steuercode = l_kredit.steuercode
                        output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                        output_list.lscheinnr = l_kredit.lscheinnr

                        if price_decimal == 0:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        else:
                            output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                        tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1


            else:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.steuercode, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.rechnr, l_kredit.lief_nr, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.steuercode, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.rechnr, L_kredit.lief_nr, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True

                    queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                    if queasy:
                        do_it = True

                        if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                            do_it = False

                        if do_it:

                            if curr_firma == "":
                                curr_firma = l_lieferant.firma

                            if curr_firma != l_lieferant.firma:
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                for i in range(1,53 + 1) :
                                    output_list.str = output_list.str + " "
                                output_list.str = output_list.str + "T O T A L "

                                if price_decimal == 0:
                                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                                else:
                                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
                                t_ap =  to_decimal("0")
                                t_pay =  to_decimal("0")
                                t_bal =  to_decimal("0")
                                curr_firma = l_lieferant.firma
                            curr_pay =  to_decimal("0")

                            if l_kredit.counter > 0:

                                for l_ap in db_session.query(L_ap).filter(
                                         (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                                    curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                                    d2 = to_string(l_ap.rgdatum)

                            if curr_pay == 0:
                                d2 = ""
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.betriebsnr = l_kredit.betriebsnr
                            output_list.ap_recid = l_kredit._recid
                            output_list.curr_pay =  to_decimal(curr_pay)
                            output_list.steuercode = l_kredit.steuercode
                            output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                            output_list.lscheinnr = l_kredit.lscheinnr

                            if price_decimal == 0:
                                output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                            else:
                                output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                            t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                            t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                            t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                            tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                            tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "T O T A L "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
            else:
                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list = Output_list()
            output_list_data.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "GRAND TOTAL "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(tot_ap, "->,>>>,>>>,>>>,>>9") + to_string(tot_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(tot_bal, "->,>>>,>>>,>>>,>>9")
            else:
                output_list.str = output_list.str + to_string(tot_ap, "->>,>>>,>>>,>>9.99") + to_string(tot_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(tot_bal, "->>,>>>,>>>,>>9.99") + " "
        else:
            do_it = False

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, lastname)]})

            if l_lieferant:

                if l_lieferant.segment1 == 0:
                    do_it = True
                else:
                    do_it = l_lieferant.segment1 == l_lieferant.segment1

            if do_it:

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.lief_nr == l_lieferant.lief_nr) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date)).order_by(L_kredit.rgdatum).all():
                    curr_pay =  to_decimal("0")

                    if l_kredit.counter > 0:

                        for l_ap in db_session.query(L_ap).filter(
                                 (L_ap.counter == l_kredit.counter) & (L_ap.zahlkonto > 0) & (L_ap.opart > 0)).order_by(L_ap.rgdatum).all():
                            curr_pay =  to_decimal(curr_pay) - to_decimal(l_ap.saldo)
                            d2 = to_string(l_ap.rgdatum)

                    if curr_pay == 0:
                        d2 = ""
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.steuercode = l_kredit.steuercode
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel) + to_string(l_kredit.rechnr, "9999999")
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                    queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                    if queasy:
                        output_list.recv_date = queasy.date1


                output_list = Output_list()
                output_list_data.append(output_list)

                for i in range(1,53 + 1) :
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + "T O T A L "

                if price_decimal == 0:
                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                else:
                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "


    if from_date == None and to_date == None:
        disp_it()

    elif from_date == None and to_date != None:
        disp_it0()
    else:
        disp_it1()

    return generate_output()