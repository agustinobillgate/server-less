#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, L_lieferant, Queasy

def ap_list_1_webbl(from_date:date, to_date:date, lastname:string, sorttype:int, price_decimal:int, check_disp:int):

    prepare_cache ([L_kredit, L_lieferant, Queasy])

    output_list_data = []
    t_ap:Decimal = to_decimal("0.0")
    t_pay:Decimal = to_decimal("0.0")
    t_bal:Decimal = to_decimal("0.0")
    tot_ap:Decimal = to_decimal("0.0")
    tot_pay:Decimal = to_decimal("0.0")
    tot_bal:Decimal = to_decimal("0.0")
    i:int = 0
    stauer_code1:int = None
    stauer_code2:int = 0
    sorttype1:int = None
    sorttype2:int = 0
    l_kredit = l_lieferant = queasy = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"betriebsnr":int, "ap_recid":int, "curr_pay":Decimal, "lscheinnr":string, "str":string, "firma":string, "billdate":date, "docunr":string, "delivnote":string, "amount":Decimal, "paid_amount":Decimal, "paiddate":string, "balance":Decimal, "duedate":date, "desc1":string, "steuercode":int, "recv_date":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, stauer_code1, stauer_code2, sorttype1, sorttype2, l_kredit, l_lieferant, queasy
        nonlocal from_date, to_date, lastname, sorttype, price_decimal, check_disp


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def disp_it1():

        nonlocal output_list_data, t_ap, t_pay, t_bal, tot_ap, tot_pay, tot_bal, i, stauer_code1, stauer_code2, sorttype1, sorttype2, l_kredit, l_lieferant, queasy
        nonlocal from_date, to_date, lastname, sorttype, price_decimal, check_disp


        nonlocal output_list
        nonlocal output_list_data

        curr_firma:string = ""
        s2:string = ""
        d2:string = ""
        curr_pay:Decimal = to_decimal("0.0")
        do_it:bool = False
        doit:bool = False
        l_ap = None
        L_ap =  create_buffer("L_ap",L_kredit)
        output_list_data.clear()
        t_ap =  to_decimal("0")
        t_pay =  to_decimal("0")
        t_bal =  to_decimal("0")
        tot_ap =  to_decimal("0")
        tot_pay =  to_decimal("0")
        tot_bal =  to_decimal("0")

        if lastname == " ":

            if check_disp == 0:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.bemerk, l_kredit.steuercode, l_kredit.lief_nr, l_kredit.opart, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.bemerk, L_kredit.steuercode, L_kredit.lief_nr, L_kredit.opart, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart >= sorttype1) & (L_kredit.opart <= sorttype2) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_kredit.opart == 1:
                        do_it = False

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.firma = "T O T A L "
                            output_list.amount =  to_decimal(t_ap)
                            output_list.paid_amount =  to_decimal(t_pay)
                            output_list.balance =  to_decimal(t_bal)
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
                            d2 = " "
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.firma = l_lieferant.firma
                        output_list.billdate = l_kredit.rgdatum
                        output_list.docunr = l_kredit.name
                        output_list.lscheinnr = l_kredit.lscheinnr
                        output_list.amount =  to_decimal(l_kredit.netto)
                        output_list.paid_amount =  to_decimal(curr_pay)
                        output_list.paiddate = d2
                        output_list.balance =  to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        output_list.duedate = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                        output_list.desc1 = l_kredit.bemerk
                        output_list.steuercode = l_kredit.steuercode
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
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.bemerk, l_kredit.steuercode, l_kredit.lief_nr, l_kredit.opart, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.bemerk, L_kredit.steuercode, L_kredit.lief_nr, L_kredit.opart, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart >= sorttype1) & (L_kredit.opart <= sorttype2) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.steuercode == 1)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_kredit.opart == 1:
                        do_it = False

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.firma = "T O T A L "
                            output_list.amount =  to_decimal(t_ap)
                            output_list.paid_amount =  to_decimal(t_pay)
                            output_list.balance =  to_decimal(t_bal)
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
                            d2 = " "
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.firma = l_lieferant.firma
                        output_list.billdate = l_kredit.rgdatum
                        output_list.docunr = l_kredit.name
                        output_list.lscheinnr = l_kredit.lscheinnr
                        output_list.amount =  to_decimal(l_kredit.netto)
                        output_list.paid_amount =  to_decimal(curr_pay)
                        output_list.paiddate = d2
                        output_list.balance =  to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        output_list.duedate = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                        output_list.desc1 = l_kredit.bemerk
                        output_list.steuercode = l_kredit.steuercode
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                        tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1

            elif check_disp == 2:

                l_kredit_obj_list = {}
                l_kredit = L_kredit()
                l_lieferant = L_lieferant()
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.bemerk, l_kredit.steuercode, l_kredit.lief_nr, l_kredit.opart, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.bemerk, L_kredit.steuercode, L_kredit.lief_nr, L_kredit.opart, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart >= sorttype1) & (L_kredit.opart <= sorttype2) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0) & (L_kredit.steuercode == 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True


                    do_it = True

                    if l_kredit.opart == 1:
                        do_it = False

                    if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                        do_it = False

                    if do_it:

                        if curr_firma == "":
                            curr_firma = l_lieferant.firma

                        if curr_firma != l_lieferant.firma:
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.firma = "T O T A L "
                            output_list.amount =  to_decimal(t_ap)
                            output_list.paid_amount =  to_decimal(t_pay)
                            output_list.balance =  to_decimal(t_bal)
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
                            d2 = " "
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.betriebsnr = l_kredit.betriebsnr
                        output_list.ap_recid = l_kredit._recid
                        output_list.curr_pay =  to_decimal(curr_pay)
                        output_list.firma = l_lieferant.firma
                        output_list.billdate = l_kredit.rgdatum
                        output_list.docunr = l_kredit.name
                        output_list.lscheinnr = l_kredit.lscheinnr
                        output_list.amount =  to_decimal(l_kredit.netto)
                        output_list.paid_amount =  to_decimal(curr_pay)
                        output_list.paiddate = d2
                        output_list.balance =  to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        output_list.duedate = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                        output_list.desc1 = l_kredit.bemerk
                        output_list.steuercode = l_kredit.steuercode
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
                for l_kredit.counter, l_kredit.betriebsnr, l_kredit._recid, l_kredit.rgdatum, l_kredit.name, l_kredit.lscheinnr, l_kredit.netto, l_kredit.ziel, l_kredit.bemerk, l_kredit.steuercode, l_kredit.lief_nr, l_kredit.opart, l_kredit.saldo, l_lieferant.segment1, l_lieferant.firma, l_lieferant.lief_nr, l_lieferant._recid in db_session.query(L_kredit.counter, L_kredit.betriebsnr, L_kredit._recid, L_kredit.rgdatum, L_kredit.name, L_kredit.lscheinnr, L_kredit.netto, L_kredit.ziel, L_kredit.bemerk, L_kredit.steuercode, L_kredit.lief_nr, L_kredit.opart, L_kredit.saldo, L_lieferant.segment1, L_lieferant.firma, L_lieferant.lief_nr, L_lieferant._recid).join(L_lieferant,(L_lieferant.lief_nr == L_kredit.lief_nr)).filter(
                         (L_kredit.lief_nr > 0) & (L_kredit.zahlkonto == 0) & (L_kredit.opart >= sorttype1) & (L_kredit.opart <= sorttype2) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_lieferant.firma, L_kredit.rgdatum).all():
                    if l_kredit_obj_list.get(l_kredit._recid):
                        continue
                    else:
                        l_kredit_obj_list[l_kredit._recid] = True

                    queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                    if queasy:
                        do_it = True

                        if l_kredit.opart == 1:
                            do_it = False

                        if l_lieferant.segment1 != 0 and l_lieferant.segment1 != l_lieferant.segment1:
                            do_it = False

                        if do_it:

                            if curr_firma == "":
                                curr_firma = l_lieferant.firma

                            if curr_firma != l_lieferant.firma:
                                output_list = Output_list()
                                output_list_data.append(output_list)

                                output_list.firma = "T O T A L "
                                output_list.amount =  to_decimal(t_ap)
                                output_list.paid_amount =  to_decimal(t_pay)
                                output_list.balance =  to_decimal(t_bal)
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
                                d2 = " "
                            output_list = Output_list()
                            output_list_data.append(output_list)

                            output_list.betriebsnr = l_kredit.betriebsnr
                            output_list.ap_recid = l_kredit._recid
                            output_list.curr_pay =  to_decimal(curr_pay)
                            output_list.firma = l_lieferant.firma
                            output_list.billdate = l_kredit.rgdatum
                            output_list.docunr = l_kredit.name
                            output_list.lscheinnr = l_kredit.lscheinnr
                            output_list.amount =  to_decimal(l_kredit.netto)
                            output_list.paid_amount =  to_decimal(curr_pay)
                            output_list.paiddate = d2
                            output_list.balance =  to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                            output_list.duedate = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                            output_list.desc1 = l_kredit.bemerk
                            output_list.steuercode = l_kredit.steuercode
                            output_list.recv_date = queasy.date1
                            t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                            t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                            t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                            tot_ap =  to_decimal(tot_ap) + to_decimal(l_kredit.netto)
                            tot_pay =  to_decimal(tot_pay) + to_decimal(curr_pay)
                            tot_bal =  to_decimal(tot_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.firma = "T O T A L "
            output_list.amount =  to_decimal(t_ap)
            output_list.paid_amount =  to_decimal(t_pay)
            output_list.balance =  to_decimal(t_bal)
            t_ap =  to_decimal("0")
            t_pay =  to_decimal("0")
            t_bal =  to_decimal("0")
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.firma = "GRAND TOTAL "
            output_list.amount =  to_decimal(tot_ap)
            output_list.paid_amount =  to_decimal(tot_pay)
            output_list.balance =  to_decimal(tot_bal)
        else:
            doit = False

            l_lieferant = get_cache (L_lieferant, {"firma": [(eq, lastname)]})

            if l_lieferant:

                if l_lieferant.segment1 == 0:
                    doit = True
                else:
                    doit = l_lieferant.segment1 == l_lieferant.segment1

            if doit:

                for l_kredit in db_session.query(L_kredit).filter(
                         (L_kredit.lief_nr == l_lieferant.lief_nr) & (L_kredit.zahlkonto == 0) & (L_kredit.opart >= sorttype1) & (L_kredit.opart <= sorttype2) & (L_kredit.rgdatum >= from_date) & (L_kredit.rgdatum <= to_date) & (L_kredit.counter >= 0) & (L_kredit.netto != 0)).order_by(L_kredit.rgdatum).all():
                    do_it = True

                    if l_kredit.opart == 1:
                        do_it = False

                    if do_it:
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
                        output_list.firma = l_lieferant.firma
                        output_list.billdate = l_kredit.rgdatum
                        output_list.docunr = l_kredit.name
                        output_list.lscheinnr = l_kredit.lscheinnr
                        output_list.desc1 = l_kredit.bemerk
                        output_list.steuercode = l_kredit.steuercode
                        output_list.amount =  to_decimal(l_kredit.netto)
                        output_list.paid_amount =  to_decimal(curr_pay)
                        output_list.paiddate = d2
                        output_list.balance =  to_decimal(l_kredit.netto) - to_decimal(curr_pay)
                        output_list.duedate = l_kredit.rgdatum + timedelta(days=l_kredit.ziel)
                        t_ap =  to_decimal(t_ap) + to_decimal(l_kredit.netto)
                        t_pay =  to_decimal(t_pay) + to_decimal(curr_pay)
                        t_bal =  to_decimal(t_bal) + to_decimal(l_kredit.netto) - to_decimal(curr_pay)

                        queasy = get_cache (Queasy, {"key": [(eq, 221)],"number1": [(eq, l_kredit.lief_nr)],"char1": [(eq, l_kredit.lscheinnr)]})

                        if queasy:
                            output_list.recv_date = queasy.date1


            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.firma = output_list.firma + "GRAND TOTAL "
            output_list.amount =  to_decimal(t_ap)
            output_list.paid_amount =  to_decimal(t_pay)
            output_list.balance =  to_decimal(t_bal)


    if sorttype == 1:
        sorttype1 = 0
        sorttype2 = 2

    elif sorttype == 0:
        sorttype1 = 0
        sorttype2 = 0

    elif sorttype == 2:
        sorttype1 = 2
        sorttype2 = 2
    disp_it1()

    return generate_output()