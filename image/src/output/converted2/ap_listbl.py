from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_kredit, L_lieferant

def ap_listbl(from_date:date, to_date:date, lastname:str, sorttype:int, price_decimal:int):
    output_list_list = []
    t_ap:decimal = to_decimal("0.0")
    t_pay:decimal = to_decimal("0.0")
    t_bal:decimal = to_decimal("0.0")
    tot_ap:decimal = to_decimal("0.0")
    tot_pay:decimal = to_decimal("0.0")
    tot_bal:decimal = to_decimal("0.0")
    i:int = 0
    l_kredit = l_lieferant = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"betriebsnr":int, "ap_recid":int, "curr_pay":decimal, "lscheinnr":str, "str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant
        nonlocal from_date, to_date, lastname, sorttype, price_decimal


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def disp_it():

        nonlocal output_list_list, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant
        nonlocal from_date, to_date, lastname, sorttype, price_decimal


        nonlocal output_list
        nonlocal output_list_list

        curr_firma:str = ""
        s2:str = ""
        d2:str = ""
        curr_pay:decimal = to_decimal("0.0")
        do_it:bool = False
        l_ap = None
        L_ap =  create_buffer("L_ap",L_kredit)
        output_list_list.clear()
        t_ap =  to_decimal("0")
        t_pay =  to_decimal("0")
        t_bal =  to_decimal("0")
        tot_ap =  to_decimal("0")
        tot_pay =  to_decimal("0")
        tot_bal =  to_decimal("0")

        if lastname == "":

            l_kredit_obj_list = []
            for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                     (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                if l_kredit._recid in l_kredit_obj_list:
                    continue
                else:
                    l_kredit_obj_list.append(l_kredit._recid)


                do_it = True

                if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                    do_it = False

                if do_it:

                    if curr_firma == "":
                        curr_firma = l_lieferant.firma

                    if curr_firma != l_lieferant.firma:
                        output_list = Output_list()
                        output_list_list.append(output_list)

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
                    output_list_list.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                    tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                    tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                    tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "T O T A L "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
            else:
                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "GRAND TOTAL "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(tot_ap, "->,>>>,>>>,>>>,>>9") + to_string(tot_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(tot_bal, "->,>>>,>>>,>>>,>>9")
            else:
                output_list.str = output_list.str + to_string(tot_ap, "->>,>>>,>>>,>>9.99") + to_string(tot_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(tot_bal, "->>,>>>,>>>,>>9.99") + " "
        else:
            do_it = False

            l_lieferant = db_session.query(L_lieferant).filter(
                     (func.lower(L_lieferant.firma) == (lastname).lower())).first()

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
                    output_list_list.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                output_list = Output_list()
                output_list_list.append(output_list)

                for i in range(1,53 + 1) :
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + "T O T A L "

                if price_decimal == 0:
                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                else:
                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "


    def disp_it0():

        nonlocal output_list_list, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant
        nonlocal from_date, to_date, lastname, sorttype, price_decimal


        nonlocal output_list
        nonlocal output_list_list

        curr_firma:str = ""
        s2:str = ""
        d2:str = ""
        curr_pay:decimal = to_decimal("0.0")
        do_it:bool = False
        l_ap = None
        L_ap =  create_buffer("L_ap",L_kredit)
        output_list_list.clear()
        t_ap =  to_decimal("0")
        t_pay =  to_decimal("0")
        t_bal =  to_decimal("0")
        tot_ap =  to_decimal("0")
        tot_pay =  to_decimal("0")
        tot_bal =  to_decimal("0")

        if lastname == "":

            l_kredit_obj_list = []
            for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                     (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                if l_kredit._recid in l_kredit_obj_list:
                    continue
                else:
                    l_kredit_obj_list.append(l_kredit._recid)


                do_it = True

                if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                    do_it = False

                if do_it:

                    if curr_firma == "":
                        curr_firma = l_lieferant.firma

                    if curr_firma != l_lieferant.firma:
                        output_list = Output_list()
                        output_list_list.append(output_list)

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
                    output_list_list.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                    tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                    tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                    tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "T O T A L "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
            else:
                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "GRAND TOTAL "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(tot_ap, "->,>>>,>>>,>>>,>>9") + to_string(tot_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(tot_bal, "->,>>>,>>>,>>>,>>9")
            else:
                output_list.str = output_list.str + to_string(tot_ap, "->>,>>>,>>>,>>9.99") + to_string(tot_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(tot_bal, "->>,>>>,>>>,>>9.99") + " "
        else:
            do_it = False

            l_lieferant = db_session.query(L_lieferant).filter(
                     (func.lower(L_lieferant.firma) == (lastname).lower())).first()

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
                    output_list_list.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                output_list = Output_list()
                output_list_list.append(output_list)

                for i in range(1,53 + 1) :
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + "T O T A L "

                if price_decimal == 0:
                    output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
                else:
                    output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "


    def disp_it1():

        nonlocal output_list_list, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, l_kredit, l_lieferant
        nonlocal from_date, to_date, lastname, sorttype, price_decimal


        nonlocal output_list
        nonlocal output_list_list

        curr_firma:str = ""
        s2:str = ""
        d2:str = ""
        curr_pay:decimal = to_decimal("0.0")
        do_it:bool = False
        l_ap = None
        L_ap =  create_buffer("L_ap",L_kredit)
        output_list_list.clear()
        t_ap =  to_decimal("0")
        t_pay =  to_decimal("0")
        t_bal =  to_decimal("0")
        tot_ap =  to_decimal("0")
        tot_pay =  to_decimal("0")
        tot_bal =  to_decimal("0")

        if lastname == "":

            l_kredit_obj_list = []
            for l_kredit, l_lieferant in db_session.query(L_kredit, L_lieferant).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                     (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart == sorttype) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                if l_kredit._recid in l_kredit_obj_list:
                    continue
                else:
                    l_kredit_obj_list.append(l_kredit._recid)


                do_it = True

                if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                    do_it = False

                if do_it:

                    if curr_firma == "":
                        curr_firma = l_lieferant.firma

                    if curr_firma != l_lieferant.firma:
                        output_list = Output_list()
                        output_list_list.append(output_list)

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
                    output_list_list.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                    tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                    tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                    tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "T O T A L "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(t_ap, "->,>>>,>>>,>>>,>>9") + to_string(t_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(t_bal, "->,>>>,>>>,>>>,>>9") + " "
            else:
                output_list.str = output_list.str + to_string(t_ap, "->>,>>>,>>>,>>9.99") + to_string(t_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(t_bal, "->>,>>>,>>>,>>9.99") + " "
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list = Output_list()
            output_list_list.append(output_list)

            for i in range(1,53 + 1) :
                output_list.str = output_list.str + " "
            output_list.str = output_list.str + "GRAND TOTAL "

            if price_decimal == 0:
                output_list.str = output_list.str + to_string(tot_ap, "->,>>>,>>>,>>>,>>9") + to_string(tot_pay, "->,>>>,>>>,>>>,>>9") + " " + to_string(tot_bal, "->,>>>,>>>,>>>,>>9")
            else:
                output_list.str = output_list.str + to_string(tot_ap, "->>,>>>,>>>,>>9.99") + to_string(tot_pay, "->>,>>>,>>>,>>9.99") + " " + to_string(tot_bal, "->>,>>>,>>>,>>9.99") + " "
        else:
            do_it = False

            l_lieferant = db_session.query(L_lieferant).filter(
                     (func.lower(L_lieferant.firma) == (lastname).lower())).first()

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
                    output_list_list.append(output_list)

                    output_list.betriebsnr = l_kredit.betriebsnr
                    output_list.ap_recid = l_kredit._recid
                    output_list.curr_pay =  to_decimal(curr_pay)
                    output_list.str = output_list.str + to_string(l_lieferant.firma, "x(26)") + to_string(l_kredit.rgdatum) + to_string(l_kredit.name, "x(14)") + to_string(l_kredit.lscheinnr, "x(19)")
                    output_list.lscheinnr = l_kredit.lscheinnr

                    if price_decimal == 0:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->,>>>,>>>,>>>,>>9") + to_string(curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->,>>>,>>>,>>>,>>9") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    else:
                        output_list.str = output_list.str + to_string(l_kredit.netto, "->>,>>>,>>>,>>9.99") + to_string(curr_pay, "->>,>>>,>>>,>>9.99") + to_string(d2, "x(8)") + to_string(l_kredit.netto - curr_pay, "->>,>>>,>>>,>>9.99") + to_string(l_kredit.rgdatum + l_kredit.ziel)
                    t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                    t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                    t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                output_list = Output_list()
                output_list_list.append(output_list)

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