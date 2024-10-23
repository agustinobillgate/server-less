from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Debitor, Artikel, Guest, Bill, Bediener, Waehrung

def ar_paylist_webbl(comment:str, cledger:bool, ccard:bool, last_sort:int, from_date:date, to_date:date, from_art:int, to_art:int, mi_payment:bool, mi_transfer:bool, show_inv:bool):
    r_no = 0
    s_list_list = []
    t_list_list = []
    t_ar_paylist_list = []
    long_digit:bool = False
    htparam = debitor = artikel = guest = bill = bediener = waehrung = None

    s_list = t_list = output_list = t_ar_paylist = tbuff = bq = None

    s_list_list, S_list = create_model("S_list", {"artnr":int, "bezeich":str, "betrag":decimal})
    t_list_list, T_list = create_model("T_list", {"artnr":int, "bezeich":str, "betrag":decimal})
    output_list_list, Output_list = create_model("Output_list", {"artnr":int, "pay_count":int, "flag":int, "pay_amt":decimal, "dbetrag":decimal, "sbetrag":str, "inv_no":str, "str":str, "bill_art":int, "debt_counter":int})
    t_ar_paylist_list, T_ar_paylist = create_model("T_ar_paylist", {"bill_date":str, "bill_num":str, "inv_num":str, "bill_rcv":str, "debt_amt":str, "pay_amt":str, "pay_famt":str, "curr":str, "pay_art":str, "pay_date":str, "uid":str, "pay_comment":str, "tot_pay":str, "artno":str, "debt_counter":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list
        return {"r_no": r_no, "s-list": s_list_list, "t-list": t_list_list, "t-ar-paylist": t_ar_paylist_list}

    def create_list():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list


        s_list_list.clear()
        t_list_list.clear()
        output_list_list.clear()

        if comment == "":

            if cledger and ccard:

                if last_sort == 1:
                    create_list1()

                elif last_sort == 2:
                    create_list1a()

                elif last_sort == 3:
                    create_list1b()

                elif last_sort == 4:
                    create_list1c()

                elif last_sort == 5:
                    create_list1d()

            elif cledger and not ccard:

                if last_sort == 1:
                    create_list2()

                elif last_sort == 2:
                    create_list2a()

                elif last_sort == 3:
                    create_list2b()

                elif last_sort == 4:
                    create_list2c()

                elif last_sort == 5:
                    create_list2d()

            elif ccard and not cledger:

                if last_sort == 1:
                    create_list3()

                elif last_sort == 2:
                    create_list3a()

                elif last_sort == 3:
                    create_list3b()

                elif last_sort == 4:
                    create_list3c()

                elif last_sort == 5:
                    create_list3d()

        elif comment != "":

            if cledger and ccard:
                create_list11()

            elif cledger and not ccard:
                create_list21()

            elif ccard and not cledger:
                create_list31()


    def create_tot_payment():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        curr_artno:int = 0
        tbetrag:decimal = to_decimal("0.0")
        curr_count:int = 0
        Tbuff = Output_list
        tbuff_list = output_list_list
        Bq = Output_list
        bq_list = output_list_list

        bq = query(bq_list, filters=(lambda bq: bq.bQ.pay_count != 0), first=True)

        if not bQ:

            return

        for bq in query(bq_list, filters=(lambda bq: bq.bQ.flag == 1 and bQ.pay_count != 0), sort_by=[("pay_count",False)]):

            if curr_count == 0:
                curr_count = bQ.pay_count

            if (curr_count != bQ.pay_count):

                for tbuff in query(tbuff_list, filters=(lambda tbuff: tbuff.pay_count == curr_count)):

                    if not long_digit:
                        tbuff.sbetrag = to_string(tbetrag, "->,>>>,>>>,>>9.99")
                    else:
                        tbuff.sbetrag = to_string(tbetrag, " ->>>,>>>,>>>,>>9")
                    tbuff.dbetrag =  to_decimal(tbetrag)
                tbetrag =  to_decimal("0")
            curr_count = bQ.pay_count
            tbetrag =  to_decimal(tbetrag) + to_decimal(bQ.pay_amt)

        for tbuff in query(tbuff_list, filters=(lambda tbuff: tbuff.pay_count == curr_count)):

            if not long_digit:
                tbuff.sbetrag = to_string(tbetrag, "->,>>>,>>>,>>9.99")
            else:
                tbuff.sbetrag = to_string(tbetrag, " ->>>,>>>,>>>,>>9")
            tbuff.dbetrag =  to_decimal(tbetrag)


    def create_list1():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,58 + 1) :
                                output_list.str = output_list.str + " "

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            tot_saldo =  to_decimal("0")
                            tot_foreign =  to_decimal("0")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt =  to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr


                output_list.debt_counter = debitor.counter

                if show_inv:

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        r_no = debitor.rechnr
                    else:
                        output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == debitor.betrieb_gastmem)).first()

                if waehrung:
                    output_list.str = output_list.str + to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + " "

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list1a():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.zahlkonto, Debitor.name, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.zahlkonto

                if curr_gastnr != debitor.zahlkonto:
                    curr_gastnr = debitor.zahlkonto
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                if show_inv:

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        r_no = debitor.rechnr
                    else:
                        output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")


    def create_list1b():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debt.rgdatum, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt =  to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr


                output_list.debt_counter = debitor.counter

                if show_inv:

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        r_no = debitor.rechnr
                    else:
                        output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == debitor.betrieb_gastmem)).first()

                if waehrung:
                    output_list.str = output_list.str + to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + " "

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list1c():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rechnr, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt =  to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr


                output_list.debt_counter = debitor.counter

                if show_inv:

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        r_no = debitor.rechnr
                    else:
                        output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == debitor.betrieb_gastmem)).first()

                if waehrung:
                    output_list.str = output_list.str + to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + " "

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list1d():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.vesrcod, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.flag = 1
                output_list.artnr = debitor.zahlkonto
                output_list.pay_amt =  to_decimal(debitor.saldo)
                output_list.pay_count = debitor.betriebsnr
                output_list.bill_art = artikel.artnr


                output_list.debt_counter = debitor.counter

                if show_inv:

                    bill = db_session.query(Bill).filter(
                             (Bill.rechnr == debitor.rechnr)).first()

                    if not bill:
                        r_no = debitor.rechnr
                    else:
                        output_list.inv_no = to_string(bill.rechnr2, ">>>>>>>>>")

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->>,>>>,>>>,>>9.99")

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == debitor.betrieb_gastmem)).first()

                if waehrung:
                    output_list.str = output_list.str + to_string(waehrung.wabkurz, "x(4)")
                else:
                    output_list.str = output_list.str + " "

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list2():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list2a():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.zahlkonto, Debitor.name, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.zahlkonto

                if curr_gastnr != debitor.zahlkonto:
                    curr_gastnr = debitor.zahlkonto
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")


    def create_list3():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.zahlkonto, Debitor.betriebsnr, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:

                        if tot_saldo != 0:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            for i in range(1,58 + 1) :
                                output_list.str = output_list.str + " "

                            if not long_digit:
                                output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                            else:
                                output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            tot_saldo =  to_decimal("0")
                            tot_foreign =  to_decimal("0")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                        tot_saldo =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list3a():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.zahlkonto, Debitor.name, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.zahlkonto

                if curr_gastnr != debitor.zahlkonto:
                    curr_gastnr = debitor.zahlkonto
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78)
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78)


    def create_list11():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (func.lower(Debitor.vesrcod) == (comment).lower()) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78)
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78)


    def create_list21():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0) & (func.lower(Debitor.vesrcod) == (comment).lower())).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78)
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78)


    def create_list31():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0) & (func.lower(Debitor.vesrcod) == (comment).lower())).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.name, Debitor.gastnr, Debitor.rgdatum, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78)
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78)


    def create_list2b():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debt.rgdatum, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list2c():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rechnr, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list2d():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.vesrcod, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(24)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list3b():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debt.rgdatum, Debitor.name, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list3c():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.rechnr, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()


    def create_list3d():

        nonlocal r_no, s_list_list, t_list_list, t_ar_paylist_list, long_digit, htparam, debitor, artikel, guest, bill, bediener, waehrung
        nonlocal comment, cledger, ccard, last_sort, from_date, to_date, from_art, to_art, mi_payment, mi_transfer, show_inv


        nonlocal s_list, t_list, output_list, t_ar_paylist, tbuff, bq
        nonlocal s_list_list, t_list_list, output_list_list, t_ar_paylist_list

        artnr:int = 0
        i:int = 0
        curr_gastnr:int = 0
        t_credit:decimal = to_decimal("0.0")
        tot_credit:decimal = to_decimal("0.0")
        t_famt:decimal = to_decimal("0.0")
        tot_famt:decimal = to_decimal("0.0")
        tot_saldo:decimal = to_decimal("0.0")
        tot_foreign:decimal = to_decimal("0.0")
        receiver:str = ""
        do_it:bool = False
        debt = None
        art = None
        t_guest = None
        tstr:str = ""
        Debt =  create_buffer("Debt",Debitor)
        Art =  create_buffer("Art",Artikel)
        T_guest =  create_buffer("T_guest",Guest)

        debitor_obj_list = []
        for debitor, debt, artikel, art, guest in db_session.query(Debitor, Debt, Artikel, Art, Guest).join(Debt,(Debt.counter == Debitor.counter) & (Debt.zahlkonto == 0)).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 7)).join(Art,(Art.artnr == Debitor.zahlkonto) & (Art.departement == 0)).join(Guest,(Guest.gastnr == Debitor.gastnr)).filter(
                 (Debitor.rgdatum >= from_date) & (Debitor.rgdatum <= to_date) & (Debitor.zahlkonto > 0) & (Debitor.artnr >= from_art) & (Debitor.artnr <= to_art) & (Debitor.counter > 0) & (Debitor.opart > 0)).order_by(Artikel.artnr, Debitor.vesrcod, Debitor.name, Debitor.rgdatum, Debitor.zahlkonto, Debitor.rechnr).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            do_it = True

            if mi_payment:

                if artikel.artart == 2 and art.artart != 4 and art.artart != 7:
                    do_it = False

                elif artikel.artart == 7 and art.artart != 4:
                    do_it = False

            elif mi_transfer:

                if artikel.artart == 2 and (art.artart == 4 or art.artart == 7):
                    do_it = False

                elif artikel.artart == 7 and art.artart == 4:
                    do_it = False

            if do_it:

                if curr_gastnr == 0:
                    curr_gastnr = debitor.gastnr

                if curr_gastnr != debitor.gastnr:
                    curr_gastnr = debitor.gastnr
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,58 + 1) :
                        output_list.str = output_list.str + " "

                    if not long_digit:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    tot_saldo =  to_decimal("0")
                    tot_foreign =  to_decimal("0")

                if artnr != artikel.artnr:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.artnr = artikel.artnr
                    t_list.bezeich = artikel.bezeich

                    if artnr != 0:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        for i in range(1,58 + 1) :
                            output_list.str = output_list.str + " "

                        if not long_digit:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        t_credit =  to_decimal("0")
                        t_famt =  to_decimal("0")
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    for i in range(1,19 + 1) :
                        output_list.str = output_list.str + " "
                    output_list.str = output_list.str + to_string(artikel.artnr, ">>>>9") + " - " + to_string(artikel.bezeich, "x(34)")
                    artnr = artikel.artnr
                t_list.betrag =  to_decimal(t_list.betrag) - to_decimal(debitor.saldo)
                receiver = guest.name + ", " + guest.vorname1 + " " + guest.anredefirma + guest.anrede1
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.bill_art = artikel.artnr
                output_list.debt_counter = debitor.counter

                if not long_digit:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, "->,>>>,>>>,>>9.99") + to_string(debitor.saldo, "->,>>>,>>>,>>9.99") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)
                else:
                    output_list.str = to_string(debt.rgdatum) + to_string(debitor.rechnr, ">>>,>>>,>>9") + to_string(receiver, "x(32)") + to_string(debt.saldo, " ->>>,>>>,>>>,>>9") + to_string(debitor.saldo, " ->>>,>>>,>>>,>>9") + to_string(art.bezeich, "x(34)") + to_string(debitor.rgdatum)

                bediener = db_session.query(Bediener).filter(
                         (Bediener.nr == debitor.bediener_nr)).first()

                if bediener:
                    output_list.str = output_list.str + to_string(bediener.userinit, "x(3)")
                else:
                    output_list.str = output_list.str + " "
                output_list.str = output_list.str + to_string(debitor.vesrcod, "x(34)")
                output_list.str = output_list.str + to_string(" ", "x(22)")

                t_guest = db_session.query(T_guest).filter(
                         (T_guest.gastnr == debt.gastnrmember)).first()

                if t_guest:
                    tstr = t_guest.name + "," + t_guest.vorname1 + " " + t_guest.anrede1
                else:
                    tstr = " "
                output_list.str = output_list.str + to_string(tstr, "x(50)")
                output_list.str = output_list.str + to_string(debit.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(debitor.zahlkonto, ">>>>9")
                output_list.str = output_list.str + to_string(debitor.vesrdep, "->,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(artikel.bezeich, "x(40)")


                t_credit =  to_decimal(t_credit) + to_decimal(debitor.saldo)
                t_famt =  to_decimal(t_famt) + to_decimal(debitor.vesrdep)
                tot_credit =  to_decimal(tot_credit) + to_decimal(debitor.saldo)
                tot_saldo =  to_decimal(tot_saldo) + to_decimal(debitor.saldo)
                tot_foreign =  to_decimal(tot_foreign) + to_decimal(debitor.vesrdep)
                tot_famt =  to_decimal(tot_famt) + to_decimal(debitor.vesrdep)

                s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == art.artnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    s_list.artnr = art.artnr
                    s_list.bezeich = art.bezeich
                s_list.betrag =  to_decimal(s_list.betrag) + to_decimal(debitor.saldo)
        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_foreign, " ->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "T O T A L " + to_string(tot_saldo, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_foreign, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,58 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(t_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Sub-Total " + to_string(t_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(t_famt, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list = Output_list()
        output_list_list.append(output_list)

        for i in range(1,56 + 1) :
            output_list.str = output_list.str + " "

        if not long_digit:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, "->,>>>,>>>,>>9.99") + fill(" ", 78) + to_string(tot_famt, "->>,>>>,>>>,>>9.99")
        else:
            output_list.str = output_list.str + "Grand TOTAL " + to_string(tot_credit, " ->>>,>>>,>>>,>>9") + fill(" ", 78) + to_string(tot_famt, " ->>>,>>>,>>>,>>9")
        create_tot_payment()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    create_list()
    t_ar_paylist_list.clear()

    for output_list in query(output_list_list):
        t_ar_paylist = T_ar_paylist()
        t_ar_paylist_list.append(t_ar_paylist)

        t_ar_paylist.bill_date = substring(output_list.str, 0, 8)
        t_ar_paylist.bill_num = substring(output_list.str, 8, 11)
        t_ar_paylist.inv_num = output_list.inv_no
        t_ar_paylist.bill_rcv = substring(output_list.str, 19, 32)
        t_ar_paylist.debt_amt = substring(output_list.str, 51, 17)
        t_ar_paylist.pay_amt = substring(output_list.str, 68, 17)
        t_ar_paylist.pay_famt = substring(output_list.str, 164, 18)
        t_ar_paylist.curr = substring(output_list.str, 182, 4)
        t_ar_paylist.pay_art = substring(output_list.str, 85, 34)
        t_ar_paylist.pay_date = substring(output_list.str, 119, 8)
        t_ar_paylist.uid = substring(output_list.str, 127, 3)
        t_ar_paylist.pay_comment = substring(output_list.str, 130, 34)
        t_ar_paylist.tot_pay = output_list.sbetrag
        t_ar_paylist.artno = to_string(output_list.bill_art)
        t_ar_paylist.debt_counter = to_string(output_list.debt_counter)

    return generate_output()